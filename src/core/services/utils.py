import sys

def questao(quest, intervalo):
    while True:
        resp = input(quest)
        if resp in intervalo:
            return resp
            # Limpa a linha anterior
        sys.stdout.write('\033[F\033[K')