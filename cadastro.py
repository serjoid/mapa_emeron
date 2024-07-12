import flet as ft
from database import Database

def tela_cadastro(page: ft.Page, usuario_logado):
    # Crie uma instância da classe Database
    db = Database()

    # Variável global para armazenar os usuários
    global usuarios
    usuarios = []

    # Campos de entrada
    nome_dropdown = ft.Dropdown(width=800, label="Nome", visible=False, bgcolor="WHITE")
    nome_input = ft.TextField(label="Nome", width=800, bgcolor="WHITE")
    email_input = ft.TextField(label="Email", width=800, bgcolor="WHITE")
    usuario_input = ft.TextField(label="Usuário", width=800, bgcolor="WHITE", read_only=False)
    senha_input = ft.TextField(label="Senha", password=True, width=800, bgcolor="WHITE")
    confirmacao_senha_input = ft.TextField(label="Confirmar Senha", password=True, width=800, bgcolor="WHITE")

    perfil_dropdown = ft.Dropdown(
        width=800,
        label="Perfil",
        bgcolor="WHITE",
        options=[
            ft.dropdown.Option("Admin"),
            ft.dropdown.Option("Suporte"),
            ft.dropdown.Option("Orientador"),
            ft.dropdown.Option("Aluno"),
        ],
        on_change=lambda e: atualizar_campos_nome(e)
    )

    def atualizar_campos_nome(e):
        perfil_selecionado = perfil_dropdown.value
        if perfil_selecionado == "Orientador":
            nome_dropdown.options = [ft.dropdown.Option(nome) for nome in db.get_orientador()]
            nome_dropdown.visible = True
            nome_input.visible = False
        elif perfil_selecionado == "Aluno":
            nome_dropdown.options = [ft.dropdown.Option(nome) for nome in db.get_aluno()]
            nome_dropdown.visible = True
            nome_input.visible = False
        else:
            nome_dropdown.visible = False
            nome_input.visible = True

        nome_dropdown.update()
        nome_input.update()
        page.update()

    def cadastrar_clique(e):
        nome = nome_dropdown.value if nome_dropdown.visible else nome_input.value
        email = email_input.value
        usuario_input.value = email  # Preencher campo "Usuário" com valor do campo "Email"
        senha = senha_input.value
        confirmacao_senha = confirmacao_senha_input.value
        perfil = perfil_dropdown.value

        page.update()  # Atualizar a página após preencher o campo "Usuário"

        if not email or not nome or not senha or not confirmacao_senha or not perfil:
            dlg = ft.AlertDialog(
                title=ft.Text("Erro"),
                content=ft.Text("Preencha todos os campos!"),
                actions=[
                    ft.TextButton("Ok", on_click=lambda e: fechar_dialogo(dlg))
                ]
            )
            page.dialog = dlg
            dlg.open = True
            page.update()
            return

        if senha != confirmacao_senha:
            dlg = ft.AlertDialog(
                title=ft.Text("Erro"),
                content=ft.Text("As senhas não coincidem!"),
                actions=[
                    ft.TextButton("Ok", on_click=lambda e: fechar_dialogo(dlg))
                ]
            )
            page.dialog = dlg
            dlg.open = True
            page.update()
            return

        log_detalhes = f"Nome: {nome}, Email: {email}, Usuário: {email}, Perfil: {perfil}"
        db.registrar_log(usuario_logado, "cadastrar_usuario", log_detalhes)

        db.cadastrar_usuario(nome, email, email, senha, perfil)

        dlg = ft.AlertDialog(
            title=ft.Text("Sucesso"),
            content=ft.Text("Usuário cadastrado com sucesso!"),
            actions=[
                ft.TextButton("Ok", on_click=lambda e: fechar_dialogo(dlg))
            ]
        )

        page.dialog = dlg
        dlg.open = True
        page.update()

        nome_input.value = ""
        email_input.value = ""
        usuario_input.value = ""
        senha_input.value = ""
        confirmacao_senha_input.value = ""
        perfil_dropdown.value = None
        nome_dropdown.value = None
        page.update()

    def fechar_dialogo(dlg):
        dlg.open = False
        page.update()

    def excluir_usuario_clique(e, usuario_excluido):
        usuarios_info = db.consultar_usuarios()
        usuario_info = next((u for u in usuarios_info if u['usuario'] == usuario_excluido), None)
        if not usuario_info:
            dlg = ft.AlertDialog(
                title=ft.Text("Erro"),
                content=ft.Text("Usuário não encontrado."),
                actions=[
                    ft.TextButton("Ok", on_click=lambda e: fechar_dialogo(dlg))
                ]
            )
            page.dialog = dlg
            dlg.open = True
            page.update()
            return

        nome = usuario_info['nome']
        email = usuario_info['email']
        perfil = usuario_info['perfil']

        def confirmar_exclusao(e):
            resultado = db.excluir_usuario(usuario_excluido)
            log_detalhes = f"Nome: {nome}, Email: {email}, Usuário: {usuario_excluido}, Perfil: {perfil}"
            db.registrar_log(usuario_logado, "excluir_usuario", log_detalhes)
            
            dlg = ft.AlertDialog(
                title=ft.Text("Resultado da Exclusão"),
                content=ft.Text("Usuário excluído com sucesso!"),
                actions=[
                    ft.TextButton("Ok", on_click=lambda e: fechar_dialogo(dlg))
                ]
            )
            page.dialog = dlg
            dlg.open = True
            page.update()

            carregar_usuarios(e)  # Chama a função para atualizar a lista de usuários

        dlg_confirmar = ft.AlertDialog(
            title=ft.Text("Confirmar Exclusão"),
            content=ft.Text(f"Tem certeza de que deseja excluir o usuário {nome}?"),
            actions=[
                ft.TextButton("Cancelar", on_click=lambda e: fechar_dialogo(dlg_confirmar)),
                ft.TextButton("Confirmar", on_click=lambda e: confirmar_exclusao(e))
            ]
        )
        page.dialog = dlg_confirmar
        dlg_confirmar.open = True
        page.update()

    def carregar_usuarios(e):
        global usuarios
        usuarios = db.consultar_usuarios()
        filtrar_usuarios()

    def filtrar_usuarios(e=None):
        termo_pesquisa = txt_pesquisa.value.lower() if txt_pesquisa.value else ""
        colunas_usuarios.controls.clear()
        for usuario in usuarios:
            nome = usuario.get('nome', 'N/A')
            email = usuario.get('email', 'N/A')
            user = usuario.get('usuario', 'N/A')
            perfil = usuario.get('perfil', 'N/A')

            if termo_pesquisa in str(usuario).lower():
                usuario_texto = ft.SelectionArea(
                    content=ft.Text(
                        f"Nome: {nome}\nEmail: {email}\nUsuário: {user}\nPerfil: {perfil}\n-------------------"
                    )
                )
                excluir_botao = ft.IconButton(ft.icons.DELETE, icon_color="RED", on_click=lambda e, usuario=user: excluir_usuario_clique(e, usuario))
                colunas_usuarios.controls.append(ft.Row([usuario_texto, excluir_botao]))

        colunas_usuarios.update()
        page.update()

    # Campo de pesquisa
    txt_pesquisa = ft.TextField(label="Pesquisar usuários", width=300)

    botao_carregar_usuarios = ft.ElevatedButton(
        text="Carregar Usuários",
        on_click=carregar_usuarios,
        width=200,
        height=40,
        elevation=4,
        bgcolor="#006BA0",
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
        color="WHITE",
    )

    botao_cadastrar = ft.ElevatedButton(
        text="Cadastrar",
        on_click=cadastrar_clique,
        width=200,
        height=40,
        elevation=4,
        bgcolor="#006BA0",
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
        color="WHITE",
    )

    divisor = ft.Divider()

    nome_campo = ft.Text("CADASTRO DE NOVO USUÁRIO", size=16, color="#006BA0", font_family="Roboto", weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER)

    colunas_usuarios = ft.Column()

    container = ft.Container(
        content=ft.Column(
            [
                nome_campo,
                divisor,
                perfil_dropdown,
                nome_dropdown,
                nome_input,
                email_input,
                senha_input,
                confirmacao_senha_input,
                botao_cadastrar,
                txt_pesquisa,  # Campo de pesquisa
                botao_carregar_usuarios,
                ft.ResponsiveRow(controls=[colunas_usuarios], width=800),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            scroll=ft.ScrollMode.ALWAYS,
        ),
    )

    return container
