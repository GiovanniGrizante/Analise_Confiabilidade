from .utils import questao
from ..ui import ui_espec
from ..filters import filter_espec
from ..dominio import distribuicoes

import matplotlib.pyplot as plt, sys
from pathlib import Path
from datetime import datetime

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

        # Limpeza da variável
        self.contexto['planta'] = None
        
        self.contexto['planta'] = planta
        return self.estado_tag
    
    # Menu para escolha da TAG
    def estado_tag(self):
        # Verifica se a TAG inserida possui 4 caracteres. Caso 0, volta para o estado anterior.
        tag = ''
        while len(tag)!=4:
            # Printa a UI do estado
            ui_espec.escolher_tag(self.contexto['planta'])
            
            tag = input('\n\rDigite a TAG desejada: ')

            if tag == '0':
                return self.estado_planta  # Voltar para escolha de planta
        
        # Filtra os dados em uma lista e armazena no dict 'contexto'.
        data = filter_espec.main(self.contexto['planta'], tag)
        
        # Se não houver dados, emitir informação de erro (GERAR ARQUIVO EXCEPTIONS) e pedir para o usuário escolher uma opção.
        if data is None:
            # Gerar classe de erros na exceptions.py
            # interface.Erro.tag
            opcoes = {
                '1': self.estado_tag,
                '2': self.estado_planta,
                '3': None,  # Menu principal
                '0': 'EXIT'
            }
            
            opcao = questao('\nEscolha a opção: ', list(opcoes.keys()))
            
            return opcoes[opcao]
            
        # Limpeza das variáveis para não colapsar os dados
        self.contexto['data'] = None
        self.contexto['tag'] = None
        
        # Armazena os dados
        self.contexto['data'] = data
        self.contexto['tag'] = tag
        
        # Próximo estado
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

        # Se escolher todos, varre o dict entre o primeiro e o último
        elif met == 'Todos':
            met = list(met_dict.values())[1:-1]
        
        # Dados precisam estar em lista para não precisar de dois tratamentos diferentes
        else:
            met = [met]
            
        # Limpeza da variável
        self.contexto['metodo'] = None
        
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
            
        # Limpeza da variável
        self.contexto['distribuicao'] = None

        self.contexto['distribuicao'] = dist
        return self.estado_graficos

    # Menu para escolha do tratamento do gráfico gerado
    def estado_graficos(self):
        # Fechar todas as figuras geradas
        # plt.close('all')

        # Iterar nas classes
        for classe_metodo in self.contexto['metodo']:
            
            ui_espec.escolher_grafico(self.contexto['planta'],
                                      self.contexto['tag'],
                                      classe_metodo.__name__, 
                                      self.contexto['distribuicao'])

            # Cria instância da classe (Weibull, Exponencial...)
            # Os parâmetros passados para a classe vão para __init__
            
            # Executa os tipos de distribuição escolhidos (CDF, SF...)
            
            self.contexto['graficos'] = None
            self.contexto['graficos'] = classe_metodo(self.contexto['data']).executar(self.contexto['distribuicao'])

            opcao_dict = {'0': self.estado_distribuicao,
                          '1': self.apresentar_grafico,
                          '2': lambda: self.salvar_grafico(classe_metodo),
                          '3': self.gerar_relatorio}
            
            opcao = questao('Escolha uma opção: ', list(opcao_dict))
            
            if opcao == '0':
                return opcao_dict[opcao]

            else:
                opcao_dict[opcao]()

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

        opcao = questao('Escolha uma opção: ', list(opcoes.keys()))
        return opcoes[opcao]

    # Função para apresentar os gráficos ao usuário
    def apresentar_grafico(self):
        plt.show(block=False)
        input('\nPressione Enter para fechar as figuras e continuar...')
        plt.close('all')

    # Função para salvar os gráficos na pasta do usuário
    def salvar_grafico(self, classe_metodo):
        today = datetime.now().strftime("%d-%m-%Y")
        
        graph_folder = (Path(__file__).parent.parent.parent / 'images' / 'Específico' / 
                        self.contexto['planta'] / self.contexto['tag'] / classe_metodo.__name__ / f'{today}')
        
        graph_folder.mkdir(parents=True, exist_ok=True)
        
        for title, graph in self.contexto['graficos'].items():
            plt.figure(graph)
            plt.savefig(graph_folder / f'{title}.png', dpi=600, bbox_inches='tight')


    def gerar_relatorio(self):
        pass
        
    # Lógica de execução
    def executar(self):
        estado_atual = self.estado_planta
        
        # Executa o loop enquanto a variável não é None
        while estado_atual:
            if estado_atual == 'EXIT':
                sys.exit()
            estado_atual = estado_atual()
        
        return  # Volta ao menu principal