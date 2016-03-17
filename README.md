# Shipping

[![Build Status](https://travis-ci.org/tiao/shipping.svg?branch=master)](https://travis-ci.org/tiao/shipping)
[![Coverage Status](https://coveralls.io/repos/github/tiao/shipping/badge.svg?branch=master)](https://coveralls.io/github/tiao/shipping?branch=master)

## Usage:

    $ axado.py [-h] origem destino nota_fiscal peso
      
    positional arguments:
    origem       Local de origem
    destino      Local de destino
    nota_fiscal  Valor da nota fiscal
    peso         Peso do objeto
      
    optional arguments:
      -h, --help   show this help message and exit

## Output

    $ axado.py florianopolis brasilia 50 7
    tabela:3, 104.79
    tabela2:2, 109.05
