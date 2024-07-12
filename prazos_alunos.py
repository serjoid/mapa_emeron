import flet as ft  # Importa a biblioteca Flet
from database import Database  # Importa a classe Database do módulo 'database.py'
from datetime import date, timedelta  # Importa as classes date e timedelta do módulo datetime
import datetime  # Importa o módulo datetime

# Inicializa a conexão com o banco de dados
db = Database()

# Define a função para exibir a tela de prazos do aluno logado
def tela_prazos_alunos(page: ft.Page, aluno_id, nome_aluno):
    """
    Exibe os prazos cadastrados para o aluno logado.

    Args:
        page (ft.Page): A página Flet atual.
        aluno_id (int): O ID do aluno logado.
        nome_aluno (str): O nome do aluno logado.
    """

    # Cria a tabela de prazos
    tabela_prazos = ft.DataTable(
        columns=[
            ft.DataColumn(  # Coluna para a fase da pesquisa
                ft.Container(ft.Text("Fase de Pesquisa"), alignment=ft.alignment.center)  # Centraliza o texto na coluna
            ),
            ft.DataColumn(  # Coluna para a data do prazo da fase
                ft.Container(
                    ft.Text("Prazo Fase Pesquisa"), alignment=ft.alignment.center  # Centraliza o texto na coluna
                )
            ),
            ft.DataColumn(  # Coluna para o prazo em dias
                ft.Container(ft.Text("Prazo em Dias"), alignment=ft.alignment.center)  # Centraliza o texto na coluna
            ),
            ft.DataColumn(  # Coluna para a situação do prazo
                ft.Container(ft.Text("Situação do Prazo"), alignment=ft.alignment.center)  # Centraliza o texto na coluna
            ),
            ft.DataColumn(  # Coluna para a situação da fase
                ft.Container(ft.Text("Situação da Fase"), alignment=ft.alignment.center)  # Centraliza o texto na coluna
            ),
            ft.DataColumn(  # Coluna para o tempo restante em dias
                ft.Container(
                    ft.Text("Tempo Restante (dias)"), alignment=ft.alignment.center  # Centraliza o texto na coluna
                )
            ),
        ],
        rows=[],  # Inicialmente, a tabela não possui linhas, serão adicionadas dinamicamente
        border=ft.border.all(2, "black"),  # Define a borda da tabela
        border_radius=ft.border_radius.all(10),  # Define o raio de borda da tabela
        bgcolor="WHITE",  # Define a cor de fundo da tabela
    )

    # Cria o container para os campos de texto dos prazos (visível apenas em telas menores que 1024 pixels de largura)
    container_info_prazos = ft.Container(
        content=ft.Column(spacing=5, width=1300),  # Define o conteúdo do container como uma coluna com espaçamento de 5 pixels entre os elementos
        visible=False  # O container é inicialmente invisível
    )

    # Cria os campos de texto para exibir as informações do aluno
    nome_aluno_text = ft.Row(  # Linha para o nome do aluno
        [
            ft.Text("Nome:", size=14, weight=ft.FontWeight.BOLD),  # Texto "Nome:" em negrito
            ft.Text(f" {nome_aluno}", size=14),  # Nome do aluno
        ]
    )
    curso_text = ft.Row(  # Linha para o curso do aluno
        [
            ft.Text("Curso:", size=14, weight=ft.FontWeight.BOLD),  # Texto "Curso:" em negrito
            ft.Text("", size=14),  # Campo de texto para o curso, inicialmente vazio
        ]
    )
    orientador_text = ft.Row(  # Linha para o orientador do aluno
        [
            ft.Text("Orientador:", size=14, weight=ft.FontWeight.BOLD),  # Texto "Orientador:" em negrito
            ft.Text("", size=14),  # Campo de texto para o orientador, inicialmente vazio
        ]
    )

    # Define a função para carregar os dados do prazo do aluno
    def carregar_dados_prazo():
        """Carrega os dados do prazo do aluno e atualiza a tabela e os campos de texto."""
        prazos = db.get_prazos_by_pessoa_id(aluno_id)  # Obtém a lista de prazos do aluno a partir do ID
        pessoa_info = db.get_pessoa_info(nome_aluno)  # Obtém as informações do aluno a partir do nome

        # Ordena a lista de prazos pela data do prazo, colocando os prazos sem data no final
        prazos.sort(
            key=lambda prazo: datetime.datetime.strptime(
                prazo["prazo_fase_pesquisa"], "%d/%m/%Y"
            ).date()
            if prazo["prazo_fase_pesquisa"]
            else datetime.date.max
        )

        global dados_tabela_prazos  # Acessa a variável global dados_tabela_prazos
        dados_tabela_prazos = prazos  # Define a variável global com a lista de prazos

        # Limpa a tabela de prazos e os campos de texto
        tabela_prazos.rows.clear()
        container_info_prazos.content.controls.clear()

        # Itera sobre a lista de prazos
        for prazo in prazos:
            # Calcula o tempo restante em dias para o prazo
            prazo_fase_pesquisa_date = (
                datetime.datetime.strptime(prazo["prazo_fase_pesquisa"], "%d/%m/%Y").date()
                if prazo["prazo_fase_pesquisa"]
                else None
            )
            tempo_restante = (
                (prazo_fase_pesquisa_date - date.today()).days
                if prazo_fase_pesquisa_date
                else "N/A"  # Define "N/A" se a data do prazo não estiver definida
            )
            # Se a situação da fase for "Concluído", o tempo restante é definido como 0
            if prazo["situacao_fase_pesquisa"] == "Concluído":
                tempo_restante = 0

            # Cria a célula "Tempo Restante" para a tabela
            tempo_restante_cell = ft.DataCell(ft.Text(str(tempo_restante)))

            # Adiciona uma nova linha à tabela de prazos com as informações do prazo
            tabela_prazos.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(prazo["fase_pesquisa"])),  # Fase da pesquisa
                        ft.DataCell(ft.Text(prazo["prazo_fase_pesquisa"])),  # Data do prazo
                        ft.DataCell(ft.Text(str(prazo["prazo_dias"]))),  # Prazo em dias (convertido para string)
                        ft.DataCell(ft.Text(prazo["prazo_situacao"])),  # Situação do prazo
                        ft.DataCell(ft.Text(prazo["situacao_fase_pesquisa"])),  # Situação da fase
                        tempo_restante_cell,  # Célula com o tempo restante em dias
                    ]
                )
            )

            # Adiciona os campos de texto com as informações do prazo ao container de informações dos prazos (visível em telas pequenas)
            container_info_prazos.content.controls.append(
                ft.Text(f"Fase da Pesquisa: {prazo['fase_pesquisa']}")
            )
            container_info_prazos.content.controls.append(
                ft.Text(f"Prazo Fase Pesquisa: {prazo['prazo_fase_pesquisa']}")
            )
            container_info_prazos.content.controls.append(
                ft.Text(f"Prazo em Dias: {str(prazo['prazo_dias'])}")
            )
            container_info_prazos.content.controls.append(
                ft.Text(f"Situação do Prazo: {prazo['prazo_situacao']}")
            )
            container_info_prazos.content.controls.append(
                ft.Text(f"Situação da Fase: {prazo['situacao_fase_pesquisa']}")
            )
            container_info_prazos.content.controls.append(
                ft.Text(f"Tempo Restante (dias): {str(tempo_restante)}")
            )
            container_info_prazos.content.controls.append(ft.Divider())

        # Define o valor dos campos de texto para o curso e orientador do aluno
        curso_text.controls[1].value = pessoa_info.get("curso", "")
        orientador_text.controls[1].value = pessoa_info.get("orientador", "")

        # Atualiza a página
        page.update()

    # Chama a função para carregar os dados do prazo do aluno
    carregar_dados_prazo()

    # Cria o título da tela
    nome_campo = ft.Text(
        "ANDAMENTO DA PESQUISA",
        size=16,
        color="#006BA0",
        font_family="Roboto",
        weight=ft.FontWeight.BOLD,  # Define o peso da fonte como negrito
        text_align=ft.TextAlign.CENTER,  # Alinha o texto ao centro
    )

    # Cria o container principal da tela
    container_prazos = ft.Container(
        expand=True,  # Permite que o container se expanda para preencher o espaço disponível
        content=ft.Column(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,  # Alinha o conteúdo horizontalmente ao centro
            scroll=ft.ScrollMode.ALWAYS,  # Habilita a rolagem vertical quando o conteúdo excede o tamanho do container
            controls=[
                nome_campo,  # Título da tela
                ft.Divider(),  # Divisor visual
                ft.ResponsiveRow(controls=[  # Linha responsiva para as informações do aluno
                    ft.Column(
                        controls=[
                            nome_aluno_text,  # Nome do aluno
                            curso_text,  # Curso do aluno
                            orientador_text,  # Orientador do aluno
                            ft.Divider(),  # Divisor visual
                        ]
                    )
                ], width=800),  # Define a largura da linha responsiva como 800 pixels
                ft.Container(  # Container para a tabela de prazos
                    width=1300,  # Define a largura do container
                    content=tabela_prazos,  # Define o conteúdo do container como a tabela de prazos
                    margin=ft.margin.only(top=10),  # Define a margem superior do container como 10 pixels
                ),
                container_info_prazos,  # Container com os campos de texto dos prazos (visível em telas pequenas)
            ],
        ),
    )

    # Define a função para redimensionar os containers quando a tela for redimensionada
    def resize_containers(e):
        """Redimensiona os containers de acordo com a largura da tela."""
        # Se a largura da tela for menor que 1024 pixels, exibe o container de informações dos prazos e oculta a tabela de prazos
        if page.width < 1024:
            tabela_prazos.visible = False
            container_info_prazos.visible = True
            # Define o tamanho da fonte dos campos de texto para 12 pixels
            nome_aluno_text.controls[0].size = 12
            nome_aluno_text.controls[1].size = 12
            curso_text.controls[0].size = 12
            curso_text.controls[1].size = 12
            orientador_text.controls[0].size = 12
            orientador_text.controls[1].size = 12
        # Se a largura da tela for maior ou igual a 1024 pixels, exibe a tabela de prazos e oculta o container de informações dos prazos
        else:
            tabela_prazos.visible = True
            container_info_prazos.visible = False
            # Define o tamanho da fonte dos campos de texto para 14 pixels
            nome_aluno_text.controls[0].size = 14
            nome_aluno_text.controls[1].size = 14
            curso_text.controls[0].size = 14
            curso_text.controls[1].size = 14
            orientador_text.controls[0].size = 14
            orientador_text.controls[1].size = 14
        page.update()  # Atualiza a página para exibir as alterações

    # Define a visibilidade inicial dos containers de acordo com a largura da tela
    if page.width < 1024:
        tabela_prazos.visible = False
        container_info_prazos.visible = True
        nome_aluno_text.controls[0].size = 12
        nome_aluno_text.controls[1].size = 12
        curso_text.controls[0].size = 12
        curso_text.controls[1].size = 12
        orientador_text.controls[0].size = 12
        orientador_text.controls[1].size = 12
    else:
        tabela_prazos.visible = True
        container_info_prazos.visible = False
        nome_aluno_text.controls[0].size = 14
        nome_aluno_text.controls[1].size = 14
        curso_text.controls[0].size = 14
        curso_text.controls[1].size = 14
        orientador_text.controls[0].size = 14
        orientador_text.controls[1].size = 14
    page.update()  # Atualiza a página

    # Define a função 'resize_containers' como a função a ser chamada quando a tela for redimensionada
    page.on_resize = resize_containers

    # Retorna o container principal da tela
    return container_prazos
