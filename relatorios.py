import flet as ft
from database import Database
import os
import http.server
import socketserver
import threading
import socket
from profile import tela_profile

# Conexão com o banco de dados
db = Database()
num_alunos = len(db.get_aluno())
df = db.get_relatorio_geral()

# Parâmetros de paginação
LINHAS_POR_PAGINA = 25
pagina_atual = 1
ITENS_POR_BATCH = 10  # Número de itens a serem carregados por vez na ListView
carregando = False  # Variável para controlar o carregamento
itens_carregados_lv = 0 # Variável global para rastrear quantos itens foram carregados na ListView

def calcular_total_paginas(total_registros):
    return (total_registros + LINHAS_POR_PAGINA - 1) // LINHAS_POR_PAGINA

def exibir_pagina(pagina, page, conteudo_container):
    global pagina_atual, datatable, datatable_cursos, datatable_orientadores, botao_anterior, botao_proximo

    pagina_atual = pagina
    inicio = (pagina - 1) * LINHAS_POR_PAGINA
    fim = inicio + LINHAS_POR_PAGINA

    fonte_paginacao = ft.FontWeight.BOLD

    def criar_linhas(dados):
        # ORDENAR OS DADOS AQUI DENTRO da função criar_linhas
        dados = sorted(dados, key=lambda x: x.cells[0].content.value) # Ordena por nome (coluna 0)
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
            for row in dados[inicio:fim] # Faz a paginação DEPOIS de ordenar
        ]

    if datatable.visible:
        datatable.content.controls[1].rows = criar_linhas(dados_relatorio)
        datatable.content.controls[0].value = f"Exibindo {len(datatable.content.controls[1].rows)} de {len(dados_relatorio)} registros"
        datatable.content.controls[2].value = f"Página {pagina_atual} de {calcular_total_paginas(len(dados_relatorio))}"
    elif datatable_cursos.visible:
        datatable_cursos.content.controls[1].rows = criar_linhas(dados_relatorio_curso)
        datatable_cursos.content.controls[0].value = f"Exibindo {len(datatable_cursos.content.controls[1].rows)} de {len(dados_relatorio_curso)} registros"
        datatable_cursos.content.controls[2].value = f"Página {pagina_atual} de {calcular_total_paginas(len(dados_relatorio_curso))}"
    elif datatable_orientadores.visible:
        datatable_orientadores.content.controls[1].rows = criar_linhas(dados_relatorio_orientador)
        datatable_orientadores.content.controls[0].value = f"Exibindo {len(datatable_orientadores.content.controls[1].rows)} de {len(dados_relatorio_orientador)} registros"
        datatable_orientadores.content.controls[2].value = f"Página {pagina_atual} de {calcular_total_paginas(len(dados_relatorio_orientador))}"

    for control in [datatable.content.controls[0], datatable.content.controls[2],
                    datatable_cursos.content.controls[0], datatable_cursos.content.controls[2],
                    datatable_orientadores.content.controls[0], datatable_orientadores.content.controls[2]]:
        control.weight = fonte_paginacao

    botao_anterior.disabled = pagina == 1
    botao_proximo.disabled = fim >= len(dados_relatorio)

    page.update() 

def abrir_tela_aluno(e, nome_aluno, page, conteudo_container):
    """Abre a tela de perfil do aluno dentro do container especificado."""
    conteudo_container.content = tela_profile(page, nome_aluno)
    conteudo_container.update()

def criar_relatorio_listview(db, page):
    global itens_carregados_lv, container_listview, lv_responsivo # Tornando lv_responsivo global

    lv_responsivo = ft.ListView(
        expand=True,
        spacing=10,
        item_extent=100,
        first_item_prototype=True,
        on_scroll=carregar_mais_itens_lv_scroll  # Chama a função no scroll
    )

    # Container para o texto e a lista
    container_listview = ft.Container( 
        content=ft.Column(
            controls=[
                ft.Text(f"Total de registros: {len(db.get_relatorio_lista())}"),
                lv_responsivo, 
            ],
            spacing=10 
        ),
        expand=True,
        padding=10
    )

    # Carrega os primeiros itens
    carregar_mais_itens_lv(page, inicial=True)  # Passa 'inicial=True' para o primeiro carregamento

    return container_listview

def carregar_mais_itens_lv(page, inicial=False):
    """Carrega mais itens na ListView e exibe um diálogo com o progresso."""
    global itens_carregados_lv, carregando

    if carregando:  # Verifica se já está carregando
        return

    carregando = True  # Impede chamadas concorrentes

    dados_alunos = db.get_relatorio_lista()
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

def carregar_mais_itens_lv_scroll(e):
    """Carrega mais itens quando o usuário rola a página."""
    global lv_responsivo

    # Verifica se o usuário rolou até o final da lista
    if e.scroll_offset + e.control.viewport_size.height >= e.control.content_size.height:
        carregar_mais_itens_lv(e.page)

def criar_container_aluno(aluno):
    """Cria um container para exibir os dados de um aluno."""
    return ft.Container(
        content=ft.Column(
            [
                ft.Text("Discente", font_family="Roboto", weight=ft.FontWeight.BOLD),
                ft.Text(aluno[0]),
                ft.Text("Curso", font_family="Roboto", weight=ft.FontWeight.BOLD),
                ft.Text(aluno[1]),
                ft.Text("Orientador", font_family="Roboto", weight=ft.FontWeight.BOLD),
                ft.Text(aluno[2]),
                ft.Text("Polo", font_family="Roboto", weight=ft.FontWeight.BOLD),
                ft.Text(aluno[3]),
                ft.Text("IES Promotora", font_family="Roboto", weight=ft.FontWeight.BOLD),
                ft.Text(aluno[4]),
                ft.Text("Ano de Ingresso", font_family="Roboto", weight=ft.FontWeight.BOLD),
                ft.Text(aluno[5]),
                ft.Text("Situação do Aluno", font_family="Roboto", weight=ft.FontWeight.BOLD),
                ft.Text(aluno[6]),
                ft.Text("Fase da pesquisa", font_family="Roboto", weight=ft.FontWeight.BOLD),
                ft.Text(aluno[7]),
                ft.Text("Prazo da fase", font_family="Roboto", weight=ft.FontWeight.BOLD),
                ft.Text(aluno[8]),
                ft.Text("Situação da fase", font_family="Roboto", weight=ft.FontWeight.BOLD),
                ft.Text(aluno[9]),
            ],
            spacing=5,
        ),
        border=ft.border.all(1),
        padding=10,
        border_radius=ft.border_radius.all(10),
        bgcolor="WHITE",
    )

def tela_relatorios(page: ft.Page):
    global dados_relatorio, dados_relatorio_curso, dados_relatorio_orientador, datatable, datatable_cursos, datatable_orientadores, botao_anterior, botao_proximo, anchor, anchor2, anchor3, lv_responsivo, botao_carregar_mais, itens_carregados_lv

    dados_relatorio = db.get_relatorio()
    dados_relatorio_curso = []
    dados_relatorio_orientador = []
    nomes_cursos = db.get_curso()
    nomes_orientadores = db.get_orientador()
    nome_alunos = db.get_aluno()

    # Cria a ListView responsiva, passando 'page' como argumento
    container_listview = criar_relatorio_listview(db, page)  # Recebe o container
    container_listview.visible = False  # Inicialmente oculta

    lv = ft.ListView()
    for nome in nomes_cursos:
        lv.controls.append(ft.ListTile(title=ft.Text(nome), on_click=lambda e, nome=nome: close_anchor(e, nome), data=nome))
    lv2 = ft.ListView()
    lv2.controls.append(ft.ListTile(title=ft.Text("A definir"), on_click=lambda e, nome="A definir": close_anchor2(e, nome), data="A definir"))
    for nome in nomes_orientadores:
        lv2.controls.append(ft.ListTile(title=ft.Text(nome), on_click=lambda e, nome=nome: close_anchor2(e, nome), data=nome))
    lv3 = ft.ListView()
    for nome in nome_alunos:
        lv3.controls.append(ft.ListTile(title=ft.Text(nome), on_click=lambda e, nome=nome: close_anchor3(e, nome), data=nome))

    def close_anchor(e, nome):
        anchor.close_view(nome)
        apply_filters()

    def close_anchor2(e, nome):
        anchor2.close_view(nome)
        apply_filters()

    def close_anchor3(e, nome):
        anchor3.close_view(nome)
        apply_filters()

    def handle_change(e):
        lv.controls.clear()
        if e.data:  # Se há texto na SearchBar, filtre a lista de cursos
            for nome in nomes_cursos:
                if e.data.lower() in nome.lower():
                    lv.controls.append(
                        ft.ListTile(
                            title=ft.Text(nome), on_click=lambda e, nome=nome: close_anchor(e, nome), data=nome
                        )
                    )
        else:  # Se não há texto na SearchBar, exiba todos os cursos
            for nome in nomes_cursos:
                lv.controls.append(
                    ft.ListTile(
                        title=ft.Text(nome), on_click=lambda e, nome=nome: close_anchor(e, nome), data=nome
                    )
                )
        lv.update()

    def handle_change2(e):
        lv2.controls.clear()
        if e.data:  # Se há texto na SearchBar, filtre a lista de orientadores
            for nome in nomes_orientadores:
                if e.data.lower() in nome.lower():
                    lv2.controls.append(
                        ft.ListTile(
                            title=ft.Text(nome), on_click=lambda e, nome=nome: close_anchor2(e, nome), data=nome
                        )
                    )
        else:  # Se não há texto na SearchBar, exiba todos os orientadores
            for nome in nomes_orientadores:
                lv2.controls.append(
                    ft.ListTile(
                        title=ft.Text(nome), on_click=lambda e, nome=nome: close_anchor2(e, nome), data=nome
                    )
                )
        lv2.update()
    
    def handle_change3(e):
        lv3.controls.clear()
        if e.data:
            for nome in nome_alunos:
                if e.data.lower() in nome.lower():
                    lv3.controls.append(
                        ft.ListTile(
                            title=ft.Text(nome), on_click=lambda e, nome=nome: close_anchor3(e, nome), data=nome
                        )
                    )
        else:
            for nome in nome_alunos:
                lv3.controls.append(
                    ft.ListTile(
                        title=ft.Text(nome), on_click=lambda e, nome=nome: close_anchor3(e, nome), data=nome
                    )
                )
        lv3.update()

    def apply_filters():
        global dados_relatorio, datatable, datatable_cursos, datatable_orientadores, itens_carregados_lv

        itens_carregados_lv = ITENS_POR_BATCH  # Reinicia a contagem quando os filtros são aplicados

        curso_filtrado = anchor.value
        orientador_filtrado = anchor2.value
        aluno_filtrado = anchor3.value 
        situacao_selecionada = filtro_situacao.value
        fase_selecionada = dropdown_fases_registro.value
        polo_selecionado = filtro_polo.value
        situacao_fase_selecionada = filtro_situacao_fase.value

        dados_relatorio = db.get_relatorio()

        # Filtragem para "Não definido" na fase da pesquisa
        if fase_selecionada == "Não definido":
            dados_relatorio = [row for row in dados_relatorio if row.cells[7].content.value == "" or row.cells[7].content.value is None]
        else:
            # Aplica os filtros normalmente se a fase selecionada não for "Não definido"
            if curso_filtrado:
                dados_relatorio = [row for row in dados_relatorio if row.cells[1].content.value == curso_filtrado]
            if orientador_filtrado:
                if orientador_filtrado == "A definir":
                    dados_relatorio = [row for row in dados_relatorio if row.cells[2].content.value == "A definir"]
                else:
                    dados_relatorio = [row for row in dados_relatorio if row.cells[2].content.value == orientador_filtrado]
            if aluno_filtrado:
                dados_relatorio = [row for row in dados_relatorio if row.cells[0].content.value == aluno_filtrado] 
            if situacao_selecionada:
                dados_relatorio = [row for row in dados_relatorio if row.cells[6].content.value == situacao_selecionada]
            if fase_selecionada:
                dados_relatorio = [row for row in dados_relatorio if row.cells[7].content.value == fase_selecionada]
            if polo_selecionado:
                dados_relatorio = [row for row in dados_relatorio if row.cells[3].content.value == polo_selecionado]
            if situacao_fase_selecionada:
                dados_relatorio = [row for row in dados_relatorio if row.cells[9].content.value == situacao_fase_selecionada]

        # Ordenar os dados pela data mais recente no campo "Prazo da fase"
        dados_relatorio.sort(key=lambda x: x.cells[8].content.value, reverse=True)

        atualizar_datatable(datatable, dados_relatorio, page)
        page.update()

    def dados_relatorio_geral(e):
        global dados_relatorio, datatable, datatable_cursos, datatable_orientadores, itens_carregados_lv

        itens_carregados_lv = ITENS_POR_BATCH  # Reinicia a contagem

        dados_relatorio = db.get_relatorio()

        # Ordenar os dados pela data mais recente no campo "Prazo da fase"
        dados_relatorio.sort(key=lambda x: x.cells[8].content.value, reverse=True)

        atualizar_datatable(datatable, dados_relatorio, page)

        # Limpa os valores dos filtros
        filtro_situacao.value = None
        dropdown_fases_registro.value = None
        filtro_polo.value = None
        filtro_situacao_fase.value = None
        apply_filters()
        page.update()

    def encontrar_porta_livre():
        """Encontra uma porta livre no sistema."""
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(("", 0))
            return s.getsockname()[1]

    def export_to_excel(e):
        global df  # Acesse a variável df global
        caminho_arquivo = os.path.join("relatorio_geral.xlsx")
        df.to_excel(caminho_arquivo, index=False)

        porta = encontrar_porta_livre()

        def serve_file():
            Handler = http.server.SimpleHTTPRequestHandler
            with socketserver.TCPServer(("", porta), Handler) as httpd:
                print(f"Servidor HTTP iniciado na porta {porta}")
                httpd.serve_forever()

        thread = threading.Thread(target=serve_file)
        thread.daemon = True
        thread.start()

        # Exibir o link de download no front-end
        download_url = f"http://{socket.gethostbyname(socket.gethostname())}:{porta}/{os.path.basename(caminho_arquivo)}"
        e.page.launch_url(download_url)

    columns = [
        ft.DataColumn(ft.Text("Discente", width=150, size=12, weight=ft.FontWeight.BOLD)),
        ft.DataColumn(ft.Text("Curso", width=200, size=12, weight=ft.FontWeight.BOLD)),
        ft.DataColumn(ft.Text("Orientador", width=150, size=12, weight=ft.FontWeight.BOLD)),
        ft.DataColumn(ft.Text("Polo", width=100, size=12, weight=ft.FontWeight.BOLD)),
        ft.DataColumn(ft.Text("IES Promotora", width=100, size=12, weight=ft.FontWeight.BOLD)),
        ft.DataColumn(ft.Text("Ano de Ingresso", width=50, size=12, weight=ft.FontWeight.BOLD)),
        ft.DataColumn(ft.Text("Situação do Aluno", width=100, size=12, weight=ft.FontWeight.BOLD)),
        ft.DataColumn(ft.Text("Fase da pesquisa", width=100, size=12, weight=ft.FontWeight.BOLD)),
        ft.DataColumn(ft.Text("Prazo da fase", width=100, size=12, weight=ft.FontWeight.BOLD)),
        ft.DataColumn(ft.Text("Situação da fase", width=100, size=12, weight=ft.FontWeight.BOLD)),
    ]

    datatable = ft.Container(
        ft.Column(
            controls=[
                ft.Text(f"Exibindo {len(dados_relatorio[:LINHAS_POR_PAGINA])} de {num_alunos} registros", weight=ft.FontWeight.BOLD),
                ft.DataTable(
                    columns=columns,
                    rows=[],
                    border=ft.border.all(2, "black"),
                    border_radius=ft.border_radius.all(10),
                    width=1700,
                    horizontal_margin=10,
                    data_row_max_height=90,
                    column_spacing=20,
                    vertical_lines=ft.border.BorderSide(0.2, "black"),
                    bgcolor="WHITE",
                ),
                ft.Text(f"Página {pagina_atual} de {calcular_total_paginas(len(dados_relatorio))} registros", weight=ft.FontWeight.BOLD),
            ]
        ),
        margin=1,
        padding=10,
        width=1700,
        visible=True,
    )

    datatable_cursos = ft.Container(
        ft.Column(
            controls=[
                ft.Text("Quantidade de registros: ", weight=ft.FontWeight.BOLD),
                ft.DataTable(
                    columns=columns,
                    rows=[],
                    border=ft.border.all(2, "black"),
                    border_radius=ft.border_radius.all(10),
                    width=1700,
                    horizontal_margin=10,
                    data_row_max_height=90,
                    column_spacing=20,
                    vertical_lines=ft.border.BorderSide(0.2, "black"),
                    bgcolor="WHITE",
                ),
                ft.Text(f"Página {pagina_atual} de {calcular_total_paginas(len(dados_relatorio_curso))}", weight=ft.FontWeight.BOLD),
            ]
        ),
        margin=1,
        padding=10,
        width=1700,
        visible=False,
    )

    datatable_orientadores = ft.Container(
        ft.Column(
            controls=[
                ft.Text("Quantidade de registros: ", weight=ft.FontWeight.BOLD),
                ft.DataTable(
                    columns=columns,
                    rows=[],
                    border=ft.border.all(2, "black"),
                    border_radius=ft.border_radius.all(10),
                    width=1700,
                    horizontal_margin=10,
                    data_row_max_height=90,
                    column_spacing=20,
                    vertical_lines=ft.border.BorderSide(0.2, "black"),
                    bgcolor="WHITE",
                ),
                ft.Text(f"Página {pagina_atual} de {calcular_total_paginas(len(dados_relatorio_orientador))}", weight=ft.FontWeight.BOLD),
            ]
        ),
        margin=1,
        padding=10,
        width=1700,
        visible=False,
    )

    anchor = ft.SearchBar(
        width=400,
        view_elevation=4,
        divider_color=ft.colors.AMBER,
        bar_hint_text="Buscar por curso",
        view_hint_text="Escolha um curso",
        on_change=handle_change,
        on_submit=lambda e: close_anchor(e, e.control.data),
        controls=[lv],
    )

    anchor2 = ft.SearchBar(
        width=400,
        view_elevation=4,
        divider_color=ft.colors.AMBER,
        bar_hint_text="Buscar orientador",
        view_hint_text="Selecione um nome",
        on_change=handle_change2,
        on_submit=lambda e: close_anchor2(e, e.control.data),
        controls=[lv2],
    )

    anchor3 = ft.SearchBar(
        width=400,
        view_elevation=4,
        divider_color=ft.colors.AMBER,
        bar_hint_text="Buscar discente",
        view_hint_text="Selecione um nome",
        on_change=handle_change3,
        on_submit=lambda e: close_anchor3(e, e.control.data),
        controls=[lv3],
    )


    filtro_situacao = ft.Dropdown(
        width=200,
        label="Situação do aluno",
        padding=10,
        options=[
            ft.dropdown.Option("Cursando"),
            ft.dropdown.Option("Concluído"),
            ft.dropdown.Option("Desistente"),
            ft.dropdown.Option("Reprovado"),
            ft.dropdown.Option("Outros"),
            ft.dropdown.Option("Não informado"),
        ],
        on_change=lambda e: apply_filters(),
        bgcolor="WHITE"
    )

    dropdown_fases_registro = ft.Dropdown(
        width=300,
        label="Fase da pesquisa",
        value="Não definido",
        padding=10,
        options=[
            ft.dropdown.Option("01 - Definição de Orientador"),
            ft.dropdown.Option("02 - Escolha do Tema"),
            ft.dropdown.Option("03 - Elaboração do projeto de Pesquisa"),
            ft.dropdown.Option("04 - Encaminhamento do projeto ao CEP"),
            ft.dropdown.Option("05 - Aprovação do CEP"),
            ft.dropdown.Option("06 - Coleta de Dados ou Materiais"),
            ft.dropdown.Option("07 - Análise de Resultados"),
            ft.dropdown.Option("08 - Escrita do TCC"),
            ft.dropdown.Option("09 - Submissão do TCC para defesa"),
            ft.dropdown.Option("10 - Qualificação"),
            ft.dropdown.Option("11 - Data da Defesa"),
            ft.dropdown.Option("12 - Adequação do TCC"),
            ft.dropdown.Option("13 - TCC finalizado e enviada a biblioteca"),
            ft.dropdown.Option("14 - Certificado"),
            ft.dropdown.Option("Não definido"),
            ft.dropdown.Option("Desistente"),
            ft.dropdown.Option("Reprovado"),
            ft.dropdown.Option("Outras situações"),
        ],
        on_change=lambda e: apply_filters(),
        bgcolor="WHITE"
    )

    filtro_polo = ft.Dropdown(
        width=200,
        label="Polo",
        padding=10,
        options=[
            ft.dropdown.Option("Porto Velho"),
            ft.dropdown.Option("Cacoal"),
            ft.dropdown.Option("N/A"),
        ],
        on_change=lambda e: apply_filters(),
        bgcolor="WHITE"
    )

    filtro_situacao_fase = ft.Dropdown(
        width=200,
        label="Situação da fase",
        padding=10,
        options=[
            ft.dropdown.Option("Em andamento"),
            ft.dropdown.Option("Suspenso"),
            ft.dropdown.Option("Concluído"),
            ft.dropdown.Option("Outras Situações"),
        ],
        on_change=lambda e: apply_filters(),
        bgcolor="WHITE"
    )

    botao_todos = ft.Container(
        ft.Row(
            controls=[
                ft.ElevatedButton(
                    text="Ver todos",
                    width=200,
                    height=40,
                    elevation=4,
                    bgcolor="#006BA0",
                    style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
                    color="WHITE",
                    on_click=dados_relatorio_geral,
                )
            ],
            alignment="center",  # Centraliza o botão no Row
        ),
        col={"sm": 2},  # Valor inicial para telas pequenas
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

    container_botoes_nav = ft.Container(
        ft.Row(
            controls=[
                botao_anterior,
                botao_proximo,
            ]
        )
    )

    botao_exportar = ft.Container(
        ft.Row(
            controls=[
                ft.ElevatedButton(
                    text="Exportar",
                    width=200,
                    height=40,
                    elevation=4,
                    bgcolor="#006BA0",
                    style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
                    color="WHITE",
                    on_click=export_to_excel,
                )
            ],
            alignment="center",  # Centraliza o botão no Row
        ),
        col={"sm": 2},  # Valor inicial para telas pequenas
    )

    botao_carregar_mais = ft.Container(
        ft.Row(
            controls=[
                ft.ElevatedButton(
                    text="Carregar Mais",
                    width=200,
                    height=40,
                    elevation=4,
                    bgcolor="#006BA0",
                    style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
                    color="WHITE",
                    on_click=lambda e: carregar_mais_itens_lv(e.page),  # Chama a função para carregar mais itens
                )
            ],
            alignment="center",
        ),
        col={"sm": 2},
        visible=False,  # Inicialmente invisível
    )

    def resize_relatorio(page, width, datatable, datatable_cursos, datatable_orientadores, anchor, anchor2, anchor3,filtro_situacao, dropdown_fases_registro, filtro_polo, filtro_situacao_fase, container_listview, botao_carregar_mais):
        global itens_carregados_lv
        if width < 1024:
            # Oculta filtros e datatable
            datatable.visible = False
            datatable_cursos.visible = False
            datatable_orientadores.visible = False
            anchor.visible = False
            anchor2.visible = False
            anchor3.visible = False
            filtro_situacao.visible = False
            dropdown_fases_registro.visible = False
            filtro_polo.visible = False
            filtro_situacao_fase.visible = False

            # Mostra o botão exportar e carregar mais
            botao_todos.visible = False
            container_botoes_nav.visible = False
            botao_carregar_mais.visible = True

            # Mostra a ListView responsiva
            container_listview.visible = True

            # Reinicia a contagem de itens carregados
            itens_carregados_lv = ITENS_POR_BATCH

            page.update()
        else:
            # Mostra filtros e datatable
            datatable.visible = True
            anchor.visible = True
            anchor2.visible = True
            anchor3.visible = True
            filtro_situacao.visible = True
            dropdown_fases_registro.visible = True
            filtro_polo.visible = True
            filtro_situacao_fase.visible = True

            # Oculta o botão exportar e carregar mais
            botao_todos.visible = True
            container_botoes_nav.visible = True
            botao_carregar_mais.visible = False

            # Oculta a ListView responsiva
            container_listview.visible = False

            # Reinicia a contagem de itens carregados
            itens_carregados_lv = ITENS_POR_BATCH

            page.update()

    def atualizar_datatable(datatable, dados, page):
        global pagina_atual

        datatable.content.controls[1].rows = [
            ft.DataRow(
                cells=[
                    ft.DataCell(
                        ft.Text(row.cells[0].content.value),
                        on_tap=lambda e, nome=row.cells[0].content.value: abrir_tela_aluno(e, nome, page, container_relatorios),
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
            for row in dados[:LINHAS_POR_PAGINA]
        ]
        datatable.content.controls[0].value = f"Exibindo {len(dados[:LINHAS_POR_PAGINA])} de {len(dados)} registros"
        datatable.content.controls[2].value = f"Página {pagina_atual} de {calcular_total_paginas(len(dados))}"

        datatable_cursos.visible = False
        datatable_orientadores.visible = False
        datatable.visible = True
        exibir_pagina(1, page, container_relatorios)
        page.update()

    nome_campo = ft.Text("RELATÓRIOS", size=16, color="#006BA0", font_family="Roboto", weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER)

    container_relatorios = ft.Container(
        expand=True,
        padding=1,
        content=ft.Container(
            content=ft.ResponsiveRow(
                vertical_alignment=ft.CrossAxisAlignment.START,
                alignment=ft.MainAxisAlignment.START,
                controls=[
                    ft.Column(
                        scroll=ft.ScrollMode.ALWAYS,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        controls=[
                            nome_campo,
                            ft.Divider(),
                            # Primeira linha
                            ft.ResponsiveRow(
                                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                                controls=[
                                    ft.Container(content=anchor, col={"sm": 2}),  # Ajuste para 2 colunas
                                    ft.Container(content=anchor2, col={"sm": 2}),  # Ajuste para 2 colunas
                                    ft.Container(content=anchor3, col={"sm": 2}),  # Ajuste para 2 colunas
                                    ft.Container(content=botao_exportar, col={"sm": 2}),  # Ajuste para 2 colunas
                                    ft.Container(content=botao_todos, col={"sm": 2}),  # Ajuste para 2 colunas
                                    ft.Container(content=container_botoes_nav, col={"sm": 2}),
                                    
                                ],
                            ),
                            # Segunda linha
                            ft.ResponsiveRow(
                                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                                controls=[
                                    ft.Container(content=filtro_polo, col={"sm": 3}),
                                    ft.Container(content=filtro_situacao, col={"sm": 3}),
                                    ft.Container(content=dropdown_fases_registro, col={"sm": 3}),
                                    ft.Container(content=filtro_situacao_fase, col={"sm": 3}),

                                ],
                            ),
                            ft.Divider(),
                            # Datatables
                            ft.Container(content=datatable, col={"sm": 12}),
                            ft.Container(content=datatable_orientadores, col={"sm": 12}),
                            ft.Container(content=datatable_cursos, col={"sm": 12}),
                            botao_carregar_mais, # Botão para carregar mais itens
                            container_listview,  # Container da ListView responsiva
                        ],
                    )
                ],
            ),
            margin=ft.margin.only(bottom=20),
        ),
    )

    # Ordenar os dados pela data mais recente no campo "Prazo da fase"
    dados_relatorio.sort(key=lambda x: x.cells[8].content.value, reverse=True)

    atualizar_datatable(datatable, dados_relatorio, page)

    page.on_resize = lambda e: resize_relatorio(
        page,
        e.control.width,
        datatable,
        datatable_cursos,
        datatable_orientadores,
        anchor,
        anchor2,
        anchor3,
        filtro_situacao,
        dropdown_fases_registro,
        filtro_polo,
        filtro_situacao_fase,
        container_listview,
        botao_carregar_mais,
    )

    exibir_pagina(1, page, container_relatorios)

    if page.width < 1024:
        # Oculta filtros e datatable
        datatable.visible = False
        datatable_cursos.visible = False
        datatable_orientadores.visible = False
        anchor.visible = False
        anchor2.visible = False
        anchor3.visible = False
        filtro_situacao.visible = False
        dropdown_fases_registro.visible = False
        filtro_polo.visible = False
        filtro_situacao_fase.visible = False
        # Mostra o botão exportar e carregar mais
        botao_todos.visible = False
        container_botoes_nav.visible = False
        botao_carregar_mais.visible = True
        # Mostra a ListView responsiva
        container_listview.visible = True
        # Reinicia a contagem de itens carregados
        itens_carregados_lv = ITENS_POR_BATCH
        page.update()

    # Chama a função apply_filters() para aplicar o filtro da fase inicial
    apply_filters()  

    dropdown_fases_registro.value = None

    page.update()

    return container_relatorios