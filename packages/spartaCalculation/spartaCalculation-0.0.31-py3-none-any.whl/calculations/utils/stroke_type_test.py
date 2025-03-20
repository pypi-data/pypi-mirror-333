import unittest

from parameterized import parameterized

from calculations.utils.stroke_type import determine_stroke_type


class TestDetermineStrokeType(unittest.TestCase):
    @parameterized.expand(
        [("Butterfly"), ("Backstroke"), ("Breaststroke"), ("Freestyle")]
    )
    def test_determine_stroke_type_for_others(self, expected):
        stroke_type = determine_stroke_type(
            0,
            {
                "lap_distance": 400,
                "relay_leg": 0,
                "stroke_type": expected,
            },
        )

        self.assertEqual(stroke_type, expected)


class TestDetermineStrokeTypeForIndividualMedley(unittest.TestCase):
    @parameterized.expand(
        [
            (400, 0, "Butterfly"),
            (400, 1, "Butterfly"),
            (400, 5, "Breaststroke"),
            (400, 7, "Freestyle"),
            (200, 0, "Butterfly"),
            (200, 1, "Backstroke"),
            (200, 2, "Breaststroke"),
            (200, 3, "Freestyle"),
        ]
    )
    def test_for_individual_medley(self, lap_distance, index, expected):
        stroke_type = determine_stroke_type(
            index,
            {
                "lap_distance": lap_distance,
                "relay_leg": 0,
                "relay_type": None,
                "stroke_type": "Individual Medley",
            },
        )

        self.assertEqual(stroke_type, expected)

        stroke_type_for_medley = determine_stroke_type(
            index,
            {
                "lap_distance": lap_distance,
                "relay_leg": 0,
                "relay_type": None,
                "stroke_type": "Medley",
            },
        )

        self.assertEqual(stroke_type_for_medley, expected)

    @parameterized.expand(
        [
            (400, 0, "Butterfly"),
            (400, 1, "Butterfly"),
            (400, 5, "Backstroke"),
            (400, 7, "Backstroke"),
            (400, 10, "Breaststroke"),
            (400, 11, "Breaststroke"),
            (400, 14, "Freestyle"),
            (200, 0, "Butterfly"),
            (200, 1, "Butterfly"),
            (200, 2, "Backstroke"),
            (200, 3, "Backstroke"),
        ]
    )
    def test_for_scm_individual_medley(self, lap_distance, index, expected):
        stroke_type = determine_stroke_type(
            index,
            {
                "lap_distance": lap_distance,
                "pool_type": "SCM",
                "relay_leg": 0,
                "relay_type": None,
                "stroke_type": "Individual Medley",
            },
        )

        self.assertEqual(stroke_type, expected)

        stroke_type_for_medley = determine_stroke_type(
            index,
            {
                "lap_distance": lap_distance,
                "pool_type": "SCM",
                "relay_leg": 0,
                "relay_type": None,
                "stroke_type": "Medley",
            },
        )

        self.assertEqual(stroke_type_for_medley, expected)


class TestDetermineStrokeTypeForParaMedley(unittest.TestCase):
    @parameterized.expand(
        [
            (150, "LCM", 0, "Backstroke"),
            (150, "LCM", 1, "Breaststroke"),
            (150, "LCM", 2, "Freestyle"),
            
            (150, "SCM", 0, "Backstroke"),
            (150, "SCM", 1, "Backstroke"),
            (150, "SCM", 2, "Breaststroke"),
            (150, "SCM", 3, "Breaststroke"),
            (150, "SCM", 4, "Freestyle"),
            (150, "SCM", 5, "Freestyle"),
        ]
    )
    def test_for_para_medley(self, lap_distance, pool_type, index, expected):
        stroke_type = determine_stroke_type(
            index,
            {
                "lap_distance": lap_distance,
                "relay_leg": 0,
                "relay_type": None,
                "stroke_type": "Para-Medley",
                "pool_type": pool_type,
            },
        )

        self.assertEqual(stroke_type, expected)


class TestDetermineStrokeTypeForRelay(unittest.TestCase):
    @parameterized.expand(
        [
            (0, 0, "Backstroke"),
            (0, 1, "Breaststroke"),
            (0, 2, "Butterfly"),
            (0, 3, "Freestyle"),
        ]
    )
    def test_for_medley(self, index, relay, expected):
        stroke_type = determine_stroke_type(
            index,
            {
                "lap_distance": 200,
                "relay_leg": relay,
                "relay_type": "Medley Relay",
                "stroke_type": "Individual Medley",
            },
        )

        self.assertEqual(stroke_type, expected)

    @parameterized.expand(
        [
            (0, 0, "Backstroke"),
            (0, 1, "Breaststroke"),
            (0, 2, "Butterfly"),
            (0, 3, "Freestyle"),
        ]
    )
    def test_for_mixed_medley(self, index, relay, expected):
        stroke_type = determine_stroke_type(
            index,
            {
                "lap_distance": 200,
                "relay_leg": relay,
                "relay_type": "Mixed Medley Relay",
                "stroke_type": "Individual Medley",
            },
        )

        self.assertEqual(stroke_type, expected)

    @parameterized.expand(
        [
            (0, 1),
            (0, 2),
            (0, 3),
            (0, 4),
        ]
    )
    def test_for_freestyle_medley(self, index, relay):
        stroke_type = determine_stroke_type(
            index,
            {
                "lap_distance": 200,
                "relay_leg": relay,
                "relay_type": "Freestyle Relay",
                "stroke_type": "Individual Medley",
            },
        )

        self.assertEqual(stroke_type, "Freestyle")

    @parameterized.expand(
        [
            (0, 1),
            (0, 2),
            (0, 3),
            (0, 4),
        ]
    )
    def test_for_mixed_freestyle_medley(self, index, relay):
        stroke_type = determine_stroke_type(
            index,
            {
                "lap_distance": 200,
                "relay_leg": relay,
                "relay_type": "Mixed Freestyle Relay",
                "stroke_type": "Individual Medley",
            },
        )

        self.assertEqual(stroke_type, "Freestyle")


if __name__ == "__main__":
    unittest.main()