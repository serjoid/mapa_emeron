import flet as ft
from database import Database

db = Database()
nomes_orientadores = db.get_orientador()
cursos = db.get_curso()

def tela_orientadores(page: ft.Page, usuario): 
    def handle_change(e):
        print(f"handle_change e.data: {e.data}")
        lv.controls.clear()
        if e.data:
            for nome in nomes_orientadores:
                if e.data.lower() in nome.lower():
                    lv.controls.append(
                        ft.ListTile(title=ft.Text(nome), on_click=close_anchor, data=nome)
                    )
        else:
            for nome in nomes_orientadores:
                lv.controls.append(
                    ft.ListTile(title=ft.Text(nome), on_click=close_anchor, data=nome)
                )
        lv.update()

    def close_anchor(e):
        print(f"Fechando a view do orientador {e.control.data}")
        anchor.close_view(e.control.data)
        sbvalue(e.control.data)

    def sbvalue(nome):
        global orientador_id
        orientador_info = db.get_orientador_info(anchor.value)
        if orientador_info:
            nome_field.value = orientador_info["nome"]
            telefone_field.value = orientador_info["telefone"]
            email_field.value = orientador_info["email"]
            curso_field.value = orientador_info["curso"]
            curso_dropdown.value = orientador_info["curso"]
            titulacao_field.value = orientador_info["titulacao"]
            instituicao_field.value = orientador_info["instituicao"]
            vinculo_field.value = orientador_info["vinculo"]
            vinculo_dropdown.value = orientador_info["vinculo"]
            polo_field.value = orientador_info["polo"]
            polo_dropdown.value = orientador_info["polo"]
            uf_instituicao_field.value = orientador_info["uf_instituicao"]
            uf_instituicao_dropdown.value = orientador_info["uf_instituicao"]
            lattes_field.value = orientador_info["lattes"]
            orientador_id = orientador_info["id"]
            # Tornando os campos visíveis/invisíveis
            curso_field.visible = True
            vinculo_field.visible = True
            polo_field.visible = True
            uf_instituicao_field.visible = True
            curso_dropdown.visible = False
            vinculo_dropdown.visible = False
            polo_dropdown.visible = False
            uf_instituicao_dropdown.visible = False
            botao_novo_orientador.visible = False
            botao_atualizar_orientador.visible = True
            botao_atualizar_orientador.visible = True
            botao_excluir_orientador.visible = False
            # Tornando os campos somente leitura
            for field in lista_textfields:
                field.read_only = True
            page.update()
        else:
            botao_atualizar_orientador.visible = False
            botao_excluir_orientador.visible = False

            # Limpando os campos
            for field in lista_textfields:
                telefone_field.value = ""
                lattes_field.value = ""
                field.value = ""

        atualizar_orientandos(anchor.value)
        page.update()

    def clrsbvalue(nome):
        for field in lista_textfields:
            telefone_field.value = ""
            lattes_field.value = ""
            field.value = ""
            field.read_only = True

        # Garantindo que os campos corretos estejam visíveis
        botao_salvar.visible = False
        curso_field.visible = True
        vinculo_field.visible = True
        polo_field.visible = True
        uf_instituicao_field.visible = True
        curso_dropdown.visible = False
        vinculo_dropdown.visible = False
        polo_dropdown.visible = False
        uf_instituicao_dropdown.visible = False

        orientandos_view.controls.clear()
        page.update()

    # Definição dos campos
    nome_field = ft.TextField(label="Nome", width=800, height=50, read_only=True, bgcolor="WHITE")
    telefone_field = ft.TextField(
        label="Telefone (Com DDD, somente números)",
        width=650,
        height=75,
        read_only=True,
        max_length=11,
        col={"sm": 10, "md": 10},
        bgcolor="WHITE"
    )
    telefone_icon = ft.IconButton(
        icon=ft.icons.PHONE,
        width=50,
        height=50,
        on_click=lambda e: abrir_whatsapp(telefone_field.value),
        tooltip="Abrir WhatsApp",
        col={"sm": 2, "md": 2},
    )
    email_field = ft.TextField(label="Email", width=800, height=50, read_only=True, bgcolor="WHITE")
    curso_field = ft.TextField(label="Curso", width=800, height=50, read_only=True, bgcolor="WHITE")
    titulacao_field = ft.TextField(label="Titulação", width=800, height=50, read_only=True, bgcolor="WHITE")
    instituicao_field = ft.TextField(label="Instituição", width=800, height=50, read_only=True, bgcolor="WHITE")
    vinculo_field = ft.TextField(label="Vínculo", width=800, height=50, read_only=True, bgcolor="WHITE")
    polo_field = ft.TextField(label="Polo", width=800, height=50, read_only=True, bgcolor="WHITE")
    uf_instituicao_field = ft.TextField(label="UF da instituição", width=800, height=50, read_only=True, bgcolor="WHITE")
    lattes_field = ft.TextField(
        label="Lattes",
        width=650,
        height=50,
        read_only=True,
        col={"sm": 10, "md": 10},
        bgcolor="WHITE"
    )
    lattes_icon = ft.IconButton(
        icon=ft.icons.LINK,
        width=50,
        height=50,
        on_click=lambda e: page.launch_url(lattes_field.value)
        if lattes_field.value
        else None,
        tooltip="Abrir Currículo Lattes",
        col={"sm": 2, "md": 2}, 
    )

    # Dropdowns
    curso_dropdown = ft.Dropdown(
        width=800,
        label="Curso",
        options=[ft.dropdown.Option(key=curso) for curso in cursos],
        visible=False,
        bgcolor="WHITE"
    )
    vinculo_dropdown = ft.Dropdown(
        width=800,
        label="Vínculo",
        options=[
            ft.dropdown.Option("Servidor"),
            ft.dropdown.Option("Magistrado"),
            ft.dropdown.Option("Externo"),
        ],
        visible=False,
        bgcolor="WHITE"
    )
    polo_dropdown = ft.Dropdown(
        width=800,
        label="Polo",
        options=[ft.dropdown.Option("Porto Velho"), ft.dropdown.Option("Cacoal"), ft.dropdown.Option("N/A")],
        visible=False,
        bgcolor="WHITE"
    )
    uf_instituicao_dropdown = ft.Dropdown(
        width=800,
        label="UF da instituição",
        options=[
            ft.dropdown.Option("RO"),
            ft.dropdown.Option("AC"),
            ft.dropdown.Option("AM"),
            ft.dropdown.Option("RR"),
            ft.dropdown.Option("PA"),
            ft.dropdown.Option("AP"),
            ft.dropdown.Option("TO"),
            ft.dropdown.Option("MA"),
            ft.dropdown.Option("PI"),
            ft.dropdown.Option("CE"),
            ft.dropdown.Option("RN"),
            ft.dropdown.Option("PB"),
            ft.dropdown.Option("PE"),
            ft.dropdown.Option("AL"),
            ft.dropdown.Option("SE"),
            ft.dropdown.Option("BA"),
            ft.dropdown.Option("MG"),
            ft.dropdown.Option("ES"),
            ft.dropdown.Option("RJ"),
            ft.dropdown.Option("SP"),
            ft.dropdown.Option("PR"),
            ft.dropdown.Option("SC"),
            ft.dropdown.Option("RS"),
            ft.dropdown.Option("MS"),
            ft.dropdown.Option("MT"),
            ft.dropdown.Option("GO"),
            ft.dropdown.Option("DF"),
        ],
        visible=False,
        bgcolor="WHITE"
    )

    # Lista de TextFields para controle
    lista_textfields = [
        nome_field,
        telefone_field,
        email_field,
        curso_field,
        titulacao_field,
        instituicao_field,
        vinculo_field,
        polo_field,
        uf_instituicao_field,
        lattes_field,
        curso_dropdown,
        vinculo_dropdown,
        polo_dropdown,
        uf_instituicao_dropdown
    ]

    lv = ft.ListView()
    for nome in nomes_orientadores:
        lv.controls.append(
            ft.ListTile(title=ft.Text(nome), on_click=close_anchor, data=nome)
        )

    anchor = ft.SearchBar(
        view_elevation=4,
        divider_color=ft.colors.AMBER,
        bar_hint_text="Buscar orientador",
        view_hint_text="Selecione um nome",
        on_change=handle_change,
        on_submit=sbvalue,
        on_tap=clrsbvalue,
        controls=[lv],
    )

    orientandos_view = ft.ListView()

    def atualizar_orientandos(orientador):
        orientando_info = db.get_orientando(orientador)
        orientandos_view.controls.clear()
        if orientando_info:
            for nome in orientando_info:
                orientandos_view.controls.append(ft.ListTile(title=ft.Text(nome)))
        orientandos_view.update()

    # Diálogos de confirmação
    dlg_confirmacao_excluir = ft.AlertDialog(
        modal=True,
        title=ft.Text("Confirmar Exclusão"),
        content=ft.Text("Tem certeza que deseja excluir este orientador?"),
        actions=[
            ft.TextButton(
                "Sim", on_click=lambda e: deletar_orientador_confirmado(orientador_id)
            ),
            ft.TextButton("Não", on_click=lambda e: fechar_dialogo_excluir(e)),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )

    dlg_confirmacao_novo = ft.AlertDialog(
        modal=True,
        title=ft.Text("Confirmar Cadastro"),
        content=ft.Text("Tem certeza que deseja cadastrar este novo orientador?"),
        actions=[
            ft.TextButton("Sim", on_click=lambda e: cadastrar_orientador_confirmado(e)),
            ft.TextButton("Não", on_click=lambda e: fechar_dialogo_novo(e)),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )

    dlg_confirmacao_atualizar = ft.AlertDialog(
        modal=True,
        title=ft.Text("Confirmar Atualização"),
        content=ft.Text("Tem certeza que deseja atualizar este orientador?"),
        actions=[
            ft.TextButton("Sim", on_click=lambda e: atualizar_orientador_confirmado(e)),
            ft.TextButton("Não", on_click=lambda e: fechar_dialogo_atualizar(e)),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )

    def fechar_dialogo_excluir(e):
        dlg_confirmacao_excluir.open = False
        page.update()

    def fechar_dialogo_novo(e):
        dlg_confirmacao_novo.open = False
        page.update()

    def fechar_dialogo_atualizar(e):
        dlg_confirmacao_atualizar.open = False
        page.update()

    def deletar_orientador_confirmado(orientador_id):
        db.deletar_pessoa(orientador_id)
        db.registrar_log(
            usuario, "excluir_orientador", f"Orientador: {nome_field.value}"
        )
        dlg_confirmacao_excluir.open = False
        page.snack_bar = ft.SnackBar(ft.Text("Orientador excluído com sucesso!"))
        page.snack_bar.open = True
        anchor.value = ""
        sbvalue(anchor.value)
        page.update()

        global nomes_orientadores
        nomes_orientadores = db.get_orientador()
        lv.controls.clear()
        for nome in nomes_orientadores:
            lv.controls.append(
                ft.ListTile(title=ft.Text(nome), on_click=close_anchor, data=nome)
            )
        lv.update()

        for field in lista_textfields:
            field.value = ""
            lattes_field.value = ""
            telefone_field.value = ""
            field.update()

        orientandos_view.controls.clear()
        page.update()

    def confirmar_exclusao(e):
        page.dialog = dlg_confirmacao_excluir
        dlg_confirmacao_excluir.open = True
        page.update()

    def novo_orientador(e):
        # Tornando os campos editáveis e limpando-os
        for field in lista_textfields:
            field.read_only = False
            lattes_field.read_only = False
            telefone_field.read_only = False
            lattes_field.value = ""
            telefone_field.value = ""
            field.value = ""
            field.update()
        # Configurando visibilidade dos campos e botões
        curso_field.visible = False
        vinculo_field.visible = False
        polo_field.visible = False
        uf_instituicao_field.visible = False
        curso_dropdown.visible = True
        vinculo_dropdown.visible = True
        polo_dropdown.visible = True
        uf_instituicao_dropdown.visible = True
        orientandos_view.controls.clear()
        botao_salvar.visible = False
        botao_cadastrar.visible = True
        botao_atualizar_orientador.visible = False
        botao_excluir_orientador.visible = False
        botao_novo_orientador.visible = False
        anchor.value = ""
        anchor.visible = False
        anchor.update()
        page.update()

    def atualizar_orientador(e):
        global orientador_id
        # Configurando visibilidade dos campos e dropdowns
        curso_field.visible = False
        vinculo_field.visible = False
        polo_field.visible = False
        uf_instituicao_field.visible = False
        curso_dropdown.visible = True
        vinculo_dropdown.visible = True
        polo_dropdown.visible = True
        uf_instituicao_dropdown.visible = True
        page.update()
        # Preenchendo os dropdowns com as informações do orientador
        orientador_info = db.get_orientador_info(anchor.value)
        curso_dropdown.value = orientador_info["curso"]
        vinculo_dropdown.value = orientador_info["vinculo"]
        polo_dropdown.value = orientador_info["polo"]
        uf_instituicao_dropdown.value = orientador_info["uf_instituicao"]
        if orientador_id:
            for field in lista_textfields:
                field.read_only = False
                lattes_field.read_only = False
                telefone_field.read_only = False
                field.update()
        botao_salvar.visible = True
        botao_novo_orientador.visible = False
        botao_atualizar_orientador.visible = False
        botao_excluir_orientador.visible = True
        page.update()

    def insert_new_orientador(e):
        page.dialog = dlg_confirmacao_novo
        dlg_confirmacao_novo.open = True
        page.update()

    def save_orientador(e):
        page.dialog = dlg_confirmacao_atualizar
        dlg_confirmacao_atualizar.open = True
        page.update()

    def cadastrar_orientador_confirmado(e):
        # Verificar se os campos obrigatórios estão preenchidos
        campos_obrigatorios = [
            nome_field,
            instituicao_field,
            vinculo_dropdown,
        ]
        campos_nao_preenchidos = [campo for campo in campos_obrigatorios if not campo.value]

        if campos_nao_preenchidos:
            # Destacar campos não preenchidos
            for campo in campos_nao_preenchidos:
                campo.bgcolor = ft.colors.RED_ACCENT_100

            # Mostrar alerta
            dlg = ft.AlertDialog(
                title=ft.Text("Campos Obrigatórios"),
                content=ft.Text("Preencha todos os campos obrigatórios."),
                actions=[ft.TextButton("Ok", on_click=lambda e: fechar_dialogo(dlg))]
            )
            page.dialog = dlg
            dlg.open = True
            page.update()

        else:
            # Criar o dicionário orientador_data com os valores dos campos
            orientador_data = {
                "nome": nome_field.value,
                "telefone": telefone_field.value if telefone_field.value else "Não informado",
                "email": email_field.value if email_field.value else "Não informado",
                "curso": curso_dropdown.value if curso_dropdown.value else "Não informado",
                "titulacao": titulacao_field.value if titulacao_field.value else "Não informado",
                "instituicao": instituicao_field.value,
                "vinculo": vinculo_dropdown.value,
                "polo": polo_dropdown.value,
                "uf_instituicao": uf_instituicao_dropdown.value,
                "lattes": lattes_field.value if lattes_field.value else "Não informado",
            }
            db.insert_orientador(orientador_data)
            db.registrar_log(
                usuario,
                "inserir_orientador",
                f"Orientador: {orientador_data['nome']}",
            )
            dlg_confirmacao_novo.open = False
            page.snack_bar = ft.SnackBar(ft.Text("Orientador cadastrado com sucesso!"))
            page.snack_bar.open = True
            page.update()
            global nomes_orientadores
            nomes_orientadores = db.get_orientador()
            lv.controls.clear()
            for nome in nomes_orientadores:
                lv.controls.append(
                    ft.ListTile(title=ft.Text(nome), on_click=close_anchor, data=nome)
                )
            lv.update()
            # Retornando os campos para o estado inicial
            for field in lista_textfields:
                field.read_only = True
                field.value = ''
            curso_field.visible = True
            vinculo_field.visible = True
            polo_field.visible = True
            uf_instituicao_field.visible = True
            curso_dropdown.visible = False
            vinculo_dropdown.visible = False
            polo_dropdown.visible = False
            uf_instituicao_dropdown.visible = False
            botao_novo_orientador.visible = True
            botao_salvar.visible = False
            botao_cadastrar.visible = False
            anchor.visible = True
            instituicao_field.bgcolor = "WHITE"
            page.update()

    def fechar_dialogo(dlg):
        dlg.open = False
        page.update()

    def atualizar_orientador_confirmado(e):
        orientador_data = {
            "nome": nome_field.value,
            "telefone": telefone_field.value,
            "email": email_field.value,
            "curso": curso_dropdown.value,
            "titulacao": titulacao_field.value,
            "instituicao": instituicao_field.value,
            "vinculo": vinculo_dropdown.value,
            "polo": polo_dropdown.value,
            "uf_instituicao": uf_instituicao_dropdown.value,
            "lattes": lattes_field.value,
            "id": orientador_id,
        }
        db.update_orientador(orientador_data)
        db.registrar_log(
            usuario,
            "atualizar_orientador",
            f"Orientador: {orientador_data['nome']}",
        )
        dlg_confirmacao_atualizar.open = False
        page.snack_bar = ft.SnackBar(ft.Text("Orientador atualizado com sucesso!"))
        page.snack_bar.open = True
        for field in lista_textfields:
            field.read_only = True
            lattes_field.read_only = True
            telefone_field.read_only = True
        sbvalue(anchor.value)
        # VISIBILIDADE DOS BOTOES
        botao_atualizar_orientador.visible = True
        botao_cadastrar.visible = False
        botao_excluir_orientador.visible = False
        botao_salvar.visible = False
        # VISIBILIDADE DOS TEXTFIELDS (Ativa)
        curso_field.visible = True
        vinculo_field.visible = True
        polo_field.visible = True
        uf_instituicao_field.visible = True
        # VISIBILIDADE DOS DROPDOWNS (Inativa)
        curso_dropdown.visible = False
        vinculo_dropdown.visible = False
        polo_dropdown.visible = False
        uf_instituicao_dropdown.visible = False
        page.update()

    # Função para abrir o WhatsApp
    def abrir_whatsapp(telefone):
        if telefone:
            page.launch_url(
                f"https://wa.me/55{telefone.replace(' ', '').replace('-', '')}"
            )

    # Botões
    botao_novo_orientador = ft.ElevatedButton(
        text="Novo orientador",
        width=185,
        height=40,
        bgcolor="#006BA0",
        color="WHITE",
        on_click=novo_orientador,
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
    )
    botao_atualizar_orientador = ft.ElevatedButton(
        text="Atualizar cadastro",
        width=185,
        height=40,
        bgcolor="#006BA0",
        color="WHITE",
        on_click=atualizar_orientador,
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
        visible=False,
    )
    botao_salvar = ft.ElevatedButton(
        text="Salvar",
        width=185,
        height=40,
        bgcolor="#006BA0",
        color="WHITE",
        on_click=save_orientador,
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
        visible=False,
    )
    botao_cadastrar = ft.ElevatedButton(
        text="Cadastrar",
        width=185,
        height=40,
        bgcolor="#006BA0",
        color="WHITE",
        on_click=insert_new_orientador,
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
        visible=False,
    )
    botao_excluir_orientador = ft.ElevatedButton(
        text="Excluir",
        width=185,
        height=40,
        bgcolor="#006BA0",
        color="WHITE",
        on_click=confirmar_exclusao,
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
        visible=False,
    )

    # Containers
    container_botoes = ft.Container(
        width=800,
        content=ft.ResponsiveRow(
            alignment=ft.MainAxisAlignment.END,
            controls=[
                botao_novo_orientador,
                botao_atualizar_orientador,
                botao_salvar,
                botao_cadastrar,
                botao_excluir_orientador,
            ],
        ),
    )

    container_listview = ft.Container(
        border=ft.border.all(1, "black"),
        border_radius=ft.border_radius.all(5),
        width=800,
        padding=10,
        content=ft.Column(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Text("Orientandos", size=20),
                orientandos_view,
            ],
        ),
    )

    nome_campo = ft.Text("DADOS CADASTRAIS - ORIENTADORES", size=16, color="#006BA0", font_family="Roboto", weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER)

    container_orientador = ft.Container(
        expand=True,
        content=ft.Column(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            scroll=ft.ScrollMode.AUTO,
            controls=[
                ft.Container(
                    width=800,
                    content=ft.Column(
                        scroll=ft.ScrollMode.ALWAYS,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        controls=[
                            nome_campo,
                            ft.Divider(),
                            anchor,
                            container_botoes,
                            nome_field,
                            ft.ResponsiveRow(controls=[telefone_field, telefone_icon]),
                            email_field,
                            curso_dropdown,
                            curso_field,
                            titulacao_field,
                            instituicao_field,
                            vinculo_dropdown,
                            vinculo_field,
                            polo_dropdown,
                            polo_field,
                            uf_instituicao_dropdown,
                            uf_instituicao_field,
                            ft.ResponsiveRow(controls=[lattes_field, lattes_icon]),
                            container_listview,
                        ],
                    ),
                ),
            ],
        ),
        margin=ft.margin.only(bottom=20),
    )

    return container_orientador