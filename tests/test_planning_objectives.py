"""U11: objective semantics and review-driven northern selection."""
import copy
import unittest
from unittest.mock import patch
from backend import planning
from backend.planning_contracts import SimulationRequest

class PlanningObjectiveTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.context=planning.planning_context('longyearbyen')

    def request(self,mode):
        data=copy.deepcopy(self.context['illustrative_scenario'])
        data['planning_objective']=mode
        return SimulationRequest.model_validate(data)

    def test_capacity_ignores_arbitrary_demand_and_uses_computed_potentials(self):
        first=self.request('capacity')
        second=first.model_copy(deep=True)
        for crop in second.crops:
            crop.target_production_kg*=123
            crop.min_production_kg*=456
        a,b=planning.simulate(first),planning.simulate(second)
        self.assertEqual(a['optimized'],b['optimized'])
        self.assertEqual(a['objective']['normalization_kg'],b['objective']['normalization_kg'])
        self.assertGreater(a['optimized']['totals']['water_m3'],0)
        for crop in a['effective_request']['crops']:
            self.assertEqual(crop['min_production_kg'],0)
            self.assertGreater(a['objective']['normalization_kg'][crop['crop_id']],0)
        self.assertEqual(b['request']['crops'][0]['min_production_kg'],second.crops[0].min_production_kg)

    def test_balanced_guarantees_computed_common_capacity_fraction(self):
        result=planning.simulate(self.request('balanced'))
        floor=result['objective']['balanced_floor']
        self.assertGreater(floor,0)
        for crop in result['optimized']['crops']:
            normalized=crop['production_kg']/result['objective']['normalization_kg'][crop['crop_id']]
            self.assertGreaterEqual(normalized,floor-1e-6)
        self.assertEqual(result['objective']['stages'][0],'max_min_single_crop_capacity_fraction')

    def test_resource_priorities_enforce_same_demand_but_select_different_methods(self):
        request=self.request('water_priority')
        lettuce=request.crops[-1].model_copy(deep=True)
        lettuce.methods=['open_field','hydroponics']
        lettuce.climate_suitable=True;lettuce.soil_suitable=True
        lettuce.yield_kg_ha=1000;lettuce.manual_net_irrigation_mm=100;lettuce.field_energy_kwh_ha=1
        request.crops=[lettuce]
        water=planning.simulate(request)
        request.planning_objective='energy_priority'
        energy=planning.simulate(request)
        self.assertEqual(water['status'],'conditional');self.assertEqual(energy['status'],'conditional')
        self.assertLess(water['optimized']['totals']['water_m3'],energy['optimized']['totals']['water_m3'])
        self.assertGreater(water['optimized']['totals']['energy_kwh'],energy['optimized']['totals']['energy_kwh'])
        for result in [water,energy]:
            self.assertGreaterEqual(result['optimized']['crops'][0]['production_kg'],999.999)
        self.assertEqual(energy['objective']['stages'][1],'min_energy')

    def test_north_default_keeps_unknowns_and_candidates_follow_review_not_fixed_list(self):
        self.assertEqual(self.context['default_scenario']['planning_objective'],'capacity')
        self.assertIsNone(self.context['default_scenario']['crops'][-1]['controlled_yield_kg_m2'])
        evidence=self.context['candidate_evidence']
        self.assertEqual(evidence['selected_ids'],['barley','potato','lettuce'])
        self.assertTrue(all(c['readiness']=='DATA_NEEDED' for c in evidence['candidates']))
        from backend.north_evidence import load_north_evidence
        review=load_north_evidence()
        review['candidates'][0]['default_candidate']=False
        with patch('backend.north_evidence.load_north_evidence',return_value=review):
            filtered=planning.northern_candidates(planning.catalog())
        self.assertNotIn('barley',filtered['selected_ids'])
        self.assertIn('potato',filtered['selected_ids'])

    def test_no_eligible_default_north_candidates_never_produce_empty_valid_plan(self):
        request=SimulationRequest.model_validate(self.context['default_scenario'])
        for objective in ('capacity','balanced'):
            request.planning_objective=objective
            result=planning.simulate(request)
            self.assertEqual(result['status'],'insufficient_data')
            self.assertIsNone(result['optimized'])
            self.assertFalse(result['solver']['success'])
            self.assertTrue(result['excluded_options'])

    def test_disabled_candidate_cannot_gain_capacity(self):
        request=self.request('capacity');request.crops[0].enabled=False
        result=planning.simulate(request)
        self.assertEqual(result['objective']['normalization_kg']['barley'],0)
        self.assertEqual(result['optimized']['crops'][0]['production_kg'],0)

if __name__=='__main__':unittest.main()
