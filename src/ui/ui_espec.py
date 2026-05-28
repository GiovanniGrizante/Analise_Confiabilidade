import os

# Função para escolha da planta
def escolher_planta():
    os.system('cls')
    print('=== ANÁLISE DE CONFIABILIDADE ===')
    print('\n=== Análise Específica ===')
    print('\n=== Escolha da Planta ===')
    print('\nPlantas disponíveis:')
    print('1 - Orgânicos')
    print('2 - Sílica')
    print('0 - Voltar')

# Função para escolha da TAG
def escolher_tag(planta):
    os.system('cls')
    print('=== ANÁLISE DE CONFIABILIDADE ===')
    print('\n=== Análise Específica ===')
    print('\n=== Escolha da TAG ===')
    print(f'\nPlanta: {planta}')
    print('\n0 - Voltar')

# Função para escolha do método (Weibull, Exponencial...)
def escolher_metodo(planta, tag):
    os.system('cls')
    print('=== ANÁLISE DE CONFIABILIDADE ===')
    print('\n=== Análise Específica ===')
    print('\n=== Escolha do Método de Distribuição ===')
    print(f'\nPlanta: {planta} | TAG: {tag}')
    print('\nMétodos disponíveis:')
    print('1 - Weibull')
    print('2 - Exponencial')
    print('3 - Lognormal')
    print('4 - Todas')
    print('0 - Voltar')

# Função para escolha da distribuição (CDF, SF, PDF...)
def escolher_dist(planta, tag, metodo):
    os.system('cls')
    print('=== ANÁLISE DE CONFIABILIDADE ===')
    print('\n=== Análise Específica ===')
    print('\n=== Escolha da Distribuição ===')
    print(f'\nPlanta: {planta} | TAG: {tag} | Método: {metodo}')
    print('\nDistribuições disponíveis:')
    print('1 - CDF')
    print('2 - SF')
    print('3 - PDF')
    print('4 - HF')
    print('5 - Probabilidade')
    print('6 - Tabela Geral')
    print('7 - Todas')
    print('0 - Voltar')

def escolher_grafico(planta, tag, metodo, distribuicao):
    os.system('cls')
    mult_distribuicao = len(distribuicao) > 1

    if mult_distribuicao:
        dist_msg = 'Todas'
    else:
        dist_msg = f'{distribuicao[0]}'
        
    print('=== ANÁLISE DE CONFIABILIDADE ===')
    print('\n=== Análise Específica ===')
    print('\n=== Opções Gráficas ===')
    print(f'\nPlanta: {planta} | TAG: {tag} | Método: {metodo} | Distribuição: {dist_msg}')
    print('\nOpções disponíveis:')
    print('1 - Apresentar')
    print('2 - Salvar')
    print('3 - Relatório')
    print('0 - Voltar')

def conclusao(planta, tag, metodo):
    os.system('cls')
    print('=== ANÁLISE DE CONFIABILIDADE ===')
    print('\n=== Análise Específica ===')
    print('\n=== Conclusão ===')
    if len(metodo) == 1:
        print(f'\nPlanta: {planta} | TAG: {tag} | Método: {metodo[0].__name__}')
    else:
        print(f'\nPlanta: {planta} | TAG: {tag} | Método: Todos')
    print('\nProcesso concluído com sucesso!')
    print('1 - Outra distribuição')
    print('2 - Outro método')
    print('3 - Outra TAG')
    print('4 - Outra planta')
    print('5 - Menu')
    print('0 - Sair')