import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from fastapi.testclient import TestClient
from backend.app import app
from backend.provenance import ProvenanceStore
from backend.pwn import simulated_profile_csv

class EndToEnd(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.store=ProvenanceStore(Path(self.temp.name)/'test.sqlite')
        self.mock=patch('backend.app.store',self.store)
        self.mock.start();self.addCleanup(self.mock.stop)
        self.client=TestClient(app)
        self.client.__enter__();self.addCleanup(self.client.__exit__,None,None,None)

    def test_real_data_to_transfer_and_decision(self):
        overview=self.client.get('/api/overview')
        self.assertEqual(overview.status_code,200)
        self.assertEqual(len(overview.json()['datasets']),6)
        transfer=self.client.get('/api/transfer')
        self.assertEqual(transfer.status_code,200)
        sites=transfer.json()['sites']
        self.assertEqual(len(sites),6)
        self.assertIsNone(next(s for s in sites if s['site_id']=='longyearbyen')['water_balance'])
        self.assertGreater(sites[0]['water_balance']['totals']['deficit_mm'],0)
        r=self.client.post('/api/decision',json={})
        self.assertEqual(r.status_code,200)
        self.assertTrue(r.json()['run_id'])
        self.assertEqual(r.json()['run_id'],self.client.post('/api/decision',json={}).json()['run_id'])

    def test_invalid_parameters_rejected(self):
        self.assertEqual(self.client.post('/api/decision',json={'output_target_kg':-1}).status_code,422)
        self.assertEqual(self.client.post('/api/decision',json={'unknown_score':87}).status_code,422)

    def test_tank_cannot_drive_marine_treatment(self):
        r=self.client.post('/api/sensitivity',json={'source_kind':'OUR_NEW_MEASUREMENT_TANK'})
        self.assertEqual(r.status_code,422)

    def test_simulation_fixture_never_becomes_observation(self):
        r=self.client.get('/api/pwn/example')
        self.assertEqual(r.status_code,200)
        self.assertEqual(r.json()['source_kind'],'SIMULATION_EXPLANATORY')
        self.assertIsNone(r.json()['derived_salinity'])
        self.assertAlmostEqual(r.json()['analysis']['layers'][0]['depth_m'],0.3,places=2)
        r=self.client.post('/api/pwn/analyze',files={'file':('profile.csv',simulated_profile_csv(),'text/csv')},data={'source_kind':'OUR_NEW_MEASUREMENT_TANK','raw_conductivity_unit':'arbitrary_unit'})
        self.assertEqual(r.status_code,422)

    def test_external_upload_requires_provenance(self):
        r=self.client.post('/api/pwn/analyze',files={'file':('profile.csv',b'x','text/csv')},data={'source_kind':'EXTERNAL_OBSERVATION','raw_conductivity_unit':'mV'})
        self.assertEqual(r.status_code,422)

    def test_valid_upload_is_immutable_and_repeatable(self):
        with patch('backend.app.ROOT',Path(self.temp.name)):
            data={'source_kind':'SIMULATION_EXPLANATORY','raw_conductivity_unit':'arbitrary_unit','depth_method':'encoder_vertical_tank'}
            files={'file':('profile.csv',simulated_profile_csv(),'text/csv')}
            first=self.client.post('/api/pwn/analyze',files=files,data=data)
            again=self.client.post('/api/pwn/analyze',files=files,data=data)
            self.assertEqual(first.status_code,200)
            self.assertEqual(first.json()['dataset_id'],again.json()['dataset_id'])
            saved=Path(self.temp.name)/'data/pwn/raw'/f"{first.json()['sha256']}.csv"
            self.assertEqual(saved.read_bytes(),simulated_profile_csv())
            revised=self.client.post('/api/pwn/analyze',files=files,data={**data,'depth_method':'unavailable'})
            self.assertEqual(revised.status_code,200)
            self.assertNotEqual(first.json()['dataset_id'],revised.json()['dataset_id'])
            self.assertEqual(first.json()['sha256'],revised.json()['sha256'])
