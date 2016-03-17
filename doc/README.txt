Sobre o teste
-------------

O teste do Axado é uma aplicação simples que não deve lhe tomar mais de um dia
para ser feito, os nossos candidatos costumam mandar os testes com menos de 200
linhas de código. Nesse teste você deve fazer um programa que calcula o prazo e
preço de frete de acordo com os detalhes definidos abaixo, é uma aplicação
simples que está relacionada com o trabalho da Axado.

Lembre-se que essa é a nossa principal forma de avaliação, então é esperado que
você faça o código no melhor das suas competências, desenvolva com a mesma
qualidade que você faria código para produção. Use de boas práticas como
nomeclatura, pep8, testes de regressão, versionamento, uma boa interface (não
há necessidade de ser GUI), aproveite a biblioteca padrão da linguagem, também
aproveite o ecosistema e faça uso de projetos de terceiros que facilitem o seu
trabalho ou melhore a qualidade do seu software, qualquer prática que você
deixar de fora não poderá ser avaliado e portanto será considerado que você não
tem conhecimento para aplica-la.

Também é importante notar que se não houver comentários no seu teste só nos
resta assumir quais foram as suas intenções, para que todo esse processo seja
melhor para ambas as partes nós recomendamos que você documente de forma mais
extensa do que o normal, explique o porque da arquitetura, do uso de cada
biblioteca, de cada try, loops, estruturas de dados, quanto mais detalhes você
der mais fácil fica para nós avaliarmos seu código, se você sentir que as suas
explicações estão atrapalhando a legibilidade do seu código é só enviar um
arquivo de texto com as explicações acompanhando seu programa.

Por fim, esse teste não tem a intenção de ser um show-off do que você consegue
ou não fazer, então não use features além do necessário como meta-programação,
descriptors ou outras funcionalidades avançadas, na próxima etapa do nosso
processo você poderá mostrar o seu conhecimento de features avançadas.

Teste
-----

A aplicação deve ser chamada `axado.py` e deve funcionar da seguinte forma:

    Assinatura:         axado.py <origem> <destino> <nota_fiscal> <peso>
    Output por tabela:  <nome da pasta>:<prazo>, <frete calculado>

Exemplo de output:

    $ axado.py florianopolis brasilia 50 7
    tabela:3, 104.79
    tabela2:2, 109.05

Cálculo
-------

O cálculo do frete deve utilizar os dados nos diretórios `tabela` e `tabela2`
e seguir as seguintes regras:

- Os preços devem ser arredondados para duas casa decimais, sempre para cima.
- As colunas dos csvs definem as taxas que devem ser cobradas, as taxas/colunas
  devem ser calculadas da seguinte maneira:

    - seguro    = valor da nota fiscal * seguro / 100
    - fixa      = o próprio valor da taxa
    - kg        = define o nome da faixa que é usada para cobrar por kilograma,
                  a faixa é definida no arquivo `preco_por_kg.csv`
    - ICMS      = valor fixo definido no arquivo `rotas.csv` que deve ser
                  utilizado por último para calcular o total do frete:
                  TOTAL = SUBTOTAL / ((100 - icms) / 100)

O ICMS deve sempre ser cobrado por último.

Tabela1
----

O ICMS dessa `tabela` é 6.

Tabela2
-------

A tabela2 tem a taxa chamada "alfandega" que sempre deve ser calculada antes do
ICMS usando a seguinte fórmula:

    subtotal * (alfandega / 100)

A tabela2 também possui uma limitação de peso para alguns locais (definida na
coluna limite do rotas.csv), indicando que não devem ser calculados os preços
quando o peso ultrapassar esse limite:

    $ axado.py saopaulo florianopolis 50 130
    tabela:1, 1393.09
    tabela2:-, -

Caso a rota não contenha nenhum valor limite, não há limites para a rota.

Glossário
---------

SUBTOTAL = Valor do preço do frete calculado até então (antes de calcular a taxa), eg.:

    TAXA   SUBTOTAL  VALOR DA TAXA   CALCULO
    seguro 0         1.5             50 * 3 / 100
    fixa   1.5       13              13
    faixa  14.5      84              7 * 12
    icms   98.5      6.29            98.5 / ((100 - 6) / 100)

    TOTAL = 104.79

ICMS    = imposto sobre circulação de mercadorias e serviços
FAIXA   = define um valor para um determinado intervalo, eg.:

    Min  Max  Valor
    00 - 10   5
    10 - 20   7
    30 - inf  8

INTERVALOS - os intervalos das faixas são vistos como mínimo inclusivo e máximo
exclusivo, ou seja, se uma faixa tem início 10 e fim 20, quer dizer que a faixa
vai de 10.00 até 19.99 excluindo 20.
