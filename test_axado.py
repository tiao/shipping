# -*- coding: utf8 -*-

from axado import load_tables, load_file, parse_arguments
from axado import shipping_cost, find_route, find_price_per_kg, main
import pytest

##############################################################################
# Data for Tests
##############################################################################

# The DIR_TEST has two directory, table1 and table2, where are the files csvs.
DIR_TEST = 'test'

# Obs: The contend of files in DIR_TEST is represented in the variables below
PRICE_PER_KG = [
    {'nome': 'flo', 'inicial': '0', 'final': '10', 'preco': '12'},
    {'nome': 'flo', 'inicial': '11', 'final': '20', 'preco': '11'},
    {'nome': 'flo', 'inicial': '20', 'final': '30', 'preco': '10'},
    {'nome': 'flo', 'inicial': '30', 'final': '', 'preco': '5'},
]

ROUTES = [
    {'origem': 'flo', 'destino': 'bsb', 'prazo': '3', 'seguro': '3',
        'kg': 'flo', 'fixa': '13'},
    {'origem': 'flo', 'destino': 'cwb', 'prazo': '3', 'seguro': '3',
        'kg': 'flo', 'fixa': '7'},
    {'origem': 'flo', 'destino': 'sao', 'prazo': '4', 'seguro': '3',
        'kg': 'flo', 'fixa': '7'},
    {'origem': 'flo', 'destino': 'vps', 'prazo': '1', 'seguro': '2',
        'kg': 'flo', 'fixa': '11'},
]

##############################################################################
# Unit Test
##############################################################################


def test_load_file_with_cvs():
    assert load_file(DIR_TEST + '/table1/price_per_kg.csv') == PRICE_PER_KG


def test_load_file_with_tvs():
    assert load_file(DIR_TEST + '/table2/price_per_kg.tsv') == PRICE_PER_KG


def test_load_file_with_txt():
    assert load_file('doc/README.txt') is None


def test_load_tables():
    data = load_tables(DIR_TEST)
    assert data is not None
    assert data is not {}
    assert data['table1']['price_per_kg'] == PRICE_PER_KG
    assert data['table1']['routes'] == ROUTES
    assert data['table2']['price_per_kg'] == PRICE_PER_KG


def test_parse_arguments(capsys):
    # happy end
    assert parse_arguments(['fln', 'cwb', '12', '34']) == {
        'src': 'fln', 'dst': 'cwb', 'price': 12, 'weight': 34}
    # missing weight or price
    with pytest.raises(SystemExit):
        parse_arguments(['fln', 'cwb', '12'])
    # missing src or dst
    with pytest.raises(SystemExit):
        parse_arguments(['fln', '12', '34'])


def test_parse_arguments_without_args(capsys):
    with pytest.raises(SystemExit):
        parse_arguments([])
    out, err = capsys.readouterr()
    assert 'error:' in err


def test_parse_argument_help(capsys):
    with pytest.raises(SystemExit):
        parse_arguments(['-h'])
    out, err = capsys.readouterr()
    assert "origem       Local de origem" in out
    assert "destino      Local de destino" in out
    assert "nota_fiscal  Valor da nota fiscal" in out
    assert "peso         Peso do objeto" in out
    assert not err


def test_shipping_cost_1():
    input_data = {'src': 'flo', 'dst': 'bsb', 'price': 50, 'weight': 7}
    result = (3, 104.79)
    assert shipping_cost(input_data, ROUTES[0], PRICE_PER_KG[0]) == result


def test_shipping_cost_2():
    input_data = {'src': 'flo', 'dst': 'bsb', 'price': 50, 'weight': 7}
    result = (2, 109.05)
    route = {'origem': 'flo', 'destino': 'bsb', 'limite': '0', 'prazo': '2',
             'seguro': '2', 'kg': 'flo', 'alfandega': '0', 'icms': '6'}
    ppk = {'nome': 'flo', 'inicial': '0', 'final': '20', 'preco': '14.5'}
    assert shipping_cost(input_data, route, ppk) == result


def test_find_route():
    input_data = {'src': 'flo', 'dst': 'bsb', 'price': 50, 'weight': 7}
    assert find_route(input_data, ROUTES) == ROUTES[0]


def test_find_route_not_found():
    input_data = {'src': 'flo', 'dst': 'eua', 'price': 50, 'weight': 7}
    assert find_route(input_data, ROUTES) is None


def test_find_route_over_limit():
    input_data = {'src': 'flo', 'dst': 'bsb', 'price': 50, 'weight': 7}
    route = {'origem': 'flo', 'destino': 'bsb', 'limite': '1', 'prazo': '2',
             'seguro': '2', 'kg': 'flo', 'alfandega': '0', 'icms': '6'}
    assert find_route(input_data, [route]) is None


def test_find_route_limit_infinite():
    input_data = {'src': 'flo', 'dst': 'bsb', 'price': 50, 'weight': 7}
    route = {'origem': 'flo', 'destino': 'bsb', 'limite': '0', 'prazo': '2',
             'seguro': '2', 'kg': 'flo', 'alfandega': '0', 'icms': '6'}
    assert find_route(input_data, [route]) == route


def test_price_per_kg():
    input_data = {'src': 'flo', 'dst': 'bsb', 'price': 50, 'weight': 7}
    assert find_price_per_kg(input_data, PRICE_PER_KG,
                             ROUTES[0]['kg']) == PRICE_PER_KG[0]


def test_price_per_kg_final_infinite():
    input_data = {'src': 'flo', 'dst': 'bsb', 'price': 50, 'weight': 60}
    assert find_price_per_kg(input_data, PRICE_PER_KG,
                             ROUTES[0]['kg']) == PRICE_PER_KG[3]


def test_price_per_kg_not_found():
    input_data = {'src': 'flo', 'dst': 'bsb', 'price': 50, 'weight': 7}
    assert find_price_per_kg(input_data, PRICE_PER_KG, 'central') is None


def test_basic_values(capsys):
    # $ axado.py florianopolis brasilia 50 7
    # tabela:3, 104.79
    # tabela2:2, 109.05
    output1 = "tabela:3, 104.79\ntabela2:2, 109.05\n"
    main(['florianopolis', 'brasilia', '50', '7'])
    out, err = capsys.readouterr()
    assert out == output1

    # $ axado.py saopaulo florianopolis 50 130
    # tabela:1, 1393.09
    # tabela2:-, -
    output2 = "tabela:1, 1393.09\ntabela2:-, -\n"
    main(['saopaulo', 'florianopolis', '50', '130'])
    out, err = capsys.readouterr()
    assert out == output2

##############################################################################
# Bugs
##############################################################################


def test_price_per_kg_bug_weight_10():
    # weight == 9.99 is OK
    input_data = {'src': 'flo', 'dst': 'bsb', 'price': 50, 'weight': 9.99}
    assert find_price_per_kg(
         input_data, PRICE_PER_KG, ROUTES[0]['kg']) == PRICE_PER_KG[0]

    # weight == 10 ... 10.99 not found table
    input_data = {'src': 'flo', 'dst': 'bsb', 'price': 50, 'weight': 10}
    assert not find_price_per_kg(input_data, PRICE_PER_KG, ROUTES[0]['kg'])

    input_data = {'src': 'flo', 'dst': 'bsb', 'price': 50, 'weight': 10.99}
    assert not find_price_per_kg(input_data, PRICE_PER_KG, ROUTES[0]['kg'])

    # weight == 11 is OK
    input_data = {'src': 'flo', 'dst': 'bsb', 'price': 50, 'weight': 11}
    assert find_price_per_kg(
         input_data, PRICE_PER_KG, ROUTES[0]['kg']) == PRICE_PER_KG[1]
    #
    # Conclusion: The error is at preco_por_kg.csv:2, range jump the number 10
    #
