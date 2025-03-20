import unittest

from sklearn.metrics import roc_auc_score, roc_curve, average_precision_score

from onad.model.unsupervised.autoencoder import Autoencoder
from onad.stream.streamer import ParquetStreamer, Dataset
from onad.transform.scale import MinMaxScaler


class TestCaseAutoencoder(unittest.TestCase):
    def test_shuttle(self):

        scaler = MinMaxScaler()

        model = Autoencoder(hidden_sizes=[32, 16],
                            latent_size=4,
                            learning_rate=0.0001,
                            dropout=0.05, seed=1)

        model = scaler | model

        labels, scores = [], []
        with ParquetStreamer(dataset=Dataset.FRAUD) as streamer:
            for i, (x, y) in enumerate(streamer):
                if y == 0 and i < 100_000:
                    model.learn_one(x)
                    continue
                model.learn_one(x)
                score = model.score_one(x)

                labels.append(y)
                scores.append(score)

        roc_auc = round(roc_auc_score(labels, scores), 3)
        self.assertEqual(roc_auc, 0.96)

        fpr, tpr, thresholds = roc_curve(labels, scores)
        print(f"{fpr}, {tpr}, {thresholds}")
        #self.assertAlmostEqual(sum(fpr), 4983.480, places=1)
        #self.assertAlmostEqual(sum(tpr), 9747.686, places=1)
        #self.assertAlmostEqual(sum(thresholds[1:]), 4703.747, places=1)

        avg_pre = round(average_precision_score(labels, scores), 3)
        print(avg_pre)
        self.assertEqual(avg_pre, 0.749)


if __name__ == '__main__':
    unittest.main()
