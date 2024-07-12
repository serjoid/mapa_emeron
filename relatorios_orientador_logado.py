import flet as ft
from database import Database
from profile import tela_profile

# Conexão com o banco de dados
db = Database()
df = db.get_relatorio_geral()

# Parâmetros de paginação
LINHAS_POR_PAGINA = 25
pagina_atual = 1
ITENS_POR_BATCH = 10  # Número de itens a serem carregados por vez na ListView
carregando = False  # Variável para controlar o carregamento
itens_carregados_lv = 0 # Variável global para rastrear quantos itens foram carregados na ListView

# Função para calcular o total de páginas
def calcular_total_paginas(total_registros):
    return (total_registros + LINHAS_POR_PAGINA - 1) // LINHAS_POR_PAGINA

# Função para exibir a página atual
def exibir_pagina(pagina, page, conteudo_container):
    global pagina_atual, datatable, botao_anterior, botao_proximo

    pagina_atual = pagina
    inicio = (pagina - 1) * LINHAS_POR_PAGINA
    fim = inicio + LINHAS_POR_PAGINA

    fonte_paginacao = ft.FontWeight.BOLD

    # Usa uma variável local 'dados_pagina'
    dados_pagina = dados_relatorio[inicio:fim] 

    def criar_linhas(dados):
        return [
            ft.DataRow(
                cells=[
                    ft.DataCell(
                        ft.Text(row.cells[0].content.value),
                        on_tap=lambda e, nome=row.cells[0].content.value: abrir_tela_aluno(e, nome, page, conteudo_container),
                    ),
                    ft.DataCell(ft.Text(row.cells[1].content.value)),
                    ft.DataCell(ft.Text(row.cells[2].content.value)),
                    ft.DataCell(ft.Text(row.cells[3].content.value)),
                    ft.DataCell(ft.Text(row.cells[4].content.value)),
                    ft.DataCell(ft.Text(row.cells[5].content.value)),
                    ft.DataCell(ft.Text(row.cells[6].content.value)),
                    ft.DataCell(ft.Text(row.cells[7].content.value)),
                    ft.DataCell(ft.Text(row.cells[8].content.value)),
                    ft.DataCell(ft.Text(row.cells[9].content.value)),
                ]
            )
            for row in dados 
        ]

    # Limpa as linhas existentes antes de adicionar as novas
    datatable.content.controls[1].rows.clear()
    datatable.content.controls[1].rows = criar_linhas(dados_pagina)  # Usa 'dados_pagina'
    datatable.content.controls[0].value = f"Exibindo {len(datatable.content.controls[1].rows)} de {len(dados_relatorio)} registros"
    datatable.content.controls[2].value = f"Página {pagina_atual} de {calcular_total_paginas(len(dados_relatorio))}"
    datatable.content.controls[0].weight = fonte_paginacao
    datatable.content.controls[2].weight = fonte_paginacao

    botao_anterior.disabled = pagina == 1
    botao_proximo.disabled = fim >= len(dados_relatorio)

    datatable.update()
    botao_anterior.update()
    botao_proximo.update()

def abrir_tela_aluno(e, nome_aluno, page, conteudo_container):
    """Abre a tela de perfil do aluno dentro do container especificado."""
    conteudo_container.content = tela_profile(page, nome_aluno)
    conteudo_container.update()

def criar_relatorio_listview(db, page, orientador):
    global itens_carregados_lv, container_listview, lv_responsivo

    lv_responsivo = ft.ListView(
        expand=True,
        spacing=10,
        item_extent=100,
        first_item_prototype=True,
        on_scroll=lambda e: carregar_mais_itens_lv_scroll(e, orientador),  
    )

    # Container para o texto e a lista
    container_listview = ft.Container(
        content=ft.Column(
            controls=[
                ft.Text(f"Total de registros: {len(db.get_orientador_relatorio_lista(orientador))}"),
                lv_responsivo,
            ],
            spacing=10
        ),
        expand=True,
        padding=10
    )

    return container_listview

def carregar_mais_itens_lv(page, orientador, inicial=False):
    """Carrega mais itens na ListView e exibe um diálogo com o progresso."""
    global itens_carregados_lv, carregando

    if carregando:  # Verifica se já está carregando
        return

    carregando = True  # Impede chamadas concorrentes

    dados_alunos = db.get_orientador_relatorio_lista(orientador)
    total_registros = len(dados_alunos)

    if itens_carregados_lv < total_registros:
        proximos_itens = min(ITENS_POR_BATCH, total_registros - itens_carregados_lv)
        for i in range(itens_carregados_lv, itens_carregados_lv + proximos_itens):
            aluno = dados_alunos[i]
            container_aluno = criar_container_aluno(aluno)
            lv_responsivo.controls.append(container_aluno)

        itens_carregados_lv += proximos_itens

        # Exibe o diálogo apenas se não for o carregamento inicial
        if not inicial:
            # Função para fechar o diálogo
            def fechar_dialogo(e):
                dlg.open = False
                page.update()

            # Exibe o diálogo com o progresso do carregamento
            dlg = ft.AlertDialog(
                modal=True,
                title=ft.Text("Carregamento"),
                content=ft.Text(f"Carregados {itens_carregados_lv} de {total_registros} registros."),
                actions=[ft.TextButton("OK", on_click=fechar_dialogo)],
            )
            page.dialog = dlg
            dlg.open = True
            page.update()

    carregando = False  # Libera para o próximo carregamento

# Modifica a função para receber 'orientador' como argumento
def carregar_mais_itens_lv_scroll(e, orientador):
    """Carrega mais itens quando o usuário rola a página."""
    global lv_responsivo

    # Verifica se o usuário rolou até o final da lista
    if e.scroll_offset + e.control.viewport_size.height >= e.control.content_size.height:
        carregar_mais_itens_lv(e.page, orientador)

def criar_container_aluno(aluno):
    """Cria um container para exibir os dados de um aluno."""
    return ft.Container(
        content=ft.Column(
            [
                ft.Text("Discente", font_family="Roboto", weight=ft.FontWeight.BOLD),
                ft.Text(aluno[0]),
                ft.Text("Curso", font_family="Roboto", weight=ft.FontWeight.BOLD),
                ft.Text(aluno[1]),
                ft.Text("Polo", font_family="Roboto", weight=ft.FontWeight.BOLD),
                ft.Text(aluno[2]),
                ft.Text("IES Promotora", font_family="Roboto", weight=ft.FontWeight.BOLD),
                ft.Text(aluno[3]),
                ft.Text("Ano de Ingresso", font_family="Roboto", weight=ft.FontWeight.BOLD),
                ft.Text(aluno[4]),
                ft.Text("Situação", font_family="Roboto", weight=ft.FontWeight.BOLD),
                ft.Text(aluno[5]),
                ft.Text("Fase da pesquisa", font_family="Roboto", weight=ft.FontWeight.BOLD),
                ft.Text(aluno[6]),
                ft.Text("Prazo da fase", font_family="Roboto", weight=ft.FontWeight.BOLD),
                ft.Text(aluno[7]),
                ft.Text("Situação da fase", font_family="Roboto", weight=ft.FontWeight.BOLD),
                ft.Text(aluno[8]),
            ],
            spacing=5,
        ),
        border=ft.border.all(1),
        padding=10,
        border_radius=ft.border_radius.all(10),
        bgcolor="WHITE",
    )

def relatorios_orientador_logado(page: ft.Page, usuario):
    global dados_relatorio, datatable, botao_anterior, botao_proximo, container_listview, itens_carregados_lv

    # Obtém o nome do orientador a partir do usuário logado
    orientador = db.get_orientador_info_por_usuario(usuario)['nome']

    dados_relatorio = db.get_orientador_relatorio(orientador)

    columns = [
        ft.DataColumn(ft.Text("Discente", width=150, size=12, weight=ft.FontWeight.BOLD)),
        ft.DataColumn(ft.Text("Curso", width=200, size=12, weight=ft.FontWeight.BOLD)),
        ft.DataColumn(ft.Text("Polo", width=100, size=12, weight=ft.FontWeight.BOLD)),
        ft.DataColumn(ft.Text("IES Promotora", width=100, size=12, weight=ft.FontWeight.BOLD)),
        ft.DataColumn(ft.Text("Ano de Ingresso", width=100, size=12, weight=ft.FontWeight.BOLD)),
        ft.DataColumn(ft.Text("Ano de Conclusão", width=100, size=12, weight=ft.FontWeight.BOLD)),
        ft.DataColumn(ft.Text("Situação", width=100, size=12, weight=ft.FontWeight.BOLD)),
        ft.DataColumn(ft.Text("Fase da pesquisa", width=100, size=12, weight=ft.FontWeight.BOLD)),
        ft.DataColumn(ft.Text("Prazo da fase", width=100, size=12, weight=ft.FontWeight.BOLD)),
        ft.DataColumn(ft.Text("Situação da fase", width=100, size=12, weight=ft.FontWeight.BOLD)),
    ]

    datatable = ft.Container(
        ft.Column(
            controls=[
                ft.Text(f"Exibindo 0 de 0 registros", weight=ft.FontWeight.BOLD),  # Inicialmente, não há registros
                ft.DataTable(
                    columns=columns,
                    rows=[],  # Inicializa as linhas como uma lista vazia
                    border=ft.border.all(2, "black"),
                    border_radius=ft.border_radius.all(10),
                    width=1700,
                    horizontal_margin=10,
                    data_row_max_height=90,
                    column_spacing=20,
                    vertical_lines=ft.border.BorderSide(0.2, "black"),
                    bgcolor="WHITE"
                ),
                ft.Text(f"Página 0 de 0 registros", weight=ft.FontWeight.BOLD),  # Inicialmente, não há páginas
            ]
        ),
        margin=1,
        padding=10,
        width=1700,
        visible=True,
    )

    botao_anterior = ft.IconButton(
        icon=ft.icons.ARROW_BACK,
        width=40,
        height=40,
        bgcolor=ft.colors.WHITE,
        disabled=True,
        on_click=lambda e: exibir_pagina(pagina_atual - 1, page, container_relatorios),
    )

    botao_proximo = ft.IconButton(
        icon=ft.icons.ARROW_FORWARD,
        width=40,
        height=40,
        bgcolor=ft.colors.WHITE,
        on_click=lambda e: exibir_pagina(pagina_atual + 1, page, container_relatorios),
    )

    def carregar_relatorio(e):
        exibir_pagina(1, page, container_relatorios)

    botao_carregar = ft.ElevatedButton(
        text="Carregar Relatório", 
        on_click=carregar_relatorio,
        width=200,
        height=40,
        elevation=4,
        bgcolor="#006BA0",
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
        color="WHITE"
    )

    botao_carregar_mais = ft.ElevatedButton(
        text="Carregar Mais",
        width=200,
        height=40,
        elevation=4,
        bgcolor="#006BA0",
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
        color="WHITE",
        on_click=lambda e: carregar_mais_itens_lv(e.page, orientador),  # Chama a função para carregar mais itens
        visible=False,  # Inicialmente invisível
    )

    # Cria a ListView responsiva
    container_listview = criar_relatorio_listview(db, page, orientador)
    container_listview.visible = False  # Inicialmente oculta

    nome_campo = ft.Text("RELATÓRIOS", size=16, color="#006BA0", font_family="Roboto", weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER)

    container_relatorios = ft.Container(
        expand=True,
        padding=1,
        content=ft.Container(  # Container externo
            content=ft.ResponsiveRow(
                vertical_alignment=ft.CrossAxisAlignment.START,
                alignment=ft.MainAxisAlignment.START,
                controls=[
                    ft.Column(
                        scroll=ft.ScrollMode.ALWAYS,
                        controls=[
                            nome_campo,
                            ft.Divider(),
                            ft.ResponsiveRow(
                                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                                controls=[
                                    ft.Container(
                                        content=ft.Row(
                                            controls=[
                                                botao_anterior,
                                                botao_proximo,
                                                botao_carregar,  # Botão para carregar o relatório
                                            ]
                                        ),
                                        col={"sm": 12},  # Ocupa toda a largura em telas pequenas
                                    ),
                                ],
                            ),
                            ft.Container(content=datatable, col={"sm": 12}),  # Container para o DataTable
                            ft.Container(content=botao_carregar_mais, col={"sm": 12}),  # Container para o botão "Carregar Mais"
                            ft.Container(content=container_listview, col={"sm": 12}),  # Container para a ListView responsiva
                        ],
                    )
                ],
            ),
            margin=ft.margin.only(bottom=20),
        ),
    )

    def resize_relatorio(e):
        global itens_carregados_lv
        width = e.control.width
        total_registros = len(db.get_orientador_relatorio_lista(orientador))

        if width < 1024:
            # Oculta datatable
            datatable.visible = False
            botao_anterior.visible = False
            botao_proximo.visible = False
            botao_carregar.visible = False
            # Mostra a ListView responsiva
            container_listview.visible = True
            # Mostra o botão "Carregar Mais" se houver mais de 10 registros
            botao_carregar_mais.visible = total_registros > ITENS_POR_BATCH
            # Carrega os itens na ListView se ainda não foram carregados
            if itens_carregados_lv == 0:
                carregar_mais_itens_lv(page, orientador, inicial=True)
            # Reinicia a contagem de itens carregados
            itens_carregados_lv = ITENS_POR_BATCH
            page.update()
        else:
            # Mostra datatable
            datatable.visible = True
            botao_anterior.visible = True
            botao_proximo.visible = True
            botao_carregar.visible = True
            # Oculta a ListView responsiva
            container_listview.visible = False
            # Oculta o botão "Carregar Mais"
            botao_carregar_mais.visible = False
            # Reinicia a contagem de itens carregados
            itens_carregados_lv = ITENS_POR_BATCH
            page.update()

    if page.width < 1024:
        # Oculta datatable
        datatable.visible = False
        botao_anterior.visible = False
        botao_proximo.visible = False
        botao_carregar.visible = False
        # Mostra a ListView responsiva
        container_listview.visible = True
        # Mostra o botão "Carregar Mais" se houver mais de 10 registros
        botao_carregar_mais.visible = True
        # Carrega os itens na ListView se ainda não foram carregados
        if itens_carregados_lv == 0:
            carregar_mais_itens_lv(page, orientador, inicial=True)
        # Reinicia a contagem de itens carregados
        itens_carregados_lv = ITENS_POR_BATCH
        page.update()
    else:
        # Mostra datatable
        datatable.visible = True
        botao_anterior.visible = True
        botao_proximo.visible = True
        botao_carregar.visible = True
        # Oculta a ListView responsiva
        container_listview.visible = False
        # Oculta o botão "Carregar Mais"
        botao_carregar_mais.visible = False
        # Reinicia a contagem de itens carregados
        itens_carregados_lv = ITENS_POR_BATCH
        page.update()

    page.on_resize = resize_relatorio

    return container_relatorios