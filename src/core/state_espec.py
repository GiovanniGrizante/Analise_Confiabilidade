from .utils import questao
from ..ui import ui_espec
from ..filters import filter_espec
from ..dominio import distribuicoes

import matplotlib.pyplot as plt, os

# Gerenciador do fluxo para análise específica
class AnaliseEspecifica:
    # Armazenamento das variáveis
    def __init__(self):
        self.contexto = {}
    
    # Menu para escolha da planta
    def estado_planta(self):
        ui_espec.escolher_planta()

        planta_dict = {'0': None,
                        '1': '1913',
                        '2': '1914'}

        opcao = questao('Escolha a planta: ', list(planta_dict.keys()))
        planta = planta_dict.get(opcao)

        if planta is None:
            return None  # Voltar ao menu principal

        self.contexto['planta'] = planta
        return self.estado_tag
    
    # Menu para escolha da TAG
    def estado_tag(self):
        ui_espec.escolher_tag(self.contexto['planta'])

        tag = input('\nDigite a TAG desejada: ')

        if tag == '0':
            return self.estado_planta  # Voltar para escolha de planta
        
        data = filter_espec.main(self.contexto['planta'], tag)
        
        if data is None:
            # Gerar classe de erros na exceptions.py
            # interface.Erro.tag
            opcoes = {
                '1': self.estado_tag,
                '2': self.estado_planta,
                '3': None,  # Menu principal
                '0': 'EXIT'
            }
            
            opcao = questao('\nEscolha a opção: ', 
                            list(opcoes.keys()))
            
            return opcoes[opcao]
            
        self.contexto['data'] = data
        self.contexto['tag'] = tag
        return self.estado_metodo
    
    # Menu para escolha do método de distribuição (Weibull, Exponencial...)
    def estado_metodo(self):
        # Atribuir os métodos de distribuições a serem executados
        ui_espec.escolher_metodo(self.contexto['planta'], self.contexto['tag'])

        met_dict = {'0': None,
                '1': distribuicoes.Weibull,
                '2': distribuicoes.Exponencial,
                '3': distribuicoes.Lognormal,
                '4': 'Todos'}

        opcao = questao('Escolha a distribuição: ', list(met_dict.keys()))
        met = met_dict.get(opcao)

        if met is None:
            return self.estado_tag

        elif met == 'Todos':
            met = list(met_dict.values())[1:-1]
        
        else:
            met = [met]
        
        self.contexto['metodo'] = met
        return self.estado_distribuicao
        
    # Menu para escolha da distribuição (CDF, SF, PDF ...)
    def estado_distribuicao(self):
        if len(self.contexto['metodo']) == 1:
            # Atribuir as distribuições a serem executados
            ui_espec.escolher_dist(self.contexto['planta'],
                                   self.contexto['tag'],
                                   self.contexto['metodo'][0].__name__)
        
        else:
            ui_espec.escolher_dist(self.contexto['planta'],
                                   self.contexto['tag'],
                                   'Todos')

        dist_dict = {'0': 'Voltar',
                    '1': 'CDF',
                    '2': 'SF',
                    '3': 'PDF',
                    '4': 'HF',
                    '5': 'Probabilidade',
                    '6': 'Tabela',
                    '7': 'Todos'}

        opcao = questao('Escolha a distribuição: ', list(dist_dict.keys()))
        dist = dist_dict.get(opcao)
    
        if dist == 'Voltar':
            return self.estado_metodo

        elif dist == 'Todos':
            dist = list(dist_dict.values())[1:-1]

        else:
            dist = [dist]

        self.contexto['distribuicao'] = dist
        return self.estado_graficos


    def estado_graficos(self):
        ui_espec.escolher_grafico(self.contexto['metodo'], self.contexto['distribuicao'])

        # Fechar todas as figuras geradas
        plt.close('all')

        # Iterar nas classes
        for classe_metodo in self.contexto['metodo']:
            self.contexto['graficos'] = {}

            # Cria instância da classe (Weibull, Exponencial...)
            # Os parâmetros passados para a classe vão para __init__
            
            # Executa os tipos de distribuição escolhidos (CDF, SF...)
            self.contexto['graficos'] = classe_metodo(self.contexto['data']).executar(self.contexto['distribuicao'])

            opcoes_graf = {'1': self.apresentar_grafico,
                        '2': self.salvar_grafico,
                        '3': '3',
                        '4': self.estado_distribuicao}
            
            usar_graf = questao('Escolha uma opção: ', list(opcoes_graf))
            
            if usar_graf != '3':
                return opcoes_graf[usar_graf]

        return self.estado_concluido
        
    # Menu de conclusão para o usuário decidir se deseja outra operação
    def estado_concluido(self):
        
        ui_espec.conclusao(self.contexto['planta'],
                           self.contexto['tag'],
                           self.contexto['metodo'])

        opcoes = {
            '1': self.estado_distribuicao,
            '2': self.estado_metodo,
            '3': self.estado_tag,
            '4': self.estado_planta,
            '5': None,  # Menu principal
            '0': 'EXIT'
        }

        opcao = questao('\nEscolha uma opção: ', list(opcoes.keys()))
        return opcoes[opcao]

    # Função para apresentar os gráficos ao usuário
    def apresentar_grafico(self):
        plt.show(block=False)
        input('\nPressione Enter para fechar as figuras e continuar...')
        plt.close('all')

    # Função para salvar os gráficos na pasta do usuário
    def salvar_grafico(self):
        print('Em processo...')
        time.sleep(4)
        return self.estado_concluido
        
    # Lógica de execução
    def executar(self):
        estado_atual = self.estado_planta
        
        # Executa o loop enquanto a variável não é None
        while estado_atual:
            if estado_atual == 'EXIT':
                sys.exit()
            estado_atual = estado_atual()
        
        return  # Volta ao menu principal