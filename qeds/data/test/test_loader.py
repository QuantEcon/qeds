import unittest
import qeds
import pandas as pd


class TestAllLoaders(unittest.TestCase):

    def test_load(self):
        for ds in qeds.data.available():
            if ds != "nyc_employee":
                print("Trying", ds)
                self.assertIsInstance(qeds.data.load(ds), pd.DataFrame)
