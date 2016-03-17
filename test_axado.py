# -*- coding: utf8 -*-

from axado import load_tables, load_file

DIR_TEST = 'test'

PRICE_PER_KG = [
    {'nome': 'flo', 'inicial': '0', 'final': '10', 'preco': '12'},
    {'nome': 'flo', 'inicial': '11', 'final': '20', 'preco': '11'},
    {'nome': 'flo', 'inicial': '20', 'final': '30', 'preco': '10'},
    {'nome': 'flo', 'inicial': '30', 'final': '', 'preco': '5'},
]

ROUTES = [
    {'origem': 'flo', 'destino': 'bsb', 'prazo': '3', 'seguro': '3', 'kg': 'flo', 'fixa': '13'},
    {'origem': 'flo', 'destino': 'cwb', 'prazo': '3', 'seguro': '3', 'kg': 'flo', 'fixa': '7'},
    {'origem': 'flo', 'destino': 'sao', 'prazo': '4', 'seguro': '3', 'kg': 'flo', 'fixa': '7'},
    {'origem': 'flo', 'destino': 'vps', 'prazo': '1', 'seguro': '2', 'kg': 'flo', 'fixa': '11'},
]


def test_load_file_with_cvs():
    assert load_file(DIR_TEST + '/table1/price_per_kg.csv') == PRICE_PER_KG


def test_load_file_with_tvs():
    assert load_file(DIR_TEST + '/table2/price_per_kg.tsv') == PRICE_PER_KG


def test_load_file_with_txt():
    assert load_file(DIR_TEST + '/file.txt') is None


def test_load_tables():
    data = load_tables(DIR_TEST)
    assert data is not None
    assert data is not {}
    assert data['table1']['price_per_kg'] == PRICE_PER_KG
    assert data['table1']['routes'] == ROUTES
    assert data['table2']['price_per_kg'] == PRICE_PER_KG
