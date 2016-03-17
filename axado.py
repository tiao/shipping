#!/usr/bin/python
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
from math import ceil
import argparse
import csv
import os
import sys

# Globals variable (environment)
DIR_DATA = 'data'
ROUTE_TABLE = 'rotas'
PPK_TABLE = 'preco_por_kg'


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


def shipping_cost(input_data, route, price_per_kg):
    """ Use input data and tables to find shipping cost

    Return a tuple with time and total
    """
    seguro = input_data['price'] * float(route['seguro']) / 100

    fixa = 0
    if 'fixa' in route.keys():
        fixa = float(route['fixa'])

    faixa = input_data['weight'] * float(price_per_kg['preco'])

    subtotal = seguro + fixa + faixa

    if 'alfandega' in route.keys():
        alfandega = subtotal * (float(route['alfandega']) / 100)
        subtotal = subtotal + alfandega

    if 'icms' in route.keys():
        icms = float(route['icms'])
    else:
        icms = 6

    total = subtotal / (float(100 - icms) / 100)
    # round up total
    total = ceil(total*100) / 100
    return (int(route['prazo']), total)


def find_route(input_data, table_data):
    """ Find a row in route table based in input data

    Return a dict with data or None
    """
    route = None
    for row in table_data:
        src_equal = (input_data['src'] == row['origem'])
        dst_equal = (input_data['dst'] == row['destino'])
        if (src_equal and dst_equal) is True:
            route = row
            break

    if route is None:
        return route

    # limit == 0 equal infinite
    if 'limite' in route.keys():
        if route['limite'] == '0':
            pass
        elif input_data['weight'] > float(route['limite']):
            return None

    return route


def find_price_per_kg(input_data, table_data, route_kg):
    """ Find a row in price_per_kg table based in input data

    Return a dict with data or None
    """
    price_per_kg = None
    for row in table_data:
        name_equal = (route_kg == row['nome'])
        initial_weight = (input_data['weight'] >= float(row['inicial']))
        # final == '' equal infinite
        if row['final'] == '':
            final_weight = True
        else:
            final_weight = (input_data['weight'] < float(row['final']))

        if (name_equal and initial_weight and final_weight) is True:
            price_per_kg = row
            break

    return price_per_kg


def main(args):
    # Get parameters and info from files csvs
    input_data = parse_arguments(args)
    tables_data = load_tables(DIR_DATA)

    # Print the shipping cost for each directory in DIR_DATA
    for table in sorted(tables_data.keys()):
        time, total = (None, None)
        route = find_route(input_data, tables_data[table][ROUTE_TABLE])
        if route:
            price_per_kg = find_price_per_kg(
                input_data, tables_data[table][PPK_TABLE], route['kg'])

            time, total = shipping_cost(input_data, route, price_per_kg)

        if total is None:
            total = '-'
            time = '-'

        print("{}:{}, {}".format(table, time, total))

if __name__ == '__main__':
    main(sys.argv[1:])
