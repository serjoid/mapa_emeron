import flet as ft
from database import Database

def orientador_aluno_logado(page: ft.Page, usuario):
    """
    Exibe as informações do orientador do aluno logado.

    Args:
        page (ft.Page): A página Flet atual.
        usuario (str): O nome de usuário do aluno logado.
    """

    db = Database()

    # Obtém as informações do aluno logado do banco de dados
    aluno_info = db.get_pessoa_info_por_usuario(usuario)

    if not aluno_info:
        # Se o aluno não for encontrado, exiba uma mensagem de erro
        page.add(ft.Text("Erro: Aluno não encontrado."))
        return

    # Obtém o nome do orientador do aluno
    nome_orientador = aluno_info['orientador']

    # Obtém as informações do orientador do banco de dados
    orientador_info = db.get_orientador_info(nome_orientador)

    if not orientador_info:
        # Se o orientador não for encontrado, exiba uma mensagem de erro
        page.add(ft.Text("Erro: Orientador não encontrado."))
        return
    
    # FUNÇÃO PARA LINK API WHATSAPP
    def abrir_whatsapp(telefone):
        if telefone:
            page.launch_url(f"https://wa.me/55{telefone.replace(' ', '').replace('-', '')}")

    # TEXTFIELDS

    # Extrai as informações do orientador
    telefone = orientador_info['telefone']
    email = orientador_info['email']
    curso = orientador_info['curso']
    titulacao = orientador_info['titulacao']
    instituicao = orientador_info['instituicao']
    vinculo = orientador_info['vinculo']
    polo = orientador_info['polo']
    uf_instituicao = orientador_info['uf_instituicao']
    lattes = orientador_info['lattes']

    # Crie os TextFields para exibir as informações do orientador (read-only)
    nome_field = ft.TextField(label="Nome", width=400, height=50, value=nome_orientador, read_only=True, bgcolor="WHITE")
    telefone_field = ft.TextField(label="Telefone (Com DDD, somente números)",width=650, height=75, value=telefone, read_only=True, max_length=11, col={"sm": 10, "md": 10},bgcolor="WHITE")
    telefone_icon = ft.IconButton(icon=ft.icons.PHONE,width=50,height=50,on_click=lambda e: abrir_whatsapp(telefone_field.value), tooltip="Abrir WhatsApp", col={"sm": 2, "md": 2})
    email_field = ft.TextField(label="Email", width=400, height=50, value=email, read_only=True, bgcolor="WHITE")
    curso_field = ft.TextField(label="Curso", width=400, height=50, value=curso, read_only=True, bgcolor="WHITE")
    titulacao_field = ft.TextField(label="Titulação", width=400, height=50, value=titulacao, read_only=True, bgcolor="WHITE")
    instituicao_field = ft.TextField(label="Instituição", width=400, height=50, value=instituicao, read_only=True, bgcolor="WHITE")
    vinculo_field = ft.TextField(label="Vínculo", width=400, height=50, value=vinculo, read_only=True, bgcolor="WHITE")
    polo_field = ft.TextField(label="Polo", width=400, height=50, value=polo, read_only=True, bgcolor="WHITE")
    uf_instituicao_field = ft.TextField(label="UF da instituição", width=400, height=50, value=uf_instituicao, read_only=True, bgcolor="WHITE")
    lattes_field = ft.TextField(label="Lattes", width=650, height=50, value=lattes, read_only=True, bgcolor="WHITE", col={"sm": 10, "md": 10})
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

    # Crie a lista de TextFields
    lista_textfields = [nome_field, 
                        ft.ResponsiveRow(controls=[telefone_field, telefone_icon], width=800),
                        email_field, 
                        curso_field, 
                        titulacao_field,
                        instituicao_field, 
                        vinculo_field, 
                        polo_field, 
                        uf_instituicao_field, 
                        ft.ResponsiveRow(controls=[lattes_field, lattes_icon], width=800),
                        ]
    
    nome_campo = ft.Text("DADOS CADASTRAIS - ORIENTADOR", size=16, color="#006BA0", font_family="Roboto", weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER)

    # Container principal para as informações do orientador 
    container_orientador = ft.Container(
        expand=True,
        content=ft.Column(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            scroll=ft.ScrollMode.ALWAYS,
            controls=[
                nome_campo,
                ft.Divider(),
                ft.Container(
                    width=800, # Largura máxima do container
                    content=ft.ResponsiveRow(
                        controls=lista_textfields
                    )
                ),
            ]
        )
    )

    return container_orientador