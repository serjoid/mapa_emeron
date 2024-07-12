import flet as ft
from database import Database

# Inicializa a conexão com o banco de dados
db = Database()

# Define variável global para armazenar o perfil do usuário logado
perfil_usuario = None

# Função para exibir a tela de login
def exibir_tela_login(page, exibir_menu_principal):
    """
    Exibe a tela de login na página fornecida.

    Args:
        page (ft.Page): A página onde a tela de login será exibida.
        exibir_menu_principal (function): Função para exibir o menu principal após o login.
    """
    
    page.controls.clear()  # Limpa os controles da página atual
    page.add(tela_login(page, exibir_menu_principal)) # Adiciona a tela de login à página
    page.update()

# Função que define a estrutura da tela de login
def tela_login(page: ft.Page, exibir_menu_principal):
    """
    Cria a estrutura da tela de login.

    Args:
        page (ft.Page): A página onde a tela de login será exibida.
        exibir_menu_principal (function): Função para exibir o menu principal após o login.

    Returns:
        ft.Container: Um container com os elementos da tela de login.
    """

    # Configurações da página
    page.title = 'MAPA - Módulo de Acompanhamento da Produção Acadêmica'
    page.theme_mode = "LIGHT"
    page.assets_dir = "assets"
    
    # Barra de aplicativo superior
    page.appbar = ft.AppBar(
        leading=ft.IconButton(ft.icons.BOOK, icon_color="WHITE"), # Ícone do livro
        leading_width=40,
        toolbar_height=40,
        title=ft.Text("MAPA - Módulo de Acompanhamento da Produção Acadêmica", color="WHITE", size=16, font_family="Roboto", weight=ft.FontWeight.W_500), # Título da AppBar
        center_title=True,
        bgcolor="#006BA0", # Cor de fundo da AppBar
        actions=[
            ft.Container( # Container para a logo
                content=ft.Image(
                    src="logo.png", # Caminho da logo
                    width=186,
                    height=40,
                    fit=ft.ImageFit.CONTAIN, 
                ),
                margin=ft.padding.all(5), # Margem do container
            )
        ]
    )

    # Barra de aplicativo inferior
    page.bottom_appbar = ft.BottomAppBar(
        height=50, 
        bgcolor="#006BA0", # Cor de fundo da BottomAppBar
        content=ft.ResponsiveRow(
            alignment=ft.MainAxisAlignment.CENTER, # Alinhamento do texto
            controls=[
                ft.Text(
                    "Desenvolvido pelo Núcleo de Inovação Tecnológica - Escola da Magistratura de Rondônia EMERON", # Texto da BottomAppBar
                    color="WHITE",
                    text_align="center"
                )
            ]
        )
    )

    # Campos de entrada de usuário e senha
    usuario_input = ft.TextField(label="Usuário", width=300, bgcolor="WHITE")
    senha_input = ft.TextField(label="Senha", password=True, width=300, bgcolor="WHITE")

    # Função para realizar o login
    def fazer_login(e):
        """
        Valida as credenciais do usuário e realiza o login.

        Args:
            e (ft.Event): O evento que acionou a função (clique no botão de login).
        """

        usuario = usuario_input.value
        senha = senha_input.value

        # Verifica se os campos de usuário e senha foram preenchidos
        if not usuario or not senha:
            mostrar_erro("Preencha todos os campos!")
            return

        # Valida as credenciais no banco de dados
        usuario_db = db.verificar_credenciais(usuario, senha)

        # Se as credenciais forem válidas
        if usuario_db:
            # Login bem-sucedido
            global perfil_usuario
            perfil_usuario = usuario_db['perfil']
            db.registrar_log(usuario, "login")  # Registra o log de login bem-sucedido

            # Limpa a página atual e exibe o menu principal
            page.controls.clear()
            exibir_menu_principal(usuario) 
            page.update()

            return usuario 
        # Se as credenciais forem inválidas
        else:
            mostrar_erro("Usuário ou senha inválidos!")
        page.update()

    # Função para exibir mensagens de erro
    def mostrar_erro(mensagem):
        """
        Exibe uma mensagem de erro em um diálogo.

        Args:
            mensagem (str): A mensagem de erro a ser exibida.
        """

        dlg = ft.AlertDialog(
            title=ft.Text("Erro"),
            content=ft.Text(mensagem),
            actions=[ft.TextButton("Ok", on_click=lambda e: fechar_dialogo(dlg))]
        )
        page.dialog = dlg
        dlg.open = True
        page.update()

    # Função para fechar o diálogo de erro
    def fechar_dialogo(dlg):
        """
        Fecha o diálogo de erro.

        Args:
            dlg (ft.AlertDialog): O diálogo de erro a ser fechado.
        """
        dlg.open = False
        page.update()

    # Botão de login
    botao_login = ft.ElevatedButton(text="Entrar", on_click=fazer_login, width=200, height=50, elevation=4, style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)), bgcolor="#006BA0", color=ft.colors.WHITE)

    # Imagem da logo
    img_logo = ft.Container(
        content=
        ft.Image(
            src="logo_img.png", # Caminho da imagem
            width=300,
            height=300,
            fit=ft.ImageFit.CONTAIN,
            border_radius=ft.border_radius.all(10)
        ),margin=ft.margin.only(bottom=20)
    )

    # Texto "ACESSO"
    nome_campo = ft.Text("ACESSO", size=16, color="#006BA0", font_family="Roboto", weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER)

    # Container principal da tela de login
    container = ft.Container(
        content=ft.Column(
            [
                img_logo, # Imagem da logo
                nome_campo, # Texto "ACESSO"
                usuario_input, # Campo de entrada de usuário
                senha_input, # Campo de entrada de senha
                botao_login, # Botão de login
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER, # Alinhamento horizontal
            alignment=ft.MainAxisAlignment.CENTER, # Alinhamento vertical
            scroll=ft.ScrollMode.ALWAYS, # Habilita a rolagem
        ),
        alignment=ft.alignment.center,  # Centraliza horizontalmente
        expand=False,  # Permite que o Container ocupe todo o espaço disponível
        bgcolor=ft.colors.BLUE_50, # Cor de fundo do container
        margin=ft.margin.only(top=20)
    )

    # Função para redimensionar a tela
    def on_resize(e):
        """
        Ajusta o layout da página quando a janela é redimensionada.

        Args:
            e (ft.Event): O evento de redimensionamento.
        """
        if page.width < 640: # Se a largura for menor que 640 pixels
            # Ajusta o título da AppBar
            page.appbar.title = ft.Text("MAPA - EMERON", color="WHITE", size=14, font_family="Roboto", weight=ft.FontWeight.W_500)
            
            # Ajusta o texto da BottomAppBar
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
        else: # Se a largura for maior ou igual a 640 pixels
            # Ajusta o título da AppBar
            page.appbar.title = ft.Text("Módulo de Acompanhamento da Produção Acadêmica - MAPA", color="WHITE", size=16, font_family="Roboto", weight=ft.FontWeight.W_500)
            # Ajusta o texto da BottomAppBar
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
        
    # Define o comportamento da página quando for redimensionada
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

# Função para realizar o logout
def sair(e, usuario, exibir_menu_principal):
    """
    Realiza o logout do usuário.

    Args:
        e (ft.Event): O evento que acionou a função (clique no botão de sair).
        usuario (str): O nome de usuário que está fazendo logout.
        exibir_menu_principal (function): Função para exibir o menu principal.
    """
    global perfil_usuario
    perfil_usuario = None # Define o perfil do usuário como None (deslogado)
    db.registrar_log(usuario, "logout") # Registra o log de logout
    
    # Limpa a página atual e exibe a tela de login
    e.page.controls.clear()
    exibir_tela_login(e.page, exibir_menu_principal) 
