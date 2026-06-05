from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Image,
    PageBreak, Table, TableStyle
)
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors

from io import BytesIO
from collections import defaultdict
from datetime import datetime

import tempfile
import os
import platform
import subprocess


# ---------------- CAPA ----------------
def title_page(planta, tag, metodo, distribuicao, logo_path, elementos, styles):

    if logo_path:
        logo = Image(logo_path, width=120, height=60)
        elementos.append(logo)

    elementos.append(Spacer(1, 40))

    elementos.append(Paragraph(
        "<b>RELATÓRIO DE ANÁLISE DE CONFIABILIDADE</b>",
        styles["Title"]
    ))

    elementos.append(Spacer(1, 30))

    elementos.append(Paragraph(f"<b>Planta:</b> {planta}", styles["Normal"]))
    elementos.append(Paragraph(f"<b>Tag:</b> {tag}", styles["Normal"]))

    elementos.append(Spacer(1, 15))

    elementos.append(Paragraph(
        f"<b>Métodos:</b> {', '.join(metodo)}",
        styles["Normal"]
    ))

    elementos.append(Paragraph(
        f"<b>Distribuições:</b> {', '.join(distribuicao)}",
        styles["Normal"]
    ))

    elementos.append(Spacer(1, 40))

    elementos.append(Paragraph(
        f"Gerado automaticamente em {datetime.now().strftime('%d/%m/%Y %H:%M')}",
        styles["Italic"]
    ))

    elementos.append(PageBreak())


# ---------------- GRID ----------------
def grid(imgs):
    colunas = 2
    linhas = []
    linha_atual = []

    for item in imgs:
        linha_atual.append(item)
        if len(linha_atual) == colunas:
            linhas.append(linha_atual)
            linha_atual = []

    if linha_atual:
        linhas.append(linha_atual)

    return linhas


# ---------------- BUILD PÁGINAS ----------------
def build_pages(elementos, linhas):
    max_linhas_por_pagina = 3  # até 6 gráficos

    for i in range(0, len(linhas), max_linhas_por_pagina):
        bloco = linhas[i:i + max_linhas_por_pagina]

        tabela = Table(bloco, colWidths=[260, 260])
        tabela.setStyle(TableStyle([
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 10)
        ]))

        elementos.append(tabela)

        if i + max_linhas_por_pagina < len(linhas):
            elementos.append(PageBreak())


# ---------------- PREPARAR GRÁFICOS ----------------
def prepare_graphs(graficos, styles):
    elementos = []

    # ordena para consistência visual
    graficos = sorted(graficos, key=lambda x: (x["metodo"], x["tipo"]))

    agrupado = defaultdict(list)

    for item in graficos:
        agrupado[item["metodo"]].append(item)

    for metodo, itens in agrupado.items():

        # ✅ título da seção
        elementos.append(Paragraph(
            f"<b>Método: {metodo}</b>",
            styles["Heading2"]
        ))

        elementos.append(Spacer(1, 15))

        imgs = []

        for item in itens:
            tipo = item["tipo"]
            fig = item["fig"]

            buffer = BytesIO()
            fig.savefig(buffer, format='png', bbox_inches='tight')
            buffer.seek(0)

            img = Image(buffer)
            img._restrictSize(250, 200)

            bloco = [
                Paragraph(tipo, styles["Heading4"]),
                Spacer(1, 5),
                img
            ]

            imgs.append(bloco)

        linhas = grid(imgs)
        build_pages(elementos, linhas)

        elementos.append(PageBreak())

    return elementos


# ---------------- CRIAR RELATÓRIO ----------------
def create_report(planta, tag, metodo, distribuicao, graficos, logo_path=None):

    buffer = BytesIO()

    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40
    )

    elementos = []
    styles = getSampleStyleSheet()

    # capa
    title_page(planta, tag, metodo, distribuicao, logo_path, elementos, styles)

    # gráficos
    elementos.extend(prepare_graphs(graficos, styles))

    doc.build(elementos)

    buffer.seek(0)
    return buffer


# ---------------- ABRIR PDF ----------------
def open_pdf(planta, tag, metodo, distribuicao, graficos, logo_path=None):

    # nomes dos métodos
    metodo = [m.__name__ for m in metodo]

    buffer = create_report(
        planta,
        tag,
        metodo,
        distribuicao,
        graficos,
        logo_path
    )

    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(buffer.getvalue())
        caminho = tmp.name

    if platform.system() == "Windows":
        os.startfile(caminho)

    elif platform.system() == "Darwin":
        subprocess.run(["open", caminho])

    else:
        subprocess.run(["xdg-open", caminho])