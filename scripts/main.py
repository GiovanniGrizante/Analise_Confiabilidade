from Arquivos import dados, distribuicoes
import os, sys, pandas as pd


if __name__ == '__main__':
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    df, per_ini, per_fim, espec = dados.main()
    distribuicoes.main(df, per_ini, per_fim, espec)