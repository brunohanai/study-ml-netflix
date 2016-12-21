# -*- coding: utf-8 -*-
import csv
from pandas import read_csv


def insert_data(label, omdb_info):
    data_file = csv.writer(open('var/data/data.csv', 'a'))

    info = list()
    info.append(label)
    map(lambda i: info.append(omdb_info[i]), adjust_omdb_info(omdb_info))

    data_file.writerow(info)


def adjust_omdb_info(omdb_info):
    # passar em cada campo
    for index, field in enumerate(omdb_info):
        omdb_info[field] = omdb_info[field].encode('utf-8')
        if omdb_info[field] == 'N/A':
            omdb_info[field] = 'None'

    omdb_info['runtime'] = omdb_info['runtime'].split()[0]
    omdb_info['year'] = omdb_info['year'].split('–')[0]

    return omdb_info


def title_is_in_database(title):
    d = read_csv('var/data/data.csv')

    return title in d['title'].unique()