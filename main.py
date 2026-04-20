from src import ingestao, queries, config
from src import dados, distribuicoes
import os, sys

# Função para verificação de inputs
def questao(quest, intervalo):
    while True:
        resp = input(quest)
        if resp in intervalo:
            return resp

# Função para escolha da distribuição
def escolher_dist(tipo=None):
    os.system('cls')
    print('=== ANÁLISE DE CONFIABILIDADE ===')
    print('\n=== Análise Específica ===') if tipo==1 else print('\n=== Análise por Criticidade ===')
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

        def escolher_tag():
            os.system('cls')
            print('=== ANÁLISE DE CONFIABILIDADE ===')
            print('\n=== Análise Específica ===')
            tag = input('\nDigite a TAG desejada (0 - Voltar): ')

            if tag == '0':
                return None
            return tag

        while True:
            planta = escolher_planta()

            # Caso o usuário deseje trocar o tipo de análise, sai da função
            if planta is None:
                return
            
            while True:
                tag = escolher_tag()

                # Caso o usuário deseje trocar a planta, sai do último looping
                if tag is None:
                    break
        
                # Filtra os dados e calcula os tempos de falha
                data = dados.especifico(planta, tag)

                # Caso não haja a TAG informada, perguntar ao usuário qual opção ele deseja continuar
                if data is None:
                    inval = questao('\nNão existe dados para essa TAG!\n1 - Pesquisar outra TAG\n2 - Pesquisar outra planta\n3 - Menu\nEscolha a opção: ', ['1', '2', '3'])
                    match inval:
                        case '1':
                            continue
                        case '2':
                            break
                        case '3':
                            return

                dist = escolher_dist(1)
                for func in dist:
                    func(data)

                print('\nProcesso concluído!')
                reinic = questao('\nDeseja fazer outro processo?\n(1 - Sim | 2 - Não): ', ['1', '2'])
                match reinic:
                    case '1':
                        return
                    case '2':
                        sys.exit()
        
    etapas = {'1': escolha1,
              '2': escolha2,
              '3': escolha3}

    while True:
        opcao = menu()
        
        if opcao == '0':
            sys.exit()
        
        acao = etapas.get(opcao)
        if acao:
            acao()


if __name__ == '__main__':
    main()