import pickle
import unittest

import pandas as pd
from sklearn.preprocessing import MinMaxScaler

from algorithms.kmeans import KMeans


class KMeansTest(unittest.TestCase):
    def setUp(self):
        sc = MinMaxScaler()

        dataset = pd.read_csv('s2/tests/datasets/iris.csv')
        dataset = dataset.iloc[:, :4].values
        self.dataset = sc.fit_transform(dataset)

        self.seed = 42

    def test_kmeans_with_invalid_clusters(self):
        with self.assertRaises(ValueError):
            _ = KMeans(K=0, name='test')

    def test_kmeans_with_invalid_visualization_dimensions(self):
        with self.assertRaises(ValueError):
            _ = KMeans(K=0, name='test')

    def test_kmeans_with_invalid_metric(self):
        with self.assertRaises(ValueError):
            _ = KMeans(K=3, metric='mahalanobis', name='test')

    def test_predict_before_fit_throws_error(self):
        kmeans = KMeans(K=3, metric='euclidean', vis_dims=0, seed=self.seed, name='test')

        with self.assertRaises(Exception):
            kmeans.predict(self.dataset)

    def test_kmeans(self):
        with open('s2/tests/datasets/iris.pkl', mode='rb') as f:
            expected_predictions = pickle.load(f)

        kmeans = KMeans(K=3, metric='euclidean', vis_dims=0, seed=self.seed, name='test')

        predictions = kmeans.fit_predict(self.dataset)

        self.assertEqual(predictions, expected_predictions)


if __name__ == '__main__':
    unittest.main()
