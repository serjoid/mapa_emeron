import flet as ft
from profile import tela_profile
from database import Database
from datetime import date, timedelta
import datetime

# Conexão com o banco de dados
db = Database()


def tela_prazos(page: ft.Page, usuario, nome_aluno=None, mostrar_botao_voltar=False):
    global dados_tabela_prazos  # Define variável global
    dados_tabela_prazos = []

    nomes_alunos = db.get_aluno()
    if nome_aluno:
        carregar_dados_prazo(nome_aluno)
        anchor.value = nome_aluno

    # Diálogos de Confirmação
    dlg_confirmacao_excluir = ft.AlertDialog(
        modal=True,
        title=ft.Text("Confirmar Exclusão"),
        content=ft.Text("Tem certeza que deseja excluir este prazo?"),
        actions=[
            ft.TextButton("Sim", on_click=lambda e: confirmar_exclusao_prazo(e)),
            ft.TextButton("Não", on_click=lambda e: fechar_dialogo(e)),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )
    dlg_confirmacao_novo = ft.AlertDialog(
        modal=True,
        title=ft.Text("Confirmar Cadastro"),
        content=ft.Text("Tem certeza que deseja cadastrar este novo prazo?"),
        actions=[
            ft.TextButton("Sim", on_click=lambda e: confirmar_salvar_novo_prazo(e)),
            ft.TextButton("Não", on_click=lambda e: fechar_dialogo(e)),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )
    dlg_confirmacao_atualizar = ft.AlertDialog(
        modal=True,
        title=ft.Text("Confirmar Atualização"),
        content=ft.Text("Tem certeza que deseja atualizar este prazo?"),
        actions=[
            ft.TextButton("Sim", on_click=lambda e: confirmar_salvar_prazo(e)),
            ft.TextButton("Não", on_click=lambda e: fechar_dialogo(e)),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )

    def fechar_dialogo(e):
        dlg_confirmacao_excluir.open = False
        dlg_confirmacao_novo.open = False
        dlg_confirmacao_atualizar.open = False
        page.update()

    def handle_change(e):
        lv.controls.clear()
        if e.data:
            for nome in nomes_alunos:
                if e.data.lower() in nome.lower():
                    lv.controls.append(
                        ft.ListTile(title=ft.Text(nome), on_click=close_anchor, data=nome)
                    )
        else:
            for nome in nomes_alunos:
                lv.controls.append(
                    ft.ListTile(title=ft.Text(nome), on_click=close_anchor, data=nome)
                )
        lv.update()

    def close_anchor(e):
        anchor.close_view(e.control.data)
        carregar_dados_prazo(e.control.data)
        anchor.value = e.control.data
        nome_aluno.value = "Nome: "+ f"{db.get_pessoa_info(nome=anchor.value).get('nome', '')}"
        curso.value = "Curso: " +f"{db.get_pessoa_info(nome=anchor.value).get('curso', '')}"
        orientador.value = "Orientador: " +f"{db.get_pessoa_info(nome=anchor.value).get('orientador', '')}"
        tema.value = "Tema: " + f"{db.get_pessoa_info(nome=anchor.value).get('titulo_tcc', '')}"
        container_info_prazos.controls.clear()  # Limpa os controles existentes
        # Faz aparecer o datatable caso a tela seja maior que 1024p de largura:
        if page.width >= 1024:
            tabela_prazos.visible = True
        # Oculta campos de edição e mostra botões padrão
        container_campos.visible = False
        container_dropdown.visible = False
        botao_salvar.visible = False
        botao_salvar_novo.visible = False
        botao_novo.visible = True
        botao_atualizar.visible = True
        container_campos.update()
        container_dropdown.update()
        container_info_prazos.update()
        atualizar_visualizacao_dados(page)
        page.update()

    def carregar_dados_prazo(nome_aluno):
        global dados_tabela_prazos
        dados_tabela_prazos = []  # Limpa os dados da tabela
        pessoa_id = db.get_pessoa_info(nome=nome_aluno).get("id")
        prazos = db.get_prazos_by_pessoa_id(pessoa_id)

        # Ordena a lista de prazos pelo prazo cadastrado,
        # colocando os prazos com 'prazo_fase_pesquisa' vazio no final
        prazos.sort(
            key=lambda prazo: datetime.datetime.strptime(
                prazo["prazo_fase_pesquisa"], "%d/%m/%Y"
            ).date()
            if prazo["prazo_fase_pesquisa"]
            else datetime.date.max
        )

        # Adiciona os prazos aos dados da tabela
        dados_tabela_prazos = prazos
        atualizar_visualizacao_dados(page)

    def excluir_prazo(prazo_id, fase_pesquisa):
        """Exclui um prazo e recarrega os dados da tabela."""
        db.excluir_prazo(prazo_id)
        db.registrar_log(
            usuario, "excluir_prazo", f"Prazo ID: {prazo_id}, Fase: {fase_pesquisa}"
        )  # Registra o log
        carregar_dados_prazo(anchor.value)  # Recarrega os prazos do aluno

    def confirmar_exclusao(e, prazo_id, fase):
        page.dialog = dlg_confirmacao_excluir
        dlg_confirmacao_excluir.open = True
        page.update()
        global prazo_id_excluir, fase_pesquisa  # Acessa as variáveis globais
        prazo_id_excluir = prazo_id
        fase_pesquisa = fase  # Recupera a fase da célula do botão

    def confirmar_exclusao_prazo(e):
        """Exclui o prazo após a confirmação do usuário."""
        global prazo_id_excluir, fase_pesquisa  # Acessa a variável global
        excluir_prazo(
            prazo_id_excluir, fase_pesquisa
        )  # Passa a fase para excluir_prazo
        fechar_dialogo(e)

    def limpar_campos():
        prazo_fase_pesquisa_field.value = ""
        prazo_dias_field.value = ""
        prazo_situacao_field.value = ""
        situacao_fase_pesquisa_dropdown.value = None
        dropdown_fases.value = None
        dropdown_fases_registro.value = None

    def preencher_campos(prazo):
        prazo_fase_pesquisa_field.value = prazo.get("prazo_fase_pesquisa", "")
        prazo_dias_field.value = str(prazo.get("prazo_dias", ""))
        prazo_situacao_field.value = prazo.get("prazo_situacao", "")
        situacao_fase_pesquisa_dropdown.value = prazo.get(
            "situacao_fase_pesquisa", ""
        )

    def novo_prazo(e):
        if not dropdown_fases_registro.options:
            dropdown_fases_registro.options = [
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
                ft.dropdown.Option(
                    "13 - TCC finalizado e enviada a biblioteca"
                ),
                ft.dropdown.Option("14 - Certificado"),
                ft.dropdown.Option("Desistente"),
                ft.dropdown.Option("Reprovado"),
                ft.dropdown.Option("Outras situações"),
            ]
        limpar_campos()
        container_campos.visible = True
        botao_salvar.visible = False
        botao_salvar_novo.visible = True
        botao_novo.visible = False
        botao_atualizar.visible = False
        container_campos.update()
        page.update()

    def salvar_novo_prazo(e):
        page.dialog = dlg_confirmacao_novo
        dlg_confirmacao_novo.open = True
        page.update()

    def confirmar_salvar_novo_prazo(e):
        pessoa_id = db.get_pessoa_info(nome=anchor.value).get("id")
        prazo_data = {
            "id_pessoa": pessoa_id,
            "fase_pesquisa": dropdown_fases_registro.value,
            "prazo_fase_pesquisa": prazo_fase_pesquisa_field.value,
            "prazo_dias": prazo_dias_field.value,
            "prazo_situacao": prazo_situacao_field.value,
            "situacao_fase_pesquisa": situacao_fase_pesquisa_dropdown.value,
        }
        db.inserir_prazo(prazo_data)

        # Registrar todos os campos no log
        campos_log = [
            f"{chave}: {valor}" for chave, valor in prazo_data.items() if chave != "id_pessoa"
        ]
        log_mensagem = f"Prazo incluído para: {anchor.value}, {', '.join(campos_log)}"
        db.registrar_log(usuario, "inserir_prazo", log_mensagem)
        carregar_dados_prazo(anchor.value)
        limpar_campos()
        container_campos.visible = False
        botao_salvar_novo.visible = False
        botao_novo.visible = True
        botao_atualizar.visible = True
        container_campos.update()
        fechar_dialogo(e)

    def salvar_prazo(e):
        page.dialog = dlg_confirmacao_atualizar
        dlg_confirmacao_atualizar.open = True
        page.update()

    def confirmar_salvar_prazo(e):
        fase_selecionada = dropdown_fases.value
        pessoa_id = db.get_pessoa_info(nome=anchor.value).get("id")
        prazos = db.get_prazos_by_pessoa_id(pessoa_id)
        prazo_a_atualizar = next(
        (p for p in prazos if p["fase_pesquisa"] == fase_selecionada), None
        )
        if prazo_a_atualizar:
            prazo_data = {
                "id": prazo_a_atualizar["id"],
                "fase_pesquisa": fase_selecionada,
                "prazo_fase_pesquisa": prazo_fase_pesquisa_field.value,
                "prazo_dias": prazo_dias_field.value,
                "prazo_situacao": prazo_situacao_field.value,
                "situacao_fase_pesquisa": situacao_fase_pesquisa_dropdown.value,
            }
        db.atualizar_prazo(prazo_data)
        # Registrar todos os campos no log
        campos_log = [
            f"{chave}: {valor}" for chave, valor in prazo_data.items() if chave != "id_pessoa"
        ]
        log_mensagem = f"Prazo alterado para: {anchor.value}, {', '.join(campos_log)}"
        db.registrar_log(usuario, "inserir_prazo", log_mensagem)
        carregar_dados_prazo(anchor.value)
        limpar_campos()
        container_campos.visible = False
        botao_salvar_novo.visible = False
        botao_novo.visible = True
        botao_atualizar.visible = True
        container_campos.update()
        fechar_dialogo(e)

    def atualizar_prazo(e):
        pessoa_id = db.get_pessoa_info(nome=anchor.value).get("id")
        prazos = db.get_prazos_by_pessoa_id(pessoa_id)

        if prazos:
            opcoes_fases = [
                ft.dropdown.Option(prazo["fase_pesquisa"]) for prazo in prazos
            ]
            dropdown_fases.options = opcoes_fases
            dropdown_fases.value = None  # Define como None para forçar o usuário a selecionar

            container_campos.visible = False
            container_dropdown.visible = True
            botao_salvar.visible = True
            botao_salvar_novo.visible = False
            botao_novo.visible = False
            botao_atualizar.visible = False

            container_campos.update()
            container_dropdown.update()
            page.update()

        else:
            print("Nenhum prazo encontrado para este aluno.")

    def preencher_campos_edicao(e):
        """Preenche os campos de edição com base na fase selecionada."""
        fase_selecionada = dropdown_fases.value
        pessoa_id = db.get_pessoa_info(nome=anchor.value).get("id")
        prazos = db.get_prazos_by_pessoa_id(pessoa_id)
        prazo_selecionado = next(
            (p for p in prazos if p["fase_pesquisa"] == fase_selecionada), None
        )

        if prazo_selecionado:
            preencher_campos(prazo_selecionado)
            container_campos.visible = True
            page.update()

    def calcular_prazo(e):
        """Calcula a data do prazo e atualiza a situação."""
        if situacao_fase_pesquisa_dropdown.value == "Concluído":
            prazo_dias_field.value = 0
            prazo_fase_pesquisa_field.value = ""
            prazo_situacao_field.value = "Concluído"
            page.update()
        else:
            try:
                # Verifica se o campo está vazio
                if prazo_dias_field.value == "":
                    prazo_fase_pesquisa_field.value = ""
                    page.update()
                    return

                dias = int(prazo_dias_field.value)

                # Verifica se o número de dias é negativo
                if dias < 0:
                    raise ValueError("Número de dias não pode ser negativo.")

                data_atual = date.today()
                data_prazo = data_atual + timedelta(days=dias)
                prazo_fase_pesquisa_field.value = data_prazo.strftime("%d/%m/%Y")
                page.update
            except ValueError:
                prazo_fase_pesquisa_field.value = "Número de dias inválido."
                page.updat
        page.update()

    # --- Criação dos Componentes da Interface ---

    dropdown_fases_registro = ft.Dropdown(
        width=250,
        label="Fase de Pesquisa",
        bgcolor="WHITE",
        options=[],
    )

    lv = ft.ListView()
    nomes_alunos = db.get_aluno()
    for i in range(0, len(nomes_alunos), 25):
        for nome in nomes_alunos[i : i + 25]:
            lv.controls.append(
                ft.ListTile(title=ft.Text(nome), on_click=close_anchor, data=nome)
            )
        page.update()

    anchor = ft.SearchBar(
        view_elevation=4,
        divider_color=ft.colors.AMBER,
        bar_hint_text="Buscar por nome do aluno.",
        view_hint_text="Escolha um aluno.",
        on_change=handle_change,
        controls=[lv],
    )

    nome_aluno = ft.Text("", size=14)
    curso = ft.Text("", size=14)
    orientador = ft.Text("", size=14)
    tema = ft.Text("", size=14)

    # --- Tabelas e ft.Text para os prazos ---

    # Define as colunas da tabela de prazos
    colunas_tabela_prazos = [
        ft.DataColumn(
            ft.Container(ft.Text("Fase de Pesquisa"), alignment=ft.alignment.center)
        ),
        ft.DataColumn(
            ft.Container(ft.Text("Prazo Fase Pesquisa"), alignment=ft.alignment.center)
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
        ft.DataColumn(ft.Container(ft.Text("Ação"), alignment=ft.alignment.center)),
    ]

    # Tabela de prazos - Inicialmente visível em telas grandes
    tabela_prazos = ft.DataTable(
        columns=colunas_tabela_prazos,
        rows=[],
        border=ft.border.all(2, "black"),
        border_radius=ft.border_radius.all(10),
        width=1300,
        bgcolor="WHITE",
        visible=False,  # Inicialmente invisível
    )

    # Container para os ft.Text dos prazos - Inicialmente invisível
    container_info_prazos = ft.Column(
        spacing=5,
        width=1300,
        visible=False,  # Inicialmente invisível
    )

    # --- Containers ---

    # Dropdown para selecionar a fase a ser atualizada
    dropdown_fases = ft.Dropdown(  # Inicializa dropdown_fases aqui
        width=200,
        bgcolor="WHITE",
        label="Selecione a fase para edição",
        options=[],  # Inicialmente vazio, será preenchido em atualizar_prazo
        on_change=preencher_campos_edicao,
    )

    # Container para o dropdown
    container_dropdown = ft.Container(
        content=ft.ResponsiveRow(
            controls=[dropdown_fases],
            alignment=ft.MainAxisAlignment.CENTER,
            width=800,
        ),
        visible=False,  # Inicialmente oculto
    )

    prazo_fase_pesquisa_field = ft.TextField(
        label="Data do prazo - DD/MM/AAAA", width=200, read_only=False, bgcolor="WHITE", max_length=10
    )

    prazo_dias_field = ft.TextField(
        label="Prazo em Dias",
        width=200,
        bgcolor="WHITE",
        on_change=calcular_prazo,
        keyboard_type=ft.KeyboardType.NUMBER,
    )
    prazo_situacao_field = ft.Dropdown(
        label="Situação do Prazo",
        width=800,
        bgcolor="WHITE",
        options=[
            ft.dropdown.Option("Vigente"),
            ft.dropdown.Option("Vencido"),
            ft.dropdown.Option("Concluído"),
            ft.dropdown.Option("Suspenso"),
        ],
    )
    situacao_fase_pesquisa_dropdown = ft.Dropdown(
        label="Situação da Fase",
        width=800,
        bgcolor="WHITE",
        on_change=calcular_prazo,
        options=[
            ft.dropdown.Option("Em andamento"),
            ft.dropdown.Option("Suspenso"),
            ft.dropdown.Option("Concluído"),
            ft.dropdown.Option("Outras Situações"),
        ],
    )

    container_campos = ft.Container(
        content=ft.ResponsiveRow(
            controls=[
                dropdown_fases_registro,
                situacao_fase_pesquisa_dropdown,
                prazo_dias_field,
                prazo_fase_pesquisa_field,
                prazo_situacao_field,  # Dropdown com as opções de situação do prazo
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        ),
        visible=False,
        width=1300,
    )

    # --- Criação dos Botões ---

    botao_novo = ft.ElevatedButton(
        text="Novo",
        width=800,
        height=40,
        elevation=4,
        bgcolor="#006BA0",
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
        color="WHITE",
        on_click=novo_prazo,
        visible=False,
    )
    botao_atualizar = ft.ElevatedButton(
        text="Atualizar",
        width=800,
        height=40,
        elevation=4,
        bgcolor="#006BA0",
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
        color="WHITE",
        on_click=atualizar_prazo,
        visible=False,
    )
    botao_salvar_novo = ft.ElevatedButton(
        text="Salvar Novo",
        width=800,
        height=40,
        elevation=4,
        bgcolor="#006BA0",
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
        color="WHITE",
        on_click=salvar_novo_prazo,
        visible=False,
    )  # botão para salvar um novo registro
    botao_salvar = ft.ElevatedButton(
        text="Salvar",
        width=800,
        height=40,
        elevation=4,
        bgcolor="#006BA0",
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
        color="WHITE",
        on_click=salvar_prazo,
        visible=False,
    )  # botão para salvar a alteração

    # Container para os botões
    container_botoes = ft.Container(
        width=1300,
        content=ft.ResponsiveRow(
            controls=[botao_novo, botao_atualizar, botao_salvar, botao_salvar_novo],
            alignment=ft.MainAxisAlignment.CENTER,
        ),
    )

    # --- Criação do Container Principal ---

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
            scroll=ft.ScrollMode.ALWAYS,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                nome_campo,
                ft.Divider(),
                anchor,
                ft.Column(
                    controls=[
                        nome_aluno,
                        curso,
                        orientador,
                        tema,
                    ]
                ),
                ft.ResponsiveRow(controls=[container_botoes], width=800),
                container_dropdown,
                tabela_prazos,  # Container para a tabela
                container_info_prazos, # Container para os ft.Text dos prazos
                container_campos,
            ],
        ),
    )

    # --- Funções para atualizar a visualização ---

    # Função para atualizar a visualização dos dados (tabela ou lista)
    def atualizar_visualizacao_dados(page):
        global dados_tabela_prazos

        if page.width < 1024 and anchor.value is not None:
            container_info_prazos.controls.clear()  # Limpa os controles existentes
            nome_aluno.size = 12
            curso.size = 12
            orientador.size = 12
            tema.size = 12
            for prazo in dados_tabela_prazos:
                # Calcula o tempo restante
                prazo_fase_pesquisa_date = (
                    datetime.datetime.strptime(
                        prazo["prazo_fase_pesquisa"], "%d/%m/%Y"
                    ).date()
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

                # Adiciona ft.Text para cada informação do prazo
                container_info_prazos.controls.append(
                    ft.Text(f"Fase de Pesquisa: {prazo['fase_pesquisa']}", size=12)
                )
                container_info_prazos.controls.append(
                    ft.Text(f"Data do Prazo: {prazo['prazo_fase_pesquisa']}", size=12)
                )
                container_info_prazos.controls.append(
                    ft.Text(f"Prazo em Dias: {prazo['prazo_dias']}", size=12)
                )
                container_info_prazos.controls.append(
                    ft.Text(f"Situação do Prazo: {prazo['prazo_situacao']}", size=12)
                )
                container_info_prazos.controls.append(
                    ft.Text(
                        f"Situação da Fase: {prazo['situacao_fase_pesquisa']}", size=12
                    )
                )
                container_info_prazos.controls.append(
                    ft.Text(f"Tempo Restante (dias): {tempo_restante}", size=12)
                )

                # Botão Excluir dentro do container_info_prazos
                container_info_prazos.controls.append(
                    ft.TextButton(
                        "Excluir",
                        on_click=lambda e, prazo_id=prazo[
                            "id"
                        ], fase=prazo[
                            "fase_pesquisa"
                        ]: confirmar_exclusao(
                            e, prazo_id, fase
                        ),
                        data=prazo["fase_pesquisa"],
                    )
                )

                container_info_prazos.controls.append(
                    ft.Divider()
                )  # Adiciona um divisor após cada prazo

            # Oculta a tabela e exibe os ft.Text dos prazos
            tabela_prazos.visible = False
            container_info_prazos.visible = True
        else:
            tabela_prazos.rows.clear()
            nome_aluno.size = 14
            curso.size = 14
            orientador.size = 14
            tema.size = 14
            if anchor.value is not None:
                for prazo in dados_tabela_prazos:
                    # Calcula o tempo restante
                    prazo_fase_pesquisa_date = (
                        datetime.datetime.strptime(
                            prazo["prazo_fase_pesquisa"], "%d/%m/%Y"
                        ).date()
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

                    excluir_cell = ft.DataCell(
                        ft.TextButton(
                            "Excluir",
                            on_click=lambda e, prazo_id=prazo[
                                "id"
                            ], fase=prazo[
                                "fase_pesquisa"
                            ]: confirmar_exclusao(
                                e, prazo_id, fase
                            ),
                            data=prazo["fase_pesquisa"],
                        )
                    )

                    tempo_restante_cell = ft.DataCell(
                        ft.Text(str(tempo_restante))
                    )

                    tabela_prazos.rows.append(
                        ft.DataRow(
                            cells=[
                                ft.DataCell(ft.Text(prazo["fase_pesquisa"])),
                                ft.DataCell(
                                    ft.Text(prazo["prazo_fase_pesquisa"])
                                ),
                                ft.DataCell(ft.Text(str(prazo["prazo_dias"]))),
                                ft.DataCell(ft.Text(prazo["prazo_situacao"])),
                                ft.DataCell(
                                    ft.Text(prazo["situacao_fase_pesquisa"])
                                ),
                                tempo_restante_cell,
                                excluir_cell,
                            ]
                        )
                    )
            # Exibe a tabela e oculta os ft.Text dos prazos
            tabela_prazos.visible = True
            container_info_prazos.visible = False

        page.update()

    if page.width < 1024 and anchor.value is not None:
        container_info_prazos.controls.clear()  # Limpa os controles existentes
        nome_aluno.size = 12
        curso.size = 12
        orientador.size = 12
        tema.size = 12
        for prazo in dados_tabela_prazos:
            # Calcula o tempo restante
            prazo_fase_pesquisa_date = (
                datetime.datetime.strptime(
                    prazo["prazo_fase_pesquisa"], "%d/%m/%Y"
                ).date()
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

            # Adiciona ft.Text para cada informação do prazo
            container_info_prazos.controls.append(
                ft.Text(f"Fase de Pesquisa: {prazo['fase_pesquisa']}", size=12)
            )
            container_info_prazos.controls.append(
                ft.Text(f"Data do Prazo: {prazo['prazo_fase_pesquisa']}", size=12)
            )
            container_info_prazos.controls.append(
                ft.Text(f"Prazo em Dias: {prazo['prazo_dias']}", size=12)
            )
            container_info_prazos.controls.append(
                ft.Text(f"Situação do Prazo: {prazo['prazo_situacao']}", size=12)
            )
            container_info_prazos.controls.append(
                ft.Text(
                    f"Situação da Fase: {prazo['situacao_fase_pesquisa']}", size=12
                )
            )
            container_info_prazos.controls.append(
                ft.Text(f"Tempo Restante (dias): {tempo_restante}", size=12)
            )

            # Botão Excluir dentro do container_info_prazos
            container_info_prazos.controls.append(
                ft.TextButton(
                    "Excluir",
                    on_click=lambda e, prazo_id=prazo[
                        "id"
                    ], fase=prazo[
                        "fase_pesquisa"
                    ]: confirmar_exclusao(
                        e, prazo_id, fase
                    ),
                    data=prazo["fase_pesquisa"],
                )
            )

            container_info_prazos.controls.append(
                ft.Divider()
            )  # Adiciona um divisor após cada prazo

        # Oculta a tabela e exibe os ft.Text dos prazos
        tabela_prazos.visible = False
        container_info_prazos.visible = True
    else:
        tabela_prazos.rows.clear()
        nome_aluno.size = 14
        curso.size = 14
        orientador.size = 14
        tema.size = 14
        if anchor.value is not None:
            for prazo in dados_tabela_prazos:
                # Calcula o tempo restante
                prazo_fase_pesquisa_date = (
                    datetime.datetime.strptime(
                        prazo["prazo_fase_pesquisa"], "%d/%m/%Y"
                    ).date()
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

                excluir_cell = ft.DataCell(
                    ft.TextButton(
                        "Excluir",
                        on_click=lambda e, prazo_id=prazo[
                            "id"
                        ], fase=prazo[
                            "fase_pesquisa"
                        ]: confirmar_exclusao(
                            e, prazo_id, fase
                        ),
                        data=prazo["fase_pesquisa"],
                    )
                )

                tempo_restante_cell = ft.DataCell(
                    ft.Text(str(tempo_restante))
                )

                tabela_prazos.rows.append(
                    ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Text(prazo["fase_pesquisa"])),
                            ft.DataCell(
                                ft.Text(prazo["prazo_fase_pesquisa"])
                            ),
                            ft.DataCell(ft.Text(str(prazo["prazo_dias"]))),
                            ft.DataCell(ft.Text(prazo["prazo_situacao"])),
                            ft.DataCell(
                                ft.Text(prazo["situacao_fase_pesquisa"])
                            ),
                            tempo_restante_cell,
                            excluir_cell,
                        ]
                    )
                )
        # Exibe a tabela e oculta os ft.Text dos prazos
        tabela_prazos.visible = True
        container_info_prazos.visible = False

    def resize_containers(e):
        if anchor.value is not None:
            carregar_dados_prazo(
                anchor.value
            )  # Carrega os dados se um aluno estiver selecionado
        atualizar_visualizacao_dados(page)

    # Chama resize_containers uma vez no início para configurar a interface corretamente
    resize_containers(None)
    page.on_resize = resize_containers

    return container_prazos