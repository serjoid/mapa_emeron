import flet as ft
from database import Database


def tela_orientador_logado(page: ft.Page, usuario):
    """
    Exibe as informações do orientador logado e a lista de seus orientandos.

    Args:
        page (ft.Page): A página Flet atual.
        usuario (str): O nome de usuário do orientador logado.
    """

    db = Database()
    cursos = db.get_curso()

    # Obtém as informações do orientador logado do banco de dados
    orientador_info = db.get_orientador_info_por_usuario(usuario)

    global orientador_id  # Declare orientador_id como global aqui

    # Verifica se o orientador foi encontrado
    if not orientador_info:
        # Se o orientador não for encontrado, exiba uma mensagem de erro
        print("Erro: Usuário não encontrado como orientador.")
        page.add(ft.Text("Erro: Você não tem permissão para acessar esta página."))
        return

    # Extrai as informações do orientador
    orientador_id = orientador_info['id']
    nome_orientador = orientador_info['nome']
    email = orientador_info['email']
    curso = orientador_info['curso']
    titulacao = orientador_info['titulacao']
    instituicao = orientador_info['instituicao']
    vinculo = orientador_info['vinculo']
    polo = orientador_info['polo']
    uf_instituicao = orientador_info['uf_instituicao']
    lattes = orientador_info['lattes']
    telefone = orientador_info['telefone']

    # Função para abrir o WhatsApp
    def abrir_whatsapp(telefone):
        if telefone:
            page.launch_url(
                f"https://wa.me/55{telefone.replace(' ', '').replace('-', '')}"
            )

    # Definição dos campos
    nome_field = ft.TextField(label="Nome", width=800, height=50, read_only=True, value=nome_orientador, bgcolor="WHITE")
    telefone_field = ft.TextField(
        label="Telefone (Com DDD, somente números)",
        width=650,
        height=75,
        read_only=True,
        value=telefone,
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
    email_field = ft.TextField(label="Email", width=800, height=50, read_only=True, value=email, bgcolor="WHITE")
    curso_field = ft.TextField(label="Curso", width=800, height=50, read_only=True, value=curso, bgcolor="WHITE")
    titulacao_field = ft.TextField(label="Titulação", width=800, height=50, read_only=True, value=titulacao, bgcolor="WHITE")
    instituicao_field = ft.TextField(label="Instituição", width=800, height=50, read_only=True, value=instituicao, bgcolor="WHITE")
    vinculo_field = ft.TextField(label="Vínculo", width=800, height=50, read_only=True, value=vinculo, bgcolor="WHITE")
    polo_field = ft.TextField(label="Polo", width=800, height=50, read_only=True, value=polo, bgcolor="WHITE")
    uf_instituicao_field = ft.TextField(label="UF da instituição", width=800, height=50, read_only=True, value=uf_instituicao, bgcolor="WHITE")
    lattes_field = ft.TextField(
        label="Lattes",
        width=650,
        height=50,
        read_only=True,
        value=lattes,
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
    ]

    # Criando o ListView para os orientandos
    orientandos_view = ft.ListView()

    # Usa nome_orientador para buscar os orientandos
    orientandos = db.get_orientando(nome_orientador)

    # Adiciona cada orientando ao ListView
    for orientando in orientandos:
        orientandos_view.controls.append(ft.ListTile(title=ft.Text(orientando)))

    # Diálogos de Confirmação
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

    def fechar_dialogo_atualizar(e):
        dlg_confirmacao_atualizar.open = False
        for field in lista_textfields:
            field.read_only = True
            field.bgcolor = ft.colors.WHITE  # Reseta a cor para branco
        telefone_field.read_only = True
        telefone_field.bgcolor = ft.colors.WHITE  # Reseta a cor para branco
        lattes_field.read_only = True
        lattes_field.bgcolor = ft.colors.WHITE  # Reseta a cor para branco
        nome_field.bgcolor = ft.colors.WHITE  # Reseta a cor para branco
        # Retornando a visibilidade dos botões para o estado inicial
        botao_atualizar_orientador.visible = True
        botao_salvar.visible = False
        page.update()

    # Funções dos botões
    def atualizar_orientador(e):
        global orientador_id
        orientador_info = db.get_orientador_info_por_usuario(usuario)
        for field in lista_textfields:
            if field != nome_field:  # Libera todos os campos, exceto o nome
                field.read_only = False
                field.bgcolor = ft.colors.WHITE  # Define a cor como branca
                nome_field.bgcolor = ft.colors.WHITE  # Reseta a cor para branco
            if field != nome_field:  # Define a cor como cinza claro se read_only
                field.bgcolor = ft.colors.GREY_200 if field.read_only else ft.colors.WHITE
        telefone_field.read_only = False
        telefone_field.bgcolor = ft.colors.WHITE  # Define a cor como branca
        lattes_field.read_only = False
        lattes_field.bgcolor = ft.colors.WHITE  # Define a cor como branca
        # EXCEÇÕES QUE O ORIENTADOR NÃO PODE ATUALIZAR
        instituicao_field.read_only = True
        polo_field.read_only = True
        uf_instituicao_field.read_only = True
        vinculo_field.read_only = True
        curso_field.read_only = True
        # Define a cor como cinza claro para os campos read_only
        nome_field.bgcolor = ft.colors.GREY_200
        instituicao_field.bgcolor = ft.colors.GREY_200 
        polo_field.bgcolor = ft.colors.GREY_200
        uf_instituicao_field.bgcolor = ft.colors.GREY_200
        vinculo_field.bgcolor = ft.colors.GREY_200
        curso_field.bgcolor = ft.colors.GREY_200
        botao_salvar.visible = True
        botao_atualizar_orientador.visible = False
        page.update()

    def save_orientador(e):
        page.dialog = dlg_confirmacao_atualizar
        dlg_confirmacao_atualizar.open = True
        page.update()

    def atualizar_orientador_confirmado(e):
        global perfil_usuario  
        orientador_data = {
            "nome": nome_field.value,
            "telefone": telefone_field.value,
            "email": email_field.value,
            "curso": curso_field.value,  
            "titulacao": titulacao_field.value,
            "instituicao": instituicao_field.value,
            "vinculo": vinculo_field.value,  
            "polo": polo_field.value,  
            "uf_instituicao": uf_instituicao_field.value,  
            "lattes": lattes_field.value,
            "id": orientador_id,  
        }
        # Utiliza o método get_pessoa_info_por_usuario para obter o valor original
        valor_original_dict = db.get_pessoa_info_por_usuario(usuario)  
        # Gera a string com as alterações para o log
        alteracoes = []
        for chave, valor in orientador_data.items():
            if chave != "id" and valor_original_dict:  
                valor_original = valor_original_dict.get(chave)  
                if valor != valor_original:
                    alteracoes.append(f"{chave}: {valor_original} -> {valor}")  
        log_mensagem = f"Orientador: {orientador_data['nome']}"
        if alteracoes:
            log_mensagem += f" - Alterações: {', '.join(alteracoes)}"
        # Chamar o método de atualização da DAO
        db.update_orientador(orientador_data)
        db.registrar_log(
            usuario,
            "atualizar_orientador",
            log_mensagem,
        )  # Registra o log com as alterações
        dlg_confirmacao_atualizar.open = False
        page.snack_bar = ft.SnackBar(ft.Text("Orientador atualizado com sucesso!"))
        page.snack_bar.open = True
        # Retornando a visibilidade dos campos para o estado inicial
        vinculo_field.visible = True
        polo_field.visible = True
        uf_instituicao_field.visible = True
        # Desabilitando a edição dos campos
        for field in lista_textfields:
            field.read_only = True
            field.bgcolor = ft.colors.WHITE # Reseta a cor para branco
        telefone_field.read_only = True
        telefone_field.bgcolor = ft.colors.WHITE # Reseta a cor para branco
        lattes_field.read_only = True
        lattes_field.bgcolor = ft.colors.WHITE # Reseta a cor para branco
        nome_field.bgcolor = ft.colors.WHITE
        # Retornando a visibilidade dos botões para o estado inicial
        botao_atualizar_orientador.visible = True
        botao_salvar.visible = False
        page.update()

    # Botões
    botao_atualizar_orientador = ft.ElevatedButton(
        text="Atualizar cadastro",
        width=185,
        height=40,
        bgcolor="#006BA0",
        color="WHITE",
        on_click=atualizar_orientador,
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
    )
    botao_salvar = ft.ElevatedButton(
        text="Salvar",
        width=185,
        height=40,
        bgcolor="#006BA0",
        color="WHITE",
        on_click=save_orientador,
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
        visible=False,  # Inicialmente invisível
    )

    # Containers
    container_botoes = ft.Container(
        width=800,
        content=ft.ResponsiveRow(
            alignment=ft.MainAxisAlignment.END,
            controls=[
                botao_atualizar_orientador,
                botao_salvar,
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

    nome_campo = ft.Text("DADOS CADASTRAIS - ORIENTADOR", size=16, color="#006BA0", font_family="Roboto", weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER)

    container_orientador = ft.Container(
        expand=True,
        content=ft.Column(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            scroll=ft.ScrollMode.ALWAYS,
            controls=[
                    nome_campo,
                    ft.Divider(),
                    container_botoes,
                    nome_field,
                    ft.ResponsiveRow(controls=[telefone_field, telefone_icon], width=800),
                    email_field,
                    curso_field,
                    titulacao_field,
                    instituicao_field,
                    vinculo_field,
                    polo_field,
                    uf_instituicao_field,
                    ft.ResponsiveRow(controls=[lattes_field, lattes_icon], width=800),
                    container_listview,
                    ],
                ),
                margin=ft.margin.only(bottom=20),
            )

    return container_orientador