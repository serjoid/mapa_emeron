import flet as ft
from database import Database
from datetime import date, timedelta
import datetime

# Conexão com o banco de dados
db = Database()


def tela_prazos_alunos(page: ft.Page, aluno_id, nome_aluno):
    """
    Exibe os prazos cadastrados para o aluno logado.

    Args:
        page (ft.Page): A página Flet atual.
        aluno_id (int): O ID do aluno logado.
        nome_aluno (str): O nome do aluno logado.
    """

    # Tabela de prazos
    tabela_prazos = ft.DataTable(
        columns=[
            ft.DataColumn(
                ft.Container(ft.Text("Fase de Pesquisa"), alignment=ft.alignment.center)
            ),
            ft.DataColumn(
                ft.Container(
                    ft.Text("Prazo Fase Pesquisa"), alignment=ft.alignment.center
                )
            ),
            ft.DataColumn(
                ft.Container(ft.Text("Prazo em Dias"), alignment=ft.alignment.center)
            ),
            ft.DataColumn(
                ft.Container(ft.Text("Situação do Prazo"), alignment=ft.alignment.center)
            ),
            ft.DataColumn(
                ft.Container(ft.Text("Situação da Fase"), alignment=ft.alignment.center)
            ),
            ft.DataColumn(
                ft.Container(
                    ft.Text("Tempo Restante (dias)"), alignment=ft.alignment.center
                )
            ),
        ],
        rows=[],
        border=ft.border.all(2, "black"),
        border_radius=ft.border_radius.all(10),
        bgcolor="WHITE",
    )

    # Container para os ft.Text dos prazos - Inicialmente invisível
    container_info_prazos = ft.Container(
        content=ft.Column(spacing=5, width=1300), visible=False
    )

    # ft.Text para as informações do aluno - Inicializados como vazios
    nome_aluno_text = ft.Row(
        [
            ft.Text("Nome:", size=14, weight=ft.FontWeight.BOLD),
            ft.Text(f" {nome_aluno}", size=14),
        ]
    )
    curso_text = ft.Row(
        [
            ft.Text("Curso:", size=14, weight=ft.FontWeight.BOLD),
            ft.Text("", size=14),
        ]
    )  # Inicializado vazio
    orientador_text = ft.Row(
        [
            ft.Text("Orientador:", size=14, weight=ft.FontWeight.BOLD),
            ft.Text("", size=14),
        ]
    )  # Inicializado vazio

    # Função para carregar os dados do prazo do aluno
    def carregar_dados_prazo():
        prazos = db.get_prazos_by_pessoa_id(aluno_id)
        pessoa_info = db.get_pessoa_info(nome_aluno)  # Busca pelo nome

        # Ordena a lista de prazos pelo prazo cadastrado,
        # colocando os prazos com 'prazo_fase_pesquisa' vazio no final
        prazos.sort(
            key=lambda prazo: datetime.datetime.strptime(
                prazo["prazo_fase_pesquisa"], "%d/%m/%Y"
            ).date()
            if prazo["prazo_fase_pesquisa"]
            else datetime.date.max
        )

        global dados_tabela_prazos
        dados_tabela_prazos = prazos

        # Atualiza a tabela de prazos (sem curso e orientador)
        tabela_prazos.rows.clear()
        container_info_prazos.content.controls.clear()  # Limpa os textos anteriores

        for prazo in prazos:
            # Calcula o tempo restante
            prazo_fase_pesquisa_date = (
                datetime.datetime.strptime(prazo["prazo_fase_pesquisa"], "%d/%m/%Y").date()
                if prazo["prazo_fase_pesquisa"]
                else None
            )
            tempo_restante = (
                (prazo_fase_pesquisa_date - date.today()).days
                if prazo_fase_pesquisa_date
                else "N/A"
            )
            if prazo["situacao_fase_pesquisa"] == "Concluído":
                tempo_restante = 0

            # Cria a célula "Tempo Restante" para a tabela
            tempo_restante_cell = ft.DataCell(ft.Text(str(tempo_restante)))

            # Adiciona a linha na tabela
            tabela_prazos.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(prazo["fase_pesquisa"])),
                        ft.DataCell(ft.Text(prazo["prazo_fase_pesquisa"])),
                        ft.DataCell(ft.Text(str(prazo["prazo_dias"]))),
                        ft.DataCell(ft.Text(prazo["prazo_situacao"])),
                        ft.DataCell(ft.Text(prazo["situacao_fase_pesquisa"])),
                        tempo_restante_cell,
                    ]
                )
            )

            # Adiciona os textos no container para telas pequenas
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

        # Define os valores para curso e orientador
        curso_text.controls[1].value = pessoa_info.get("curso", "")
        orientador_text.controls[1].value = pessoa_info.get("orientador", "")

        # Atualiza a página
        page.update()

    # Chama a função para carregar os dados
    carregar_dados_prazo()

    nome_campo = ft.Text(
        "ANDAMENTO DA PESQUISA",
        size=16,
        color="#006BA0",
        font_family="Roboto",
        weight=ft.FontWeight.BOLD,
        text_align=ft.TextAlign.CENTER,
    )

    container_prazos = ft.Container(
        expand=True,
        content=ft.Column(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            scroll=ft.ScrollMode.ALWAYS,
            controls=[
                nome_campo,
                ft.Divider(),
                ft.ResponsiveRow(controls=[
                ft.Column(
                    controls=[
                        nome_aluno_text,
                        curso_text,
                        orientador_text,
                        ft.Divider(),
                    ]
                )], width=800),
                ft.Container(
                    width=1300,
                    content=tabela_prazos,
                    margin=ft.margin.only(top=10),
                ),
                container_info_prazos,
            ],
        ),
    )

    def resize_containers(e):
        if page.width < 1024:
            tabela_prazos.visible = False
            container_info_prazos.visible = True
            nome_aluno_text.controls[0].size = 12
            nome_aluno_text.controls[1].size = 12
            # Ajusta o tamanho da fonte dos textos de curso e orientador
            curso_text.controls[0].size = 12
            curso_text.controls[1].size = 12
            orientador_text.controls[0].size = 12
            orientador_text.controls[1].size = 12
        else:
            tabela_prazos.visible = True
            container_info_prazos.visible = False
            nome_aluno_text.controls[0].size = 14
            nome_aluno_text.controls[1].size = 14
            # Ajusta o tamanho da fonte dos textos de curso e orientador
            curso_text.controls[0].size = 14
            curso_text.controls[1].size = 14
            orientador_text.controls[0].size = 14
            orientador_text.controls[1].size = 14
        page.update()

    if page.width < 1024:
        tabela_prazos.visible = False
        container_info_prazos.visible = True
        nome_aluno_text.controls[0].size = 12
        nome_aluno_text.controls[1].size = 12
        # Ajusta o tamanho da fonte dos textos de curso e orientador
        curso_text.controls[0].size = 12
        curso_text.controls[1].size = 12
        orientador_text.controls[0].size = 12
        orientador_text.controls[1].size = 12
    else:
        tabela_prazos.visible = True
        container_info_prazos.visible = False
        nome_aluno_text.controls[0].size = 14
        nome_aluno_text.controls[1].size = 14
        # Ajusta o tamanho da fonte dos textos de curso e orientador
        curso_text.controls[0].size = 14
        curso_text.controls[1].size = 14
        orientador_text.controls[0].size = 14
        orientador_text.controls[1].size = 14
    page.update()

    page.on_resize = resize_containers

    return container_prazos