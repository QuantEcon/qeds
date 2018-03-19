import unittest
import valorum
import pandas as pd


class TestAllLoaders(unittest.TestCase):

    def test_load(self):
        for ds in valorum.data.available():
            if ds != "nyc_employee":
                print("Trying", ds)
                self.assertIsInstance(valorum.data.load(ds), pd.DataFrame)
