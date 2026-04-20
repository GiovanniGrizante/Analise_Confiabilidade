from src import ingestao, queries, config
from src import dados, distribuicoes
import os, sys

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

# Função para escolha da distribuição
def escolher_dist(espec=None):
    os.system('cls')
    print('=== ANÁLISE DE CONFIABILIDADE ===')
    print('\n=== Análise Específica ===') if espec is not None else print('\n=== Análise por Criticidade ===')
    print('\n=== Escolha da Distribuição ===')
    print('\nDistribuições disponíveis:')
    print('1 - Weibull')
    print('2 - Exponencial')
    print('3 - Lognormal')
    print('4 - Todas')

    dist = questao('Escolha a distribuição: ', ['1', '2', '3', '4'])

    dist_dict = {'1': distribuicoes.Weibull,
                 '2': distribuicoes.Exponencial,
                 '3': distribuicoes.Lognormal}

    if dist == '4':
        return list(dist_dict.values())
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

            planta = questao('Escolha a planta: ', ['0', '1', '2'])

            planta_dict = {'1': '1913',
                        '2': '1914'}

            if planta == '0':
                    return None
            return planta_dict[planta]

# Função para escolha da TAG
def escolher_tag():
    os.system('cls')
    print('=== ANÁLISE DE CONFIABILIDADE ===')
    print('\n=== Análise Específica ===')
    tag = input('\nDigite a TAG desejada (0 - Voltar): ')

    if tag == '0':
        return None
    return tag

# Gerenciador do fluxo para análise específica
class AnaliseEspecifica:
    def __init__(self):
        self.contexto = {}
    
    def estado_planta(self):
        planta = escolher_planta()
        if planta is None:
            return None  # Voltar ao menu principal
        self.contexto['planta'] = planta
        return self.estado_tag
    
    def estado_tag(self):
        tag = escolher_tag()
        if tag is None:
            return self.estado_planta  # Voltar para escolha de planta
        
        data = dados.especifico(self.contexto['planta'], tag)
        
        if data is None:
            print('\nNão existe dados para essa TAG!')
            opcao = questao('1 - Nova TAG | 2 - Nova planta | 3 - Menu | 0 - Sair: ', 
                            ['1', '2', '3', '0'])
            
            opcoes = {
            '1': self.estado_tag,
            '2': self.estado_planta,
            '3': None,  # Menu principal
            '0': 'EXIT'
            }
            return opcoes[opcao]
        
        self.contexto['data'] = data
        self.contexto['tag'] = tag
        return self.estado_resultado
    
    def estado_resultado(self):
        dist = escolher_dist(espec=1)
        for func in dist:
            func(self.contexto['data'], espec=1)
        
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
        ingestao.main()
        queries.main()

        print('\nProcesso concluído!')
        reinic = questao('\nDeseja fazer outro processo?\n(1 - Sim | 2 - Não): ', ['1', '2'])
        if reinic == '2':
            sys.exit()

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

    while True:
        opcao = menu()
        
        if opcao == '0':
            sys.exit()
        
        acao = etapas.get(opcao)
        acao()


if __name__ == '__main__':
    main()