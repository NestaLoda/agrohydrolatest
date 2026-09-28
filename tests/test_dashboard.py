import unittest
import tempfile
import json
import shutil
from pathlib import Path
from unittest.mock import patch
from backend.contracts import DecisionRequest, BenchmarkRequest, FieldComparisonRequest, FieldPoint
from backend.optimizer import solve_decision
from backend.repository import benchmarks, north_context
from backend.field import compare_field
from backend.provenance import ProvenanceStore

class DecisionDashboard(unittest.TestCase):
    def test_binding_freshwater_and_positive_energy_slack(self):
        r=solve_decision(DecisionRequest())
        c={x['id']:x for x in r['constraints']}
        self.assertTrue(c['freshwater']['binding'])
        self.assertFalse(c['energy']['binding'])
        self.assertAlmostEqual(c['energy']['slack'],879.25)
        self.assertEqual(r['failure_diagnostics']['target_shortfall_kg'],0)

    def test_infeasible_target_reports_capacity_without_fake_allocation(self):
        r=solve_decision(DecisionRequest(energy_budget_kwh=10000))
        self.assertIsNone(r['totals'])
        self.assertAlmostEqual(r['failure_diagnostics']['max_supported_production_kg'],400)
        self.assertAlmostEqual(r['failure_diagnostics']['target_shortfall_kg'],600)
        self.assertTrue(all(c['used'] is None and c['binding'] is None for c in r['constraints']))

    def test_unsupported_treatment_energy_is_missing_not_zero(self):
        r=solve_decision(DecisionRequest(seawater_temperature_c=-1))
        self.assertTrue(all(o['energy_kwh_per_kg'] is None for o in r['options'] if o['water_source']=='desalinated_seawater'))

    def test_five_regions_same_basis_different_climate(self):
        r=benchmarks()
        self.assertEqual(len(r['sites']),5)
        self.assertNotIn('longyearbyen',[s['site_id'] for s in r['sites']])
        deficits=[]
        for s in r['sites']:
            self.assertEqual(s['water_balance']['season_start'],'2022-11-01')
            self.assertEqual(s['water_balance']['totals']['capacity_mm'],60)
            self.assertEqual(s['budget_screen']['budget_mm'],100)
            deficits.append(s['budget_screen']['reference_deficit_mm'])
        self.assertGreater(len(set(round(x,1) for x in deficits)),3)

    def test_shared_budget_only_changes_budget_screen_not_weather(self):
        a=benchmarks(BenchmarkRequest(site_ids=['konya','seyhan_adana'],net_irrigation_budget_mm=0))
        b=benchmarks(BenchmarkRequest(site_ids=['konya','seyhan_adana'],net_irrigation_budget_mm=2000))
        for first,last in zip(a['sites'],b['sites']):
            self.assertEqual(first['monthly'],last['monthly'])
            self.assertEqual(first['water_balance'],last['water_balance'])
            self.assertEqual(last['budget_screen']['gap_mm'],0)
            self.assertGreater(first['budget_screen']['gap_mm'],0)

    def test_northern_site_is_not_a_turkey_benchmark(self):
        with self.assertRaises(ValueError):benchmarks(BenchmarkRequest(site_ids=['longyearbyen']))

    def test_north_display_cannot_diverge_from_raw_model(self):
        source=Path(__file__).resolve().parents[1]
        with tempfile.TemporaryDirectory() as folder:
            root=Path(folder);(root/'data/north').mkdir(parents=True)
            summary=json.loads((source/'data/north/summary.json').read_text(encoding='utf-8'))
            for meta in summary['provenance']:
                destination=root/meta['raw_path'];destination.parent.mkdir(parents=True,exist_ok=True)
                shutil.copyfile(source/meta['raw_path'],destination)
            summary['future']['mean_annual_gdd5_degree_days']+=100
            (root/'data/north/summary.json').write_text(json.dumps(summary),encoding='utf-8')
            with patch('backend.repository.ROOT',root),self.assertRaises(ValueError):north_context()


class FieldRelevance(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup)
        self.store=ProvenanceStore(Path(self.temp.name)/'test.sqlite')

    def test_matching_scenario_changes_feasibility_not_confidence(self):
        r=compare_field(FieldComparisonRequest(decision=DecisionRequest(energy_budget_kwh=25110)),self.store)
        self.assertTrue(r['collocation']['passed'])
        self.assertEqual(r['residual_temperature_C'],-5)
        self.assertEqual(r['before']['status'],'conditional')
        self.assertEqual(r['after']['status'],'unsuitable')
        self.assertTrue(r['changed_decision'])
        self.assertIsNone(r['confidence_score'])
        self.assertFalse(r['calibration_applied'])
        self.assertEqual(r['observation_evidence'],'SIMULATION / EXPLANATORY')

    def test_location_mismatch_blocks_update(self):
        r=compare_field(FieldComparisonRequest(observed=FieldPoint(temperature_C=5,latitude=75)),self.store)
        self.assertEqual(r['status'],'not_comparable')
        self.assertIsNone(r['after'])
        self.assertIsNone(r['residual_temperature_C'])

    def test_time_and_depth_mismatch_blocks_update(self):
        for point in [FieldPoint(timestamp_utc='2026-09-23T12:00:00Z'),FieldPoint(depth_m=15)]:
            r=compare_field(FieldComparisonRequest(observed=point),self.store)
            self.assertFalse(r['collocation']['passed'])
            self.assertIsNone(r['energy_delta_kwh'])

    def test_lower_cost_alone_is_not_changed_recommendation(self):
        r=compare_field(FieldComparisonRequest(),self.store)
        self.assertGreater(r['energy_delta_kwh'],0)
        self.assertFalse(r['changed_decision'])

    def test_claimed_external_values_need_registered_source(self):
        with self.assertRaises(ValueError):compare_field(FieldComparisonRequest(evidence_kind='EXTERNAL_OBSERVATION'),self.store)

    def test_potential_temperature_is_not_subtracted_from_in_situ(self):
        r=compare_field(FieldComparisonRequest(expected=FieldPoint(temperature_kind='potential')),self.store)
        self.assertFalse(r['collocation']['passed'])
        self.assertIsNone(r['residual_temperature_C'])

    def test_cold_outside_ro_range_does_not_extrapolate(self):
        r=compare_field(FieldComparisonRequest(observed=FieldPoint(temperature_C=-1)),self.store)
        self.assertIsNone(r['after']['treatment']['specific_energy_kwh_m3'])
        self.assertIsNone(r['energy_delta_kwh'])
