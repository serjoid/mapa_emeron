from database import Database
import flet as ft


# Conexão com o banco de dados
db = Database()

def tela_profile(page: ft.Page, nome_aluno):
    # Criar os TextFields para exibir as informações do aluno
    nome_field = ft.TextField(label="Nome", width=800, height=50, read_only=True, bgcolor="WHITE")
    telefone_field = ft.TextField(
        label="Telefone (Com DDD, somente números)",
        width=650,
        height=75,
        read_only=True,
        max_length=11,
        col={"sm": 10, "md": 10},
        bgcolor="WHITE"  # Remove o valor=telefone daqui
    )

    telefone_icon = ft.IconButton(
        icon=ft.icons.PHONE,
        width=50,
        height=50,
        on_click=lambda e: abrir_whatsapp(telefone_field.value),
        tooltip="Abrir WhatsApp",
        col={"sm": 2, "md": 2}
    )
    def abrir_whatsapp(telefone):
        if telefone:
            page.launch_url(f"https://wa.me/55{telefone.replace(' ', '').replace('-', '')}")
    # TextField do telefone fora do container
    email_field = ft.TextField(label="Email", width=800, height=50, read_only=True, bgcolor="WHITE")
    orientador_field = ft.TextField(
        label="Orientador", width=800, height=50, read_only=True, bgcolor="WHITE"
    )
    curso_field = ft.TextField(label="Curso", width=800, height=50, read_only=True, bgcolor="WHITE")
    nivel_curso_field = ft.TextField(
        label="Nível do curso", width=800, height=50, read_only=True, bgcolor="WHITE"
    )
    ano_ingresso_field = ft.TextField(
        label="Ano de ingresso", width=800, height=50, read_only=True, bgcolor="WHITE"
    )
    ano_conclusao_field = ft.TextField(
        label="Ano de conclusão", width=800, height=50, read_only=True, bgcolor="WHITE"
    )
    situacao_field = ft.TextField(
        label="Situação", width=800, height=50, read_only=True, bgcolor="WHITE"
    )
    instituicao_field = ft.TextField(
        label="Instituição", width=800, height=50, read_only=True, bgcolor="WHITE"
    )
    tipo_tcc_field = ft.TextField(
        label="Tipo do TCC", width=800, height=50, read_only=True, bgcolor="WHITE"
    )
    tema_field = ft.TextField(
        label="Tema", width=800, height=50, text_size=10, read_only=True, bgcolor="WHITE"
    )
    bolsa_field = ft.TextField(label="Bolsa", width=800, height=50, read_only=True, bgcolor="WHITE")
    tipo_bolsa_field = ft.TextField(
        label="Tipo da bolsa", width=800, height=50, read_only=True, bgcolor="WHITE"
    )
    vinculo_field = ft.TextField(
        label="Vínculo", width=800, height=50, read_only=True, bgcolor="WHITE"
    )
    polo_field = ft.TextField(label="Polo", width=800, height=50, read_only=True, bgcolor="WHITE")
    matricula_field = ft.TextField(
        label="Matrícula", width=800, height=50, read_only=True, bgcolor="WHITE"
    )
    doc_compromisso_field = ft.TextField(
        label="Documento de compromisso", width=800, height=50, read_only=True, bgcolor="WHITE"
    )
    uf_instituicao_field = ft.TextField(
        label="UF da instituição", width=800, height=50, read_only=True, bgcolor="WHITE"
    )
    lattes_field = ft.TextField(label="Lattes", width=650, height=50, read_only=True, col={"sm": 10, "md": 10}, bgcolor="WHITE")
    lattes_icon = ft.IconButton(
        icon=ft.icons.LINK,
        width=50,
        height=50,
        on_click=lambda e: page.launch_url(lattes_field.value) if lattes_field.value else None,
        tooltip="Abrir Currículo Lattes",
        col={"sm": 2, "md": 2}
    )
    situacao_matricula_field = ft.TextField(
        label="Situação da matrícula", width=800, height=50, read_only=True, bgcolor="WHITE"
    )
    grupo_pesquisa_field = ft.TextField(
        label="Grupo de pesquisa", width=800, height=50, read_only=True, bgcolor="WHITE"
    )
    linha_pesquisa_field = ft.TextField(
        label="Linha de pesquisa", width=800, height=50, read_only=True, bgcolor="WHITE"
    )
    via_tcc_entregue_field = ft.TextField(label="Via do TCC entregue", width=650, height=50, read_only=True, col={"sm": 10, "md": 10}, bgcolor="WHITE")
    via_tcc_entregue_icon = ft.IconButton(
        icon=ft.icons.LINK,
        width=50,
        height=50,
        on_click=lambda e: page.launch_url(via_tcc_entregue_field.value) if via_tcc_entregue_field.value else None,
        tooltip="Abrir Link da via do TCC entregue",
        col={"sm": 2, "md": 2}
    )

    # Criar um ListView para exibir as fases e prazos (inicialmente vazio)
    fases_prazos_listview = ft.ListView(height=100)

    lista_textfields = [
        nome_field,
        ft.ResponsiveRow(controls=[telefone_field, telefone_icon]),
        email_field,
        orientador_field,
        curso_field,
        nivel_curso_field,
        ano_ingresso_field,
        ano_conclusao_field,
        situacao_field,
        instituicao_field,
        tipo_tcc_field,
        tema_field,
        bolsa_field,
        tipo_bolsa_field,
        vinculo_field,
        polo_field,
        matricula_field,
        doc_compromisso_field,
        uf_instituicao_field,
        ft.ResponsiveRow(controls=[lattes_field, lattes_icon]),
        situacao_matricula_field,
        grupo_pesquisa_field,
        linha_pesquisa_field,
        ft.ResponsiveRow(controls=[via_tcc_entregue_field, via_tcc_entregue_icon]),
        fases_prazos_listview
    ]

    global aluno_id
    aluno_info = db.get_pessoa_info(nome_aluno)
    if aluno_info:
        aluno_id = aluno_info["id"]
        nome_field.value = aluno_info["nome"]
        # Define o valor do TextField do telefone dentro do bloco if:
        telefone_field.value = aluno_info["telefone"] 
        email_field.value = aluno_info["email"]
        orientador_field.value = aluno_info["orientador"]
        curso_field.value = aluno_info["curso"]
        nivel_curso_field.value = aluno_info["nivel_curso"]
        ano_ingresso_field.value = aluno_info["ano_ingresso"]
        ano_conclusao_field.value = aluno_info["ano_conclusao"]
        situacao_field.value = aluno_info["situacao_aluno_curso"]
        instituicao_field.value = aluno_info["instituicao"]
        tipo_tcc_field.value = aluno_info["tipo_tcc"]
        tema_field.value = aluno_info["titulo_tcc"]
        bolsa_field.value = aluno_info["bolsa"]
        tipo_bolsa_field.value = aluno_info["tipo_bolsa"]
        vinculo_field.value = aluno_info["vinculo"]
        polo_field.value = aluno_info["polo"]
        matricula_field.value = aluno_info["matricula"]
        doc_compromisso_field.value = aluno_info["doc_compromisso"]
        uf_instituicao_field.value = aluno_info["uf_instituicao"]
        lattes_field.value = aluno_info["lattes"]
        situacao_matricula_field.value = aluno_info["situacao_matricula"]
        grupo_pesquisa_field.value = aluno_info["grupo_pesquisa"]
        linha_pesquisa_field.value = aluno_info["linha_pesquisa"]
        via_tcc_entregue_field.value = aluno_info["via_tcc_entregue"]

        # Obter os prazos do aluno da tabela 'prazos'
        prazos_aluno = db.get_prazos_by_pessoa_id(aluno_info["id"])
        fases_prazos_listview.controls.clear()
        for prazo in prazos_aluno:
            fase = prazo.get("fase_pesquisa", "N/A")
            prazo_str = prazo.get("prazo_fase_pesquisa", "N/A")
            fases_prazos_listview.controls.append(
                ft.ListTile(title=ft.Text(f"{fase}: {prazo_str}"))
            )

    nome_campo = ft.Text("DADOS CADASTRAIS - DISCENTES", size=16, color="#006BA0", font_family="Roboto", weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER)

    # Estrutura do layout simplificada:
    container_profile = ft.Container(
        expand=True,
        content=ft.Column(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            scroll=ft.ScrollMode.AUTO,
            controls=[
                ft.Container(
                    width=800,
                    content=ft.Column(
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        controls=[
                            nome_campo,
                            ft.Divider(),
                            *lista_textfields  # Adiciona todos os campos diretamente aqui
                        ]
                    )
                )
            ],
        ),
        margin=ft.margin.only(bottom=50),
    )

    return container_profile
