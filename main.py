import flet as ft
import home
import acesso
from database import Database
import navegacao

db = Database()
global searchbar

def main(page: ft.Page):
    page.bgcolor = ft.colors.BLUE_50

    def exibir_menu_principal(usuario):
        perfil_usuario = acesso.perfil_usuario  # Obtém o perfil do usuário logado

        botao_cadastro = ft.ElevatedButton(
            text="Cadastro",
            width=120,
            height=40,
            elevation=4,
            bgcolor="#006BA0",
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
            content=ft.Column(
                controls=[
                    ft.Text(
                        "Cadastro", size=12, color="WHITE", text_align=ft.TextAlign.CENTER
                    )
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            color="WHITE",
            on_click=lambda e: navegacao.navegar(e, usuario, page, perfil_usuario),  # Usa a variável local
            visible=(perfil_usuario == "Admin"),
        )

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
            on_click=lambda e: navegacao.navegar(e, usuario, page, perfil_usuario),  # Usa a variável local
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
            on_click=lambda e: navegacao.navegar(e, usuario, page, perfil_usuario),  # Usa a variável local
            visible=usuario is not None,
        )

        botao_sair = ft.ElevatedButton(
            text="Sair",
            width=120,
            height=40,
            elevation=4,
            bgcolor="#D32F2F",
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
            on_click=lambda e: acesso.sair(e, usuario, exibir_menu_principal),
            visible=usuario is not None,
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
            on_click=lambda e: navegacao.navegar(e, usuario, page, perfil_usuario),  # Usa a variável local
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
            on_click=lambda e: navegacao.navegar(e, usuario, page, perfil_usuario),  # Usa a variável local
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
            on_click=lambda e: navegacao.navegar(e, usuario, page, perfil_usuario),  # Usa a variável local
            visible=(perfil_usuario == "Admin"),
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
            on_click=lambda e: navegacao.navegar(e, usuario, page, perfil_usuario),  # Usa a variável local
            visible=(perfil_usuario != "Aluno"),
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
            on_click=lambda e: navegacao.navegar(e, usuario, page, perfil_usuario),  # Usa a variável local
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
            on_click=lambda e: navegacao.navegar(e, usuario, page, perfil_usuario),  # Usa a variável local
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
                        "Andamento\nda Pesquisa",
                        size=12,
                        color="WHITE",
                        text_align=ft.TextAlign.CENTER,
                    )
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            color="WHITE",
            on_click=lambda e: navegacao.navegar(e, usuario, page, perfil_usuario),  # Usa a variável local
        )

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
            on_click=lambda _: page.launch_url("https://emeron.tjro.jus.br/"),
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
            on_click=lambda _: page.launch_url("https://emeron.tjro.jus.br/cepep"),
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
            on_click=lambda _: page.launch_url("https://emeron.tjro.jus.br/biblioteca"),
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
            ),
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
                        "Manual\ndo Usuário",
                        size=12,
                        color="WHITE",
                        text_align=ft.TextAlign.CENTER,
                    )
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            on_click=lambda _: page.launch_url(
                "# INSIRA AQUI O LINK PARA O MANUAL DO SISTEMA"
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
            on_click=lambda e: navegacao.navegar(e, usuario, page, perfil_usuario),  # Usa a variável local
        )

        menu_navegacao = ft.Container(
            width=160,
            height=900,
            padding=10,
            bgcolor=ft.colors.BLUE_50,
            border_radius=ft.border_radius.all(10),
            content=ft.Column(
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Text(
                        "MENU",
                        size=16,
                        color="#006BA0",
                        font_family="Roboto",
                        weight=ft.FontWeight.BOLD,
                        text_align=ft.TextAlign.CENTER,
                    ),
                    ft.Divider(),
                    botao_inicio,
                    botao_cursos,
                    botao_orientadores,
                    botao_alunos,
                    botao_relatorios,
                    botao_andamento_pesquisa,
                    botao_submissoes,
                    botao_cadastro,
                    botao_logs,
                    botao_alterar_senha,
                    ft.Divider(),
                    botao_emeron,
                    botao_cepep,
                    botao_biblioteca,
                    botao_periodicos,
                    botao_manual,
                    ft.Divider(),
                    botao_sair,
                ],
            ),
            visible=True,  # Inicialmente visível
        )

        conteudo_container = ft.Container(
            expand=True,
            height=900,
            padding=10,
            bgcolor=ft.colors.BLUE_50,
            border_radius=ft.border_radius.all(10),
        )

        def oculta_navegacao(e):
            menu_navegacao.visible = not menu_navegacao.visible
            menu_navegacao.update()

        page.title = "MAPA - EMERON"
        page.theme_mode = "LIGHT"
        page.assets_dir = "assets"
        page.appbar = ft.AppBar(
            leading=ft.IconButton(
                ft.icons.BOOK, icon_color="WHITE", on_click=oculta_navegacao
            ),
            leading_width=40,
            toolbar_height=40,
            title=ft.Text(
                "Módulo de Acompanhamento da Produção Acadêmica - MAPA",
                color="WHITE",
                size=16,
                font_family="Roboto",
                weight=ft.FontWeight.W_500,
            ),
            center_title=True,
            bgcolor="#006BA0",
            actions=[
                ft.Container(
                    content=ft.Image(
                        src="logo.png", width=186, height=40, fit=ft.ImageFit.CONTAIN
                    ),
                    margin=ft.margin.only(right=20),
                )
            ],
        )

        page.scroll = True

        menu_principal = ft.Container(
            ft.Column(
                controls=[
                    ft.Row(
                        vertical_alignment=ft.CrossAxisAlignment.START,
                        controls=[menu_navegacao, conteudo_container],
                    )
                ],
                scroll=ft.ScrollMode.ALWAYS,
            )
        )

        page.controls.clear()
        page.add(menu_principal)
        page.update()

        conteudo_container.content = home.tela_inicial(page)
        conteudo_container.update()

        def on_resize(e):
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
            page.update()

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
        page.update()

        page.on_resize = on_resize

    acesso.exibir_tela_login(page, exibir_menu_principal)

ft.app(target=main, view=ft.AppView.WEB_BROWSER, port=4253)
