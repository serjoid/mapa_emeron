import flet as ft
from database import Database

# Inicializa a conexão com o banco de dados
db = Database()

# Define uma lista de cores para os gráficos
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

# Define a função para exibir a tela inicial
def tela_inicial(page: ft.Page):
    """
    Cria a tela inicial com informações sobre alunos, orientadores e cursos.

    Args:
        page (ft.Page): A página Flet atual.
    """

    # Calcula a quantidade de alunos, cursos e orientadores
    alunos = [aluno for aluno in db.get_aluno() if " (2)" not in aluno]  # Obtém a lista de alunos, excluindo duplicatas
    num_alunos = len(alunos)  # Calcula o número de alunos
    num_cursos = len(db.get_curso())  # Calcula o número de cursos
    num_orientadores = len(db.get_orientador())  # Calcula o número de orientadores

    # Cria os cards com as informações textuais
    info_cards = ft.ResponsiveRow(
        controls=[
            ft.Card(  # Card para o número de alunos
                content=
                ft.Column(
                    [
                        ft.Text("Alunos", style=ft.TextStyle(size=14, color=ft.colors.WHITE)),  # Título do card
                        ft.Text(f"{num_alunos}", style=ft.TextStyle(size=18, color=ft.colors.WHITE, weight=ft.FontWeight.W_500)),  # Valor do número de alunos
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,  # Alinhamento vertical do conteúdo
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,  # Alinhamento horizontal do conteúdo
                    height=70,
                    width=200,
                    spacing=2,  # Espaçamento entre os elementos
                ),
                color="#006BA0",  # Cor de fundo do card
                margin=10,  # Margem do card
                col={"sm": 4},  # Ocupa 4 colunas em telas médias e maiores
            ),
            ft.Card(  # Card para o número de orientadores (estrutura similar ao card de alunos)
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
                col={"sm": 4},
            ),
            ft.Card(  # Card para o número de cursos (estrutura similar ao card de alunos)
                content=ft.Column(
                    [
                        ft.Text("Cursos", style=ft.TextStyle(size=14, color=ft.colors.WHITE)),
                        ft.Text(f"{num_cursos}", style=ft.TextStyle(size=18, color=ft.colors.WHITE, weight=ft.FontWeight.W_500)),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    height=70,
                    width=200,
                    spacing=2,
                ),
                color="#006BA0",
                margin=10,
                col={"sm": 4},
            ),
        ],
        alignment=ft.MainAxisAlignment.CENTER,  # Alinhamento horizontal dos cards
        width=1200,  # Largura máxima dos cards
    )
    
    # Obtém os dados para os gráficos de pizza
    dados_pie_chart_1 = db.get_alunos_por_curso()  # Obtém os dados de alunos por curso
    dados_pie_chart_2 = db.get_alunos_por_fase_pesquisa()  # Obtém os dados de alunos por fase da pesquisa

    # Cria o gráfico de pizza 1: Alunos Ativos por Curso
    pie_chart_1 = ft.Container(
        content=ft.Column(
            controls=[
                ft.Text("Alunos por Curso", style=ft.TextStyle(size=18)),  # Título do gráfico
                ft.PieChart(
                    sections=[
                        ft.PieChartSection(
                            value,  # Valor da seção
                            color=CORES[i % len(CORES)],  # Define a cor da seção usando a lista CORES
                            border_side=ft.border.BorderSide(width=0),  # Remove a borda da seção
                            radius=100  # Define o raio do gráfico
                        )
                        for i, (label, value) in enumerate(dados_pie_chart_1)  # Itera sobre os dados do gráfico
                    ],
                    center_space_radius=0,  # Define o raio do espaço central do gráfico como 0
                ),
                ft.Column(  # Coluna para a legenda do gráfico
                    controls=[
                        ft.Row(  # Linha para cada item da legenda
                            controls=[
                                ft.Container(  # Container para a cor da legenda
                                    width=10,
                                    height=10,
                                    bgcolor=CORES[i % len(CORES)],  # Define a cor da legenda usando a lista CORES
                                ),
                                ft.Text(f"{label}: {value}", style=ft.TextStyle(size=14)),  # Texto da legenda
                            ]
                        )
                        for i, (label, value) in enumerate(dados_pie_chart_1)  # Itera sobre os dados do gráfico
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,  # Alinhamento vertical da legenda
                ),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,  # Alinhamento horizontal do conteúdo do gráfico
        ),
        width=400,
        height=600,
        padding=20,
        bgcolor=ft.colors.with_opacity(0.1, ft.colors.BLUE_50),  # Cor de fundo do container
        margin=ft.margin.all(10),  # Margem do container
    )

    # Cria o gráfico de pizza 2: Fases de Pesquisa (estrutura similar ao gráfico de pizza 1)
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

    # Cria o gráfico de pizza 3: Alunos Ativos por Curso (versão responsiva)
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
                ft.Column(  # Coluna para a legenda do gráfico 3
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

    # Cria o gráfico de pizza 4: Fases de Pesquisa (versão responsiva, estrutura similar ao gráfico de pizza 3)
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
                ft.Column(  # Coluna para a legenda do gráfico 4
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

    # Cria o container para a imagem do fluxo de trabalho
    fluxo_img = ft.Container(
        ft.Container(
            content=ft.Image(
                src="fluxo.png",  # Caminho para a imagem do fluxo de trabalho
                fit=ft.ImageFit.CONTAIN,  # Define o ajuste da imagem dentro do container
                width=1200,  # Define a largura da imagem
            ),
            expand=True,  # Permite que o container se expanda para preencher o espaço disponível
            alignment=ft.alignment.center,  # Alinha a imagem no centro do container
        ),
        padding=20,  # Define o espaçamento interno do container
        border_radius=ft.border_radius.all(10),  # Define o raio de borda do container
        bgcolor=ft.colors.with_opacity(0.1, ft.colors.BLUE_50),  # Define a cor de fundo do container
    )

    # Cria o container para os gráficos (versão para telas maiores)
    graficos_container = ft.Row(
        controls=[
            ft.Column(controls=[pie_chart_1], alignment=ft.MainAxisAlignment.CENTER),  # Coluna para o gráfico de pizza 1
            ft.Column(controls=[pie_chart_2], alignment=ft.MainAxisAlignment.CENTER),  # Coluna para o gráfico de pizza 2
        ],
        alignment=ft.MainAxisAlignment.SPACE_AROUND,  # Define o espaçamento entre as colunas
    )

    # Cria o container para os gráficos (versão responsiva para telas menores)
    graficos_container2 = ft.ResponsiveRow(
        controls=[
            ft.Column(controls=[pie_chart_3], alignment=ft.MainAxisAlignment.START),  # Coluna para o gráfico de pizza 3
            ft.Column(controls=[pie_chart_4], alignment=ft.MainAxisAlignment.START),  # Coluna para o gráfico de pizza 4
        ],
        alignment=ft.MainAxisAlignment.SPACE_AROUND,  # Define o espaçamento entre as colunas
    )

    # Cria um divisor visual
    divisor = ft.ResponsiveRow(controls=[ft.Divider()], alignment=ft.MainAxisAlignment.CENTER)

    # Cria o título da tela inicial
    nome_campo = ft.Text("PÁGINA INICIAL", size=16, color="#006BA0", font_family="Roboto", weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER)

    # Cria o container principal da tela inicial
    container_home = ft.Container(
        expand=True,  # Permite que o container se expanda para preencher o espaço disponível
        content=
        ft.Column(
            controls=[
                nome_campo,  # Título da tela
                divisor,  # Divisor visual
                info_cards,  # Cards com informações sobre alunos, orientadores e cursos
                divisor,  # Divisor visual
                graficos_container,  # Container para os gráficos (versão para telas maiores)
                graficos_container2,  # Container para os gráficos (versão responsiva para telas menores)
                divisor,  # Divisor visual
                fluxo_img,  # Container para a imagem do fluxo de trabalho
            ],
            scroll=ft.ScrollMode.ALWAYS,  # Habilita a rolagem vertical
            horizontal_alignment="CENTER"  # Define o alinhamento horizontal do conteúdo
        )
    )

    # Define a função para lidar com o evento de redimensionamento da tela
    def on_resize(e):
        """
        Ajusta a visibilidade dos containers de gráficos de acordo com a largura da tela.
        """
        # Se a largura da tela for menor que 1024 pixels, exibe os gráficos responsivos e oculta os gráficos lado a lado
        if page.width < 1024:
            graficos_container.visible = False
            graficos_container2.visible = True
        # Caso contrário, exibe os gráficos lado a lado e oculta os gráficos responsivos
        else:
            graficos_container.visible = True
            graficos_container2.visible = False
        page.update()  # Atualiza a página

    # Define a visibilidade inicial dos containers de gráficos de acordo com a largura da tela
    if page.width < 1024:
        graficos_container.visible = False
        graficos_container2.visible = True
    else:
        graficos_container.visible = True
        graficos_container2.visible = False

    # Atualiza a página
    page.update()

    # Define a função on_resize como a função a ser chamada quando a tela for redimensionada
    page.on_resize = on_resize

    # Retorna o container principal da tela inicial
    return container_home
