# Sistema de Análise de Confiabilidade

Sistema para análise estatística de falhas de equipamentos industriais, com foco em manutenção preditiva e confiabilidade.

## 📋 Funcionalidades

### Atuais
- **Ingestão de dados** - Suporte a CSV, Excel e Parquet
- **Análise Específica** - Estudo detalhado de TAGs individuais
- **Distribuições estatísticas**:
  - Weibull (2 parâmetros)
  - Exponencial (1 parâmetro)
  - Lognormal (2 parâmetros)
- **Métricas de confiabilidade**:
  - CDF (Função Acumulada de Falha)
  - SF (Função de Sobrevivência)
  - PDF (Função Densidade de Probabilidade)
  - HF (Função Taxa de Falha)
  - Probability Plot
  - Tabela de parâmetros (α, β, λ, μ, σ com intervalos de confiança)

### Em desenvolvimento
- **Análise por Criticidade** - Classificação de equipamentos por nível de criticidade (Alta/Média/Baixa)
- **Exportação para PDF** - Relatórios completos com gráficos e métricas
- **Interpretação automática** - Sugestões baseadas nos parâmetros das distribuições

## 🏗️ Arquitetura

O projeto segue princípios de **clean architecture** com separação clara entre:

```bash
src/
├── core/ # Lógica de negócio (independente de UI)
├── ui/ # Interface terminal (substituível por GUI/API)
├── filters/ # Regras de filtragem e preparação de dados
├── dominio/ # Modelos de distribuições estatísticas
├── database/ # Persistência (SQLite + SQLAlchemy)
└── settings/ # Configurações e utilitários
```

### Diferencial arquitetural
- **Backend-first** - Toda lógica implementada independente da camada de apresentação
- **Facilmente extensível** - Pode adicionar GUI (Tkinter/PyQt), API REST (FastAPI) ou manter terminal
- **Testável** - Estados e regras de negócio testáveis sem UI

## 🚀 Instalação

### Dependências

```bash
pip install pandas scikit-learn numpy scipy reliability matplotlib openpyxl sqlalchemy
```

## 💻 Uso

### Executando o sistema

```bash
python main.py
```

### Fluxo de trabalho

1. Primeira execução - Escolha opção 1 para atualizar banco de dados

2. Análise específica - Opção 3 → fluxo interativo:

- Selecione a planta (Orgânicos/Sílica)

- Digite a TAG do equipamento (4 caracteres)

- Escolha distribuição (Weibull/Exponencial/Lognormal/Todas)

- Selecione as métricas desejadas (CDF/SF/PDF/HF/Probabilidade/Tabela/Todas)

- Visualize, salve ou gere relatório dos gráficos

### Navegação

- 0 - Voltar ao menu anterior

- 0 (no menu principal) - Sair do sistema

- Enter após visualizar gráficos para continuar

## 📊 Exemplo de saída

### Gráficos gerados

- CDF: Probabilidade acumulada de falha ao longo do tempo

- SF: Probabilidade de sobrevivência (1 - CDF)

- PDF: Taxa instantânea de falhas

- HF: Taxa de risco (falhas por unidade de tempo)

- Probability Plot: Validação visual do ajuste da distribuição

- Tabela: Parâmetros ajustados com intervalos de confiança e métricas de qualidade (Log-likelihood, AICc, BIC, Anderson-Darling)

### Interpretação dos parâmetros Weibull

- β < 1: Falhas prematuras ("mortalidade infantil")

- β = 1: Falhas aleatórias (equivalente à exponencial)

- β > 1: Falhas por desgaste (recomenda troca preventiva)

## 🔧 Personalização

### Adicionando nova distribuição

1. Crie classe em dominio/distribuicoes.py seguindo o padrão Weibull/Exponencial/Lognormal

2. Implemente métodos CDF(), SF(), PDF(), HF(), Probabilidade(), Tabela()

3. Adicione ao dicionário met_dict em estado_metodo()

### Modificando interface

- As funções de UI estão isoladas em ui/

- Substitua por Tkinter mantendo as mesmas assinaturas de função

## 📝 Observações técnicas

### Banco de dados

- SQLite com duas tabelas principais: ordens_clean e notas_clean

- Junção via Ordem para correlacionar notas de falha com ordens de serviço

- Dados de criticidade futuramente integrados via Excel compartilhado (OneDrive/SharePoint)

### Cálculo de tempos de falha

- Baseado na diferença entre data_hora_fim de uma ordem e data_hora_inicio da próxima

- Considera censura à direita (período final de análise) e à esquerda (início do histórico)

- Unidade: horas

### Dependência externa

- Biblioteca reliability para fitting estatístico (requer licença para uso comercial? Verificar)

- Alternativa futura: implementar MLE manual para maior controle

## 🤝 Contribuição

1. Fork o projeto

2. Crie sua feature branch (git checkout -b feature/nova-distribuicao)

3. Commit suas mudanças (git commit -m 'Adiciona distribuição Gama')

4. Push para a branch (git push origin feature/nova-distribuicao)

5. Abra um Pull Request
