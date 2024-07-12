import flet as ft
from database import Database

def tela_logs(page: ft.Page):
    db = Database()
    logs = []  # Lista para armazenar os logs

    # Campo de pesquisa
    txt_pesquisa = ft.TextField(label="Pesquisar nos logs", width=300)

    def carregar_logs(e):
        nonlocal logs
        logs = db.consultar_logs()
        filtrar_logs()

    def filtrar_logs(e=None):
        termo_pesquisa = txt_pesquisa.value.lower() if txt_pesquisa.value else ""
        coluna_logs.controls.clear()
        for log in logs:
            acao = log.get('acao', 'N/A')
            data = log.get('data_hora', 'N/A')
            usuario = log.get('usuario', 'N/A')
            detalhes = log.get('detalhes', 'N/A')

            if termo_pesquisa in str(log).lower():
                log_texto = ft.SelectionArea(
                    content=ft.Text(
                        f"Ação: {acao}\nData e hora: {data}\nUsuário: {usuario}\nDetalhes: {detalhes}\n-------------------"
                    )
                )
                coluna_logs.controls.append(log_texto)

        coluna_logs.update()
        page.update()

    botao_carregar_logs = ft.ElevatedButton(
        text="Carregar Logs",
        on_click=carregar_logs,
        width=200,
        height=40,
        elevation=4,
        bgcolor="#006BA0",
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
        color="WHITE",
    )

    coluna_logs = ft.Column()

    divisor = ft.ResponsiveRow(controls=[ft.Divider()], width=800)

    nome_campo = ft.Text("Logs do sistema", size=16, color="#006BA0", font_family="Roboto", weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER)

    container = ft.Container(
        content=ft.Column(
            [
                nome_campo,
                divisor,
                txt_pesquisa,  # Campo de pesquisa
                botao_carregar_logs,
                ft.ResponsiveRow(controls=[coluna_logs], width = 800),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            scroll=ft.ScrollMode.ALWAYS,
        ),
    )

    return container
