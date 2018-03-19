"""
tests for valorum.data.bls

@author : Spencer Lyon
@date : 2014-07-31

"""
import os
import unittest

import pandas as pd
import valorum
from valorum.data import options


DIR = os.path.join(options["PATHS.data"], "test")

if not os.path.exists(DIR):
    os.makedirs(DIR)


def _gen_data():
    b = valorum.data.BLSData()
    df1 = b.get("LASST040000000000006", 1990, 1990, nice_names=0)
    df2 = b.get("LASST040000000000006", 1990, 1990, nice_names=1)
    df3 = b.get("LASST040000000000006", 1990, 1990, nice_names=0, wide=1)
    df4 = b.get("LASST040000000000006", 1990, 1990, nice_names=1, wide=1)

    df1.to_csv(os.path.join(DIR, "LASST040000000000006_1990_1990.csv"))
    df2.to_csv(os.path.join(DIR, "LASST040000000000006_1990_1990_nice.csv"))
    df3.to_csv(os.path.join(DIR, "LASST040000000000006_1990_1990_wide.csv"))
    df4.to_csv(os.path.join(DIR, "LASST040000000000006_1990_1990_nice_wide.csv"))


class TestBLSData(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.b = valorum.data.BLSData()

    def test_get_one_series(self):
        files = [
            os.path.join(DIR, "LASST040000000000006_1990_1990.csv"),
            os.path.join(DIR, "LASST040000000000006_1990_1990_nice.csv"),
            os.path.join(DIR, "LASST040000000000006_1990_1990_wide.csv"),
            os.path.join(DIR, "LASST040000000000006_1990_1990_nice_wide.csv")
        ]
        if not os.path.exists(files[0]):
            _gen_data()

        for fn, nice, wide in zip(files, [0, 1, 0, 1], [0, 0, 1, 1]):
            print(fn)
            want = pd.read_csv(fn, index_col=0, parse_dates=["Date"])
            have = self.b.get(
                "LASST040000000000006", 1990, 1990, nice_names=nice, wide=wide
            )
            assert want.equals(have)

            if not wide:
                self.assertTrue(have.shape == (12, 3))
                if nice:
                    self.assertTrue(
                        (have["variable"] == "Labor Force: Arizona (S)").all()
                    )
                else:
                    self.assertTrue(
                        (have["variable"] == "LASST040000000000006").all()
                    )
            else:
                self.assertTrue(have.shape == (12, 1))
                self.assertIsInstance(have.index, pd.DatetimeIndex)
