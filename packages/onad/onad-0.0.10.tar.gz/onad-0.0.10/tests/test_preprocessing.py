import unittest

from onad.stream.streamer import ParquetStreamer, Dataset
from onad.transform.scale import MinMaxScaler


class MyTestCase(unittest.TestCase):
    def test_min_max_scaler(self):

        scaler = MinMaxScaler()

        normalized_vals = []
        with ParquetStreamer(dataset=Dataset.FRAUD) as streamer:
            for x, y in streamer:
                scaler.learn_one(x)
                scaled_x = scaler.transform_one(x)
                normalized_vals.append(scaled_x)

        self.assertIsNotNone(normalized_vals)
        for i, (normalized_dict) in enumerate(normalized_vals):
            for key, value in normalized_dict.items():
                self.assertTrue(
                    0 <= value <= 1,
                    f"Instance {i} with value {value} for key {key} is not correctly normalized.",
                )


if __name__ == "__main__":
    unittest.main()
