#from src import ingestao, tratamento
import os, sys


def questao(quest, intervalo):
    while True:
        resp = input(quest)
        if resp in intervalo:
            return resp


def escolher_planta():
    os.system('cls')
    print('=== ANÁLISE DE CONFIABILIDADE ===')
    print('\nPlantas disponíveis:')
    print('1 - Orgânicos')
    print('2 - Sílica')
    print('0 - Voltar')

    planta = questao('Escolha a planta: ', ['0', '1', '2'])
    return planta


def menu():
    os.system('cls')
    print('=== ANÁLISE DE CONFIABILIDADE ===')
    print('\n1 - Atualizar banco de dados')
    print('2 - Análise por criticidade')
    print('3 - Análise específica de motor')
    print('0 - Sair')

    opcao = questao('Escolha uma opção: ', ['0', '1', '2', '3'])
    return opcao


def main():
    etapas = {'1': [lambda: ingestao.main(), lambda: queries.main()],
              '2': [lambda: dados.crit(), lambda: distribuicoes.main()],
              '3': [lambda: escolher_planta(), lambda: dados.espec(), lambda: distribuicoes.main()]}

    while True:
        opcao = menu()
        
        if opcao == '0':
            sys.exit()
        
        if opcao in etapas.keys():
            for func in etapas[opcao]:
                func()



if __name__ == '__main__':
    main()