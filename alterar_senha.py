import flet as ft
from database import Database

def def_alterar_senha(page: ft.Page, usuario_logado):  # Recebe o usuário como argumento
    db = Database()

    # Campos de entrada
    senha_atual_input = ft.TextField(label="Senha Atual", password=True, width=800, bgcolor="WHITE")
    nova_senha_input = ft.TextField(label="Nova Senha", password=True, width=800, bgcolor="WHITE")
    confirmar_nova_senha_input = ft.TextField(label="Confirmar Nova Senha", password=True, width=800, bgcolor="WHITE")

    # Função para fechar o diálogo e atualizar a página
    def fechar_dialogo(dlg):
        dlg.open = False
        page.update()

    # Função para lidar com o clique no botão "Alterar"
    def alterar_senha_clique(e):
        senha_atual = senha_atual_input.value
        nova_senha = nova_senha_input.value
        confirmar_nova_senha = confirmar_nova_senha_input.value

        # Validação
        if not senha_atual or not nova_senha or not confirmar_nova_senha:
            mostrar_erro("Preencha todos os campos!")
            return

        if nova_senha != confirmar_nova_senha:
            mostrar_erro("As novas senhas não coincidem!")
            return

        # Atualiza a senha no banco de dados
        if db.alterar_senha(usuario_logado, senha_atual, nova_senha):
            mostrar_sucesso("Senha alterada com sucesso!")
        else:
            mostrar_erro("Erro ao alterar a senha.")

        # Limpa os campos de entrada
        senha_atual_input.value = ""
        nova_senha_input.value = ""
        confirmar_nova_senha_input.value = ""
        senha_atual_input.update()
        nova_senha_input.update()
        confirmar_nova_senha_input.update()

    # Função auxiliar para mostrar mensagens de erro
    def mostrar_erro(mensagem):
        dlg = ft.AlertDialog(
            title=ft.Text("Erro"),
            content=ft.Text(mensagem),
            actions=[ft.TextButton("Ok", on_click=lambda e: fechar_dialogo(dlg))]
        )
        page.dialog = dlg
        dlg.open = True
        page.update()

    # Função auxiliar para mostrar mensagens de sucesso
    def mostrar_sucesso(mensagem):
        dlg = ft.AlertDialog(
            title=ft.Text("Sucesso"),
            content=ft.Text(mensagem),
            actions=[ft.TextButton("Ok", on_click=lambda e: fechar_dialogo(dlg))]
        )
        page.dialog = dlg
        dlg.open = True
        page.update()

    # Botão "Alterar"
    botao_alterar = ft.ElevatedButton(
        text="Alterar",
        on_click=alterar_senha_clique,
        width=200,
        height=40,
        elevation=4,
        bgcolor="#006BA0",
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
        color="WHITE",
    )

    divisor = ft.ResponsiveRow(controls=[ft.Divider()], width=800)

    nome_campo = ft.Text("ALTERAÇÃO DE SENHA DO USUÁRIO", size=16, color="#006BA0", font_family="Roboto", weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER)

    # Container com a coluna centralizada
    container = ft.Container(
        content=ft.Column(
            [
                nome_campo,
                divisor,
                senha_atual_input,
                nova_senha_input,
                confirmar_nova_senha_input,
                botao_alterar,
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        #alignment=ft.alignment.center,
    )

    return container