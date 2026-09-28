"""Source-driven northern analysis changes with data while keeping approval unknown."""
import unittest
from backend.automatic_baseline import analyze_northern_baseline

class AutomaticNorthernBaselineTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.low=analyze_northern_baseline('nasa_ssp245_2035')
        cls.high=analyze_northern_baseline('nasa_ssp585_2035')
        cls.multi=analyze_northern_baseline('ec_earth_2030_2049')

    def test_scenario_selection_changes_calculated_data_not_only_metadata(self):
        a,b=self.low,self.high
        self.assertEqual(a['row_count'],365)
        self.assertNotEqual(a['monthly'],b['monthly'])
        self.assertAlmostEqual(a['summary']['mean_annual_precipitation_mm'],590.662231445,places=3)
        self.assertAlmostEqual(b['summary']['mean_annual_precipitation_mm'],679.999694824,places=3)
        self.assertNotEqual(a['summary']['mean_annual_et0_proxy_mm'],b['summary']['mean_annual_et0_proxy_mm'])
        self.assertGreater(a['summary']['mean_annual_heating_degree_hours_18c'],b['summary']['mean_annual_heating_degree_hours_18c'])

    def test_frost_window_retains_real_dates_and_matches_verified_summary(self):
        self.assertEqual(self.low['summary']['longest_frost_free_window'],{'days':45,'start':'2035-07-09','end':'2035-08-22'})
        self.assertEqual(self.high['summary']['longest_frost_free_window']['days'],47)
        self.assertAlmostEqual(self.low['summary']['mean_annual_gdd5_c_days'],41.18836975,places=4)

    def test_twenty_year_monthly_precipitation_is_annual_mean_not_accumulated_supply(self):
        self.assertEqual(self.multi['row_count'],7305)
        self.assertEqual(len(self.multi['annual']),20)
        self.assertAlmostEqual(sum(m['precipitation_mm'] for m in self.multi['monthly']),self.multi['summary']['mean_annual_precipitation_mm'])
        self.assertFalse(self.multi['production_input_applied'])
        self.assertEqual(self.multi['field_evidence']['terrestrial_allocation'],'DATA_NEEDED')

    def test_thermal_screen_does_not_authorize_soil_or_yield(self):
        crops={c['crop_id']:c for c in self.low['candidate_analysis']}
        self.assertEqual(crops['barley']['thermal_screen']['status'],'screening_pass_not_validated')
        self.assertEqual(crops['potato']['thermal_screen']['status'],'screened_out')
        self.assertEqual(crops['lettuce']['thermal_screen']['status'],'NOT_APPLICABLE_CONTROLLED_ENVIRONMENT')
        for crop in crops.values():
            self.assertIsNone(crop['soil_suitable']);self.assertIsNone(crop['climate_suitable']);self.assertIsNone(crop['local_yield_kg_ha'])
        self.assertFalse(self.low['et0_method']['irrigation_or_allocation'])
        self.assertFalse(self.low['et0_method']['locally_validated'])
        self.assertIn('automatic_parameters',self.low['source']['hashes'])

    def test_unknown_context_is_rejected_not_silently_substituted(self):
        with self.assertRaises(ValueError):analyze_northern_baseline('nasa_ssp585_2050')

if __name__=='__main__':unittest.main()
