# -*- coding: utf8 -*-
""" Shipping Calculation

Makes the shipping calculation based in input parameters:
  -> source
  -> destination
  -> price
  -> weight.

The csv tables in data directory contains all the information for
the calculations.
"""
import csv
import os
import argparse


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


def parse_arguments(args):
    """  Parser args from command line

    The basic usage is:
    axado.py <origem> <destino> <nota_fiscal> <peso>

    Return a dict with informations
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('origem', type=str, help='Local de origem')
    parser.add_argument('destino', type=str, help='Local de destino')
    parser.add_argument('nota_fiscal', type=float, help='Valor da nota fiscal')
    parser.add_argument('peso', type=float, help='Peso do objeto')
    values = parser.parse_args(args)

    data = {}
    data['src'] = values.origem
    data['dst'] = values.destino
    data['price'] = values.nota_fiscal
    data['weight'] = values.peso

    return data
