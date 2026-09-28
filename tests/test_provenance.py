import tempfile
import unittest
from pathlib import Path
from backend.provenance import ProvenanceStore, digest, immutable_write

class ProvenanceTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root=Path(self.temp.name)
        self.store=ProvenanceStore(self.root/'db.sqlite')
        self.raw=b'original data'
        self.meta=dict(dataset_id='example-v1',content_sha256=digest(self.raw),provider='test',source_url='local:test',classification='SIMULATION / EXPLANATORY',access_date='2026-09-22',units={'x':'m'},license='test-only')

    def test_raw_is_immutable(self):
        path=self.root/'raw'
        immutable_write(path,self.raw)
        immutable_write(path,self.raw)
        with self.assertRaises(ValueError): immutable_write(path,b'changed')
        self.assertEqual(path.read_bytes(),self.raw)

    def test_hash_mismatch_and_missing_provenance_rejected(self):
        with self.assertRaises(ValueError): self.store.register(self.meta,b'changed')
        with self.assertRaises(ValueError): self.store.register({**self.meta,'license':''},self.raw)

    def test_registered_version_cannot_be_relabelled(self):
        self.store.register(self.meta,self.raw)
        with self.assertRaises(ValueError): self.store.register({**self.meta,'classification':'EXTERNAL OBSERVATION'},self.raw)

    def test_run_identity_is_reproducible_and_parameter_sensitive(self):
        first=self.store.record_run({'budget':10},{'output':3})
        self.assertEqual(first,self.store.record_run({'budget':10},{'output':3}))
        self.assertNotEqual(first,self.store.record_run({'budget':11},{'output':3}))

