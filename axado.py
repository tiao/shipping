# -*- coding: utf8 -*-
""" Shipping Calculation

Makes the shipping calculation based in input parameters:
  -> source
  -> destination
  -> price
  -> package weight.

The csv tables in data directory contains all the information for
the calculations.
"""
import csv
import os


def load_file(filename):
    """ Load filename csv/tsv and return a dictionary

    The header of csv is used as keys od dict.
    """
    if '.tsv' in filename:
        delimiter = '\t'
    elif '.csv' in filename:
        delimiter = ','
    else:
        print('Unsuported format: ' + filename)
        return None

    with open(filename) as cvsfile:
        reader = csv.DictReader(cvsfile, delimiter=delimiter)
        return [row for row in reader]


def load_tables(data_dir):
    """ Load the tables from data_dir and return a dictionary with all data
    """
    tables = [d for d in os.listdir(data_dir)
              if os.path.isdir(os.path.join(data_dir, d))]
    data = {}
    for table in tables:
        data.update({table: {}})
        table_dir = os.path.join(data_dir, table)
        for f in os.listdir(table_dir):
            name = os.path.splitext(f)
            file = os.path.join(table_dir, f)
            data[table].update({name[0]: load_file(file)})

    return data
