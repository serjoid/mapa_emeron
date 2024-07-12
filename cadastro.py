import flet as ft
from database import Database

# Define a função para exibir a tela de cadastro de usuários
def tela_cadastro(page: ft.Page, usuario_logado):
    """
    Exibe a tela de cadastro de novos usuários.

    Args:
        page (ft.Page): A página Flet atual.
        usuario_logado (str): O nome de usuário do administrador logado.
    """

    # Cria uma instância da classe Database para interação com o banco de dados
    db = Database()

    # Variável global para armazenar os usuários
    global usuarios
    usuarios = []

    # Define os campos de entrada para as informações do usuário
    nome_dropdown = ft.Dropdown(width=800, label="Nome", visible=False, bgcolor="WHITE") # Dropdown para selecionar o nome do usuário (visível apenas para perfis "Orientador" e "Aluno")
    nome_input = ft.TextField(label="Nome", width=800, bgcolor="WHITE") # Campo de texto para inserir o nome do usuário (visível para outros perfis)
    email_input = ft.TextField(label="Email", width=800, bgcolor="WHITE") # Campo de texto para inserir o email do usuário
    usuario_input = ft.TextField(label="Usuário", width=800, bgcolor="WHITE", read_only=False) # Campo de texto para inserir o nome de usuário (preenchido automaticamente com o email)
    senha_input = ft.TextField(label="Senha", password=True, width=800, bgcolor="WHITE") # Campo de texto para inserir a senha do usuário
    confirmacao_senha_input = ft.TextField(label="Confirmar Senha", password=True, width=800, bgcolor="WHITE") # Campo de texto para confirmar a senha do usuário

    # Dropdown para selecionar o perfil do usuário
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
        on_change=lambda e: atualizar_campos_nome(e) # Define a função a ser chamada quando o valor do dropdown for alterado
    )

    # Função para atualizar os campos de nome de acordo com o perfil selecionado
    def atualizar_campos_nome(e):
        """Atualiza a visibilidade dos campos de nome (dropdown e input) de acordo com o perfil selecionado."""
        perfil_selecionado = perfil_dropdown.value
        if perfil_selecionado == "Orientador":
            # Se o perfil for "Orientador", carrega os nomes dos orientadores no dropdown
            nome_dropdown.options = [ft.dropdown.Option(nome) for nome in db.get_orientador()]
            nome_dropdown.visible = True
            nome_input.visible = False
        elif perfil_selecionado == "Aluno":
            # Se o perfil for "Aluno", carrega os nomes dos alunos no dropdown
            nome_dropdown.options = [ft.dropdown.Option(nome) for nome in db.get_aluno()]
            nome_dropdown.visible = True
            nome_input.visible = False
        else:
            # Para outros perfis, exibe o campo de texto para inserir o nome
            nome_dropdown.visible = False
            nome_input.visible = True

        # Atualiza os campos na tela
        nome_dropdown.update()
        nome_input.update()
        page.update()

    # Função para lidar com o clique no botão "Cadastrar"
    def cadastrar_clique(e):
        """Cadastra um novo usuário no banco de dados."""

        # Obtém os valores dos campos de entrada
        nome = nome_dropdown.value if nome_dropdown.visible else nome_input.value
        email = email_input.value
        usuario_input.value = email  # Preenche o campo "Usuário" com o valor do campo "Email"
        senha = senha_input.value
        confirmacao_senha = confirmacao_senha_input.value
        perfil = perfil_dropdown.value

        # Atualiza a página para exibir o valor do campo "Usuário"
        page.update()

        # Valida se todos os campos foram preenchidos
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

        # Valida se as senhas coincidem
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

        # Registra o log do cadastro do usuário
        log_detalhes = f"Nome: {nome}, Email: {email}, Usuário: {email}, Perfil: {perfil}"
        db.registrar_log(usuario_logado, "cadastrar_usuario", log_detalhes)

        # Cadastra o usuário no banco de dados
        db.cadastrar_usuario(nome, email, email, senha, perfil)

        # Exibe um diálogo de sucesso
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

        # Limpa os campos de entrada após o cadastro
        nome_input.value = ""
        email_input.value = ""
        usuario_input.value = ""
        senha_input.value = ""
        confirmacao_senha_input.value = ""
        perfil_dropdown.value = None
        nome_dropdown.value = None
        page.update()

    # Função para fechar um diálogo
    def fechar_dialogo(dlg):
        """Fecha o diálogo."""
        dlg.open = False
        page.update()

    # Função para lidar com o clique no botão "Excluir" de um usuário
    def excluir_usuario_clique(e, usuario_excluido):
        """Exclui um usuário do banco de dados."""
        # Obtém as informações de todos os usuários do banco de dados
        usuarios_info = db.consultar_usuarios()
        # Encontra as informações do usuário a ser excluído
        usuario_info = next((u for u in usuarios_info if u['usuario'] == usuario_excluido), None)
        # Verifica se o usuário foi encontrado
        if not usuario_info:
            # Se o usuário não for encontrado, exibe uma mensagem de erro
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

        # Extrai as informações do usuário
        nome = usuario_info['nome']
        email = usuario_info['email']
        perfil = usuario_info['perfil']

        # Define a função para confirmar a exclusão do usuário
        def confirmar_exclusao(e):
            """Exclui o usuário do banco de dados e registra a ação no log."""
            # Exclui o usuário do banco de dados
            resultado = db.excluir_usuario(usuario_excluido)
            # Registra a ação no log
            log_detalhes = f"Nome: {nome}, Email: {email}, Usuário: {usuario_excluido}, Perfil: {perfil}"
            db.registrar_log(usuario_logado, "excluir_usuario", log_detalhes)
            
            # Exibe um diálogo de sucesso
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

            # Atualiza a lista de usuários na tela
            carregar_usuarios(e)

        # Exibe um diálogo de confirmação de exclusão
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

    # Função para carregar os usuários do banco de dados e exibi-los na tela
    def carregar_usuarios(e):
        """Carrega os usuários do banco de dados e os exibe na tela."""
        global usuarios # Acessa a variável global
        usuarios = db.consultar_usuarios() # Obtém a lista de usuários do banco de dados
        filtrar_usuarios() # Filtra os usuários de acordo com o termo de pesquisa

    # Função para filtrar os usuários de acordo com o termo de pesquisa
    def filtrar_usuarios(e=None):
        """Filtra os usuários de acordo com o termo de pesquisa e os exibe na tela."""
        termo_pesquisa = txt_pesquisa.value.lower() if txt_pesquisa.value else "" # Obtém o termo de pesquisa do campo de texto
        colunas_usuarios.controls.clear() # Limpa a lista de usuários na tela

        # Itera sobre a lista de usuários
        for usuario in usuarios:
            nome = usuario.get('nome', 'N/A') # Obtém o nome do usuário
            email = usuario.get('email', 'N/A') # Obtém o email do usuário
            user = usuario.get('usuario', 'N/A') # Obtém o nome de usuário
            perfil = usuario.get('perfil', 'N/A') # Obtém o perfil do usuário

            # Verifica se o termo de pesquisa está presente nas informações do usuário
            if termo_pesquisa in str(usuario).lower():
                # Cria um texto com as informações do usuário
                usuario_texto = ft.SelectionArea(
                    content=ft.Text(
                        f"Nome: {nome}\nEmail: {email}\nUsuário: {user}\nPerfil: {perfil}\n-------------------"
                    )
                )
                # Cria um botão para excluir o usuário
                excluir_botao = ft.IconButton(ft.icons.DELETE, icon_color="RED", on_click=lambda e, usuario=user: excluir_usuario_clique(e, usuario))
                # Adiciona o texto e o botão de excluir à lista de usuários na tela
                colunas_usuarios.controls.append(ft.Row([usuario_texto, excluir_botao]))

        # Atualiza a lista de usuários na tela
        colunas_usuarios.update()
        page.update()

    # Campo de texto para pesquisar usuários
    txt_pesquisa = ft.TextField(label="Pesquisar usuários", width=300)
    # Botão para carregar a lista de usuários
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
    # Botão para cadastrar um novo usuário
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

    # Divisor visual
    divisor = ft.Divider()

    # Título da seção de cadastro de usuário
    nome_campo = ft.Text("CADASTRO DE NOVO USUÁRIO", size=16, color="#006BA0", font_family="Roboto", weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER)

    # Coluna para exibir os usuários
    colunas_usuarios = ft.Column()

    # Container principal da tela de cadastro
    container = ft.Container(
        content=ft.Column(
            [
                nome_campo, # Título da seção
                divisor, # Divisor visual
                perfil_dropdown, # Dropdown para selecionar o perfil do usuário
                nome_dropdown, # Dropdown para selecionar o nome do usuário (visível apenas para perfis "Orientador" e "Aluno")
                nome_input, # Campo de texto para inserir o nome do usuário (visível para outros perfis)
                email_input, # Campo de texto para inserir o email do usuário
                senha_input, # Campo de texto para inserir a senha do usuário
                confirmacao_senha_input, # Campo de texto para confirmar a senha do usuário
                botao_cadastrar, # Botão para cadastrar o usuário
                txt_pesquisa, # Campo de texto para pesquisar usuários
                botao_carregar_usuarios, # Botão para carregar a lista de usuários
                ft.ResponsiveRow(controls=[colunas_usuarios], width=800), # Linha para exibir a lista de usuários
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER, # Alinhamento horizontal dos elementos
            scroll=ft.ScrollMode.ALWAYS, # Habilita a rolagem da tela
        ),
    )

    # Retorna o container principal da tela
    return container
