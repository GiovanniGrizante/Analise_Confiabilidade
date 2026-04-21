from src import ingestao, queries, config
from src import dados, distribuicoes
import os, sys, matplotlib.pyplot as plt, time

# === Funções Gerais ===
# Função para verificação de inputs
def questao(quest, intervalo):
    while True:
        resp = input(quest)
        if resp in intervalo:
            return resp

# Função para apresentação do menu principal
def menu():
    os.system('cls')
    print('=== ANÁLISE DE CONFIABILIDADE ===')
    print('\n1 - Atualizar banco de dados')
    print('2 - Análise por criticidade')
    print('3 - Análise específica de motor')
    print('0 - Sair')

    opcao = questao('Escolha uma opção: ', ['0', '1', '2', '3'])
    return opcao

# Função para escolha do método (Weibull, Exponencial...)
def escolher_metodo(espec=None):
    os.system('cls')
    print('=== ANÁLISE DE CONFIABILIDADE ===')
    print('\n=== Análise por Criticidade ===') if espec is None else print('\n=== Análise Específica ===')
    print('\n=== Escolha do Método de Distribuição ===')
    print('\nMétodos disponíveis:')
    print('1 - Weibull')
    print('2 - Exponencial')
    print('3 - Lognormal')
    print('4 - Todas')
    print('0 - Voltar')
    
    met_dict = {'0': '0',
                '1': distribuicoes.Weibull,
                '2': distribuicoes.Exponencial,
                '3': distribuicoes.Lognormal,
                '4': '4'}

    met = questao('Escolha a distribuição: ', list(met_dict.keys()))

    if met == '4':
        return list(met_dict.values())[1:-1]
    return [met_dict[met]]

# Função para escolha da distribuição (CDF, SF, PDF...)
def escolher_dist(espec=None):
    os.system('cls')
    print('=== ANÁLISE DE CONFIABILIDADE ===')
    print('\n=== Análise por Criticidade ===') if espec is None else print('\n=== Análise Específica ===')
    print('\n=== Escolha da Distribuição ===')
    print('\nDistribuições disponíveis:')
    print('1 - CDF')
    print('2 - SF')
    print('3 - PDF')
    print('4 - HF')
    print('5 - Probabilidade')
    print('6 - Tabela Geral')
    print('7 - Todas')
    print('0 - Voltar')
    
    dist_dict = {'0': '0',
                 '1': 'CDF',
                 '2': 'SF',
                 '3': 'PDF',
                 '4': 'HF',
                 '5': 'Probabilidade',
                 '6': 'Tabela',
                 '7': '7'}
    
    dist = questao('Escolha a distribuição: ', list(dist_dict.keys()))
    
    if dist == '7':
        return list(dist_dict.values())[1:-1]
    return [dist_dict[dist]]


# === Funções para Análise Específica ===
# Função para escolha da planta
def escolher_planta():
            os.system('cls')
            print('=== ANÁLISE DE CONFIABILIDADE ===')
            print('\n=== Análise Específica ===')
            print('\nPlantas disponíveis:')
            print('1 - Orgânicos')
            print('2 - Sílica')
            print('0 - Voltar')

            planta_dict = {'0': '0',
                           '1': '1913',
                           '2': '1914'}
            
            planta = questao('Escolha a planta: ', list(planta_dict.keys()))
            return planta_dict[planta]

# Função para escolha da TAG
def escolher_tag():
    os.system('cls')
    print('=== ANÁLISE DE CONFIABILIDADE ===')
    print('\n=== Análise Específica ===')
    tag = input('\nDigite a TAG desejada (0 - Voltar): ')

    return tag

# Gerenciador do fluxo para análise específica
class AnaliseEspecifica:
    # Armazenamento das variáveis
    def __init__(self):
        self.contexto = {}
    
    # Menu para escolha da planta
    def estado_planta(self):
        planta = escolher_planta()
        if planta == '0':
            return None  # Voltar ao menu principal
        self.contexto['planta'] = planta
        return self.estado_tag
    
    # Menu para escolha da TAG
    def estado_tag(self):
        tag = escolher_tag()
        if tag == '0':
            return self.estado_planta  # Voltar para escolha de planta
        
        data = dados.especifico(self.contexto['planta'], tag)
        
        if data is None:
            print('\nNão existe dados para essa TAG!')
            
            opcoes = {
            '1': self.estado_tag,
            '2': self.estado_planta,
            '3': None,  # Menu principal
            '0': 'EXIT'
            }
            
            opcao = questao('1 - Nova TAG | 2 - Nova planta | 3 - Menu | 0 - Sair: ', 
                            list(opcoes.keys()))
            
            return opcoes[opcao]
        
        self.contexto['data'] = data
        self.contexto['tag'] = tag
        return self.estado_resultado
    
    # Menu para escolha do método de distribuição (Weibull, Exponencial...)
    def estado_metodo(self):
        # Atribuir os métodos de distribuições a serem executados
        met = escolher_metodo(espec=1)
        if met == '0':
            return self.estado_tag
        
        self.contexto['metodo'] = met
        return self.estado_distribuicao
        
    # Menu para escolha da distribuição (CDF, SF, PDF ...)
    def estado_distribuicao(self):
        # Atribuir as distribuições a serem executados
        dist = escolher_dist(espec=1)
        if dist == ['0']:
            return self.estado_metodo
        
        # Iterar nas classes
        for classe_metodo in self.contexto['metodo']:
            # Cria instância da classe (Weibull, Exponencial...)
            # Os parâmetros passados para a classe vão para __init__
            analisador = classe_metodo(self.contexto['data'])
            
            # Executa os tipos de distribuição escolhidos (CDF, SF...)
            self.contexto['graficos'] = analisador.executar(dist)
            
            opcoes_graf = {'1': self.apresentar_grafico,
                           '2': self.salvar_grafico,
                           '3': '3'}
            
            usar_graf = questao(f'''\nGráficos do método {classe_metodo.__name__} gerados!
                                \n1 - Apresentar
                                \n2 - Salvar
                                \n3 - Continuar
                                \nEscolha uma opção: ''', list(opcoes_graf))
            
            if usar_graf != '3':
                return opcoes_graf[usar_graf]
                    
        print('\nProcesso concluído!')
        opcao = questao('1 - Nova TAG | 2 - Nova planta | 3 - Menu | 0 - Sair: ',
                        ['1', '2', '3', '0'])
        
        opcoes = {
            '1': self.estado_tag,
            '2': self.estado_planta,
            '3': None,  # Menu principal
            '0': 'EXIT'
        }
        return opcoes[opcao]
            
    # Função para apresentar os gráficos ao usuário
    def apresentar_grafico(self):
        for figura in self.contexto['graficos'].values():
            figura.show()
        input('\nPressione Enter para fechar todas as figuras e continuar...')
        plt.close('all')
    
    # Função para salvar os gráficos na pasta do usuário
    def salvar_grafico(self):
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


def main():
    # Atualizar banco de dados
    def escolha1():
        print('Processando...')
        
        ingestao.main()
        queries.main()
        time.sleep(4)
        
        print('\nProcesso concluído!')
        
    # Análise por criticidade
    def escolha2():
        print('Em processo')
        sys.exit()
        # dados.crit()
        # distribuicoes.main()

    # Análise específica
    def escolha3():
        # Versão refatorada com POO
        analise = AnaliseEspecifica()
        analise.executar()
        
    etapas = {'1': escolha1,
              '2': escolha2,
              '3': escolha3}
    
    # Função para criação das pastas no diretório
    config.create_engine()

    while True:
        opcao = menu()
        
        if opcao == '0':
            sys.exit()
        
        acao = etapas.get(opcao)
        acao()


if __name__ == '__main__':
    main()