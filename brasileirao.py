#!/usr/bin/env python

API_KEY = 'Bearer live_372001cb123d107aaa92737aab6fa3'
#API_KEY = 'Bearer test_a8c37778328495ac24c5d0d3c3923b'

from json import loads
from time import time
from typing import Union
from urllib.request import (
    Request,
    urlopen
)


def request(url: str) -> Union[list, dict]:
    '''Request an URI and retrive it content.'''

    request = Request(url, headers={'Authorization': API_KEY})

    with urlopen(request) as r:
        return loads(r.read())



def mostra_tabela() -> None:
    tabela = request('https://api.api-futebol.com.br/v1/campeonatos/10/tabela')
    rodada = request('https://api.api-futebol.com.br/v1/campeonatos/10')
    print('Nomenclatura: P = Pontos, J = Jogos, V = Vitorias, E = Empates, GP = Gols Pró, GC = Gols Contra, SG = Saldo de Gols, A = Aproveitamenteo, VR = Variação')
    print(' -------------------------------------------------------------------------')
    print('| Equipe                       | P | J | V | E | D | GP| GC| SG|  A  | VR|')
    print(' ------------------------------|---|---|---|---|---|---|---|---|-----|---|')
    for counter, time in enumerate(tabela):
        row = {
            'nome': time.get('time').get('nome_popular'),
            'pontos': time.get('pontos'),
            'jogos': time.get('jogos'),
            'vitorias': time.get('vitorias'),
            'empates': time.get('empates'),
            'derrotas': time.get('derrotas'),
            'gols_pro': time.get('gols_pro'),
            'gols_contra': time.get('gols_contra'),
            'saldo_gols': time.get('saldo_gols'),
            'aproveitamento': time.get('aproveitamento'),
            'variacao_posicao': time.get('variacao_posicao')
        }
        row = '| {nome:29}|{pontos:3}|{jogos:3}|{vitorias:3}|{empates:3}|{derrotas:3}|{gols_pro:3}|{gols_contra:3}|{saldo_gols:3}|{aproveitamento:4}%|{variacao_posicao:3}|'.format(**row)
        _row = row
        if counter < 4:
            # Libertadores
            _row = '\033[94m' + row + '\033[0m'
        if 3 < counter < 6:
            # Pre Libertadores
            _row = '\033[96m' + row + '\033[0m'
        if 5 < counter < 12:
            # Sulamericana
            _row = '\033[92m' + row + '\033[0m'
        if counter > 15:
            # Rebaixamento
            _row = '\033[91m' + row + '\033[0m'
        print(_row)
        print(' ------------------------------|---|---|---|---|---|---|---|---|-----|---|')


def mostra_rodada(roada = None) -> None:
    _roadada = request('https://api.api-futebol.com.br/v1/campeonatos/10/rodadas/{rodada}')
    print(_roadada)

if __name__ == '__main__':
    mostra_tabela()
    #mostra_rodada(1)
