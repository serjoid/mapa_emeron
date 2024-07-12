import flet as ft
from database import Database

db = Database()  # Instancia o objeto Database

# Variável global para armazenar o perfil do usuário
perfil_usuario = None

def exibir_tela_login(page, exibir_menu_principal): # Recebe a função como argumento
    page.controls.clear()  # Limpa os controles da página atual
    page.add(tela_login(page, exibir_menu_principal)) # Passa a função para tela_login
    page.update()

# Tela de Login
def tela_login(page: ft.Page, exibir_menu_principal): # Recebe a função como argumento
    page.title = 'MAPA - Módulo de Acompanhamento da Produção Acadêmica'
    page.theme_mode = "LIGHT"
    page.assets_dir = "assets"
    page.appbar = ft.AppBar(
        leading=ft.IconButton(ft.icons.BOOK, icon_color="WHITE"),
        leading_width=40,
        toolbar_height=40,
        title=ft.Text("MAPA - Módulo de Acompanhamento da Produção Acadêmica", color="WHITE", size=16, font_family="Roboto", weight=ft.FontWeight.W_500),
        center_title=True,
        bgcolor="#006BA0",
        actions=[
            ft.Container(
                content=ft.Image(
                    src="logo.png",
                    width=186,
                    height=40,
                    fit=ft.ImageFit.CONTAIN,
                ),
                margin=ft.padding.all(5),
            )
        ]
    )
    page.bottom_appbar = ft.BottomAppBar(
        height=50,  # Define a altura da BottomAppBar
        bgcolor="#006BA0",
        content=ft.ResponsiveRow(
            alignment=ft.MainAxisAlignment.CENTER,
            controls=[
                ft.Text(
                    "Desenvolvido pelo Núcleo de Inovação Tecnológica - Escola da Magistratura de Rondônia EMERON",
                    color="WHITE",
                    text_align="center"
                )
            ]
        )
    )
    usuario_input = ft.TextField(label="Usuário", width=300, bgcolor="WHITE")
    senha_input = ft.TextField(label="Senha", password=True, width=300, bgcolor="WHITE")

    def fazer_login(e):
        usuario = usuario_input.value
        senha = senha_input.value

        # Verifica se os campos estão preenchidos
        if not usuario or not senha:
            mostrar_erro("Preencha todos os campos!")
            return

        # Verifica as credenciais no banco de dados
        usuario_db = db.verificar_credenciais(usuario, senha)

        if usuario_db:
            # Login bem-sucedido
            global perfil_usuario
            perfil_usuario = usuario_db['perfil']
            db.registrar_log(usuario, "login")  # Registra o log de entrada

            # Após o login ser bem-sucedido:
            page.controls.clear()
            exibir_menu_principal(usuario) # Chama a função passada como argumento
            page.update()

            return usuario # Retorna o usuário para ser utilizado no main.py
        else:
            # Credenciais inválidas
            mostrar_erro("Usuário ou senha inválidos!")
        page.update()

    def mostrar_erro(mensagem):
        dlg = ft.AlertDialog(
            title=ft.Text("Erro"),
            content=ft.Text(mensagem),
            actions=[ft.TextButton("Ok", on_click=lambda e: fechar_dialogo(dlg))]
        )
        page.dialog = dlg
        dlg.open = True
        page.update()

    def fechar_dialogo(dlg):
        dlg.open = False
        page.update()

    botao_login = ft.ElevatedButton(text="Entrar", on_click=fazer_login, width=200, height=50, elevation=4, style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)), bgcolor="#006BA0", color=ft.colors.WHITE)

    img_logo = ft.Container(
        content=
        ft.Image(
            src="logo_img.png",
            width=300,
            height=300,
            fit=ft.ImageFit.CONTAIN,
            border_radius=ft.border_radius.all(10)
        ),margin=ft.margin.only(bottom=20)
    )


    nome_campo = ft.Text("ACESSO", size=16, color="#006BA0", font_family="Roboto", weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER)

    container = ft.Container(
        content=ft.Column(
            [
                img_logo,
                nome_campo,
                usuario_input,
                senha_input,
                botao_login,
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER,
            scroll=ft.ScrollMode.ALWAYS,
        ),
        alignment=ft.alignment.center,  # Centraliza horizontalmente
        expand=False,  # Permite que o Container ocupe todo o espaço disponível
        bgcolor=ft.colors.BLUE_50,
        margin=ft.margin.only(top=20)
    )

    def on_resize(e):
        if page.width < 640:
            page.appbar.title = ft.Text("MAPA - EMERON", color="WHITE", size=14, font_family="Roboto", weight=ft.FontWeight.W_500)
            page.bottom_appbar.content = ft.ResponsiveRow(
                alignment=ft.MainAxisAlignment.CENTER,
                controls=[
                    ft.Text(
                        "By Núcleo de Inovação Tecnológica - EMERON",
                        color="WHITE",
                        text_align="center"
                    )
                ]
            )
        else:
            page.appbar.title = ft.Text("Módulo de Acompanhamento da Produção Acadêmica - MAPA", color="WHITE", size=16, font_family="Roboto", weight=ft.FontWeight.W_500)
            page.bottom_appbar.content = ft.ResponsiveRow(
                alignment=ft.MainAxisAlignment.CENTER,
                controls=[
                    ft.Text(
                        "Desenvolvido pelo Núcleo de Inovação Tecnológica - Escola da Magistratura de Rondônia EMERON",
                        color="WHITE",
                        text_align="center"
                    )
                ]
            )
        page.update()
        
    if page.width < 640:
        page.appbar.title = ft.Text("MAPA - EMERON", color="WHITE", size=14, font_family="Roboto", weight=ft.FontWeight.W_500)
        page.bottom_appbar.content = ft.ResponsiveRow(
            alignment=ft.MainAxisAlignment.CENTER,
            controls=[
                ft.Text(
                    "By Núcleo de Inovação Tecnológica - EMERON",
                    color="WHITE",
                    text_align="center"
                )
            ]
        )
    else:
        page.appbar.title = ft.Text("Módulo de Acompanhamento da Produção Acadêmica - MAPA", color="WHITE", size=16, font_family="Roboto", weight=ft.FontWeight.W_500)
        page.bottom_appbar.content = ft.ResponsiveRow(
            alignment=ft.MainAxisAlignment.CENTER,
            controls=[
                ft.Text(
                    "Desenvolvido pelo Núcleo de Inovação Tecnológica - Escola da Magistratura de Rondônia EMERON",
                    color="WHITE",
                    text_align="center"
                )
            ]
        )

    page.on_resize = on_resize
    
    return container

def sair(e, usuario, exibir_menu_principal): # Recebe a função como argumento
    global perfil_usuario
    perfil_usuario = None
    db.registrar_log(usuario, "logout")
    # Correção: Limpa a página e chama exibir_tela_login diretamente
    e.page.controls.clear()
    exibir_tela_login(e.page, exibir_menu_principal) 