import unittest
import numpy as np
from backend.science import climate_metrics, mm_to_m3, kj_to_kwh, water_balance, suitability, treatment_energy
from backend.contracts import DecisionRequest
from backend.optimizer import solve_decision


class PhysicalCalculations(unittest.TestCase):
    def test_unit_conversions(self):
        self.assertEqual(mm_to_m3(100, 2), 2000)
        self.assertEqual(kj_to_kwh(90000), 25)
        for missing in (None, float('nan'), -1):
            with self.assertRaises(ValueError): mm_to_m3(missing, 1)

    def test_bucket_conserves_water_every_day(self):
        result=water_balance([0,100,1,0], [10,4,70,10], [1,1,1,1])
        for d in result['daily']:
            self.assertAlmostEqual(d['start_storage_mm']+d['precipitation_mm'], d['storage_mm']+d['actual_et_mm']+d['drainage_mm'])
            self.assertAlmostEqual(d['potential_et_mm'], d['actual_et_mm']+d['deficit_mm'])
            self.assertGreaterEqual(d['storage_mm'],0)
            self.assertLessEqual(d['storage_mm'],60)
        total=result['totals']
        self.assertAlmostEqual(total['initial_storage_mm']+total['precipitation_mm'],total['final_storage_mm']+total['actual_et_mm']+total['drainage_mm'])

    def test_drought_cannot_create_water(self):
        r=water_balance([0]*10,[5]*10,[1]*10,initial_mm=0)['totals']
        self.assertEqual(r['actual_et_mm'],0)
        self.assertEqual(r['deficit_mm'],50)
        with self.assertRaises(ValueError): water_balance([float('nan')],[5],[1])

    def test_climate_metrics_known_sequence(self):
        r=climate_metrics([-1,2,3,-2,5],[9,10,11,8,15])
        self.assertEqual(r['frost_free_longest_days'],2)
        self.assertEqual(r['gdd_base5_c_days'],8)
        with self.assertRaises(ValueError): climate_metrics([None],[20])

    def test_unknown_soil_is_not_suitable(self):
        self.assertEqual(suitability(True,None)['status'],'insufficient_data')
        self.assertEqual(suitability(True,False)['status'],'unsuitable')

    def test_ro_stays_inside_published_support(self):
        self.assertEqual(treatment_energy(5)['specific_energy_kwh_m3'],10.5)
        self.assertAlmostEqual(treatment_energy(18)['specific_energy_kwh_m3'],6.7)
        self.assertIsNone(treatment_energy(-1)['specific_energy_kwh_m3'])
        self.assertFalse(treatment_energy(10,20)['salinity_used_in_energy_model'])


class OptimizerConstraints(unittest.TestCase):
    def test_default_plan_respects_all_budgets(self):
        q=DecisionRequest()
        r=solve_decision(q); t=r['totals']
        self.assertEqual(r['status'],'conditional')
        self.assertAlmostEqual(t['production_kg'],q.output_target_kg)
        self.assertLessEqual(t['energy_kwh'],q.energy_budget_kwh+1e-6)
        self.assertLessEqual(t['freshwater_m3'],q.freshwater_capacity_m3+1e-6)
        self.assertLessEqual(t['desalinated_water_m3'],q.desalination_capacity_m3+1e-6)
        self.assertAlmostEqual(t['feed_seawater_m3'],t['desalinated_water_m3']/q.recovery_fraction)
        self.assertTrue(all(a['option_id'].startswith('hydroponics') for a in r['allocations']))

    def test_no_resources_produces_no_fictitious_plan(self):
        r=solve_decision(DecisionRequest(freshwater_capacity_m3=0,desalination_capacity_m3=0,energy_budget_kwh=0))
        self.assertIsNone(r['totals'])
        self.assertEqual(r['allocations'],[])
        self.assertFalse(r['solver']['success'])

    def test_actual_cold_unsupported_desal_is_excluded(self):
        r=solve_decision(DecisionRequest(seawater_temperature_c=-1,freshwater_capacity_m3=5))
        self.assertIsNone(r['totals'])
        self.assertTrue(all(o['status']=='insufficient_data' for o in r['options'] if o['water_source']=='desalinated_seawater'))

    def test_scenario_choice_does_not_invent_local_climate(self):
        a=solve_decision(DecisionRequest(scenario_id='ssp126'))
        b=solve_decision(DecisionRequest(scenario_id='ssp585'))
        self.assertEqual(a['totals'],b['totals'])

    def test_resource_increase_cannot_raise_optimum_energy(self):
        previous=float('inf')
        for water in [0,5,10,20,30]:
            r=solve_decision(DecisionRequest(freshwater_capacity_m3=water))
            energy=r['totals']['energy_kwh']
            self.assertLessEqual(energy,previous+1e-6)
            previous=energy

