import unittest

import pandas as pd
import numpy as np
import qiime2

from genome_sampler.subsample_longitudinal import subsample_longitudinal


class TestSubsampleLongitudinal(unittest.TestCase):

    _N_TEST_ITERATIONS = 50

    def setUp(self):
        s1 = pd.Series(['2019-12-31', '2020-01-09', '2020-01-10',
                        '2019-11-01', '2020-01-11', '2020-02-21',
                        '2020-02-21', '2020-02-21', '2020-03-15'],
                       index=[chr(x) for x in range(65, 74)])
        s1.index.name = 'id'
        s1.name = 'date-md'
        self.md1 = qiime2.CategoricalMetadataColumn(s1)

        s2 = pd.Series(['2020-01-02', '2019-11-01', '2020-02-21',
                        '2020-02-21', '2020-02-21', '2020-03-15',
                        '2020-01-03', '2020-01-04', '2020-01-05',
                        '2020-01-06', '2020-01-07', '2020-01-08',
                        '2020-01-09', '2020-01-10', '2020-01-11',
                        '2020-01-12', '2020-01-13', '2020-01-14',
                        '2020-01-15', '2020-01-16', '2020-01-17'],
                       index=[chr(x) for x in range(65, 86)])
        s2.index.name = 'id'
        s2.name = 'date-md'
        self.md2 = qiime2.CategoricalMetadataColumn(s2)

    def test_default(self):
        sel = subsample_longitudinal(self.md1)

        self.assertEqual(sel.inclusion.sum(), 9)
        self.assertEqual(sel.metadata.get_column('date-md'), self.md1)
        self.assertEqual(sel.label, 'subsample_longitudinal')

    def test_start_date_in_data(self):
        sel = subsample_longitudinal(self.md1, start_date='2019-12-31')

        self.assertEqual(sel.inclusion.sum(), 8)
        self.assertEqual(sel.metadata.get_column('date-md'), self.md1)
        self.assertEqual(sel.label, 'subsample_longitudinal')
        self.assertFalse(np.nan in list(sel.inclusion.index))

    def test_start_date_not_in_data(self):
        sel = subsample_longitudinal(self.md1, start_date='2019-12-30')

        self.assertEqual(sel.inclusion.sum(), 8)
        self.assertEqual(sel.metadata.get_column('date-md'), self.md1)
        self.assertEqual(sel.label, 'subsample_longitudinal')
        self.assertFalse(np.nan in list(sel.inclusion.index))

    def test_one_sample_per_interval(self):
        sel = subsample_longitudinal(self.md1, samples_per_interval=1)

        self.assertEqual(sel.inclusion.sum(), 6)
        self.assertEqual(sel.metadata.get_column('date-md'), self.md1)
        self.assertEqual(sel.label, 'subsample_longitudinal')

    def test_two_sample_per_interval(self):
        sel = subsample_longitudinal(self.md1, samples_per_interval=2)

        self.assertEqual(sel.inclusion.sum(), 8)
        self.assertEqual(sel.metadata.get_column('date-md'), self.md1)
        self.assertEqual(sel.label, 'subsample_longitudinal')

    def test_interval_bounds1(self):
        for _ in range(self._N_TEST_ITERATIONS):
            sel = subsample_longitudinal(self.md2, samples_per_interval=1,
                                         start_date='2019-12-26')

            exp_int1_dates = ['2020-01-02', '2020-01-03', '2020-01-04',
                              '2020-01-05', '2020-01-06', '2020-01-07',
                              '2020-01-08']
            exp_int2_dates = ['2020-01-09', '2020-01-10', '2020-01-11',
                              '2020-01-12', '2020-01-13', '2020-01-14',
                              '2020-01-15']
            exp_int3_dates = ['2020-01-16', '2020-01-17']
            exp_int4_dates = ['2020-02-21']
            exp_int5_dates = ['2020-03-15']

            self.assertEqual(sel.inclusion.sum(), 5)
            self.assertEqual(sel.metadata.get_column('date-md'), self.md2)
            self.assertEqual(sel.label, 'subsample_longitudinal')

            sampled_dates = set(self.md2.to_series()[sel.inclusion].values)
            self.assertEqual(len(sampled_dates & set(exp_int1_dates)), 1)
            self.assertEqual(len(sampled_dates & set(exp_int2_dates)), 1)
            self.assertEqual(len(sampled_dates & set(exp_int3_dates)), 1)
            self.assertEqual(len(sampled_dates & set(exp_int4_dates)), 1)
            self.assertEqual(len(sampled_dates & set(exp_int5_dates)), 1)

    def test_interval_bounds2(self):
        for _ in range(self._N_TEST_ITERATIONS):
            sel = subsample_longitudinal(self.md2, samples_per_interval=1,
                                         start_date='2019-12-27')

            exp_int1_dates = ['2020-01-02']
            exp_int2_dates = ['2020-01-03', '2020-01-04', '2020-01-05',
                              '2020-01-06', '2020-01-07', '2020-01-08',
                              '2020-01-09']
            exp_int3_dates = ['2020-01-10', '2020-01-11', '2020-01-12',
                              '2020-01-13', '2020-01-14', '2020-01-15',
                              '2020-01-16']
            exp_int4_dates = ['2020-01-17']
            exp_int5_dates = ['2020-02-21']
            exp_int6_dates = ['2020-03-15']

            self.assertEqual(sel.inclusion.sum(), 6)
            self.assertEqual(sel.metadata.get_column('date-md'), self.md2)
            self.assertEqual(sel.label, 'subsample_longitudinal')

            sampled_dates = set(self.md2.to_series()[sel.inclusion].values)
            self.assertEqual(len(sampled_dates & set(exp_int1_dates)), 1)
            self.assertEqual(len(sampled_dates & set(exp_int2_dates)), 1)
            self.assertEqual(len(sampled_dates & set(exp_int3_dates)), 1)
            self.assertEqual(len(sampled_dates & set(exp_int4_dates)), 1)
            self.assertEqual(len(sampled_dates & set(exp_int5_dates)), 1)
            self.assertEqual(len(sampled_dates & set(exp_int6_dates)), 1)

    def test_interval_bounds3(self):
        for _ in range(self._N_TEST_ITERATIONS):
            sel = subsample_longitudinal(self.md2, samples_per_interval=1,
                                         start_date='2019-12-28')

            exp_int1_dates = ['2020-01-02', '2020-01-03']
            exp_int2_dates = ['2020-01-04', '2020-01-05',
                              '2020-01-06', '2020-01-07', '2020-01-08',
                              '2020-01-09', '2020-01-10']
            exp_int3_dates = ['2020-01-11', '2020-01-12',
                              '2020-01-13', '2020-01-14', '2020-01-15',
                              '2020-01-16', '2020-01-17']
            exp_int4_dates = ['2020-02-21']
            exp_int5_dates = ['2020-03-15']

            self.assertEqual(sel.inclusion.sum(), 5)
            self.assertEqual(sel.metadata.get_column('date-md'), self.md2)
            self.assertEqual(sel.label, 'subsample_longitudinal')

            sampled_dates = set(self.md2.to_series()[sel.inclusion].values)
            self.assertEqual(len(sampled_dates & set(exp_int1_dates)), 1)
            self.assertEqual(len(sampled_dates & set(exp_int2_dates)), 1)
            self.assertEqual(len(sampled_dates & set(exp_int3_dates)), 1)
            self.assertEqual(len(sampled_dates & set(exp_int4_dates)), 1)
            self.assertEqual(len(sampled_dates & set(exp_int5_dates)), 1)

    def test_interval_size(self):
        for _ in range(self._N_TEST_ITERATIONS):
            sel = subsample_longitudinal(self.md2, start_date='2019-12-19',
                                         samples_per_interval=1,
                                         days_per_interval=14)

            exp_int1_dates = ['2020-01-02', '2020-01-03', '2020-01-04',
                              '2020-01-05', '2020-01-06', '2020-01-07',
                              '2020-01-08', '2020-01-09', '2020-01-10',
                              '2020-01-11', '2020-01-12', '2020-01-13',
                              '2020-01-14', '2020-01-15']
            exp_int2_dates = ['2020-01-16', '2020-01-17']
            exp_int3_dates = ['2020-02-21']
            exp_int4_dates = ['2020-03-15']

            self.assertEqual(sel.inclusion.sum(), 4)
            self.assertEqual(sel.metadata.get_column('date-md'), self.md2)
            self.assertEqual(sel.label, 'subsample_longitudinal')

            sampled_dates = set(self.md2.to_series()[sel.inclusion].values)
            self.assertEqual(len(sampled_dates & set(exp_int1_dates)), 1)
            self.assertEqual(len(sampled_dates & set(exp_int2_dates)), 1)
            self.assertEqual(len(sampled_dates & set(exp_int3_dates)), 1)
            self.assertEqual(len(sampled_dates & set(exp_int4_dates)), 1)

    def test_seed(self):
        sel1 = subsample_longitudinal(self.md2, samples_per_interval=1,
                                      start_date='2019-12-26', seed=1)
        for _ in range(self._N_TEST_ITERATIONS):
            sel2 = subsample_longitudinal(self.md2, samples_per_interval=1,
                                          start_date='2019-12-26', seed=1)
            self.assertEqual(list(sel1.inclusion.items()),
                             list(sel2.inclusion.items()))
