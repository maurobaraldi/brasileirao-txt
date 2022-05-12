from datetime import datetime
from json import dumps
from lxml.html import (
    HtmlElement,
    fromstring
)
from urllib.request import urlopen

def request(url: str) -> str:
    '''Request uri and return it as data (str).'''

    with urlopen(url) as r:
        return fromstring(r.read().decode('utf8'))


URL_BASE = "https://www.cbf.com.br/futebol-brasileiro/competicoes/campeonato-brasileiro-serie-a/"
ANOS = [2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021]

JOGOS = range(1, 381)

def pega_ano(ano: int) -> None:
    return request(URL_BASE + str(ano))

def pega_rodada(pagina: HtmlElement, rodada: int) -> dict:

    return pagina.xpath(f'/html/body/div[1]/main/article/div[1]/div/div/section/div[2]/aside/div/div[{rodada}]/div/ul/li/div')
    
def pega_jogo(pagina: HtmlElement, rodada: int, jogo: int) -> list:
    _jogo = pagina.xpath(f'/html/body/div[1]/main/article/div[1]/div/div/section/div[2]/aside/div/div[{rodada}]/div/ul/li[{jogo}]/div')
    return {
        "data": _jogo[0].find('span').text.split('-')[0].strip()[5:].split()[0],
        "hora": _jogo[0].find('span').text.split('-')[0].strip()[5:].split()[1],
        "numero": _jogo[0].find('span').text.split('-')[1].replace('Jogo: ', '').strip(),
        "times": {
            'mandante': {
                'nome': _jogo[0].find(f'.//div/a/div[1]/img').attrib.get('title').split(' - ')[0],
                'estado': _jogo[0].find(f'.//div/a/div[1]/img').attrib.get('title').split(' - ')[1],
            },
            'visitante': {
                'nome': _jogo[0].find(f'.//div/a/div[2]/img').attrib.get('title').split(' - ')[0],
                'estado': _jogo[0].find(f'.//div/a/div[2]/img').attrib.get('title').split(' - ')[1],
            },
        },
        "resultado": _jogo[0].find(f'.//div/a/strong/span').text,
        "estadio": {
            'nome': _jogo[0].find(f'.//span[2]').text.strip().split(' - ')[0],
            'cidade': _jogo[0].find(f'.//span[2]').text.strip().split(' - ')[1],
            'estado': _jogo[0].find(f'.//span[2]').text.strip().split(' - ')[2]
        }
        
    }

def pega_arbritragem(ano: int, jogo: int) -> dict:
    data = request(f'https://www.cbf.com.br/futebol-brasileiro/competicoes/campeonato-brasileiro-serie-a/{ano}/{jogo}?ref=botao')
    arbitros = []
    for i in range(len(data.xpath('//*[@id="arbitros"]/table/tbody/tr'))):
        arbitros.append(
            {
                'titulo': data.xpath('//*[@id="arbitros"]/table/tbody/tr')[i].find('./th').text,
                'nome': data.xpath('//*[@id="arbitros"]/table/tbody/tr/td/a')[i].text.strip(),
                'estado': data.xpath('//*[@id="arbitros"]/table/tbody/tr/td[2]')[i].text
            }
        )
    return arbitros
    

if __name__ == '__main__':
    for ano in ANOS:
        print(f'Capturando dados do ano {ano}')
        arquivo = f'brasileirao_serie_a_{ano}.json'
        campeonato = {}
        _ano = pega_ano(ano)
        for rodada in range(1, 39):
            print(f'  Capturando dados da rodada {rodada}')
            _rodada = pega_rodada(_ano, rodada)
            for jogo in range(1, 11):
                if ano == 2016 and rodada == 38 and jogo == 8:
                    pass
                else:
                    _jogo = pega_jogo(_ano, rodada, jogo)
                    _jogo['arbritragem'] = pega_arbritragem(ano, jogo)
                    numero = _jogo.pop('numero')
                    campeonato[numero] = _jogo

        with open(arquivo, 'w') as _:
            _.write(dumps(campeonato))
