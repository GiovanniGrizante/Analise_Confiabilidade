from reliability.Fitters import Fit_Exponential_1P, Fit_Lognormal_2P
from reliability.Probability_plotting import plot_points, Weibull_probability_plot
import matplotlib.pyplot as plt

# Distribuição exponencial - Assume falhas aleatórias, taxa de falha constante.
# Bom para eletrônicos, sensores, componentes sem desgaste.

# Distribuição Weibull - Pode modelar qualquer tipo.
# Beta - Forma. Eta - Vida característica dos equipamentos
# Para beta < 1 - Falhas infantis
# Para beta = 1 - Aleatório
# Para beta > 1 - Desgaste

# Distribuição lognormal - Boa quando a falha depende de várias pequenas causas

class Weibull:
    def __init__(self, data):
        self.data = data
        
        from reliability.Fitters import Fit_Weibull_2P
        
        self.fit = Fit_Weibull_2P(failures=self.data, 
                                  show_probability_plot=False, 
                                  print_results=False)
    
    def CDF(self):
        fig = plt.figure(figsize=(8, 5))
        
        self.fit.distribution.CDF(label="Weibull ajustada")
        plot_points(failures=self.data, func="CDF")

        plt.title("Função Acumulada de Falha (CDF)")
        plt.xlabel('Horas')
        plt.ylabel('Probabilidade Acumulada de Falha')

        plt.grid(True, which="both")
        # plt.legend()
        return fig

    def SF(self):
        fig = plt.figure(figsize=(8, 5))

        self.fit.distribution.SF(label='Weibull ajustada')
        plot_points(failures=self.data, func='SF')

        plt.title("Função de Sobrevivência (SF)")
        plt.xlabel('Horas')
        plt.ylabel('Probabilidade Acumulada de Sobrevivência')

        plt.grid(True, which="both")
        # plt.legend()
        return fig

    def PDF(self):
        fig = plt.figure(figsize=(8, 5))

        self.fit.distribution.PDF(label='Weibull ajustada')

        plt.title("Função de Densidade de Probabilidade (PDF)")
        plt.xlabel('Horas')
        plt.ylabel('Densidade de Probabilidade')

        plt.grid(True, which="both")
        # plt.legend()
        return fig

    def HF(self):
        fig = plt.figure(figsize=(8, 5))

        self.fit.distribution.HF(label='Weibull ajustada')

        plt.title("Função de Taxa de Falha (HF)")
        plt.xlabel('Horas')
        plt.ylabel('Taxa de Falha')

        plt.grid(True, which="both")
        # plt.legend()
        return fig

    def Probabilidade(self):
        fig = plt.figure(figsize=(8, 5))

        Weibull_probability_plot(failures=self.data)

        plt.title("Probabilidade Weibull")
        plt.xlabel('Horas')
        plt.ylabel('Probabilidade Acumulada de Falha')

        plt.grid(True, which="both")
        # plt.legend()
        return fig

    def Tabela(self):
        fig = plt.figure(figsize=(8, 5))
        
        plt.axis('off')  # remove eixos

        # Dados da tabela
        cell_text = [
            ["Alpha (α)", f"{self.fit.alpha:.2f}", f"{self.fit.alpha_SE:.2f}",
            f"{self.fit.alpha_lower:.2f}", f"{self.fit.alpha_upper:.2f}"],

            ["Beta (β)", f"{self.fit.beta:.4f}", f"{self.fit.beta_SE:.4f}",
            f"{self.fit.beta_lower:.4f}", f"{self.fit.beta_upper:.4f}"],

            ["Log-likelihood", f'{self.fit.loglik:.3f}' if isinstance(self.fit.loglik, (int,float)) else self.fit.loglik, "-", "-", "-"],
            ["AICc", f"{self.fit.AICc:.3f}" if isinstance(self.fit.AICc, (int,float)) else self.fit.AICc, "-", "-", "-"],
            ["BIC", f"{self.fit.BIC:.3f}" if isinstance(self.fit.BIC, (int,float)) else self.fit.BIC, "-", "-", "-"],
            ["Anderson-Darling", f"{self.fit.AD:.4f}" if isinstance(self.fit.AD, (int,float)) else self.fit.AD, "-", "-", "-"],
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
        return fig

    def executar(self, dist):
        graficos = {}
        for distribuicao in dist:
            graficos[distribuicao] = getattr(self, distribuicao)
        return graficos


class Exponencial:
    def __init__(self, dados, espec):
        return 0
    
    def executar(data, espec=None):
        return 0


class Lognormal:
    def __init__(self, dados, espec):
        return 0
    
    def executar(data, espec=None):
        return 0


# def Exponencial(data, salvar=None):
    
#     def CDF(dist, fit, data):
#         fig = plt.figure(figsize=(8, 5))
        
#         fit.distribution.CDF(label="Weibull ajustada")
#         plot_points(failures=data, func="CDF")

#         plt.title("Função Acumulada de Falha (CDF)")
#         plt.xlabel('Horas')
#         plt.ylabel('Probabilidade Acumulada de Falha')

#         plt.grid(True, which="both")
#         # plt.legend()
#         salvar(dist, 'CDF')

#     def SF(dist, fit, data):
#         fig = plt.figure(figsize=(8, 5))

#         fit.distribution.SF(label='Weibull ajustada')
#         plot_points(failures=data, func='SF')

#         plt.title("Função de Sobrevivência (SF)")
#         plt.xlabel('Horas')
#         plt.ylabel('Probabilidade Acumulada de Sobrevivência')

#         plt.grid(True, which="both")
#         # plt.legend()
#         salvar(dist, 'SF')

#     def PDF(dist, fit, data):
#         fig = plt.figure(figsize=(8, 5))

#         fit.distribution.PDF(label='Weibull ajustada')

#         plt.title("Função de Densidade de Probabilidade (PDF)")
#         plt.xlabel('Horas')
#         plt.ylabel('Densidade de Probabilidade')

#         plt.grid(True, which="both")
#         # plt.legend()
#         salvar(dist, 'PDF')

#     def HF(dist, fit, data):
#         fig = plt.figure(figsize=(8, 5))

#         fit.distribution.HF(label='Weibull ajustada')

#         plt.title("Função de Taxa de Falha (HF)")
#         plt.xlabel('Horas')
#         plt.ylabel('Taxa de Falha')

#         plt.grid(True, which="both")
#         # plt.legend()
#         salvar(dist, 'HF')

#     def Probability_Plot(dist, fit, data):
#         fig = plt.figure(figsize=(8, 5))

#         Weibull_probability_plot(failures=data)

#         plt.title("Probabilidade Weibull")
#         plt.xlabel('Horas')
#         plt.ylabel('Probabilidade Acumulada de Falha')

#         plt.grid(True, which="both")
#         # plt.legend()
#         salvar(dist, 'Probabilidade')

#     def Tabela(dist, fit=None, data=None):
#         fig = plt.figure(figsize=(8, 5))
        
#         plt.axis('off')  # remove eixos

#         # Dados da tabela
#         cell_text = [
#             ["Lambda (λ)", f"{fit.Lambda:.5f}", f"{fit.Lambda_SE:.5f}",
#             f"{fit.Lambda_lower:.5f}", f"{fit.Lambda_upper:.5f}"],

#             ["MTTF (θ = 1/λ)", f"{1/fit.Lambda:.2f}", "-", "-", "-"],

#             ["Log-likelihood", f'{fit.loglik:.3f}' if isinstance(fit.loglik, (int,float)) else fit.loglik, "-", "-", "-"],
#             ["AICc", f"{fit.AICc:.3f}" if isinstance(fit.AICc, (int,float)) else fit.AICc, "-", "-", "-"],
#             ["BIC", f"{fit.BIC:.3f}" if isinstance(fit.BIC, (int,float)) else fit.BIC, "-", "-", "-"],
#             ["Anderson-Darling", f"{fit.AD:.4f}" if isinstance(fit.AD, (int,float)) else fit.AD, "-", "-", "-"],
#         ]

#         table = plt.table(
#             cellText=cell_text,
#             colLabels=["Parâmetro", "Estimativa", "Erro Padrão", "CI Inf", "CI Sup"],
#             loc="center",
#             cellLoc="center"
#         )

#         table.scale(1, 1.8)
#         table.auto_set_font_size(False)
#         table.set_fontsize(9)

#         plt.title("Resultados do Ajuste Weibull")
#         salvar(dist, 'Dados')

#     # ======================================================

#     def salvar(dist, nome):
#         if espec == 'N':
#             os.makedirs(os.path.join('Dados', df['Planta'][0], df['Criticidade'][0], tag, dist), exist_ok=True)
#             plt.savefig(os.path.join('Dados', df['Planta'][0], df['Criticidade'][0], tag, dist, f'{nome}.png'),
#                                     dpi=300, bbox_inches="tight")
#             plt.close()

#     fit = Fit_Exponential_1P(failures=data, show_probability_plot=False, print_results=False)

#     # Obter o nome da distribuição principal
#     dist = inspect.currentframe().f_code.co_name

#     plots = [CDF,
#             SF,
#             PDF,
#             HF,
#             Probability_Plot,
#             Tabela]

#     for func in plots:
#         func(dist, fit, data)
#         if espec == 'S':
#             def submit(text):
#                 try:
#                     valor = float(text)
#                 except ValueError:
#                     pass
        
#             # Área do TextBox
#             axbox = plt.axes([0.2, 0.1, 0.6, 0.075])
#             text_box = TextBox(axbox, 'a = ', initial="1")

#             text_box.on_submit(submit)
#             plt.show()

# def Lognormal(data, salvar=None):
    
#     def CDF(dist, fit, data):
#         fig = plt.figure(figsize=(8, 5))
        
#         fit.distribution.CDF(label="Weibull ajustada")
#         plot_points(failures=data, func="CDF")

#         plt.title("Função Acumulada de Falha (CDF)")
#         plt.xlabel('Horas')
#         plt.ylabel('Probabilidade Acumulada de Falha')

#         plt.grid(True, which="both")
#         # plt.legend()
#         salvar(dist, 'CDF')

#     def SF(dist, fit, data):
#         fig = plt.figure(figsize=(8, 5))

#         fit.distribution.SF(label='Weibull ajustada')
#         plot_points(failures=data, func='SF')

#         plt.title("Função de Sobrevivência (SF)")
#         plt.xlabel('Horas')
#         plt.ylabel('Probabilidade Acumulada de Sobrevivência')

#         plt.grid(True, which="both")
#         # plt.legend()
#         salvar(dist, 'SF')

#     def PDF(dist, fit, data):
#         fig = plt.figure(figsize=(8, 5))

#         fit.distribution.PDF(label='Weibull ajustada')

#         plt.title("Função de Densidade de Probabilidade (PDF)")
#         plt.xlabel('Horas')
#         plt.ylabel('Densidade de Probabilidade')

#         plt.grid(True, which="both")
#         # plt.legend()
#         salvar(dist, 'PDF')

#     def HF(dist, fit, data):
#         fig = plt.figure(figsize=(8, 5))

#         fit.distribution.HF(label='Weibull ajustada')

#         plt.title("Função de Taxa de Falha (HF)")
#         plt.xlabel('Horas')
#         plt.ylabel('Taxa de Falha')

#         plt.grid(True, which="both")
#         # plt.legend()
#         salvar(dist, 'HF')

#     def Probability_Plot(dist, fit, data):
#         fig = plt.figure(figsize=(8, 5))

#         Weibull_probability_plot(failures=data)

#         plt.title("Probabilidade Weibull")
#         plt.xlabel('Horas')
#         plt.ylabel('Probabilidade Acumulada de Falha')

#         plt.grid(True, which="both")
#         # plt.legend()
#         salvar(dist, 'Probabilidade')

#     def Tabela(dist, fit=None, data=None):
#         fig = plt.figure(figsize=(8, 5))
        
#         plt.axis('off')  # remove eixos

#         # Dados da tabela
#         cell_text = [
#             ["Mu (μ)", f"{fit.mu:.4f}", f"{fit.mu_SE:.4f}",
#             f"{fit.mu_lower:.4f}", f"{fit.mu_upper:.4f}"],

#             ["Sigma (σ)", f"{fit.sigma:.4f}", f"{fit.sigma_SE:.4f}",
#             f"{fit.sigma_lower:.4f}", f"{fit.sigma_upper:.4f}"],

#             ["Log-likelihood", f"{fit.loglik:.3f}" if isinstance(fit.loglik, (int, float)) else fit.loglik, "-", "-", "-"],
#             ["AICc", f"{fit.AICc:.3f}" if isinstance(fit.AICc, (int, float)) else fit.AICc, "-", "-", "-"],
#             ["BIC", f"{fit.BIC:.3f}" if isinstance(fit.BIC, (int, float)) else fit.BIC, "-", "-", "-"],
#             ["Anderson-Darling", f"{fit.AD:.4f}" if isinstance(fit.AD, (int, float)) else fit.AD, "-", "-", "-"],
#         ]

#         table = plt.table(
#             cellText=cell_text,
#             colLabels=["Parâmetro", "Estimativa", "Erro Padrão", "CI Inf", "CI Sup"],
#             loc="center",
#             cellLoc="center"
#         )

#         table.scale(1, 1.8)
#         table.auto_set_font_size(False)
#         table.set_fontsize(9)

#         plt.title("Resultados do Ajuste Weibull")
#         salvar(dist, 'Dados')

#     # ======================================================

#     def salvar(dist, nome):
#         if espec == 'N':
#             os.makedirs(os.path.join('Dados', df['Planta'][0], df['Criticidade'][0], tag, dist), exist_ok=True)
#             plt.savefig(os.path.join('Dados', df['Planta'][0], df['Criticidade'][0], tag, dist, f'{nome}.png'),
#                                     dpi=300, bbox_inches="tight")
#             plt.close()

#     fit = Fit_Lognormal_2P(failures=data, show_probability_plot=False, print_results=False)

#     # Obter o nome da distribuição principal
#     dist = inspect.currentframe().f_code.co_name

#     plots = [CDF,
#             SF,
#             PDF,
#             HF,
#             Probability_Plot,
#             Tabela]

#     for func in plots:
#         func(dist, fit, data)
#         if espec == 'S':
#             def submit(text):
#                 try:
#                     valor = float(text)
#                 except ValueError:
#                     pass
        
#             # Área do TextBox
#             axbox = plt.axes([0.2, 0.1, 0.6, 0.075])
#             text_box = TextBox(axbox, 'a = ', initial="1")

#             text_box.on_submit(submit)
#             plt.show()