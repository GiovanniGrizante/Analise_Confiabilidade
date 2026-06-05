from ..services.utils import questao
from ..services.graphic import show_graph, save_graph
from ..services.report import open_pdf

from ...ui import ui_espec
from ...filters import filter_espec
from ...dominio import distribuicoes

import sys
from pathlib import Path
from matplotlib.pyplot import close

# Gerenciador do fluxo para análise específica
class AnaliseEspecifica:

    def __init__(self):
        self.contexto = {}

    # ---------------- PLANTA ----------------
    def estado_planta(self):
        self.contexto.clear()  # reset total

        ui_espec.escolher_planta()

        planta_dict = {
            '0': None,
            '1': '1913',
            '2': '1914'
        }

        opcao = questao('Escolha a planta: ', list(planta_dict.keys()))
        planta = planta_dict.get(opcao)

        if planta is None:
            return None

        self.contexto['planta'] = planta
        return self.estado_tag

    # ---------------- TAG ----------------
    def estado_tag(self):
        self.contexto['tag'] = None
        self.contexto['data'] = None

        while True:
            ui_espec.escolher_tag(self.contexto['planta'])
            tag = input('\n\rDigite a TAG desejada: ')

            if tag == '0':
                return self.estado_planta

            if len(tag) == 4:
                break

        data = filter_espec.main(self.contexto['planta'], tag)

        if data is None:
            opcoes = {
                '1': self.estado_tag,
                '2': self.estado_planta,
                '3': None,
                '0': 'EXIT'
            }

            opcao = questao('\nEscolha a opção: ', list(opcoes.keys()))
            return opcoes.get(opcao)

        self.contexto['tag'] = tag
        self.contexto['data'] = data

        return self.estado_metodo

    # ---------------- MÉTODO ----------------
    def estado_metodo(self):
        self.contexto['metodo'] = []

        ui_espec.escolher_metodo(
            self.contexto['planta'],
            self.contexto['tag']
        )

        met_dict = {
            '0': None,
            '1': distribuicoes.Weibull,
            '2': distribuicoes.Exponencial,
            '3': distribuicoes.Lognormal,
            '4': 'Todos'
        }

        opcao = questao('Escolha o método: ', list(met_dict.keys()))
        met = met_dict.get(opcao)

        if met is None:
            return self.estado_tag

        if met == 'Todos':
            met = list(met_dict.values())[1:-1]
        else:
            met = [met]

        self.contexto['metodo'] = met
        return self.estado_distribuicao

    # ---------------- DISTRIBUIÇÃO ----------------
    def estado_distribuicao(self):
        self.contexto['distribuicao'] = []

        metodo_nome = (
            self.contexto['metodo'][0].__name__
            if len(self.contexto['metodo']) == 1
            else 'Todos'
        )

        ui_espec.escolher_dist(
            self.contexto['planta'],
            self.contexto['tag'],
            metodo_nome
        )

        dist_dict = {
            '0': None,
            '1': 'CDF',
            '2': 'SF',
            '3': 'PDF',
            '4': 'HF',
            '5': 'Probabilidade',
            '6': 'Tabela',
            '7': 'Todos'
        }

        opcao = questao('Escolha a distribuição: ', list(dist_dict.keys()))
        dist = dist_dict.get(opcao)

        if dist is None:
            self.contexto['metodo'] = []
            return self.estado_metodo

        if dist == 'Todos':
            dist = list(dist_dict.values())[1:-1]
        else:
            dist = [dist]

        self.contexto['distribuicao'] = dist
        return self.estado_graficos

    # ---------------- GRÁFICOS ----------------
    def estado_graficos(self):
        close('all')    # Fechar todos os gráficos abertos
        self.contexto['graficos'] = []

        metodo_nome = (
            'Todos'
            if len(self.contexto['metodo']) > 1
            else self.contexto['metodo'][0].__name__
        )

        ui_espec.escolher_processamento(
            self.contexto['planta'],
            self.contexto['tag'],
            metodo_nome,
            self.contexto['distribuicao']
        )

        for classe_metodo in self.contexto['metodo']:
            metodo = classe_metodo.__name__

            grafico = classe_metodo(self.contexto['data']).executar(
                self.contexto['distribuicao']
            )

            for tipo, fig in grafico.items():
                self.contexto['graficos'].append({
                    "metodo": metodo,
                    "tipo": tipo,
                    "fig": fig
                })

        return self.estado_pos_processamento

    # ---------------- PÓS PROCESSAMENTO ----------------
    def estado_pos_processamento(self):

        opcao_dict = {
            '0': None,
            '1': show_graph,
            '2': lambda:save_graph(
                    self.contexto['planta'],
                    self.contexto['tag'],
                    self.contexto['graficos']),
            '3': lambda: open_pdf(
                self.contexto['planta'],
                self.contexto['tag'],
                self.contexto['metodo'],
                self.contexto['distribuicao'],
                self.contexto['graficos']
            )
        }

        opcao = questao('Escolha a opção: ', list(opcao_dict.keys()))

        if opcao_dict.get(opcao) is None:
            self.contexto['distribuicao'] = []
            return self.estado_distribuicao

        opcao_dict[opcao]()
        return self.estado_concluido

    # ---------------- CONCLUSÃO ----------------
    def estado_concluido(self):

        ui_espec.conclusao(
            self.contexto['planta'],
            self.contexto['tag'],
            self.contexto['metodo']
        )

        opcoes = {
            '1': self.estado_distribuicao,
            '2': self.estado_metodo,
            '3': self.estado_tag,
            '4': self.estado_planta,
            '5': None,
            '0': 'EXIT'
        }

        opcao = questao('Escolha uma opção: ', list(opcoes.keys()))
        return opcoes.get(opcao)

    # ---------------- EXECUÇÃO ----------------
    def executar(self):
        estado_atual = self.estado_planta

        while estado_atual:
            if estado_atual == 'EXIT':
                sys.exit()

            estado_atual = estado_atual()
        estado_atual = self.estado_planta
        
        # Executa o loop enquanto a variável não é None
        while estado_atual:
            if estado_atual == 'EXIT':
                sys.exit()
            estado_atual = estado_atual()
        
        return  # Volta ao menu principal