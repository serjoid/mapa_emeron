import flet as ft
import home  # Importa o módulo 'home.py'
import acesso  # Importa o módulo 'acesso.py'
from database import Database  # Importa a classe 'Database' do módulo 'database.py'
import navegacao  # Importa o módulo 'navegacao.py'

# Inicializa a conexão com o banco de dados
db = Database()

# Declara a variável 'searchbar' como global, embora não seja utilizada neste código
global searchbar

# Define a função principal da aplicação
def main(page: ft.Page):
    """
    Função principal da aplicação Flet.

    Args:
        page (ft.Page): A página Flet atual.
    """

    # Define a cor de fundo da página
    page.bgcolor = ft.colors.BLUE_50

    # Define a função para exibir o menu principal após o login
    def exibir_menu_principal(usuario):
        """
        Exibe o menu principal da aplicação após o login.

        Args:
            usuario (str): O nome de usuário do usuário logado.
        """

        # Obtém o perfil do usuário logado a partir da variável global 'perfil_usuario' no módulo 'acesso'
        perfil_usuario = acesso.perfil_usuario

        # Cria os botões do menu principal

        botao_cadastro = ft.ElevatedButton(
            text="Cadastro",  # Texto do botão
            width=120,  # Largura do botão
            height=40,  # Altura do botão
            elevation=4,  # Elevação do botão
            bgcolor="#006BA0",  # Cor de fundo do botão
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),  # Estilo do botão (borda arredondada)
            content=ft.Column(  # Conteúdo do botão (coluna com texto centralizado)
                controls=[
                    ft.Text(
                        "Cadastro", size=12, color="WHITE", text_align=ft.TextAlign.CENTER  # Texto do botão
                    )
                ],
                alignment=ft.MainAxisAlignment.CENTER,  # Alinhamento vertical do conteúdo
            ),
            color="WHITE",  # Cor do texto do botão
            on_click=lambda e: navegacao.navegar(e, usuario, page, perfil_usuario),  # Função a ser chamada quando o botão for clicado (navega para a tela de cadastro)
            visible=(perfil_usuario == "Admin"),  # Visível apenas para usuários com perfil "Admin"
        )

        # Os outros botões seguem a mesma estrutura do botão 'botao_cadastro', com algumas variações:
        # - Texto do botão
        # - Função a ser chamada quando o botão for clicado (navega para a tela correspondente)
        # - Visibilidade do botão de acordo com o perfil do usuário

        botao_logs = ft.ElevatedButton(
            text="Logs",
            width=120,
            height=40,
            elevation=4,
            bgcolor="#006BA0",
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
            content=ft.Column(
                controls=[
                    ft.Text(
                        "Logs", size=12, color="WHITE", text_align=ft.TextAlign.CENTER
                    )
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            color="WHITE",
            on_click=lambda e: navegacao.navegar(e, usuario, page, perfil_usuario),
            visible=(perfil_usuario == "Admin"),
        )

        botao_alterar_senha = ft.ElevatedButton(
            text="Senha",
            width=120,
            height=40,
            elevation=4,
            bgcolor="#006BA0",
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
            content=ft.Column(
                controls=[
                    ft.Text(
                        "Senha", size=12, color="WHITE", text_align=ft.TextAlign.CENTER
                    )
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            color="WHITE",
            on_click=lambda e: navegacao.navegar(e, usuario, page, perfil_usuario),
            visible=usuario is not None,  # Visível apenas se o usuário estiver logado
        )

        botao_sair = ft.ElevatedButton(
            text="Sair",
            width=120,
            height=40,
            elevation=4,
            bgcolor="#D32F2F",  # Cor de fundo vermelha para o botão "Sair"
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
            content=ft.Column(
                controls=[
                    ft.Text(
                        "Sair", size=12, color="WHITE", text_align=ft.TextAlign.CENTER
                    )
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            color="WHITE",
            on_click=lambda e: acesso.sair(e, usuario, exibir_menu_principal),  # Chama a função 'sair' do módulo 'acesso' para realizar o logout
            visible=usuario is not None,  # Visível apenas se o usuário estiver logado
        )

        botao_submissoes = ft.ElevatedButton(
            text="Submissões",
            width=120,
            height=40,
            elevation=4,
            bgcolor="#006BA0",
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
            content=ft.Column(
                controls=[
                    ft.Text(
                        "Submissões",
                        size=12,
                        color="WHITE",
                        text_align=ft.TextAlign.CENTER,
                    )
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            color="WHITE",
            on_click=lambda e: navegacao.navegar(e, usuario, page, perfil_usuario),
        )

        botao_orientadores = ft.ElevatedButton(
            text="Orientadores",
            width=120,
            height=40,
            elevation=4,
            bgcolor="#006BA0",
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
            content=ft.Column(
                controls=[
                    ft.Text(
                        "Orientadores",
                        size=12,
                        color="WHITE",
                        text_align=ft.TextAlign.CENTER,
                    )
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            color="WHITE",
            on_click=lambda e: navegacao.navegar(e, usuario, page, perfil_usuario),
        )

        botao_cursos = ft.ElevatedButton(
            text="Cursos",
            width=120,
            height=40,
            elevation=4,
            bgcolor="#006BA0",
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
            content=ft.Column(
                controls=[
                    ft.Text(
                        "Cursos", size=12, color="WHITE", text_align=ft.TextAlign.CENTER
                    )
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            color="WHITE",
            on_click=lambda e: navegacao.navegar(e, usuario, page, perfil_usuario),
            visible=(perfil_usuario == "Admin"),  # Visível apenas para usuários com perfil "Admin"
        )

        botao_relatorios = ft.ElevatedButton(
            text="Relatórios",
            width=120,
            height=40,
            elevation=4,
            bgcolor="#006BA0",
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
            content=ft.Column(
                controls=[
                    ft.Text(
                        "Relatórios",
                        size=12,
                        color="WHITE",
                        text_align=ft.TextAlign.CENTER,
                    )
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            color="WHITE",
            on_click=lambda e: navegacao.navegar(e, usuario, page, perfil_usuario),
            visible=(perfil_usuario != "Aluno"),  # Visível apenas para usuários que não são "Aluno"
        )

        botao_inicio = ft.ElevatedButton(
            text="Início",
            width=120,
            height=40,
            elevation=4,
            bgcolor="#006BA0",
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
            content=ft.Column(
                controls=[
                    ft.Text(
                        "Início", size=12, color="WHITE", text_align=ft.TextAlign.CENTER
                    )
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            color="WHITE",
            on_click=lambda e: navegacao.navegar(e, usuario, page, perfil_usuario),
        )

        botao_alunos = ft.ElevatedButton(
            text="Alunos",
            width=120,
            height=40,
            elevation=4,
            bgcolor="#006BA0",
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
            content=ft.Column(
                controls=[
                    ft.Text(
                        "Alunos", size=12, color="WHITE", text_align=ft.TextAlign.CENTER
                    )
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            color="WHITE",
            on_click=lambda e: navegacao.navegar(e, usuario, page, perfil_usuario),
        )

        botao_andamento_pesquisa = ft.ElevatedButton(
            text="Andamento da Pesquisa",
            width=120,
            height=40,
            elevation=4,
            bgcolor="#006BA0",
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
            content=ft.Column(
                controls=[
                    ft.Text(
                        "Andamento\nda Pesquisa",  # Texto do botão em duas linhas
                        size=12,
                        color="WHITE",
                        text_align=ft.TextAlign.CENTER,
                    )
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            color="WHITE",
            on_click=lambda e: navegacao.navegar(e, usuario, page, perfil_usuario),
        )

        # Botões para links externos (EMERON, CEPEP, Biblioteca, Periódicos, Manual do Usuário)

        botao_emeron = ft.ElevatedButton(
            text="EMERON",
            width=120,
            height=40,
            elevation=4,
            bgcolor="#006BA0",
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
            content=ft.Column(
                controls=[
                    ft.Text(
                        "EMERON", size=12, color="WHITE", text_align=ft.TextAlign.CENTER
                    )
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            color="WHITE",
            on_click=lambda _: page.launch_url("https://emeron.tjro.jus.br/"),  # Abre o link da EMERON em uma nova aba
        )

        botao_cepep = ft.ElevatedButton(
            text="CEPEP",
            width=120,
            height=40,
            elevation=4,
            bgcolor="#006BA0",
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
            content=ft.Column(
                controls=[
                    ft.Text(
                        "CEPEP", size=12, color="WHITE", text_align=ft.TextAlign.CENTER
                    )
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            color="WHITE",
            on_click=lambda _: page.launch_url("https://emeron.tjro.jus.br/cepep"),  # Abre o link do CEPEP em uma nova aba
        )

        botao_biblioteca = ft.ElevatedButton(
            text="BIBLIOTECA",
            width=120,
            height=40,
            elevation=4,
            bgcolor="#006BA0",
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
            content=ft.Column(
                controls=[
                    ft.Text(
                        "BIBLIOTECA",
                        size=12,
                        color="WHITE",
                        text_align=ft.TextAlign.CENTER,
                    )
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            color="WHITE",
            on_click=lambda _: page.launch_url("https://emeron.tjro.jus.br/biblioteca"),  # Abre o link da Biblioteca em uma nova aba
        )

        botao_periodicos = ft.ElevatedButton(
            text="PERIÓDICOS",
            width=120,
            height=40,
            elevation=4,
            bgcolor="#006BA0",
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
            content=ft.Column(
                controls=[
                    ft.Text(
                        "PERIÓDICOS",
                        size=12,
                        color="WHITE",
                        text_align=ft.TextAlign.CENTER,
                    )
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            color="WHITE",
            on_click=lambda _: page.launch_url(
                "https://periodicos.emeron.edu.br/index.php/emeron"
            ),  # Abre o link dos Periódicos em uma nova aba
        )

        botao_manual = ft.ElevatedButton(
            text="Manual do Usuário",
            width=120,
            height=40,
            elevation=4,
            bgcolor="#006BA0",
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
            color="WHITE",
            content=ft.Column(
                controls=[
                    ft.Text(
                        "Manual\ndo Usuário",  # Texto do botão em duas linhas
                        size=12,
                        color="WHITE",
                        text_align=ft.TextAlign.CENTER,
                    )
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            on_click=lambda _: page.launch_url(
                "# INSIRA AQUI O LINK PARA O MANUAL DO SISTEMA"  # Substitua pelo link real do manual do sistema
            ),
        )

        botao_assistente = ft.ElevatedButton(
            text="Assistente",
            width=120,
            height=40,
            elevation=4,
            bgcolor="#006BA0",
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
            content=ft.Column(
                controls=[
                    ft.Text(
                        "Assistente",
                        size=12,
                        color="WHITE",
                        text_align=ft.TextAlign.CENTER,
                    )
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            color="WHITE",
            on_click=lambda e: navegacao.navegar(e, usuario, page, perfil_usuario),
        )

        # Cria o container do menu de navegação lateral
        menu_navegacao = ft.Container(
            width=160,
            height=900,
            padding=10,
            bgcolor=ft.colors.BLUE_50,  # Cor de fundo do menu
            border_radius=ft.border_radius.all(10),  # Borda arredondada
            content=ft.Column(  # Conteúdo do menu (coluna com os botões)
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,  # Alinhamento horizontal dos botões
                controls=[
                    ft.Text(  # Título do menu
                        "MENU",
                        size=16,
                        color="#006BA0",
                        font_family="Roboto",
                        weight=ft.FontWeight.BOLD,
                        text_align=ft.TextAlign.CENTER,
                    ),
                    ft.Divider(),  # Divisor visual
                    botao_inicio,  # Botão "Início"
                    botao_cursos,  # Botão "Cursos"
                    botao_orientadores,  # Botão "Orientadores"
                    botao_alunos,  # Botão "Alunos"
                    botao_relatorios,  # Botão "Relatórios"
                    botao_andamento_pesquisa,  # Botão "Andamento da Pesquisa"
                    botao_submissoes,  # Botão "Submissões"
                    botao_cadastro,  # Botão "Cadastro"
                    botao_logs,  # Botão "Logs"
                    botao_alterar_senha,  # Botão "Alterar Senha"
                    ft.Divider(),  # Divisor visual
                    botao_emeron,  # Botão "EMERON" (link externo)
                    botao_cepep,  # Botão "CEPEP" (link externo)
                    botao_biblioteca,  # Botão "Biblioteca" (link externo)
                    botao_periodicos,  # Botão "Periódicos" (link externo)
                    botao_manual,  # Botão "Manual do Usuário" (link externo)
                    ft.Divider(),  # Divisor visual
                    botao_sair,  # Botão "Sair"
                ],
            ),
            visible=True,  # O menu é inicialmente visível
        )

        # Cria o container para o conteúdo principal da página
        conteudo_container = ft.Container(
            expand=True,  # Permite que o container se expanda para preencher o espaço disponível
            height=900,  # Altura do container
            padding=10,  # Espaçamento interno do container
            bgcolor=ft.colors.BLUE_50,  # Cor de fundo do container
            border_radius=ft.border_radius.all(10),  # Borda arredondada
        )

        # Define a função para ocultar/exibir o menu de navegação
        def oculta_navegacao(e):
            """
            Oculta ou exibe o menu de navegação lateral.

            Args:
                e (ft.Event): O evento que acionou a função (clique no botão do menu).
            """
            menu_navegacao.visible = not menu_navegacao.visible  # Inverte a visibilidade do menu
            menu_navegacao.update()  # Atualiza o menu na tela

        # Configurações da página
        page.title = "MAPA - EMERON"  # Define o título da página
        page.theme_mode = "LIGHT"  # Define o tema da página como claro
        page.assets_dir = "assets"  # Define o diretório de assets da página
        page.appbar = ft.AppBar(  # Define a barra de aplicativo superior
            leading=ft.IconButton(  # Botão de menu (ícone de livro)
                ft.icons.BOOK, icon_color="WHITE", on_click=oculta_navegacao  # Chama a função 'oculta_navegacao' quando o botão for clicado
            ),
            leading_width=40,  # Largura do botão de menu
            toolbar_height=40,  # Altura da barra de aplicativo
            title=ft.Text(  # Título da barra de aplicativo
                "Módulo de Acompanhamento da Produção Acadêmica - MAPA",
                color="WHITE",
                size=16,
                font_family="Roboto",
                weight=ft.FontWeight.W_500,  # Define o peso da fonte como médio
            ),
            center_title=True,  # Centraliza o título na barra de aplicativo
            bgcolor="#006BA0",  # Cor de fundo da barra de aplicativo
            actions=[
                ft.Container(  # Container para a logo da EMERON
                    content=ft.Image(  # Imagem da logo
                        src="logo.png", width=186, height=40, fit=ft.ImageFit.CONTAIN  # Define a imagem, largura, altura e ajuste
                    ),
                    margin=ft.margin.only(right=20),  # Define a margem do container
                )
            ],
        )

        page.scroll = True  # Habilita a rolagem da página

        # Cria o layout principal da página (menu lateral + conteúdo)
        menu_principal = ft.Container(
            ft.Column(
                controls=[
                    ft.Row(  # Linha com o menu lateral e o conteúdo
                        vertical_alignment=ft.CrossAxisAlignment.START,  # Alinhamento vertical dos elementos da linha
                        controls=[menu_navegacao, conteudo_container],  # Adiciona o menu lateral e o container de conteúdo à linha
                    )
                ],
                scroll=ft.ScrollMode.ALWAYS,  # Habilita a rolagem da coluna
            )
        )

        # Limpa a página e adiciona o layout principal
        page.controls.clear()
        page.add(menu_principal)
        page.update()

        # Define o conteúdo inicial do container de conteúdo como a tela inicial
        conteudo_container.content = home.tela_inicial(page)
        conteudo_container.update()

        # Define a função para lidar com o evento de redimensionamento da tela
        def on_resize(e):
            """
            Ajusta o layout da página quando a janela é redimensionada.

            Args:
                e (ft.Event): O evento de redimensionamento.
            """
            # Se a largura da tela for menor que 640 pixels, oculta o menu lateral e ajusta o título da barra de aplicativo
            if page.width < 640:
                menu_navegacao.visible = False
                page.appbar.title = ft.Text(
                    "MAPA - EMERON",
                    color="WHITE",
                    size=16,
                    font_family="Roboto",
                    weight=ft.FontWeight.W_500,
                )
            # Caso contrário, exibe o menu lateral e define o título completo da barra de aplicativo
            else:
                menu_navegacao.visible = True
                page.appbar.title = ft.Text(
                    "Módulo de Acompanhamento da Produção Acadêmica - MAPA",
                    color="WHITE",
                    size=16,
                    font_family="Roboto",
                    weight=ft.FontWeight.W_500,
                )
            page.update()  # Atualiza a página para exibir as alterações

        # Define a visibilidade inicial do menu lateral e o título da barra de aplicativo de acordo com a largura da tela
        if page.width < 640:
            menu_navegacao.visible = False
            page.appbar.title = ft.Text(
                "MAPA - EMERON",
                color="WHITE",
                size=16,
                font_family="Roboto",
                weight=ft.FontWeight.W_500,
            )
        else:
            menu_navegacao.visible = True
            page.appbar.title = ft.Text(
                "Módulo de Acompanhamento da Produção Acadêmica - MAPA",
                color="WHITE",
                size=16,
                font_family="Roboto",
                weight=ft.FontWeight.W_500,
            )
        page.update()  # Atualiza a página

        # Define a função 'on_resize' como a função a ser chamada quando a tela for redimensionada
        page.on_resize = on_resize

    # Exibe a tela de login ao iniciar a aplicação
    acesso.exibir_tela_login(page, exibir_menu_principal)

# Inicia a aplicação Flet
ft.app(target=main, view=ft.AppView.WEB_BROWSER, port=4253)
