from database import Database
import flet as ft

# Conexão com o banco de dados
db = Database()

def tela_alunos_logado(page: ft.Page, usuario):
    """
    Exibe as informações do aluno logado para edição de telefone e email.

    Args:
        page (ft.Page): A página Flet atual.
        usuario (str): O nome de usuário do aluno logado.
    """
    global aluno_id  # Define aluno_id como global aqui
    # Obtém as informações do aluno logado do banco de dados
    aluno_info = db.get_pessoa_info_por_usuario(usuario)

    if not aluno_info:
        # Se o aluno não for encontrado, exiba uma mensagem de erro
        page.add(ft.Text("Erro: Aluno não encontrado."))
        return

    # Extrai as informações do aluno
    aluno_id = aluno_info['id']
    nome_aluno = aluno_info['nome']
    telefone = aluno_info['telefone']
    email = aluno_info['email']
    orientador = aluno_info['orientador']
    curso = aluno_info['curso']
    nivel_curso = aluno_info['nivel_curso']
    ano_ingresso = aluno_info['ano_ingresso']
    ano_conclusao = aluno_info['ano_conclusao']
    situacao = aluno_info['situacao_aluno_curso']
    instituicao = aluno_info['instituicao']
    tipo_tcc = aluno_info['tipo_tcc']
    tema = aluno_info['titulo_tcc']
    bolsa = aluno_info['bolsa']
    tipo_bolsa = aluno_info['tipo_bolsa']
    vinculo = aluno_info['vinculo']
    polo = aluno_info['polo']
    matricula = aluno_info['matricula']
    doc_compromisso = aluno_info['doc_compromisso']
    uf_instituicao = aluno_info['uf_instituicao']
    lattes = aluno_info['lattes']
    situacao_matricula = aluno_info['situacao_matricula']
    grupo_pesquisa = aluno_info['grupo_pesquisa']
    linha_pesquisa = aluno_info['linha_pesquisa']
    via_tcc_entregue = aluno_info['via_tcc_entregue']

    # Mensagem para o aluno
    mensagem_aluno = ft.Text(
        "Em caso de necessidade de alteração cadastral, além dos dados de contato, contactar o orientador ou coordenador do curso.",
        width=800,
        text_align=ft.TextAlign.CENTER, # Centraliza o texto
        style=ft.TextStyle(weight=ft.FontWeight.BOLD)
    )

    # Crie os TextFields para exibir as informações do aluno
    nome_field = ft.TextField(label="Nome", width=800, height=50, value=nome_aluno, read_only=True, bgcolor="WHITE")
    telefone_field = ft.TextField(
        label="Telefone (Com DDD, somente números)", width=800, height=75, value=telefone, read_only=True, max_length=11, bgcolor="WHITE")
    email_field = ft.TextField(label="Email", width=800, height=50, value=email, read_only=True, bgcolor="WHITE")
    orientador_field = ft.TextField(label="Orientador", width=800, height=50, value=orientador, read_only=True, bgcolor="WHITE")
    curso_field = ft.TextField(label="Curso", width=800, height=50, value=curso, read_only=True, bgcolor="WHITE")
    nivel_curso_field = ft.TextField(label="Nível do curso", width=800, height=50, value=nivel_curso, read_only=True, bgcolor="WHITE")
    ano_ingresso_field = ft.TextField(label="Ano de ingresso", width=800, height=50, value=ano_ingresso, read_only=True, bgcolor="WHITE")
    ano_conclusao_field = ft.TextField(label="Ano de conclusão", width=800, height=50, value=ano_conclusao, read_only=True, bgcolor="WHITE")
    situacao_field = ft.TextField(label="Situação", width=800, height=50, value=situacao, read_only=True, bgcolor="WHITE")
    instituicao_field = ft.TextField(label="Instituição", width=800, height=50, value=instituicao, read_only=True, bgcolor="WHITE")
    tipo_tcc_field = ft.TextField(label="Tipo do TCC", width=800, height=50, value=tipo_tcc, read_only=True, bgcolor="WHITE")
    tema_field = ft.TextField(label="Tema", width=800, height=50, text_size=10, value=tema, read_only=True, bgcolor="WHITE")
    bolsa_field = ft.TextField(label="Bolsa", width=800, height=50, value=bolsa, read_only=True, bgcolor="WHITE")
    tipo_bolsa_field = ft.TextField(label="Tipo da bolsa", width=800, height=50, value=tipo_bolsa, read_only=True, bgcolor="WHITE")
    vinculo_field = ft.TextField(label="Vínculo", width=800, height=50, value=vinculo, read_only=True, bgcolor="WHITE")
    polo_field = ft.TextField(label="Polo", width=800, height=50, value=polo, read_only=True, bgcolor="WHITE")
    matricula_field = ft.TextField(label="Matrícula", width=800, height=50, value=matricula, read_only=True, bgcolor="WHITE")
    doc_compromisso_field = ft.TextField(label="Documento de compromisso", width=800, height=50, value=doc_compromisso, read_only=True, bgcolor="WHITE")
    uf_instituicao_field = ft.TextField(label="UF da instituição", width=800, height=50, value=uf_instituicao, read_only=True, bgcolor="WHITE")
    lattes_field = ft.TextField(label="Lattes", width=800, height=50, value=lattes, read_only=True, bgcolor="WHITE")
    situacao_matricula_field = ft.TextField(label="Situação da matrícula", width=800, height=50, value=situacao_matricula, read_only=True, bgcolor="WHITE")
    grupo_pesquisa_field = ft.TextField(label="Grupo de pesquisa", width=800, height=50, value=grupo_pesquisa, read_only=True, bgcolor="WHITE")
    linha_pesquisa_field = ft.TextField(label="Linha de pesquisa", width=800, height=50, value=linha_pesquisa, read_only=True, bgcolor="WHITE")
    via_tcc_entregue_field = ft.TextField(label="Via TCC entregue", width=800, height=50, value=via_tcc_entregue, read_only=True, bgcolor="WHITE")


    # Diálogos de Confirmação
    dlg_confirmacao_atualizar = ft.AlertDialog(
        modal=True,
        title=ft.Text("Confirmar Atualização"),
        content=ft.Text("Tem certeza que deseja atualizar seus dados?"),
        actions=[
            ft.TextButton("Sim", on_click=lambda e: atualizar_aluno_confirmado(e)),
            ft.TextButton("Não", on_click=lambda e: fechar_dialogo_atualizar(e)),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )

    def fechar_dialogo_atualizar(e):
        dlg_confirmacao_atualizar.open = False
        page.update()

    def atualizar_aluno(e):
        global aluno_id
        if aluno_id:
            # Habilita a edição de telefone e email
            telefone_field.read_only = False
            email_field.read_only = False
            telefone_field.update()
            email_field.update()
            # Oculta os campos que não devem ser editados
            orientador_field.visible = False
            curso_field.visible = False
            nivel_curso_field.visible = False
            ano_ingresso_field.visible = False
            ano_conclusao_field.visible = False
            situacao_field.visible = False
            instituicao_field.visible = False
            tipo_tcc_field.visible = False
            tema_field.visible = False
            bolsa_field.visible = False
            tipo_bolsa_field.visible = False
            vinculo_field.visible = False
            polo_field.visible = False
            matricula_field.visible = False
            doc_compromisso_field.visible = False
            uf_instituicao_field.visible = False
            lattes_field.visible = False
            situacao_matricula_field.visible = False
            grupo_pesquisa_field.visible = False
            linha_pesquisa_field.visible = False
            via_tcc_entregue_field.visible = False
            mensagem_aluno.visible = False
            # Altera a visibilidade dos botões
            botao_atualizar_aluno.visible = False
            botao_salvar.visible = True
            page.update()
            botoes.update()

    def save_aluno(e):
        # Abre o diálogo de confirmação
        page.dialog = dlg_confirmacao_atualizar
        dlg_confirmacao_atualizar.open = True
        page.update()

    def atualizar_aluno_confirmado(e):
        global aluno_id
        # Coletar dados dos TextField
        aluno_data = {
            'id': aluno_id,
            'perfil': 'Discente',
            'nome': nome_field.value,
            'telefone': telefone_field.value,
            'email': email_field.value,
            'orientador': orientador_field.value,
            'curso': curso_field.value,
            'nivel_curso': nivel_curso_field.value,
            'ano_ingresso': ano_ingresso_field.value,
            'ano_conclusao': ano_conclusao_field.value,
            'situacao_aluno_curso': situacao_field.value,
            'instituicao': instituicao_field.value,
            'tipo_tcc': tipo_tcc_field.value,
            'titulo_tcc': tema_field.value,
            'bolsa': bolsa_field.value,
            'tipo_bolsa': tipo_bolsa_field.value,
            'vinculo': vinculo_field.value,
            'polo': polo_field.value,
            'matricula': matricula_field.value,
            'doc_compromisso': doc_compromisso_field.value,
            'uf_instituicao': uf_instituicao_field.value,
            'lattes': lattes_field.value,
            'situacao_matricula': situacao_matricula_field.value,
            'grupo_pesquisa': grupo_pesquisa_field.value,
            'linha_pesquisa': linha_pesquisa_field.value,
            'via_tcc_entregue': via_tcc_entregue_field.value,
        }
        # Chamar o método de atualização da DAO
        db.update_pessoa(aluno_data)
        db.registrar_log(usuario, "atualizar_aluno", f"Aluno: {aluno_data['nome']}") # Registra o log de atualização
        dlg_confirmacao_atualizar.open = False
        page.snack_bar = ft.SnackBar(ft.Text("Dados atualizados com sucesso!"))
        page.snack_bar.open = True
        page.update()

        # Desabilita a edição de telefone e email
        telefone_field.read_only = True
        email_field.read_only = True

        # Torna os campos visíveis novamente
        orientador_field.visible = True
        curso_field.visible = True
        nivel_curso_field.visible = True
        ano_ingresso_field.visible = True
        ano_conclusao_field.visible = True
        situacao_field.visible = True
        instituicao_field.visible = True
        tipo_tcc_field.visible = True
        tema_field.visible = True
        bolsa_field.visible = True
        tipo_bolsa_field.visible = True
        vinculo_field.visible = True
        polo_field.visible = True
        matricula_field.visible = True
        doc_compromisso_field.visible = True
        uf_instituicao_field.visible = True
        lattes_field.visible = True
        situacao_matricula_field.visible = True
        grupo_pesquisa_field.visible = True
        linha_pesquisa_field.visible = True
        via_tcc_entregue_field.visible = True
        mensagem_aluno.visible = True

        # Altera a visibilidade dos botões
        botao_atualizar_aluno.visible = True
        botao_salvar.visible = False
        page.update()
        botoes.update()

    # Botões
    botao_atualizar_aluno = ft.ElevatedButton(
        text="Atualizar dados",
        width=200,
        height=40,
        bgcolor="#006BA0",
        color="WHITE",
        on_click=atualizar_aluno, 
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
        visible=True
    )
    botao_salvar = ft.ElevatedButton(
        text="Salvar",
        width=200,
        height=40,
        bgcolor="#006BA0",
        color="WHITE",
        on_click=save_aluno,
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
        visible=False
    )

    botoes = ft.Container(
        width=800,
        content=ft.ResponsiveRow(
            alignment=ft.MainAxisAlignment.END,
            controls=[
                botao_atualizar_aluno,
                botao_salvar,
            ]
        )
    )

    nome_campo = ft.Text("DADOS CADASTRAIS - DISCENTE", size=16, color="#006BA0", font_family="Roboto", weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER)

    container_alunos = ft.Container(
        expand=True,
        content=ft.Column( 
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            scroll=ft.ScrollMode.ALWAYS,
            controls=[
                nome_campo,
                ft.Divider(),
                mensagem_aluno, 
                botoes,
                nome_field, 
                telefone_field, 
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
                lattes_field,
                situacao_matricula_field, 
                grupo_pesquisa_field, 
                linha_pesquisa_field, 
                via_tcc_entregue_field
            ]
        ), margin=ft.margin.only(bottom=50)
    )

    return container_alunos