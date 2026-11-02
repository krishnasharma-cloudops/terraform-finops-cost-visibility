import importlib.util
import json
import pathlib
import unittest
from decimal import Decimal
ROOT = pathlib.Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('cost_report', ROOT / 'scripts' / 'cost_report.py')
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

class CostReportTests(unittest.TestCase):
    def test_infracost(self):
        data = json.loads((ROOT / 'samples' / 'infracost-example.json').read_text())
        rows = module.infracost_report(data)
        self.assertEqual(sum((x[1] for x in rows), Decimal('0')), Decimal('20.50'))

    def test_opencost(self):
        data = json.loads((ROOT / 'samples' / 'opencost-example.json').read_text())
        rows = module.opencost_report(data)
        self.assertEqual(rows[0], ('dev', Decimal('4.25')))

    def test_render_distinguishes_time_bases(self):
        text = module.report({'projects': []}, {'data': []})
        self.assertIn('different time bases', text)

    def test_bad_schema(self):
        with self.assertRaises(ValueError):
            module.infracost_report({'projects': 'not-a-list'})

if __name__ == '__main__':
    unittest.main()
