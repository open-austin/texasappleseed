#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import division, print_function

import os
from multiprocessing.pool import Pool

import pandas as pd

race_columns = [
    u'Asian', u'Black_or_African_American', u'Hispanic_Latino',
    u'Two_or_more_races', u'White', u'American_Indian_or_Alaska_Nat',
    u'Native_Hawaiian_Other_Pacific'
]

categorical_columns = {'DISTNAME', 'CATEGORY', 'ACTION_GROUP'}


def as_categories(df, cols):
    df = df.copy()
    for col in categorical_columns.intersection(cols).intersection(df.columns):
        df[col] = df[col].astype('category')
    return df


def read_enrollment(fn):
    df = pd.read_excel(fn, index_col='DISTRICT', na_values=-99)
    #  df = as_categories(df, categorical_columns)
    df.rename(columns={"ECONOMIC": "TOTAL"}, inplace=True)
    return df


def read_discipline(fn):
    df = pd.read_excel(fn, na_values=-99)

    # The values of discipline.CATEGORY are all columns in enrollment
    # Remove special chars so they match exactly
    df.CATEGORY.replace(
        regex=True,
        to_replace=r'[^0-9a-zA-Z]+',
        value='_',
        inplace=True
    )

    #  df = as_categories(df, categorical_columns)

    return df


def unique_actions(df):
    return df.query('CATEGORY == "MALE" or CATEGORY == "FEMALE"')


def actions_by_district(df, fillna=1):
    df = unique_actions(df.fillna(fillna))
    actions = df.groupby(['DISTRICT', 'ACTION_GROUP']).ACTIONS.sum()
    actions = actions.reset_index(name='ACTIONS')
    actions = actions.pivot(
        index='DISTRICT', columns='ACTION_GROUP', values='ACTIONS'
    )
    return actions.fillna(0)


def fraction_of_pop(enrollment, discipline, fillna=1):
    actions = actions_by_district(discipline, fillna=fillna)
    totals = enrollment['TOTAL']
    frac = (actions.T / totals).T
    frac = frac.fillna(0)
    frac['TOTAL'] = enrollment['TOTAL']
    return frac


def create_hdf5(fn):
    pool = Pool(3)
    files = [
        '2012 District Enrollment data.xlsx',
        '2013 District Enrollment Data.xlsx',
        '2014 District Enrollment Data.xlsx',
    ]
    result = pool.map(read_enrollment, files)
    e = {12: result[0], 13: result[1], 14: result[2]}
    files = [
        '2012 District Discipline Data.xlsx',
        '2013 District Discipline Data.xlsx',
        '2014 District Discipline data.xlsx',
    ]
    result = pool.map(read_discipline, files)
    d = {12: result[0], 13: result[1], 14: result[2]}

    pool.close()
    pool.join()

    for year in 12, 13, 14:
        key = '20{}/district/'.format(year)
        e[year].to_hdf(fn, key + 'enrollment')
        d[year].to_hdf(fn, key + 'discipline')


def load_data(fn):
    store = pd.HDFStore(fn)
    e = {}
    d = {}
    for year in 12, 13, 14:
        key = '20{}/district/'.format(year)
        e[year] = store[key + 'enrollment']
        d[year] = store[key + 'discipline']
    return e, d


def output_reports(e, d):
    for year in (12, 13, 14):
        frac = fraction_of_pop(e[year], d[year])
        name = "20{}_actions_per_capita.csv".format(year)
        frac.to_csv(name)

    d_all = pd.concat(d.values())

    def drop(e):
        return e.drop(['YEAR', 'DISTNAME'], axis=1).fillna(1)
    e_all = drop(e[12]) + drop(e[13]) + drop(e[14])

    frac = fraction_of_pop(e_all, d_all)
    name = "all_actions_per_capita.csv"
    frac.to_csv(name)


def main():
    datafile = 'discipline.h5'
    if not os.path.isfile(datafile):
        create_hdf5(datafile)
    e, d = load_data(datafile)
    output_reports(e, d)


if __name__ == '__main__':
    main()
