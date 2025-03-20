import unittest

from parameterized import parameterized
from glom import glom
from calculations.columns.dps import calculate_dps
from calculations.test_data.utils import read_test_data


class TestCalculateDpsFor50mLCM(unittest.TestCase):
    def setUp(self):
        self.annotation = read_test_data("lcm/50meter_race/annotations.json")
        self.laptimes = read_test_data("lcm/50meter_race/lap_times.json")

        self.start_frame = self.annotation["0"]["frames"][0]

    @parameterized.expand([("Freestyle"), ("Backstroke")])
    def test_calculate_dps(self, stroke_type):
        """It returns the dps for the segment passed"""
        result = calculate_dps(
            annotation=self.annotation["0"],
            start=0,
            end=15,
            lane_info={"stroke_type": stroke_type},
            pool_length=50,
        )

        self.assertEqual(result, 2.15)

    @parameterized.expand([("Freestyle"), ("Backstroke")])
    def test_calculate_dps_exclude_extra_stroke(self, stroke_type):
        """It returns the dps for the segment passed excluding extra stroke"""
        result = calculate_dps(
            annotation=self.annotation["0"],
            start=0,
            end=15,
            lane_info={"stroke_type": stroke_type},
            pool_length=50,
            exclude_extra_pickup=True,
        )

        self.assertEqual(result, 2.1)

    @parameterized.expand([("Breaststroke")])
    def test_calculate_dps_other_stroke_types(self, stroke_type):
        """It returns the dps for the other stroke types"""
        result = calculate_dps(
            annotation=self.annotation["0"],
            start=0,
            end=15,
            lane_info={"stroke_type": stroke_type},
            pool_length=50,
        )

        self.assertEqual(result, 1.05)


class TestCalculateDpsFor100mBfSCM(unittest.TestCase):
    def setUp(self):
        self.annotation = glom(
            read_test_data("scm/100meter_bf_race/annotations.json"),
            "annotations.correctedAnnotations",
        )

        self.start_frame = self.annotation["0"].get("frames")[0]

    @parameterized.expand([("Butterfly")])
    def test_calculate_dps(self, stroke_type):
        """It returns the dps for the segment passed"""
        result = calculate_dps(
            annotation=self.annotation["0"],
            start=15,
            end=20,
            lane_info={"stroke_type": stroke_type},
            pool_length=25,
        )

        self.assertEqual(result, 1.93)

        # calculate dps for last segment
        result = calculate_dps(
            annotation=self.annotation["3"],
            start=85,
            end=95,
            lane_info={"stroke_type": stroke_type},
            pool_length=25,
        )

        self.assertEqual(result, 1.75)


class TestCalculateDpsFor200mFrSCM(unittest.TestCase):
    def setUp(self):
        self.annotation = glom(
            read_test_data("scm/200meter_fs_race/annotations.json"),
            "annotations.correctedAnnotations",
        )

        self.start_frame = self.annotation["0"].get("frames")[0]

    @parameterized.expand([("Freestyle"), ("Backstroke")])
    def test_calculate_dps(self, stroke_type):
        """It returns the dps for the segment passed"""
        start_segment_result = calculate_dps(
            annotation=self.annotation["1"],
            start=25,
            end=50,
            lane_info={"stroke_type": stroke_type},
            pool_length=25,
        )

        self.assertEqual(start_segment_result, 2.37)

        mid_segment_result = calculate_dps(
            annotation=self.annotation["4"],
            start=100,
            end=125,
            lane_info={"stroke_type": stroke_type},
            pool_length=25,
        )

        self.assertEqual(mid_segment_result, 2.33)

        # calculate dps for last segment
        last_segment_result = calculate_dps(
            annotation=self.annotation["7"],
            start=175,
            end=200,
            lane_info={"stroke_type": stroke_type},
            pool_length=25,
        )

        self.assertEqual(last_segment_result, 2.28)


if __name__ == "__main__":
    unittest.main()
