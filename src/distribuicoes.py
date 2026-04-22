from reliability.Probability_plotting import plot_points, Weibull_probability_plot, Exponential_probability_plot, Lognormal_probability_plot
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
        plt.figure(figsize=(8, 5))

        self.fit.distribution.CDF(label="Weibull ajustada")
        plot_points(failures=self.data, func="CDF")

        plt.title("Função Acumulada de Falha (CDF)")
        plt.xlabel('Horas')
        plt.ylabel('Probabilidade Acumulada de Falha')

        plt.grid(True, which="both")
        # plt.legend()

        fig = plt.gcf()
        return fig

    def SF(self):
        plt.figure(figsize=(8, 5))

        self.fit.distribution.SF(label='Weibull ajustada')
        plot_points(failures=self.data, func='SF')

        plt.title("Função de Sobrevivência (SF)")
        plt.xlabel('Horas')
        plt.ylabel('Probabilidade Acumulada de Sobrevivência')

        plt.grid(True, which="both")
        # plt.legend()
        fig = plt.gcf()
        return fig

    def PDF(self):
        plt.figure(figsize=(8, 5))

        self.fit.distribution.PDF(label='Weibull ajustada')

        plt.title("Função de Densidade de Probabilidade (PDF)")
        plt.xlabel('Horas')
        plt.ylabel('Densidade de Probabilidade')

        plt.grid(True, which="both")
        # plt.legend()
        fig = plt.gcf()
        return fig

    def HF(self):
        plt.figure(figsize=(8, 5))

        self.fit.distribution.HF(label='Weibull ajustada')

        plt.title("Função de Taxa de Falha (HF)")
        plt.xlabel('Horas')
        plt.ylabel('Taxa de Falha')

        plt.grid(True, which="both")
        # plt.legend()
        fig = plt.gcf()
        return fig

    def Probabilidade(self):
        plt.figure(figsize=(8, 5))

        Weibull_probability_plot(failures=self.data)

        plt.title("Probabilidade Weibull")
        plt.xlabel('Horas')
        plt.ylabel('Probabilidade Acumulada de Falha')

        plt.grid(True, which="both")
        # plt.legend()
        fig = plt.gcf()
        return fig

    def Tabela(self):
        plt.figure(figsize=(8, 5))

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
        fig = plt.gcf()
        return fig

    def executar(self, dist):
        graficos = {}
        for distribuicao in dist:
            funcao = getattr(self, distribuicao)
            graficos[distribuicao] = funcao()
        return graficos


class Exponencial:
    def __init__(self, data):
        self.data = data
        
        from reliability.Fitters import Fit_Exponential_1P
        
        self.fit = Fit_Exponential_1P(failures=self.data, 
                                  show_probability_plot=False, 
                                  print_results=False)
    
    def CDF(self):
        plt.figure(figsize=(8, 5))

        self.fit.distribution.CDF(label="Weibull ajustada")
        plot_points(failures=self.data, func="CDF")

        plt.title("Função Acumulada de Falha (CDF)")
        plt.xlabel('Horas')
        plt.ylabel('Probabilidade Acumulada de Falha')

        plt.grid(True, which="both")
        # plt.legend()

        fig = plt.gcf()
        return fig

    def SF(self):
        plt.figure(figsize=(8, 5))

        self.fit.distribution.SF(label='Weibull ajustada')
        plot_points(failures=self.data, func='SF')

        plt.title("Função de Sobrevivência (SF)")
        plt.xlabel('Horas')
        plt.ylabel('Probabilidade Acumulada de Sobrevivência')

        plt.grid(True, which="both")
        # plt.legend()
        fig = plt.gcf()
        return fig

    def PDF(self):
        plt.figure(figsize=(8, 5))

        self.fit.distribution.PDF(label='Weibull ajustada')

        plt.title("Função de Densidade de Probabilidade (PDF)")
        plt.xlabel('Horas')
        plt.ylabel('Densidade de Probabilidade')

        plt.grid(True, which="both")
        # plt.legend()
        fig = plt.gcf()
        return fig

    def HF(self):
        plt.figure(figsize=(8, 5))

        self.fit.distribution.HF(label='Weibull ajustada')

        plt.title("Função de Taxa de Falha (HF)")
        plt.xlabel('Horas')
        plt.ylabel('Taxa de Falha')

        plt.grid(True, which="both")
        # plt.legend()
        fig = plt.gcf()
        return fig

    def Probabilidade(self):
        plt.figure(figsize=(8, 5))

        Exponential_probability_plot(failures=self.data)

        plt.title("Probabilidade Weibull")
        plt.xlabel('Horas')
        plt.ylabel('Probabilidade Acumulada de Falha')

        plt.grid(True, which="both")
        # plt.legend()
        fig = plt.gcf()
        return fig

    def Tabela(self):
        plt.figure(figsize=(8, 5))
        
        plt.axis('off')  # remove eixos

        # Dados da tabela
        cell_text = [
            ["Lambda (λ)", f"{self.fit.Lambda:.5f}", f"{self.fit.Lambda_SE:.5f}",
            f"{self.fit.Lambda_lower:.5f}", f"{self.fit.Lambda_upper:.5f}"],

            ["MTTF (θ = 1/λ)", f"{1/self.fit.Lambda:.2f}", "-", "-", "-"],

            ["Log-likelihood", f'{self.fit.loglik:.3f}' if isinstance(self.fit.loglik, (int,float)) else self.fit.loglik, "-", "-", "-"],
            ["AICc", f"{self.fit.AICc:.3f}" if isinstance(self.fit.AICc, (int,float)) else self.fit.AICc, "-", "-", "-"],
            ["BIC", f"{self.fit.BIC:.3f}" if isinstance(self.fit.BIC, (int,float)) else self.fit.BIC, "-", "-", "-"],
            ["Anderson-Darling", f"{self.fit.AD:.4f}" if isinstance(self.fit.AD, (int,float)) else fit.AD, "-", "-", "-"],
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
        fig = plt.gcf()
        return fig

    def executar(self, dist):
        graficos = {}
        for distribuicao in dist:
            funcao = getattr(self, distribuicao)
            graficos[distribuicao] = funcao()
        return graficos


class Lognormal:
    def __init__(self, data):
        self.data = data
        
        from reliability.Fitters import Fit_Lognormal_2P
        
        self.fit = Fit_Lognormal_2P(failures=self.data, 
                                  show_probability_plot=False, 
                                  print_results=False)
    
    def CDF(self):
        plt.figure(figsize=(8, 5))

        self.fit.distribution.CDF(label="Weibull ajustada")
        plot_points(failures=self.data, func="CDF")

        plt.title("Função Acumulada de Falha (CDF)")
        plt.xlabel('Horas')
        plt.ylabel('Probabilidade Acumulada de Falha')

        plt.grid(True, which="both")
        # plt.legend()

        fig = plt.gcf()
        return fig

    def SF(self):
        plt.figure(figsize=(8, 5))

        self.fit.distribution.SF(label='Weibull ajustada')
        plot_points(failures=self.data, func='SF')

        plt.title("Função de Sobrevivência (SF)")
        plt.xlabel('Horas')
        plt.ylabel('Probabilidade Acumulada de Sobrevivência')

        plt.grid(True, which="both")
        # plt.legend()
        fig = plt.gcf()
        return fig

    def PDF(self):
        plt.figure(figsize=(8, 5))

        self.fit.distribution.PDF(label='Weibull ajustada')

        plt.title("Função de Densidade de Probabilidade (PDF)")
        plt.xlabel('Horas')
        plt.ylabel('Densidade de Probabilidade')

        plt.grid(True, which="both")
        # plt.legend()
        fig = plt.gcf()
        return fig

    def HF(self):
        plt.figure(figsize=(8, 5))

        self.fit.distribution.HF(label='Weibull ajustada')

        plt.title("Função de Taxa de Falha (HF)")
        plt.xlabel('Horas')
        plt.ylabel('Taxa de Falha')

        plt.grid(True, which="both")
        # plt.legend()
        fig = plt.gcf()
        return fig

    def Probabilidade(self):
        plt.figure(figsize=(8, 5))

        Lognormal_probability_plot(failures=self.data)

        plt.title("Probabilidade Weibull")
        plt.xlabel('Horas')
        plt.ylabel('Probabilidade Acumulada de Falha')

        plt.grid(True, which="both")
        # plt.legend()
        fig = plt.gcf()
        return fig

    def Tabela(self):
        plt.figure(figsize=(8, 5))
        
        plt.axis('off')  # remove eixos

        # Dados da tabela
        cell_text = [
            ["Mu (μ)", f"{self.fit.mu:.4f}", f"{self.fit.mu_SE:.4f}",
            f"{self.fit.mu_lower:.4f}", f"{self.fit.mu_upper:.4f}"],

            ["Sigma (σ)", f"{self.fit.sigma:.4f}", f"{self.fit.sigma_SE:.4f}",
            f"{self.fit.sigma_lower:.4f}", f"{self.fit.sigma_upper:.4f}"],

            ["Log-likelihood", f"{self.fit.loglik:.3f}" if isinstance(self.fit.loglik, (int, float)) else self.fit.loglik, "-", "-", "-"],
            ["AICc", f"{self.fit.AICc:.3f}" if isinstance(self.fit.AICc, (int, float)) else self.fit.AICc, "-", "-", "-"],
            ["BIC", f"{self.fit.BIC:.3f}" if isinstance(self.fit.BIC, (int, float)) else self.fit.BIC, "-", "-", "-"],
            ["Anderson-Darling", f"{self.fit.AD:.4f}" if isinstance(self.fit.AD, (int, float)) else self.fit.AD, "-", "-", "-"],
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
        fig = plt.gcf()
        return fig

    def executar(self, dist):
        graficos = {}
        for distribuicao in dist:
            funcao = getattr(self, distribuicao)
            graficos[distribuicao] = funcao()
        return graficos