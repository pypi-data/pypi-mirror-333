import unittest

from sklearn.metrics import roc_auc_score, roc_curve, average_precision_score

from onad.model.unsupervised.lstm_autoencoder import LSTMAutoencoder
from onad.stream.streamer import ParquetStreamer, Dataset
from onad.transform.scale import MinMaxScaler


class TestCaseAutoencoder(unittest.TestCase):
    def test_shuttle(self):

        scaler = MinMaxScaler()

        model = LSTMAutoencoder(
            encoder_units=[128, 64],
            decoder_units=[64, 128],
            latent_size=4,
            dropout=0.15,
            learning_rate=0.005,
            seed=1,
        )

        model = scaler | model

        labels, scores = [], []
        with ParquetStreamer(dataset=Dataset.SHUTTLE) as streamer:
            for i, (x, y) in enumerate(streamer):
                if i < 10_000:
                    model.learn_one(x)
                    continue
                model.learn_one(x)
                score = model.score_one(x)

                labels.append(y)
                scores.append(score)

        roc_auc = round(roc_auc_score(labels, scores), 3)
        self.assertEqual(roc_auc, 0.985)

        fpr, tpr, thresholds = roc_curve(labels, scores)
        self.assertAlmostEqual(sum(fpr), 96.616, places=1)
        self.assertAlmostEqual(sum(tpr), 331.771, places=1)
        self.assertAlmostEqual(sum(thresholds[1:]), 2.343, places=1)

        avg_pre = round(average_precision_score(labels, scores), 3)
        self.assertEqual(avg_pre, 0.959)


if __name__ == "__main__":
    unittest.main()
