import flet as ft
from database import Database
from datetime import date, timedelta
import datetime

# Conexão com o banco de dados
db = Database()


def prazos_orientador_logado(page: ft.Page, usuario):
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

    # Função para carregar os dados do prazo com base no aluno selecionado no dropdown
    def carregar_dados_prazo_dropdown(e):
        nome_aluno = dropdown_alunos.value
        if nome_aluno:
            carregar_dados_prazo(nome_aluno)
            resize_containers(e)  # Ajusta a visualização ao trocar de aluno

    def carregar_dados_prazo(nome_aluno):
        pessoa_id = db.get_pessoa_info(nome=nome_aluno).get("id")
        prazos = db.get_prazos_by_pessoa_id(pessoa_id)
        pessoa_info = db.get_pessoa_info(nome=nome_aluno)

        # Ordena a lista de prazos pelo prazo cadastrado
        prazos.sort(
            key=lambda prazo: datetime.datetime.strptime(
                prazo["prazo_fase_pesquisa"], "%d/%m/%Y"
            ).date()
            if prazo["prazo_fase_pesquisa"]
            else datetime.date.max
        )

        global dados_tabela_prazos, dados_info_aluno
        botao_novo.visible = True
        botao_atualizar.visible = True
        dados_tabela_prazos = prazos
        dados_info_aluno = [pessoa_info]  # Transforma em lista para manter a compatibilidade
        atualizar_visualizacao_dados(page)
        atualizar_visualizacao_info_aluno(page)

    def excluir_prazo(prazo_id, fase_pesquisa):
        db.excluir_prazo(prazo_id)
        db.registrar_log(
            usuario, "excluir_prazo", f"Prazo ID: {prazo_id}, Fase: {fase_pesquisa}"
        )
        carregar_dados_prazo(dropdown_alunos.value)

    def confirmar_exclusao(e, prazo_id, fase):
        page.dialog = dlg_confirmacao_excluir
        dlg_confirmacao_excluir.open = True
        page.update()
        global prazo_id_excluir, fase_pesquisa
        prazo_id_excluir = prazo_id
        fase_pesquisa = fase

    def confirmar_exclusao_prazo(e):
        global prazo_id_excluir, fase_pesquisa
        excluir_prazo(prazo_id_excluir, fase_pesquisa)
        fechar_dialogo(e)

    def limpar_campos():
        prazo_fase_pesquisa_field.value = ""
        prazo_dias_field.value = ""
        prazo_situacao_field.value = ""
        situacao_fase_pesquisa_dropdown.value = None
        dropdown_fases.value = None
        dropdown_fases_registro.value = None
        page.update()

    def preencher_campos(prazo):
        prazo_fase_pesquisa_field.value = prazo.get("prazo_fase_pesquisa", "")
        prazo_dias_field.value = str(prazo.get("prazo_dias", ""))
        prazo_situacao_field.value = prazo.get("prazo_situacao", "")
        situacao_fase_pesquisa_dropdown.value = prazo.get(
            "situacao_fase_pesquisa", ""
        )
        page.update()

    def novo_prazo(e):
        limpar_campos()
        container_campos.visible = True
        container_dropdown.visible = False
        botao_salvar.visible = False
        botao_salvar_novo.visible = True
        botao_novo.visible = False
        botao_atualizar.visible = False
        page.update()

    def salvar_novo_prazo(e):
        page.dialog = dlg_confirmacao_novo
        dlg_confirmacao_novo.open = True
        page.update()

    def confirmar_salvar_novo_prazo(e):
        pessoa_id = db.get_pessoa_info(nome=dropdown_alunos.value).get("id")
        prazo_data = {
            "id_pessoa": pessoa_id,
            "fase_pesquisa": dropdown_fases_registro.value,
            "prazo_fase_pesquisa": prazo_fase_pesquisa_field.value,
            "prazo_dias": prazo_dias_field.value,
            "prazo_situacao": prazo_situacao_field.value,
            "situacao_fase_pesquisa": situacao_fase_pesquisa_dropdown.value,
        }
        db.inserir_prazo(prazo_data)
        db.registrar_log(
            usuario,
            "inserir_prazo",
            f"Prazo para: {dropdown_alunos.value}, Fase: {prazo_data['fase_pesquisa']}",
        )
        carregar_dados_prazo(dropdown_alunos.value)
        limpar_campos()
        container_campos.visible = False
        botao_salvar_novo.visible = False
        botao_novo.visible = True
        botao_atualizar.visible = True
        page.update()
        fechar_dialogo(e)

    def salvar_prazo(e):
        page.dialog = dlg_confirmacao_atualizar
        dlg_confirmacao_atualizar.open = True
        page.update()

    def confirmar_salvar_prazo(e):
        fase_selecionada = dropdown_fases.value
        pessoa_id = db.get_pessoa_info(nome=dropdown_alunos.value).get("id")
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
            db.registrar_log(
                usuario,
                "atualizar_prazo",
                f"Prazo ID: {prazo_a_atualizar['id']}, Fase: {fase_selecionada}",
            )
            carregar_dados_prazo(dropdown_alunos.value)
            limpar_campos()
            container_campos.visible = False
            container_dropdown.visible = False
            botao_salvar.visible = False
            botao_novo.visible = True
            botao_atualizar.visible = True
            page.update()
            fechar_dialogo(e)

        else:
            print(f"Nenhum prazo encontrado para a fase '{fase_selecionada}'.")

    def atualizar_prazo(e):
        pessoa_id = db.get_pessoa_info(nome=dropdown_alunos.value).get("id")
        prazos = db.get_prazos_by_pessoa_id(pessoa_id)

        if prazos:
            opcoes_fases = [
                ft.dropdown.Option(prazo["fase_pesquisa"]) for prazo in prazos
            ]
            dropdown_fases.options = opcoes_fases
            dropdown_fases.value = None

            container_campos.visible = False
            container_dropdown.visible = True
            botao_salvar.visible = True
            botao_salvar_novo.visible = False
            botao_novo.visible = False
            botao_atualizar.visible = False

            page.update()

        else:
            print("Nenhum prazo encontrado para este aluno.")

    def preencher_campos_edicao(e):
        fase_selecionada = dropdown_fases.value
        pessoa_id = db.get_pessoa_info(nome=dropdown_alunos.value).get("id")
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

    # ---- Componentes da interface ----
    dropdown_fases_registro = ft.Dropdown(
        width=250,
        label="Fase de Pesquisa",
        bgcolor="WHITE",
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
            ft.dropdown.Option("Desistente"),
            ft.dropdown.Option("Reprovado"),
            ft.dropdown.Option("Outras situações"),
        ],
    )

    orientador = db.get_orientador_info_por_usuario(usuario)["nome"]
    nomes_alunos = db.get_orientando(orientador)

    dropdown_alunos = ft.Dropdown(
        width=1300,
        options=[ft.dropdown.Option(nome) for nome in nomes_alunos],
        on_change=carregar_dados_prazo_dropdown,
        bgcolor="WHITE",
    )

    # Define as colunas da tabela
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

    global dados_tabela_prazos
    dados_tabela_prazos = []

    # Tabela de prazos - Inicialmente visível
    tabela_prazos = ft.DataTable(
        columns=colunas_tabela_prazos,
        rows=[],
        border=ft.border.all(2, "black"),
        border_radius=ft.border_radius.all(10),
        bgcolor="WHITE",
        visible=False,
    )

    # ListView para os prazos - Inicialmente invisível
    lista_prazos = ft.ListView(
        expand=True,
        spacing=10,
        padding=10,
        visible=False,
    )

    # ListView para informações do aluno - Inicialmente invisível
    lista_info_aluno = ft.ListView(
        expand=True,
        spacing=10,
        padding=10,
        visible=False,
    )

    global dados_info_aluno
    dados_info_aluno = []

    dropdown_fases = ft.Dropdown(
        width=200,
        label="Selecione a fase para edição",
        options=[],
        on_change=preencher_campos_edicao,
        bgcolor="WHITE",
    )

    container_dropdown = ft.Container(
        width=1300,
        content=ft.ResponsiveRow(
            controls=[dropdown_fases], alignment=ft.MainAxisAlignment.CENTER
        ),
        visible=False,
    )

    prazo_fase_pesquisa_field = ft.TextField(
        label="Data do prazo", width=200, read_only=False, bgcolor="WHITE"
    )
    prazo_dias_field = ft.TextField(
        label="Prazo em Dias",
        width=200,
        on_change=calcular_prazo,
        keyboard_type=ft.KeyboardType.NUMBER,
        bgcolor="WHITE",
    )
    prazo_situacao_field = ft.Dropdown(
        label="Situação do Prazo",
        width=200,
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
        width=200,
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
        width=1300,
        content=ft.ResponsiveRow(
            controls=[
                dropdown_fases_registro,
                situacao_fase_pesquisa_dropdown,
                prazo_dias_field,
                prazo_fase_pesquisa_field,
                prazo_situacao_field,
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        ),
        visible=False,
    )

    botao_novo = ft.ElevatedButton(
        text="Novo",
        width=150,
        height=40,
        elevation=4,
        bgcolor="#006BA0",
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
        color="WHITE",
        on_click=novo_prazo,
        visible=False,  # Inicialmente invisível
    )
    botao_atualizar = ft.ElevatedButton(
        text="Atualizar",
        width=150,
        height=40,
        elevation=4,
        bgcolor="#006BA0",
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
        color="WHITE",
        on_click=atualizar_prazo,
        visible=False,  # Inicialmente invisível
    )
    botao_salvar_novo = ft.ElevatedButton(
        text="Salvar Novo",
        width=150,
        height=40,
        elevation=4,
        bgcolor="#006BA0",
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
        color="WHITE",
        on_click=salvar_novo_prazo,
        visible=False,
    )
    botao_salvar = ft.ElevatedButton(
        text="Salvar",
        width=150,
        height=40,
        elevation=4,
        bgcolor="#006BA0",
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
        color="WHITE",
        on_click=salvar_prazo,
        visible=False,
    )

    container_botoes = ft.Container(
        width=1300,
        content=ft.ResponsiveRow(
            controls=[botao_novo, botao_atualizar, botao_salvar, botao_salvar_novo],
            alignment=ft.MainAxisAlignment.CENTER,
        ),
    )

    nome_campo = ft.Text(
        "ANDAMENTO DA PESQUISA",
        size=16,
        color="#006BA0",
        font_family="Roboto",
        weight=ft.FontWeight.BOLD,
        text_align=ft.TextAlign.CENTER,
    )

    # Container principal para os dados da tabela ou da lista
    container_dados = ft.Container(
        width=1300,
        content=None,
        margin=ft.margin.only(bottom=10),
    )

    # Container para informações do aluno
    container_info_aluno = ft.Container(
        width=1300,
        content=ft.Column(
            [
                ft.Text(
                    "Nome:",
                    size=14,
                    weight=ft.FontWeight.BOLD,
                ),
                ft.Text(
                    "",
                    size=14,
                ),
                ft.Text(
                    "Curso:",
                    size=14,
                    weight=ft.FontWeight.BOLD,
                ),
                ft.Text(
                    "",
                    size=14,
                ),
                ft.Text(
                    "Orientador:",
                    size=14,
                    weight=ft.FontWeight.BOLD,
                ),
                ft.Text(
                    "",
                    size=14,
                ),
            ]
        ),
        margin=ft.margin.only(top=10),
    )

    container_prazos = ft.Container(
        expand=True,
        content=ft.Column(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            scroll=ft.ScrollMode.ALWAYS,
            controls=[
                nome_campo,
                ft.Divider(),
                ft.ResponsiveRow(controls=[dropdown_alunos], width=800),
                ft.ResponsiveRow(controls=[container_botoes], width=800),
                ft.ResponsiveRow(controls=[container_info_aluno], width=800), # Container para informações do aluno
                ft.ResponsiveRow(controls=[ft.Divider()], width=800),
                container_dropdown,
                container_campos,
                container_dados,
            ],
            alignment="START",
        ),
    )

    # Função para atualizar a visualização dos dados (tabela ou lista)
    def atualizar_visualizacao_dados(page):
        global dados_tabela_prazos
        if page.width < 1024:
            lista_prazos.controls.clear()
            for prazo in dados_tabela_prazos:
                lista_prazos.controls.append(criar_item_lista_prazo(prazo))
            container_dados.content = lista_prazos
            lista_prazos.visible = True
            tabela_prazos.visible = False
        else:
            tabela_prazos.rows.clear()
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

                tempo_restante_cell = ft.DataCell(ft.Text(str(tempo_restante)))

                tabela_prazos.rows.append(
                    ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Text(prazo["fase_pesquisa"])),
                            ft.DataCell(ft.Text(prazo["prazo_fase_pesquisa"])),
                            ft.DataCell(ft.Text(str(prazo["prazo_dias"]))),
                            ft.DataCell(ft.Text(prazo["prazo_situacao"])),
                            ft.DataCell(ft.Text(prazo["situacao_fase_pesquisa"])),
                            tempo_restante_cell,
                            excluir_cell,
                        ]
                    )
                )
            container_dados.content = tabela_prazos
            tabela_prazos.visible = True
            lista_prazos.visible = False
        page.update()

    # Função para atualizar a visualização das informações do aluno
    def atualizar_visualizacao_info_aluno(page):
        global dados_info_aluno
        if dados_info_aluno:
            pessoa_info = dados_info_aluno[0]
            container_info_aluno.content.controls[1].value = pessoa_info.get(
                "nome", ""
            )
            container_info_aluno.content.controls[3].value = pessoa_info.get(
                "curso", ""
            )
            container_info_aluno.content.controls[5].value = pessoa_info.get(
                "orientador", ""
            )
        page.update()

    # Função para criar um item da ListView de prazos
    def criar_item_lista_prazo(prazo):
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

        return ft.ListTile(
            title=ft.Text(prazo["fase_pesquisa"]),
            subtitle=ft.Column(
                [
                    ft.Row(
                        [ft.Text("Prazo:"), ft.Text(prazo["prazo_fase_pesquisa"])]
                    ),
                    ft.Row([ft.Text("Dias:"), ft.Text(str(prazo["prazo_dias"]))]),
                    ft.Row(
                        [ft.Text("Situação Prazo:"), ft.Text(prazo["prazo_situacao"])]
                    ),
                    ft.Row(
                        [
                            ft.Text("Situação Fase:"),
                            ft.Text(prazo["situacao_fase_pesquisa"]),
                        ]
                    ),
                    ft.Row(
                        [ft.Text("Tempo Restante:"), ft.Text(str(tempo_restante))]
                    ),
                ]
            ),
            trailing=ft.IconButton(
                icon=ft.icons.DELETE,
                on_click=lambda e, prazo_id=prazo["id"], fase=prazo[
                    "fase_pesquisa"
                ]: confirmar_exclusao(e, prazo_id, fase),
            ),
        )


    def resize_containers(e):
        atualizar_visualizacao_dados(page)
        atualizar_visualizacao_info_aluno(page)

    # Chama resize_containers uma vez no início para configurar a interface corretamente
    resize_containers(None)

    page.on_resize = resize_containers

    return container_prazos