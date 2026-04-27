from src import ingestao, queries, config
from src import dados, distribuicoes
import os, sys, matplotlib.pyplot as plt, time
from pathlib import Path

dir_base = Path(__file__).resolve().parent

# === Funções Gerais ===
# Função para verificação de inputs
def questao(quest, intervalo):
    while True:
        resp = input(quest)
        if resp in intervalo:
            return resp
            # Limpa a linha anterior
        sys.stdout.write('\033[F\033[K')

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
def escolher_metodo(self, espec=None):
    os.system('cls')
    print('=== ANÁLISE DE CONFIABILIDADE ===')
    print('\n=== Análise por Criticidade ===') if espec is None else print('\n=== Análise Específica ===')
    print('\n=== Escolha do Método de Distribuição ===')
    print(f'\nPlanta: {self.contexto['planta']} | TAG: {self.contexto['tag']}')
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
                '4': 'Todos'}

    met = questao('Escolha a distribuição: ', list(met_dict.keys()))

    if met == '4':
        return list(met_dict.values())[1:-1]
    return [met_dict[met]]

# Função para escolha da distribuição (CDF, SF, PDF...)
def escolher_dist(self, espec=None):
    os.system('cls')
    print('=== ANÁLISE DE CONFIABILIDADE ===')
    print('\n=== Análise por Criticidade ===') if espec is None else print('\n=== Análise Específica ===')
    print('\n=== Escolha da Distribuição ===\n')

    if espec is None:
        msg = f'Planta: {self.contexto['planta']} | TAG: {self.contexto['tag']} | Método: '
        if len(self.contexto['metodo']) == 1:
            print(msg + self.contexto['metodo'][0].__name__)
        else:
            print(msg + 'Todos')


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
            print('\n=== Escolha da Planta ===')
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
def escolher_tag(self):
    os.system('cls')
    print('=== ANÁLISE DE CONFIABILIDADE ===')
    print('\n=== Análise Específica ===')
    print('\n=== Escolha da TAG ===')
    print(f'\nPlanta: {self.contexto['planta']}')
    print('\n0 - Voltar')

    tag = input('\nDigite a TAG desejada: ')

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
        self.contexto['planta'] = {}
        self.contexto['planta'] = planta
        return self.estado_tag
    
    # Menu para escolha da TAG
    def estado_tag(self):
        tag = escolher_tag(self)
        if tag == '0':
            return self.estado_planta  # Voltar para escolha de planta
        
        data = dados.especifico(self.contexto['planta'], tag)
        
        if data is None:
            print('\nNão existe dados para essa TAG!')
            print('\n1 - Outra TAG')
            print('2 - Outra planta')
            print('3 - Menu')
            print('0 - Sair')
            
            opcoes = {
            '1': self.estado_tag,
            '2': self.estado_planta,
            '3': None,  # Menu principal
            '0': 'EXIT'
            }
            
            opcao = questao('\nEscolha a opção: ', 
                            list(opcoes.keys()))
            
            return opcoes[opcao]
        
        self.contexto['data'] = {}
        self.contexto['data'] = data
        self.contexto['tag'] = {}
        self.contexto['tag'] = tag
        return self.estado_metodo
    
    # Menu para escolha do método de distribuição (Weibull, Exponencial...)
    def estado_metodo(self):
        # Atribuir os métodos de distribuições a serem executados
        met = escolher_metodo(self, espec=1)
        if met == ['0']:
            return self.estado_tag
        
        self.contexto['metodo'] = {}
        self.contexto['metodo'] = met
        return self.estado_distribuicao
        
    # Menu para escolha da distribuição (CDF, SF, PDF ...)
    def estado_distribuicao(self):
        # Fechar todas as figuras geradas
        plt.close('all')

        # Atribuir as distribuições a serem executados
        dist = escolher_dist(self, espec=1)
        if dist == ['0']:
            return self.estado_metodo

        self.contexto['distribuicao'] = {}
        self.contexto['distribuicao'] = dist
        
        # Iterar nas classes
        for classe_metodo in self.contexto['metodo']:
            self.contexto['graficos'] = {}

            # Cria instância da classe (Weibull, Exponencial...)
            # Os parâmetros passados para a classe vão para __init__
            analisador = classe_metodo(self.contexto['data'])
            
            # Executa os tipos de distribuição escolhidos (CDF, SF...)
            self.contexto['graficos'] = analisador.executar(dist)

            if len(dist) == 1:
                msg = f'Gráfico {dist[0]} - Método {classe_metodo.__name__} concluído'
            else:
                msg = f'Todos os gráficos - Método {classe_metodo.__name__} concluído!'
            
            print(f'\n{msg}')
            print('\n1 - Apresentar')
            print('2 - Salvar')
            print('3 - Continuar')
            print('4 - Voltar')
            
            opcoes_graf = {'1': self.apresentar_grafico,
                           '2': self.salvar_grafico,
                           '3': '3',
                           '4': self.estado_distribuicao}
            
            usar_graf = questao('Escolha uma opção: ',list(opcoes_graf))
            
            if usar_graf != '3':
                return opcoes_graf[usar_graf]

        return self.estado_concluido
        
    # Menu de conclusão para o usuário decidir se deseja outra operação
    def estado_concluido(self):
        # Dados para o print
        # --- Método ---
        if len(self.contexto['metodo']) == 1:
            metodo = self.contexto['metodo'][0].__name__
        else:
            metodo = 'Todos'

        # --- Distribuição ---
        if len(self.contexto['distribuicao']) == 1:
            distribuicao = self.contexto['distribuicao'][0]
        else:
            distribuicao = 'Todas'

        msg = (
            f"Planta: {self.contexto['planta']} | "
            f"TAG: {self.contexto['tag']} | "
            f"Método: {metodo} | "
            f"Distribuição: {distribuicao}"
        )


        os.system('cls')
        print('=== ANÁLISE DE CONFIABILIDADE ===')
        print('\n=== Análise Específica ===')
        print('\n=== Conclusão ===')
        print(f'\n{msg}')
        print('\n1 - Outra distribuição')
        print('2 - Outro método')
        print('3 - Outra TAG')
        print('4 - Outra planta')
        print('5 - Menu')
        print('0 - Sair')

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
        return self.estado_concluido

    # Função para salvar os gráficos na pasta do usuário
    def salvar_grafico(self):
        for classe in self.contexto['metodo']:
            metodo = classe.__name__

            caminho = (dir_base / 'images' / self.contexto['planta'] / self.contexto['tag'] / metodo)
            caminho.mkdir(parents=True, exist_ok=True)

            for nome, fig in self.contexto['graficos'].items():
                arquivo = caminho / f"{nome}.png"
                fig.savefig(arquivo, dpi=300)

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


def main():
    # Atualizar banco de dados
    def escolha1():
        print('Processando...')
        
        ingestao.main()
        queries.main()
        time.sleep(2)
        
        print('\nProcesso concluído!')
        time.sleep(3)
        
    # Análise por criticidade
    def escolha2():
        dados.criticidade()
        # dados.crit()
        # distribuicoes.main()

    # Análise específica
    def escolha3():
        # Versão refatorada com POO (Máquina de estados)
        analise = AnaliseEspecifica()
        analise.executar()
        
    etapas = {'1': escolha1,
              '2': escolha2,
              '3': escolha3}
    
    # Função para criação das pastas no diretório
    if not os.path.isdir(dir_base / 'data' / 'raw') or not os.path.isdir(dir_base / 'images'):
        config.create_folders(dir_base)

    while True:
        opcao = menu()
        
        if opcao == '0':
            sys.exit()
        
        acao = etapas.get(opcao)
        acao()


if __name__ == '__main__':
    main()