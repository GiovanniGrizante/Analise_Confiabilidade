import matplotlib.pyplot as plt
from datetime import datetime
from pathlib import Path

def show_graph():
    plt.show(block=False)
    input('\nPressione Enter para fechar as figuras e continuar...')
    plt.close('all')

def save_graph(planta, tag, classe_metodo, graficos):
    today = datetime.now().strftime("%d-%m-%Y")
        
    graph_folder = (Path(__file__).parent.parent.parent.parent / 'images' / 'Específico' / 
                    planta / tag / classe_metodo / f'{today}')
    
    graph_folder.mkdir(parents=True, exist_ok=True)
    
    for title, graph in graficos.items():
        plt.figure(graph)
        plt.savefig(graph_folder / f'{title}.png', dpi=600, bbox_inches='tight')