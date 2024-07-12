import flet as ft  # Importa a biblioteca Flet para a criação da interface
from database import Database  # Importa a classe Database para interagir com o banco de dados
from profile import tela_profile  # Importa a função tela_profile do módulo profile.py
from datetime import date, timedelta  # Importa as classes date e timedelta do módulo datetime
import datetime  # Importa o módulo datetime

# Inicializa a conexão com o banco de dados
db = Database()
df = db.get_relatorio_geral()  # Obtém o DataFrame com os dados do relatório geral

# Parâmetros de paginação para o DataTable
LINHAS_POR_PAGINA = 25  # Número de linhas a serem exibidas por página
pagina_atual = 1  # Página atual, inicia na página 1

# Parâmetros de carregamento para a ListView responsiva
ITENS_POR_BATCH = 10  # Número de itens a serem carregados por vez na ListView
carregando = False  # Variável para controlar o carregamento, inicialmente definido como False
itens_carregados_lv = 0  # Variável global para rastrear quantos itens foram carregados na ListView, inicialmente definido como 0

# Função para calcular o total de páginas do DataTable
def calcular_total_paginas(total_registros):
    """Calcula o total de páginas do DataTable com base no número total de registros."""
    return (total_registros + LINHAS_POR_PAGINA - 1) // LINHAS_POR_PAGINA

# Função para exibir a página atual do DataTable
def exibir_pagina(pagina, page, conteudo_container):
    """Exibe a página atual do DataTable."""
    global pagina_atual, datatable, botao_anterior, botao_proximo  # Acessa as variáveis globais

    pagina_atual = pagina  # Define a página atual
    inicio = (pagina - 1) * LINHAS_POR_PAGINA  # Calcula o índice inicial dos dados da página atual
    fim = inicio + LINHAS_POR_PAGINA  # Calcula o índice final dos dados da página atual

    fonte_paginacao = ft.FontWeight.BOLD  # Define o peso da fonte para os textos de paginação

    # Obtém os dados da página atual do relatório
    dados_pagina = dados_relatorio[inicio:fim]

    # Define a função para criar as linhas do DataTable
    def criar_linhas(dados):
        """Cria as linhas do DataTable com base nos dados fornecidos."""
        return [
            ft.DataRow(
                cells=[
                    ft.DataCell(  # Célula com o nome do aluno, clicável para abrir a tela de perfil do aluno
                        ft.Text(row.cells[0].content.value),  # Texto com o nome do aluno
                        on_tap=lambda e, nome=row.cells[0].content.value: abrir_tela_aluno(
                            e, nome, page, conteudo_container
                        ),  # Define a função a ser chamada quando a célula for clicada
                    ),
                    ft.DataCell(ft.Text(row.cells[1].content.value)),  # Célula com o curso do aluno
                    ft.DataCell(ft.Text(row.cells[2].content.value)),  # Célula com o polo do aluno
                    ft.DataCell(ft.Text(row.cells[3].content.value)),  # Célula com a instituição promotora do aluno
                    ft.DataCell(ft.Text(row.cells[4].content.value)),  # Célula com o ano de ingresso do aluno
                    ft.DataCell(ft.Text(row.cells[5].content.value)),  # Célula com o ano de conclusão do aluno
                    ft.DataCell(ft.Text(row.cells[6].content.value)),  # Célula com a situação do aluno
                    ft.DataCell(ft.Text(row.cells[7].content.value)),  # Célula com a fase da pesquisa do aluno
                    ft.DataCell(ft.Text(row.cells[8].content.value)),  # Célula com o prazo da fase da pesquisa do aluno
                    ft.DataCell(ft.Text(row.cells[9].content.value)),  # Célula com a situação da fase da pesquisa do aluno
                ]
            )
            for row in dados  # Itera sobre os dados da página atual do relatório
        ]

    # Limpa as linhas existentes do DataTable e adiciona as novas linhas
    datatable.content.controls[1].rows.clear()
    datatable.content.controls[1].rows = criar_linhas(dados_pagina)

    # Atualiza os textos de paginação do DataTable
    datatable.content.controls[0].value = f"Exibindo {len(datatable.content.controls[1].rows)} de {len(dados_relatorio)} registros"
    datatable.content.controls[2].value = f"Página {pagina_atual} de {calcular_total_paginas(len(dados_relatorio))}"
    datatable.content.controls[0].weight = fonte_paginacao
    datatable.content.controls[2].weight = fonte_paginacao

    # Habilita ou desabilita os botões de paginação de acordo com a página atual
    botao_anterior.disabled = pagina == 1
    botao_proximo.disabled = fim >= len(dados_relatorio)

    # Atualiza os widgets na tela
    datatable.update()
    botao_anterior.update()
    botao_proximo.update()

# Função para abrir a tela de perfil do aluno
def abrir_tela_aluno(e, nome_aluno, page, conteudo_container):
    """Abre a tela de perfil do aluno dentro do container especificado."""
    conteudo_container.content = tela_profile(
        page, nome_aluno
    )  # Define o conteúdo do container como a tela de perfil do aluno
    conteudo_container.update()  # Atualiza o container na tela

# Função para criar a ListView responsiva para exibir os dados do relatório
def criar_relatorio_listview(db, page, orientador):
    """Cria a ListView responsiva para exibir os dados do relatório."""
    global itens_carregados_lv, container_listview, lv_responsivo  # Acessa as variáveis globais

    # Cria a ListView responsiva
    lv_responsivo = ft.ListView(
        expand=True,  # Permite que a ListView se expanda para preencher o espaço disponível
        spacing=10,  # Define o espaçamento entre os itens da ListView
        item_extent=100,  # Define a altura de cada item da ListView
        first_item_prototype=True,  # Define o primeiro item como protótipo para melhorar o desempenho
        on_scroll=lambda e: carregar_mais_itens_lv_scroll(
            e, orientador
        ),  # Define a função a ser chamada quando o usuário rolar a ListView
    )

    # Cria o container para o texto de total de registros e a ListView responsiva
    container_listview = ft.Container(
        content=ft.Column(  # Define o conteúdo do container como uma coluna
            controls=[
                ft.Text(  # Texto com o total de registros
                    f"Total de registros: {len(db.get_orientador_relatorio_lista(orientador))}"
                ),
                lv_responsivo,  # ListView responsiva
            ],
            spacing=10  # Define o espaçamento entre os elementos da coluna
        ),
        expand=True,  # Permite que o container se expanda para preencher o espaço disponível
        padding=10  # Define o espaçamento interno do container
    )

    # Retorna o container
    return container_listview

# Função para carregar mais itens na ListView responsiva
def carregar_mais_itens_lv(page, orientador, inicial=False):
    """Carrega mais itens na ListView responsiva."""
    global itens_carregados_lv, carregando  # Acessa as variáveis globais

    # Se já estiver carregando itens, retorna
    if carregando:
        return

    # Define a variável 'carregando' como True para impedir chamadas concorrentes
    carregando = True

    # Obtém os dados dos alunos do relatório do orientador logado
    dados_alunos = db.get_orientador_relatorio_lista(orientador)

    # Obtém o número total de registros
    total_registros = len(dados_alunos)

    # Se ainda houver itens para carregar
    if itens_carregados_lv < total_registros:
        # Calcula o número de itens a serem carregados neste batch
        proximos_itens = min(ITENS_POR_BATCH, total_registros - itens_carregados_lv)

        # Adiciona os próximos itens à ListView responsiva
        for i in range(itens_carregados_lv, itens_carregados_lv + proximos_itens):
            aluno = dados_alunos[i]  # Obtém as informações do aluno
            container_aluno = criar_container_aluno(
                aluno
            )  # Cria um container com as informações do aluno
            lv_responsivo.controls.append(
                container_aluno
            )  # Adiciona o container do aluno à ListView

        # Incrementa o número de itens carregados
        itens_carregados_lv += proximos_itens

        # Exibe o diálogo de progresso apenas se não for o carregamento inicial
        if not inicial:
            # Define a função para fechar o diálogo
            def fechar_dialogo(e):
                """Fecha o diálogo de progresso."""
                dlg.open = False
                page.update()

            # Cria o diálogo de progresso
            dlg = ft.AlertDialog(
                modal=True,  # Define o diálogo como modal
                title=ft.Text("Carregamento"),  # Define o título do diálogo
                content=ft.Text(  # Define o conteúdo do diálogo com o progresso do carregamento
                    f"Carregados {itens_carregados_lv} de {total_registros} registros."
                ),
                actions=[ft.TextButton("OK", on_click=fechar_dialogo)],  # Define o botão "OK" para fechar o diálogo
            )
            page.dialog = dlg  # Define o diálogo na página
            dlg.open = True  # Abre o diálogo
            page.update()  # Atualiza a página

    # Define a variável 'carregando' como False para permitir o próximo carregamento
    carregando = False

# Função para carregar mais itens na ListView responsiva quando o usuário rolar a tela
def carregar_mais_itens_lv_scroll(e, orientador):
    """Carrega mais itens na ListView responsiva quando o usuário rolar a tela."""
    global lv_responsivo  # Acessa a variável global lv_responsivo

    # Verifica se o usuário rolou até o final da lista
    if (
        e.scroll_offset + e.control.viewport_size.height
        >= e.control.content_size.height
    ):
        carregar_mais_itens_lv(
            e.page, orientador
        )  # Chama a função para carregar mais itens

# Função para criar um container com as informações do aluno
def criar_container_aluno(aluno):
    """Cria um container para exibir os dados de um aluno."""
    return ft.Container(
        content=ft.Column(  # Define o conteúdo do container como uma coluna
            [
                ft.Text(  # Texto "Discente" em negrito
                    "Discente", font_family="Roboto", weight=ft.FontWeight.BOLD
                ),
                ft.Text(aluno[0]),  # Nome do aluno
                ft.Text(  # Texto "Curso" em negrito
                    "Curso", font_family="Roboto", weight=ft.FontWeight.BOLD
                ),
                ft.Text(aluno[1]),  # Curso do aluno
                ft.Text(  # Texto "Polo" em negrito
                    "Polo", font_family="Roboto", weight=ft.FontWeight.BOLD
                ),
                ft.Text(aluno[2]),  # Polo do aluno
                ft.Text(  # Texto "IES Promotora" em negrito
                    "IES Promotora", font_family="Roboto", weight=ft.FontWeight.BOLD
                ),
                ft.Text(aluno[3]),  # IES promotora do aluno
                ft.Text(  # Texto "Ano de Ingresso" em negrito
                    "Ano de Ingresso", font_family="Roboto", weight=ft.FontWeight.BOLD
                ),
                ft.Text(aluno[4]),  # Ano de ingresso do aluno
                ft.Text(  # Texto "Situação" em negrito
                    "Situação", font_family="Roboto", weight=ft.FontWeight.BOLD
                ),
                ft.Text(aluno[5]),  # Situação do aluno
                ft.Text(  # Texto "Fase da pesquisa" em negrito
                    "Fase da pesquisa", font_family="Roboto", weight=ft.FontWeight.BOLD
                ),
                ft.Text(aluno[6]),  # Fase da pesquisa do aluno
                ft.Text(  # Texto "Prazo da fase" em negrito
                    "Prazo da fase", font_family="Roboto", weight=ft.FontWeight.BOLD
                ),
                ft.Text(aluno[7]),  # Prazo da fase da pesquisa do aluno
                ft.Text(  # Texto "Situação da fase" em negrito
                    "Situação da fase", font_family="Roboto", weight=ft.FontWeight.BOLD
                ),
                ft.Text(aluno[8]),  # Situação da fase da pesquisa do aluno
            ],
            spacing=5,  # Define o espaçamento entre os elementos da coluna
        ),
        border=ft.border.all(1),  # Define a borda do container
        padding=10,  # Define o espaçamento interno do container
        border_radius=ft.border_radius.all(10),  # Define o raio de borda do container
        bgcolor="WHITE",  # Define a cor de fundo do container
    )

# Define a função para criar a tela de relatórios do orientador logado
def relatorios_orientador_logado(page: ft.Page, usuario):
    """
    Cria a tela de relatórios para o orientador logado.

    Args:
        page (ft.Page): A página Flet atual.
        usuario (str): O nome de usuário do orientador logado.
    """
    global dados_relatorio, datatable, botao_anterior, botao_proximo, container_listview, itens_carregados_lv  # Acessa as variáveis globais

    # Obtém o nome do orientador a partir do usuário logado
    orientador = db.get_orientador_info_por_usuario(usuario)['nome']

    # Obtém os dados do relatório do orientador logado
    dados_relatorio = db.get_orientador_relatorio(orientador)

    # Define as colunas do DataTable
    columns = [
        ft.DataColumn(ft.Text("Discente", width=150, size=12, weight=ft.FontWeight.BOLD)),  # Coluna para o nome do aluno
        ft.DataColumn(ft.Text("Curso", width=200, size=12, weight=ft.FontWeight.BOLD)),  # Coluna para o curso do aluno
        ft.DataColumn(ft.Text("Polo", width=100, size=12, weight=ft.FontWeight.BOLD)),  # Coluna para o polo do aluno
        ft.DataColumn(ft.Text("IES Promotora", width=100, size=12, weight=ft.FontWeight.BOLD)),  # Coluna para a IES promotora do aluno
        ft.DataColumn(ft.Text("Ano de Ingresso", width=100, size=12, weight=ft.FontWeight.BOLD)),  # Coluna para o ano de ingresso do aluno
        ft.DataColumn(ft.Text("Ano de Conclusão", width=100, size=12, weight=ft.FontWeight.BOLD)),  # Coluna para o ano de conclusão do aluno
        ft.DataColumn(ft.Text("Situação", width=100, size=12, weight=ft.FontWeight.BOLD)),  # Coluna para a situação do aluno
        ft.DataColumn(ft.Text("Fase da pesquisa", width=100, size=12, weight=ft.FontWeight.BOLD)),  # Coluna para a fase da pesquisa do aluno
        ft.DataColumn(ft.Text("Prazo da fase", width=100, size=12, weight=ft.FontWeight.BOLD)),  # Coluna para o prazo da fase da pesquisa do aluno
        ft.DataColumn(ft.Text("Situação da fase", width=100, size=12, weight=ft.FontWeight.BOLD)),  # Coluna para a situação da fase da pesquisa do aluno
    ]

    # Cria o container para o DataTable
    datatable = ft.Container(
        ft.Column(
            controls=[
                ft.Text(f"Exibindo 0 de 0 registros", weight=ft.FontWeight.BOLD),  # Texto com o número de registros exibidos, inicialmente 0
                ft.DataTable(
                    columns=columns,  # Define as colunas do DataTable
                    rows=[],  # Inicialmente, a tabela não possui linhas, serão adicionadas dinamicamente
                    border=ft.border.all(2, "black"),  # Define a borda da tabela
                    border_radius=ft.border_radius.all(10),  # Define o raio de borda da tabela
                    width=1700,  # Define a largura da tabela
                    horizontal_margin=10,  # Define a margem horizontal da tabela
                    data_row_max_height=90,  # Define a altura máxima de cada linha da tabela
                    column_spacing=20,  # Define o espaçamento entre as colunas da tabela
                    vertical_lines=ft.border.BorderSide(
                        0.2, "black"
                    ),  # Define as linhas verticais da tabela
                    bgcolor="WHITE"  # Define a cor de fundo da tabela
                ),
                ft.Text(f"Página 0 de 0 registros", weight=ft.FontWeight.BOLD),  # Texto com a paginação, inicialmente 0
            ]
        ),
        margin=1,  # Define a margem do container
        padding=10,  # Define o espaçamento interno do container
        width=1700,  # Define a largura do container
        visible=True,  # O container é inicialmente visível
    )

    # Cria os botões de paginação do DataTable
    botao_anterior = ft.IconButton(
        icon=ft.icons.ARROW_BACK,  # Define o ícone do botão como uma seta para trás
        width=40,  # Define a largura do botão
        height=40,  # Define a altura do botão
        bgcolor=ft.colors.WHITE,  # Define a cor de fundo do botão
        disabled=True,  # O botão é inicialmente desabilitado
        on_click=lambda e: exibir_pagina(  # Define a função a ser chamada quando o botão for clicado
            pagina_atual - 1, page, container_relatorios  # Passa a página anterior, a página atual e o container de relatórios como argumentos
        ),
    )
    botao_proximo = ft.IconButton(
        icon=ft.icons.ARROW_FORWARD,  # Define o ícone do botão como uma seta para frente
        width=40,
        height=40,
        bgcolor=ft.colors.WHITE,
        on_click=lambda e: exibir_pagina(  # Define a função a ser chamada quando o botão for clicado
            pagina_atual + 1, page, container_relatorios  # Passa a página seguinte, a página atual e o container de relatórios como argumentos
        ),
    )

    # Define a função para carregar o relatório
    def carregar_relatorio(e):
        """Carrega o relatório na página 1."""
        exibir_pagina(1, page, container_relatorios)  # Chama a função 'exibir_pagina' para exibir a página 1

    # Cria o botão para carregar o relatório
    botao_carregar = ft.ElevatedButton(
        text="Carregar Relatório",  # Texto do botão
        on_click=carregar_relatorio,  # Define a função 'carregar_relatorio' para ser chamada quando o botão for clicado
        width=200,  # Largura do botão
        height=40,  # Altura do botão
        elevation=4,  # Elevação do botão
        bgcolor="#006BA0",  # Cor de fundo do botão
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),  # Estilo do botão (borda arredondada)
        color="WHITE"  # Cor do texto do botão
    )

    # Cria o botão "Carregar Mais" para a ListView responsiva (inicialmente invisível)
    botao_carregar_mais = ft.ElevatedButton(
        text="Carregar Mais",  # Texto do botão
        width=200,  # Largura do botão
        height=40,  # Altura do botão
        elevation=4,  # Elevação do botão
        bgcolor="#006BA0",  # Cor de fundo do botão
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),  # Estilo do botão (borda arredondada)
        color="WHITE",  # Cor do texto do botão
        on_click=lambda e: carregar_mais_itens_lv(
            e.page, orientador
        ),  # Define a função 'carregar_mais_itens_lv' para ser chamada quando o botão for clicado
        visible=False,  # O botão é inicialmente invisível
    )

    # Cria a ListView responsiva
    container_listview = criar_relatorio_listview(
        db, page, orientador
    )  # Chama a função 'criar_relatorio_listview' para criar a ListView responsiva
    container_listview.visible = False  # O container da ListView é inicialmente oculto

    # Cria o título da tela
    nome_campo = ft.Text(
        "RELATÓRIOS",
        size=16,
        color="#006BA0",
        font_family="Roboto",
        weight=ft.FontWeight.BOLD,  # Define o peso da fonte como negrito
        text_align=ft.TextAlign.CENTER,  # Alinha o texto ao centro
    )

    # Cria o container principal da tela
    container_relatorios = ft.Container(
        expand=True,  # Permite que o container se expanda para preencher o espaço disponível
        padding=1,  # Define o espaçamento interno do container
        content=ft.Container(  # Container externo
            content=ft.ResponsiveRow(
                vertical_alignment=ft.CrossAxisAlignment.START,  # Alinha os elementos verticalmente ao início
                alignment=ft.MainAxisAlignment.START,  # Alinha os elementos horizontalmente ao início
                controls=[
                    ft.Column(
                        scroll=ft.ScrollMode.ALWAYS,  # Habilita a rolagem vertical na coluna
                        controls=[
                            nome_campo,  # Título da tela
                            ft.Divider(),  # Divisor visual
                            ft.ResponsiveRow(  # Linha responsiva para os botões de paginação e carregamento
                                vertical_alignment=ft.CrossAxisAlignment.CENTER,  # Alinha os elementos verticalmente ao centro
                                controls=[
                                    ft.Container(
                                        content=ft.Row(  # Linha com os botões de paginação e carregamento
                                            controls=[
                                                botao_anterior,  # Botão para voltar para a página anterior
                                                botao_proximo,  # Botão para avançar para a próxima página
                                                botao_carregar,  # Botão para carregar o relatório
                                            ]
                                        ),
                                        col={"sm": 12},  # Ocupa toda a largura em telas pequenas
                                    ),
                                ],
                            ),
                            ft.Container(
                                content=datatable, col={"sm": 12}  # Container para o DataTable, ocupa toda a largura em telas pequenas
                            ),
                            ft.Container(
                                content=botao_carregar_mais,
                                col={"sm": 12},  # Container para o botão "Carregar Mais", ocupa toda a largura em telas pequenas
                            ),
                            ft.Container(
                                content=container_listview,
                                col={"sm": 12},  # Container para a ListView responsiva, ocupa toda a largura em telas pequenas
                            ),
                        ],
                    )
                ],
            ),
            margin=ft.margin.only(bottom=20),  # Define a margem inferior do container externo
        ),
    )

    # Define a função para redimensionar o relatório quando a tela for redimensionada
    def resize_relatorio(e):
        """Redimensiona o relatório de acordo com a largura da tela."""
        global itens_carregados_lv  # Acessa a variável global itens_carregados_lv
        width = e.control.width  # Obtém a largura da tela
        total_registros = len(
            db.get_orientador_relatorio_lista(orientador)
        )  # Obtém o número total de registros do relatório

        # Se a largura da tela for menor que 1024 pixels, exibe a ListView responsiva e oculta o DataTable
        if width < 1024:
            datatable.visible = False  # Oculta o DataTable
            botao_anterior.visible = False  # Oculta o botão "Anterior"
            botao_proximo.visible = False  # Oculta o botão "Próximo"
            botao_carregar.visible = False  # Oculta o botão "Carregar Relatório"
            container_listview.visible = True  # Exibe a ListView responsiva
            botao_carregar_mais.visible = (
                total_registros > ITENS_POR_BATCH
            )  # Exibe o botão "Carregar Mais" se houver mais registros do que o número de itens por batch
            # Carrega os itens na ListView responsiva se ainda não foram carregados
            if itens_carregados_lv == 0:
                carregar_mais_itens_lv(
                    page, orientador, inicial=True
                )  # Carrega os primeiros itens na ListView responsiva
            itens_carregados_lv = (
                ITENS_POR_BATCH
            )  # Define o número de itens carregados como o número de itens por batch
            page.update()  # Atualiza a página
        # Se a largura da tela for maior ou igual a 1024 pixels, exibe o DataTable e oculta a ListView responsiva
        else:
            datatable.visible = True  # Exibe o DataTable
            botao_anterior.visible = True  # Exibe o botão "Anterior"
            botao_proximo.visible = True  # Exibe o botão "Próximo"
            botao_carregar.visible = True  # Exibe o botão "Carregar Relatório"
            container_listview.visible = False  # Oculta a ListView responsiva
            botao_carregar_mais.visible = False  # Oculta o botão "Carregar Mais"
            itens_carregados_lv = (
                ITENS_POR_BATCH
            )  # Define o número de itens carregados como o número de itens por batch
            page.update()  # Atualiza a página

    # Define a visibilidade inicial dos elementos de acordo com a largura da tela
    if page.width < 1024:
        datatable.visible = False
        botao_anterior.visible = False
        botao_proximo.visible = False
        botao_carregar.visible = False
        container_listview.visible = True
        botao_carregar_mais.visible = True
        if itens_carregados_lv == 0:
            carregar_mais_itens_lv(page, orientador, inicial=True)
        itens_carregados_lv = ITENS_POR_BATCH
        page.update()
    else:
        datatable.visible = True
        botao_anterior.visible = True
        botao_proximo.visible = True
        botao_carregar.visible = True
        container_listview.visible = False
        botao_carregar_mais.visible = False
        itens_carregados_lv = ITENS_POR_BATCH
        page.update()

    # Define a função 'resize_relatorio' como a função a ser chamada quando a tela for redimensionada
    page.on_resize = resize_relatorio

    # Retorna o container principal da tela
    return container_relatorios
