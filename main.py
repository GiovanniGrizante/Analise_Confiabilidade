from src.ui import base
from src.core import state_critic, state_espec, utils
from src.settings import folders
from src.database import ingestao, queries

import os, sys, time

# Atualizar banco de dados
def escolha1():
    print('Processando...')
    
    ingestao.main()
    queries.main()
    time.sleep(4)
    
    print('\nProcesso concluído!')
    input('Pressione Enter para continuar...')
    
# Análise por criticidade
def escolha2():
    print('Em processo')
    time.sleep(3)
    # dados.crit()
    # distribuicoes.main()

# Análise específica
def escolha3():
    analise = state_espec.AnaliseEspecifica()
    analise.executar()
    
# Função para criação das pastas no diretório
# settings.folders()

while True:
    base.menu()

    opcao_dict = {'0': sys.exit,
                  '1': escolha1,
                  '2': escolha2,
                  '3': escolha3}
    
    opcao = utils.questao('Escolha a opção: ', list(opcao_dict.keys()))
    
    acao = opcao_dict.get(opcao)
    acao()