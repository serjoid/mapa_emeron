import flet as ft
from database import Database

db = Database()

# Definindo uma lista de cores
CORES = [
    ft.colors.BLUE,
    ft.colors.RED,
    ft.colors.GREEN,
    ft.colors.YELLOW,
    ft.colors.PURPLE,
    ft.colors.ORANGE,
    ft.colors.PINK,
    ft.colors.LIGHT_BLUE,
    ft.colors.LIGHT_GREEN,
    ft.colors.AMBER,
    ft.colors.DEEP_ORANGE,
    ft.colors.DEEP_PURPLE,
    ft.colors.CYAN,
    ft.colors.TEAL
]

def tela_inicial(page: ft.Page):
    # Calcula os dados
    alunos = [aluno for aluno in db.get_aluno() if " (2)" not in aluno]
    num_alunos = len(alunos)
    num_cursos = len(db.get_curso())
    num_orientadores = len(db.get_orientador())

    # Informações textuais em cards separados
    info_cards = ft.ResponsiveRow(
        controls=[
            ft.Card(  # Card 1
                content=
                ft.Column(
                    [
                        ft.Text("Alunos", style=ft.TextStyle(size=14, color=ft.colors.WHITE)),
                        ft.Text(f"{num_alunos}", style=ft.TextStyle(size=18, color=ft.colors.WHITE, weight=ft.FontWeight.W_500)), 
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    height=70,
                    width=200,
                    spacing=2,
                ),
                color="#006BA0",
                margin=10,
                col={"sm": 4},  # Ocupa 4 colunas em telas médias e maiores
            ),
            ft.Card(  # Card 2
                content=ft.Column(
                    [
                        ft.Text("Orientadores", style=ft.TextStyle(size=14, color=ft.colors.WHITE)),
                        ft.Text(f"{num_orientadores}", style=ft.TextStyle(size=18, color=ft.colors.WHITE, weight=ft.FontWeight.W_500)),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    height=70,
                    width=200,
                    spacing=2,
                ),
                color="#006BA0",
                margin=10,
                col={"sm": 4},  # Ocupa 4 colunas em telas médias e maiores
            ),
            ft.Card(  # Card 3
                content=ft.Column(
                    [
                        ft.Text("Cursos", style=ft.TextStyle(size=14, color=ft.colors.WHITE)),
                        ft.Text(f"{num_cursos}", style=ft.TextStyle(size=18, color=ft.colors.WHITE, weight=ft.FontWeight.W_500)), # Fonte bold
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    height=70,
                    width=200,
                    spacing=2,
                ),
                color="#006BA0",
                margin=10,
                col={"sm": 4},  # Ocupa 4 colunas em telas médias e maiores
            ),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        width=1200,  # Largura máxima dos cards
    )
    
    # Dados para o pie chart 1 (Alunos Ativos por Curso)
    dados_pie_chart_1 = db.get_alunos_por_curso()

    # Dados para o pie chart 2 (Fases de Pesquisa)
    dados_pie_chart_2 = db.get_alunos_por_fase_pesquisa()

    # Pie chart 1: Alunos Ativos por Curso
    pie_chart_1 = ft.Container(
        content=ft.Column(
            controls=[
                ft.Text("Alunos por Curso", style=ft.TextStyle(size=18)),
                ft.PieChart(
                    sections=[
                        ft.PieChartSection(
                            value,
                            color=CORES[i % len(CORES)],
                            border_side=ft.border.BorderSide(width=0),
                            radius=100
                        )
                        for i, (label, value) in enumerate(dados_pie_chart_1)
                    ],
                    center_space_radius=0,
                ),
                ft.Column(  # Coluna para a legenda do gráfico 1
                    controls=[
                        ft.Row(
                            controls=[
                                ft.Container(
                                    width=10,
                                    height=10,
                                    bgcolor=CORES[i % len(CORES)],
                                ),
                                ft.Text(f"{label}: {value}", style=ft.TextStyle(size=14)),
                            ]
                        )
                        for i, (label, value) in enumerate(dados_pie_chart_1)
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,  # Centraliza a legenda
                ),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,  # Centraliza todo o conteúdo do gráfico
        ),
        width=400,
        height=600,
        padding=20,
        bgcolor=ft.colors.with_opacity(0.1, ft.colors.BLUE_50),
        margin=ft.margin.all(10),  # Margem para espaçamento
    )

    # Pie chart 2: Fases de Pesquisa (Estrutura idêntica ao pie_chart_1)
    pie_chart_2 = ft.Container(
        content=ft.Column(
            controls=[
                ft.Text("Fases da Pesquisa", style=ft.TextStyle(size=18)),
                ft.PieChart(
                    sections=[
                        ft.PieChartSection(
                            value,
                            color=CORES[i % len(CORES)],
                            border_side=ft.border.BorderSide(width=0),
                            radius=100
                        )
                        for i, (label, value) in enumerate(dados_pie_chart_2)
                    ],
                    center_space_radius=0,
                    
                ),
                ft.Column(  # Coluna para a legenda do gráfico 2
                    controls=[
                        ft.Row(
                            controls=[
                                ft.Container(
                                    width=10,
                                    height=10,
                                    bgcolor=CORES[i % len(CORES)],
                                ),
                                ft.Text(f"{label}: {value}", style=ft.TextStyle(size=14)), 
                            ]
                        )
                        for i, (label, value) in enumerate(dados_pie_chart_2)
                    ],
                    alignment=ft.MainAxisAlignment.CENTER, 
                ),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER, 
        ),
        width=400,
        height=600,
        padding=20,
        bgcolor=ft.colors.with_opacity(0.1, ft.colors.BLUE_50),
        margin=ft.margin.all(10),  
    )

    # Pie chart 1: Alunos Ativos por Curso - responsivo
    pie_chart_3 = ft.Container(
        content=ft.Column(
            controls=[
                ft.Text("Alunos Ativos por Curso", style=ft.TextStyle(size=16)),
                ft.PieChart(
                    sections=[
                        ft.PieChartSection(
                            value,
                            color=CORES[i % len(CORES)],
                            border_side=ft.border.BorderSide(width=0),
                            radius=100
                        )
                        for i, (label, value) in enumerate(dados_pie_chart_1)
                    ],
                    center_space_radius=0,
                ),
                ft.Column(  # Coluna para a legenda do gráfico 1
                    controls=[
                        ft.Row(
                            controls=[
                                ft.Container(
                                    width=10,
                                    height=10,
                                    bgcolor=CORES[i % len(CORES)],
                                ),
                                ft.Text(f"{label}: {value}", style=ft.TextStyle(size=12)),
                            ]
                        )
                        for i, (label, value) in enumerate(dados_pie_chart_1)
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,  # Centraliza a legenda
                ),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,  # Centraliza todo o conteúdo do gráfico
        ),
        width=400,
        height=600,
        padding=20,
        bgcolor=ft.colors.with_opacity(0.1, ft.colors.BLUE_50),
        margin=ft.margin.all(10),  # Margem para espaçamento
    )

    # Pie chart 2: Fases de Pesquisa (Estrutura idêntica ao pie_chart_1) - responsivo
    pie_chart_4 = ft.Container(
        content=ft.Column(
            controls=[
                ft.Text("Fases de Pesquisa em Andamento", style=ft.TextStyle(size=16)),
                ft.PieChart(
                    sections=[
                        ft.PieChartSection(
                            value,
                            color=CORES[i % len(CORES)],
                            border_side=ft.border.BorderSide(width=0),
                            radius=100
                        )
                        for i, (label, value) in enumerate(dados_pie_chart_2)
                    ],
                    center_space_radius=0,
                    
                ),
                ft.Column(  # Coluna para a legenda do gráfico 2
                    controls=[
                        ft.Row(
                            controls=[
                                ft.Container(
                                    width=10,
                                    height=10,
                                    bgcolor=CORES[i % len(CORES)],
                                ),
                                ft.Text(f"{label}: {value}", style=ft.TextStyle(size=12)), 
                            ]
                        )
                        for i, (label, value) in enumerate(dados_pie_chart_2)
                    ],
                    alignment=ft.MainAxisAlignment.CENTER, 
                ),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER, 
        ),
        width=400,
        height=600,
        padding=20,
        bgcolor=ft.colors.with_opacity(0.1, ft.colors.BLUE_50),
        margin=ft.margin.all(10),  
    )

    fluxo_img = ft.Container(
        ft.Container(
            content=ft.Image(
                src="fluxo.png",
                fit=ft.ImageFit.CONTAIN,
                width=1200,
            ),
            expand=True,
            alignment=ft.alignment.center,
        ),
        padding=20,
        border_radius=ft.border_radius.all(10),
        bgcolor=ft.colors.with_opacity(0.1, ft.colors.BLUE_50),
    )

    # Container para os gráficos
    graficos_container = ft.Row(
        controls=[
            ft.Column(controls=[pie_chart_1], alignment=ft.MainAxisAlignment.CENTER),
            ft.Column(controls=[pie_chart_2], alignment=ft.MainAxisAlignment.CENTER),
        ],
        alignment=ft.MainAxisAlignment.SPACE_AROUND,
    )
    # Container para os gráficos responsivos
    graficos_container2 = ft.ResponsiveRow(
        controls=[
            ft.Column(controls=[pie_chart_3], alignment=ft.MainAxisAlignment.START),
            ft.Column(controls=[pie_chart_4], alignment=ft.MainAxisAlignment.START),
        ],
        alignment=ft.MainAxisAlignment.SPACE_AROUND,
    )

    divisor = ft.ResponsiveRow(controls=[ft.Divider()], alignment=ft.MainAxisAlignment.CENTER)

    nome_campo = ft.Text("PÁGINA INICIAL", size=16, color="#006BA0", font_family="Roboto", weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER)

    # Container principal da tela inicial
    container_home = ft.Container(
        expand=True,
        content=
        ft.Column(
            controls=[
                nome_campo,
                divisor,
                info_cards,
                divisor,
                graficos_container,  # Container para gráficos lado a lado
                graficos_container2,
                divisor,
                fluxo_img,
            ],
            scroll=ft.ScrollMode.ALWAYS,
            horizontal_alignment="CENTER"  # Habilita o scroll vertical
        )
    )

    def on_resize(e):
        if page.width < 1024:
            graficos_container.visible = False
            graficos_container2.visible = True
        else:
            graficos_container.visible = True
            graficos_container2.visible = False
        page.update()

    if page.width < 1024:
        graficos_container.visible = False
        graficos_container2.visible = True
    else:
        graficos_container.visible = True
        graficos_container2.visible = False

    page.update()

    page.on_resize = on_resize

    return container_home