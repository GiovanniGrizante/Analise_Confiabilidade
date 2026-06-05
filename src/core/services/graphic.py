import matplotlib.pyplot as plt
from datetime import datetime
from pathlib import Path

def show_graph():
    plt.show(block=False)
    input('\nPressione Enter para fechar as figuras e continuar...')
    plt.close('all')

def save_graph(planta, tag, graficos):
    today = datetime.now().strftime("%d-%m-%Y")
    time = datetime.now().strftime("%H%M%S")

    base_path = (
        Path(__file__).parent.parent.parent.parent
        / 'images' / 'Específico' / planta / tag / f'{today}'
    )

    for item in graficos:
        metodo = item["metodo"]
        tipo = item["tipo"]
        fig = item["fig"]

        # pasta por método
        graph_folder = base_path / metodo
        graph_folder.mkdir(parents=True, exist_ok=True)

        # nome do arquivo
        filename = f"{tipo}_{time}.png"

        fig.savefig(graph_folder / filename, dpi=600, bbox_inches='tight')
