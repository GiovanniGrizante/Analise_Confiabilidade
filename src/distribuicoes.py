from reliability.Fitters import Fit_Weibull_2P, Fit_Exponential_1P, Fit_Lognormal_2P
from reliability.Probability_plotting import plot_points, Weibull_probability_plot
import matplotlib.pyplot as plt
from matplotlib.widgets import TextBox
import os, sys, time, inspect

# Distribuição exponencial - Assume falhas aleatórias, taxa de falha constante.
# Bom para eletrônicos, sensores, componentes sem desgaste.

# Distribuição Weibull - Pode modelar qualquer tipo.
# Beta - Forma. Eta - Vida característica dos equipamentos
# Para beta < 1 - Falhas infantis
# Para beta = 1 - Aleatório
# Para beta > 1 - Desgaste

# Distribuição lognormal - Boa quando a falha depende de várias pequenas causas

def Weibull(tag, df, data, espec):
    
    def CDF(dist, fit, data):
        fig = plt.figure(figsize=(8, 5))
        
        fit.distribution.CDF(label="Weibull ajustada")
        plot_points(failures=data, func="CDF")

        plt.title("Função Acumulada de Falha (CDF)")
        plt.xlabel('Horas')
        plt.ylabel('Probabilidade Acumulada de Falha')

        plt.grid(True, which="both")
        # plt.legend()
        salvar(dist, 'CDF')

    def SF(dist, fit, data):
        fig = plt.figure(figsize=(8, 5))

        fit.distribution.SF(label='Weibull ajustada')
        plot_points(failures=data, func='SF')

        plt.title("Função de Sobrevivência (SF)")
        plt.xlabel('Horas')
        plt.ylabel('Probabilidade Acumulada de Sobrevivência')

        plt.grid(True, which="both")
        # plt.legend()
        salvar(dist, 'SF')

    def PDF(dist, fit, data):
        fig = plt.figure(figsize=(8, 5))

        fit.distribution.PDF(label='Weibull ajustada')

        plt.title("Função de Densidade de Probabilidade (PDF)")
        plt.xlabel('Horas')
        plt.ylabel('Densidade de Probabilidade')

        plt.grid(True, which="both")
        # plt.legend()
        salvar(dist, 'PDF')

    def HF(dist, fit, data):
        fig = plt.figure(figsize=(8, 5))

        fit.distribution.HF(label='Weibull ajustada')

        plt.title("Função de Taxa de Falha (HF)")
        plt.xlabel('Horas')
        plt.ylabel('Taxa de Falha')

        plt.grid(True, which="both")
        # plt.legend()
        salvar(dist, 'HF')

    def Probability_Plot(dist, fit, data):
        fig = plt.figure(figsize=(8, 5))

        Weibull_probability_plot(failures=data)

        plt.title("Probabilidade Weibull")
        plt.xlabel('Horas')
        plt.ylabel('Probabilidade Acumulada de Falha')

        plt.grid(True, which="both")
        # plt.legend()
        salvar(dist, 'Probabilidade')

    def Tabela(dist, fit=None, data=None):
        fig = plt.figure(figsize=(8, 5))
        
        plt.axis('off')  # remove eixos

        # Dados da tabela
        cell_text = [
            ["Alpha (α)", f"{fit.alpha:.2f}", f"{fit.alpha_SE:.2f}",
            f"{fit.alpha_lower:.2f}", f"{fit.alpha_upper:.2f}"],

            ["Beta (β)", f"{fit.beta:.4f}", f"{fit.beta_SE:.4f}",
            f"{fit.beta_lower:.4f}", f"{fit.beta_upper:.4f}"],

            ["Log-likelihood", f'{fit.loglik:.3f}' if isinstance(fit.loglik, (int,float)) else fit.loglik, "-", "-", "-"],
            ["AICc", f"{fit.AICc:.3f}" if isinstance(fit.AICc, (int,float)) else fit.AICc, "-", "-", "-"],
            ["BIC", f"{fit.BIC:.3f}" if isinstance(fit.BIC, (int,float)) else fit.BIC, "-", "-", "-"],
            ["Anderson-Darling", f"{fit.AD:.4f}" if isinstance(fit.AD, (int,float)) else fit.AD, "-", "-", "-"],
        ]

        table = plt.table(
            cellText=cell_text,
            colLabels=["Parâmetro", "Estimativa", "Erro Padrão", "CI Inf", "CI Sup"],
            loc="center",
            cellLoc="center"
        )

        table.scale(1, 1.8)
        table.auto_set_font_size(False)
        table.set_fontsize(9)

        plt.title("Resultados do Ajuste Weibull")
        salvar(dist, 'Dados')

    # ======================================================

    def salvar(dist, nome):
        if espec == 'N':
            os.makedirs(os.path.join('Dados', df['Planta'][0], df['Criticidade'][0], tag, dist), exist_ok=True)
            plt.savefig(os.path.join('Dados', df['Planta'][0], df['Criticidade'][0], tag, dist, f'{nome}.png'),
                                    dpi=300, bbox_inches="tight")
            plt.close()

    fit = Fit_Weibull_2P(failures=data, show_probability_plot=False, print_results=False)

    # Obter o nome da distribuição principal
    dist = inspect.currentframe().f_code.co_name

    plots = [CDF,
            SF,
            PDF,
            HF,
            Probability_Plot,
            Tabela]

    for func in plots:
        func(dist, fit, data)
        if espec == 'S':
            def submit(text):
                try:
                    valor = float(text)
                except ValueError:
                    pass
        
            # Área do TextBox
            axbox = plt.axes([0.2, 0.1, 0.6, 0.075])
            text_box = TextBox(axbox, 'a = ', initial="1")

            text_box.on_submit(submit)
            plt.show()

def Exponencial(tag, df, data, espec):
    
    def CDF(dist, fit, data):
        fig = plt.figure(figsize=(8, 5))
        
        fit.distribution.CDF(label="Weibull ajustada")
        plot_points(failures=data, func="CDF")

        plt.title("Função Acumulada de Falha (CDF)")
        plt.xlabel('Horas')
        plt.ylabel('Probabilidade Acumulada de Falha')

        plt.grid(True, which="both")
        # plt.legend()
        salvar(dist, 'CDF')

    def SF(dist, fit, data):
        fig = plt.figure(figsize=(8, 5))

        fit.distribution.SF(label='Weibull ajustada')
        plot_points(failures=data, func='SF')

        plt.title("Função de Sobrevivência (SF)")
        plt.xlabel('Horas')
        plt.ylabel('Probabilidade Acumulada de Sobrevivência')

        plt.grid(True, which="both")
        # plt.legend()
        salvar(dist, 'SF')

    def PDF(dist, fit, data):
        fig = plt.figure(figsize=(8, 5))

        fit.distribution.PDF(label='Weibull ajustada')

        plt.title("Função de Densidade de Probabilidade (PDF)")
        plt.xlabel('Horas')
        plt.ylabel('Densidade de Probabilidade')

        plt.grid(True, which="both")
        # plt.legend()
        salvar(dist, 'PDF')

    def HF(dist, fit, data):
        fig = plt.figure(figsize=(8, 5))

        fit.distribution.HF(label='Weibull ajustada')

        plt.title("Função de Taxa de Falha (HF)")
        plt.xlabel('Horas')
        plt.ylabel('Taxa de Falha')

        plt.grid(True, which="both")
        # plt.legend()
        salvar(dist, 'HF')

    def Probability_Plot(dist, fit, data):
        fig = plt.figure(figsize=(8, 5))

        Weibull_probability_plot(failures=data)

        plt.title("Probabilidade Weibull")
        plt.xlabel('Horas')
        plt.ylabel('Probabilidade Acumulada de Falha')

        plt.grid(True, which="both")
        # plt.legend()
        salvar(dist, 'Probabilidade')

    def Tabela(dist, fit=None, data=None):
        fig = plt.figure(figsize=(8, 5))
        
        plt.axis('off')  # remove eixos

        # Dados da tabela
        cell_text = [
            ["Lambda (λ)", f"{fit.Lambda:.5f}", f"{fit.Lambda_SE:.5f}",
            f"{fit.Lambda_lower:.5f}", f"{fit.Lambda_upper:.5f}"],

            ["MTTF (θ = 1/λ)", f"{1/fit.Lambda:.2f}", "-", "-", "-"],

            ["Log-likelihood", f'{fit.loglik:.3f}' if isinstance(fit.loglik, (int,float)) else fit.loglik, "-", "-", "-"],
            ["AICc", f"{fit.AICc:.3f}" if isinstance(fit.AICc, (int,float)) else fit.AICc, "-", "-", "-"],
            ["BIC", f"{fit.BIC:.3f}" if isinstance(fit.BIC, (int,float)) else fit.BIC, "-", "-", "-"],
            ["Anderson-Darling", f"{fit.AD:.4f}" if isinstance(fit.AD, (int,float)) else fit.AD, "-", "-", "-"],
        ]

        table = plt.table(
            cellText=cell_text,
            colLabels=["Parâmetro", "Estimativa", "Erro Padrão", "CI Inf", "CI Sup"],
            loc="center",
            cellLoc="center"
        )

        table.scale(1, 1.8)
        table.auto_set_font_size(False)
        table.set_fontsize(9)

        plt.title("Resultados do Ajuste Weibull")
        salvar(dist, 'Dados')

    # ======================================================

    def salvar(dist, nome):
        if espec == 'N':
            os.makedirs(os.path.join('Dados', df['Planta'][0], df['Criticidade'][0], tag, dist), exist_ok=True)
            plt.savefig(os.path.join('Dados', df['Planta'][0], df['Criticidade'][0], tag, dist, f'{nome}.png'),
                                    dpi=300, bbox_inches="tight")
            plt.close()

    fit = Fit_Exponential_1P(failures=data, show_probability_plot=False, print_results=False)

    # Obter o nome da distribuição principal
    dist = inspect.currentframe().f_code.co_name

    plots = [CDF,
            SF,
            PDF,
            HF,
            Probability_Plot,
            Tabela]

    for func in plots:
        func(dist, fit, data)
        if espec == 'S':
            def submit(text):
                try:
                    valor = float(text)
                except ValueError:
                    pass
        
            # Área do TextBox
            axbox = plt.axes([0.2, 0.1, 0.6, 0.075])
            text_box = TextBox(axbox, 'a = ', initial="1")

            text_box.on_submit(submit)
            plt.show()

def Lognormal(tag, df, data, espec):
    
    def CDF(dist, fit, data):
        fig = plt.figure(figsize=(8, 5))
        
        fit.distribution.CDF(label="Weibull ajustada")
        plot_points(failures=data, func="CDF")

        plt.title("Função Acumulada de Falha (CDF)")
        plt.xlabel('Horas')
        plt.ylabel('Probabilidade Acumulada de Falha')

        plt.grid(True, which="both")
        # plt.legend()
        salvar(dist, 'CDF')

    def SF(dist, fit, data):
        fig = plt.figure(figsize=(8, 5))

        fit.distribution.SF(label='Weibull ajustada')
        plot_points(failures=data, func='SF')

        plt.title("Função de Sobrevivência (SF)")
        plt.xlabel('Horas')
        plt.ylabel('Probabilidade Acumulada de Sobrevivência')

        plt.grid(True, which="both")
        # plt.legend()
        salvar(dist, 'SF')

    def PDF(dist, fit, data):
        fig = plt.figure(figsize=(8, 5))

        fit.distribution.PDF(label='Weibull ajustada')

        plt.title("Função de Densidade de Probabilidade (PDF)")
        plt.xlabel('Horas')
        plt.ylabel('Densidade de Probabilidade')

        plt.grid(True, which="both")
        # plt.legend()
        salvar(dist, 'PDF')

    def HF(dist, fit, data):
        fig = plt.figure(figsize=(8, 5))

        fit.distribution.HF(label='Weibull ajustada')

        plt.title("Função de Taxa de Falha (HF)")
        plt.xlabel('Horas')
        plt.ylabel('Taxa de Falha')

        plt.grid(True, which="both")
        # plt.legend()
        salvar(dist, 'HF')

    def Probability_Plot(dist, fit, data):
        fig = plt.figure(figsize=(8, 5))

        Weibull_probability_plot(failures=data)

        plt.title("Probabilidade Weibull")
        plt.xlabel('Horas')
        plt.ylabel('Probabilidade Acumulada de Falha')

        plt.grid(True, which="both")
        # plt.legend()
        salvar(dist, 'Probabilidade')

    def Tabela(dist, fit=None, data=None):
        fig = plt.figure(figsize=(8, 5))
        
        plt.axis('off')  # remove eixos

        # Dados da tabela
        cell_text = [
            ["Mu (μ)", f"{fit.mu:.4f}", f"{fit.mu_SE:.4f}",
            f"{fit.mu_lower:.4f}", f"{fit.mu_upper:.4f}"],

            ["Sigma (σ)", f"{fit.sigma:.4f}", f"{fit.sigma_SE:.4f}",
            f"{fit.sigma_lower:.4f}", f"{fit.sigma_upper:.4f}"],

            ["Log-likelihood", f"{fit.loglik:.3f}" if isinstance(fit.loglik, (int, float)) else fit.loglik, "-", "-", "-"],
            ["AICc", f"{fit.AICc:.3f}" if isinstance(fit.AICc, (int, float)) else fit.AICc, "-", "-", "-"],
            ["BIC", f"{fit.BIC:.3f}" if isinstance(fit.BIC, (int, float)) else fit.BIC, "-", "-", "-"],
            ["Anderson-Darling", f"{fit.AD:.4f}" if isinstance(fit.AD, (int, float)) else fit.AD, "-", "-", "-"],
        ]

        table = plt.table(
            cellText=cell_text,
            colLabels=["Parâmetro", "Estimativa", "Erro Padrão", "CI Inf", "CI Sup"],
            loc="center",
            cellLoc="center"
        )

        table.scale(1, 1.8)
        table.auto_set_font_size(False)
        table.set_fontsize(9)

        plt.title("Resultados do Ajuste Weibull")
        salvar(dist, 'Dados')

    # ======================================================

    def salvar(dist, nome):
        if espec == 'N':
            os.makedirs(os.path.join('Dados', df['Planta'][0], df['Criticidade'][0], tag, dist), exist_ok=True)
            plt.savefig(os.path.join('Dados', df['Planta'][0], df['Criticidade'][0], tag, dist, f'{nome}.png'),
                                    dpi=300, bbox_inches="tight")
            plt.close()

    fit = Fit_Lognormal_2P(failures=data, show_probability_plot=False, print_results=False)

    # Obter o nome da distribuição principal
    dist = inspect.currentframe().f_code.co_name

    plots = [CDF,
            SF,
            PDF,
            HF,
            Probability_Plot,
            Tabela]

    for func in plots:
        func(dist, fit, data)
        if espec == 'S':
            def submit(text):
                try:
                    valor = float(text)
                except ValueError:
                    pass
        
            # Área do TextBox
            axbox = plt.axes([0.2, 0.1, 0.6, 0.075])
            text_box = TextBox(axbox, 'a = ', initial="1")

            text_box.on_submit(submit)
            plt.show()

# Gera o vetor de tempo entre falhas
def tempo_falha(df, per_ini, per_fim):
    data = None

    diff_inicio = round(((df['DataHora início'].iloc[0] - per_ini).total_seconds()/3600), 2)
    diff_fim = round(((per_fim - df['DataHora fim'].iloc[-1]).total_seconds()/3600), 2)

    # Gerar lista com os tempos de operação
    diff_ordens = (
            (df['DataHora início'].shift(-1) - df['DataHora fim'])
            .dt.total_seconds()/3600
            ).round(2)[:-1].tolist()
    
    # Se houver 'DataHora fim' > 'DataHora início', não deve ser considerado
    diff_ordens = [x for x in diff_ordens if x > 0]

    data = [diff_inicio] + diff_ordens

    # Se 'DataHora fim' for o período final de análise, não considera
    if diff_fim != 0:
        data.append(diff_fim)
    return data


def main(df, per_ini, per_fim, espec):
    funcs = {'1': Weibull, '2': Exponencial, '3': Lognormal}

    while True:
        os.system('cls')
        dist = input('Escolha a distribuição:\n(1 - Weibull | 2 - Exponencial | 3 - Lognormal | Em branco p/ todas): ')
        funcoes = list(funcs.values()) if dist == '' else [funcs.get(dist)]

        if funcoes is None:
            print('Opção inválida!')
            time.sleep(4)
            continue
        
        funcoes = [func]
        break

    if espec == 'S':
        tag = None
        data = tempo_falha(df, per_ini, per_fim)
        for func in funcoes:
            func(tag, df, data, espec)
    else:
        for tag in df.keys():
            if not df[tag].empty:
                data = tempo_falha(df[tag], per_ini, per_fim)
                print(tag, data)
                for func in funcoes:
                    func(tag, df[tag], data, espec)