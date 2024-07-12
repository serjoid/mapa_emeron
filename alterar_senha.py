import flet as ft
from database import Database

def def_alterar_senha(page: ft.Page, usuario_logado):
    """
    Define a função para alteração de senha do usuário.

    Args:
        page (ft.Page): A página onde a função está sendo utilizada.
        usuario_logado (str): O nome de usuário do usuário atualmente logado.

    Returns:
        ft.Container: Um container com os elementos da tela de alteração de senha.
    """
    
    db = Database() # Cria uma instância da classe Database para interação com o banco de dados

    # Define os campos de entrada para a alteração de senha
    senha_atual_input = ft.TextField(label="Senha Atual", password=True, width=800, bgcolor="WHITE")
    nova_senha_input = ft.TextField(label="Nova Senha", password=True, width=800, bgcolor="WHITE")
    confirmar_nova_senha_input = ft.TextField(label="Confirmar Nova Senha", password=True, width=800, bgcolor="WHITE")

    # Função para fechar o diálogo de alerta
    def fechar_dialogo(dlg):
        """
        Fecha o diálogo de alerta.

        Args:
            dlg (ft.AlertDialog): O diálogo de alerta a ser fechado.
        """
        dlg.open = False
        page.update()

    # Função para lidar com o evento de clique no botão "Alterar"
    def alterar_senha_clique(e):
        """
        Processa a alteração de senha quando o botão "Alterar" é clicado.

        Args:
            e (ft.Event): O evento de clique no botão.
        """

        # Obtém os valores dos campos de senha
        senha_atual = senha_atual_input.value
        nova_senha = nova_senha_input.value
        confirmar_nova_senha = confirmar_nova_senha_input.value

        # Valida se todos os campos foram preenchidos
        if not senha_atual or not nova_senha or not confirmar_nova_senha:
            mostrar_erro("Preencha todos os campos!")
            return

        # Valida se as novas senhas coincidem
        if nova_senha != confirmar_nova_senha:
            mostrar_erro("As novas senhas não coincidem!")
            return

        # Tenta alterar a senha no banco de dados
        if db.alterar_senha(usuario_logado, senha_atual, nova_senha):
            # Se a alteração for bem-sucedida, exibe uma mensagem de sucesso
            mostrar_sucesso("Senha alterada com sucesso!")
        else:
            # Se ocorrer um erro durante a alteração, exibe uma mensagem de erro
            mostrar_erro("Erro ao alterar a senha.")

        # Limpa os campos de entrada de senha após a tentativa de alteração
        senha_atual_input.value = ""
        nova_senha_input.value = ""
        confirmar_nova_senha_input.value = ""
        senha_atual_input.update()
        nova_senha_input.update()
        confirmar_nova_senha_input.update()

    # Função auxiliar para exibir mensagens de erro em um diálogo
    def mostrar_erro(mensagem):
        """
        Exibe uma mensagem de erro em um diálogo de alerta.

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

    # Função auxiliar para exibir mensagens de sucesso em um diálogo
    def mostrar_sucesso(mensagem):
        """
        Exibe uma mensagem de sucesso em um diálogo de alerta.

        Args:
            mensagem (str): A mensagem de sucesso a ser exibida.
        """
        dlg = ft.AlertDialog(
            title=ft.Text("Sucesso"),
            content=ft.Text(mensagem),
            actions=[ft.TextButton("Ok", on_click=lambda e: fechar_dialogo(dlg))]
        )
        page.dialog = dlg
        dlg.open = True
        page.update()

    # Define o botão "Alterar" para acionar a alteração de senha
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

    # Cria um divisor visual
    divisor = ft.ResponsiveRow(controls=[ft.Divider()], width=800)

    # Define o título da seção de alteração de senha
    nome_campo = ft.Text("ALTERAÇÃO DE SENHA DO USUÁRIO", size=16, color="#006BA0", font_family="Roboto", weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER)

    # Organiza os elementos da tela de alteração de senha em um container
    container = ft.Container(
        content=ft.Column(
            [
                nome_campo, # Título da seção
                divisor, # Divisor visual
                senha_atual_input, # Campo para inserir a senha atual
                nova_senha_input, # Campo para inserir a nova senha
                confirmar_nova_senha_input, # Campo para confirmar a nova senha
                botao_alterar, # Botão para confirmar a alteração
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER, # Centraliza os elementos horizontalmente
        ),
        #alignment=ft.alignment.center,
    )

    return container # Retorna o container com os elementos da tela de alteração de senha
