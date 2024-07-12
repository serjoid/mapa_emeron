from database import Database
import flet as ft

# Conexão com o banco de dados
db = Database()

def tela_alunos_orientador_logado(page: ft.Page, usuario):
    """
    Exibe a tela para o orientador visualizar e editar informações dos seus orientandos.

    Args:
        page (ft.Page): A página Flet atual.
        usuario (str): O nome de usuário do orientador logado.
    """

    # Obtém a lista de cursos disponíveis no banco de dados
    cursos = db.get_curso()

    # Obtém o nome do orientador logado a partir do seu usuário
    orientador = db.get_orientador_info_por_usuario(usuario)['nome']

    # Obtém a lista de nomes dos alunos orientandos do orientador logado
    nomes_alunos = db.get_orientando(orientador)

    # Define a função para carregar os dados do aluno selecionado no dropdown
    def carregar_dados_aluno_dropdown(e):
        """Carrega os dados do aluno selecionado no dropdown para os campos da tela."""
        nome_aluno = dropdown_alunos.value
        if nome_aluno:
            preencher_campos(nome_aluno)
            botao_salvar.visible = False
            botao_atualizar_aluno.visible = True
            page.update()

    # Cria o dropdown para selecionar o aluno
    dropdown_alunos = ft.Dropdown(
        width=800,
        options=[ft.dropdown.Option(nome) for nome in nomes_alunos],
        on_change=carregar_dados_aluno_dropdown,  # Define a função a ser chamada quando o valor do dropdown mudar
        bgcolor="WHITE",
    )

    # Define a função para preencher os campos da tela com as informações do aluno
    def preencher_campos(nome):
        """Preenche os campos da tela com as informações do aluno."""
        global aluno_id  # Define aluno_id como global para ser acessível em outras funções
        aluno_info = db.get_pessoa_info(nome)  # Obtém as informações do aluno do banco de dados a partir do nome

        if aluno_info:
            # Preenche os campos de texto com as informações do aluno
            nome_field.value = aluno_info["nome"]
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
            aluno_id = aluno_info['id']

            # Preenche a ListView com os prazos do aluno
            prazos_aluno = db.get_prazos_by_pessoa_id(aluno_info["id"])
            fases_prazos_listview.controls.clear()
            for prazo in prazos_aluno:
                fase = prazo.get("fase_pesquisa", "N/A")
                prazo_str = prazo.get("prazo_fase_pesquisa", "N/A")
                fases_prazos_listview.controls.append(ft.ListTile(title=ft.Text(f"{fase}: {prazo_str}")))

            # Desabilita a edição dos campos
            for field in lista_textfields:
                field.read_only = True
                telefone_field.read_only = True
                lattes_field.read_only = True
                via_tcc_entregue_field.read_only = True

            # Define a visibilidade dos botões
            botao_atualizar_aluno.visible = True
            botao_salvar.visible = False

            # Define a visibilidade dos campos de texto (ativa)
            curso_field.visible = True
            polo_field.visible = True
            nivel_curso_field.visible = True
            vinculo_field.visible = True
            uf_instituicao_field.visible = True
            orientador_field.visible = True

            page.update()

    # Função para abrir o WhatsApp com o número de telefone do aluno
    def abrir_whatsapp(telefone):
        """Abre o WhatsApp Web com o número de telefone fornecido."""
        if telefone:
            page.launch_url(f"https://wa.me/55{telefone.replace(' ', '').replace('-', '')}")

    # Cria os campos de texto da tela
    nome_field = ft.TextField(label="Nome", width=800, height=50, read_only=True, bgcolor="WHITE")
    telefone_field = ft.TextField(label="Telefone (Com DDD, somente números)",width=650, height=75, read_only=True, max_length=11, col={"sm": 10, "md": 10},bgcolor="WHITE")
    telefone_icon = ft.IconButton(icon=ft.icons.PHONE,width=50,height=50,on_click=lambda e: abrir_whatsapp(telefone_field.value), tooltip="Abrir WhatsApp", col={"sm": 2, "md": 2})
    email_field = ft.TextField(label="Email", width=800, height=50, read_only=True, bgcolor="WHITE")
    orientador_field = ft.TextField(label="Orientador", width=800, height=50, read_only=True, bgcolor="WHITE")
    curso_field = ft.TextField(label="Curso", width=800, height=50, read_only=True, bgcolor="WHITE")
    nivel_curso_field = ft.TextField(label="Nível do curso", width=800, height=50, read_only=True, bgcolor="WHITE")
    ano_ingresso_field = ft.TextField(label="Ano de ingresso", width=800, height=50, read_only=True, bgcolor="WHITE")
    ano_conclusao_field = ft.TextField(label="Ano de conclusão", width=800, height=50, read_only=True, bgcolor="WHITE")
    situacao_field = ft.TextField(label="Situação", width=800, height=50, read_only=True, bgcolor="WHITE")
    instituicao_field = ft.TextField(label="Instituição", width=800, height=50, read_only=True, bgcolor="WHITE")
    tipo_tcc_field = ft.TextField(label="Tipo do TCC", width=800, height=50, read_only=True, bgcolor="WHITE")
    tema_field = ft.TextField(label="Tema", width=800, height=50, text_size=10, read_only=True, bgcolor="WHITE")
    bolsa_field = ft.TextField(label="Bolsa", width=800, height=50, read_only=True, bgcolor="WHITE")
    tipo_bolsa_field = ft.TextField(label="Tipo da bolsa", width=800, height=50, read_only=True, bgcolor="WHITE")
    vinculo_field = ft.TextField(label="Vínculo", width=800, height=50, read_only=True, bgcolor="WHITE")
    polo_field = ft.TextField(label="Polo", width=800, height=50, read_only=True, bgcolor="WHITE")
    matricula_field = ft.TextField(label="Matrícula", width=800, height=50, read_only=True, bgcolor="WHITE")
    doc_compromisso_field = ft.TextField(label="Documento de compromisso", width=800, height=50, read_only=True, bgcolor="WHITE")
    uf_instituicao_field = ft.TextField(label="UF da instituição", width=800, height=50, read_only=True, bgcolor="WHITE")
    lattes_field = ft.TextField(label="Lattes", width=650, height=50, read_only=True, col={"sm": 10, "md": 10}, bgcolor="WHITE")
    lattes_icon = ft.IconButton(icon=ft.icons.LINK, width=50,height=50,on_click=lambda e: page.launch_url(lattes_field.value) if lattes_field.value else None,tooltip="Abrir Currículo Lattes",col={"sm": 2, "md": 2})
    situacao_matricula_field = ft.TextField(label="Situação da matrícula", width=800, height=50, read_only=True, bgcolor="WHITE")
    grupo_pesquisa_field = ft.TextField(label="Grupo de pesquisa", width=800, height=50, read_only=True, bgcolor="WHITE")
    linha_pesquisa_field = ft.TextField(label="Linha de pesquisa", width=800, height=50, read_only=True, bgcolor="WHITE")
    via_tcc_entregue_field = ft.TextField(label="Via do TCC entregue", width=650, height=50, read_only=True, col={"sm": 10, "md": 10}, bgcolor="WHITE")
    via_tcc_entregue_icon = ft.IconButton(icon=ft.icons.LINK, width=50, height=50, on_click=lambda e: page.launch_url(via_tcc_entregue_field.value) if via_tcc_entregue_field.value else None, tooltip="Abrir Link da via do TCC entregue", col={"sm": 2, "md": 2})
    fases_prazos_listview = ft.ListView(height=100)

    # Função para habilitar a edição de alguns campos do aluno
    def atualizar_aluno(e):
        """Habilita a edição de campos específicos do aluno."""
        global aluno_id  # Acessa a variável global

        if aluno_id:
            # Liberando campos para edição e definindo a cor de fundo como branca
            telefone_field.read_only = False
            telefone_field.bgcolor = ft.colors.WHITE
            lattes_field.read_only = False
            lattes_field.bgcolor = ft.colors.WHITE
            via_tcc_entregue_field.read_only = False
            via_tcc_entregue_field.bgcolor = ft.colors.WHITE
            tipo_tcc_field.read_only = False
            tipo_tcc_field.bgcolor = ft.colors.WHITE
            tema_field.read_only = False
            tema_field.bgcolor = ft.colors.WHITE
            grupo_pesquisa_field.read_only = False
            grupo_pesquisa_field.bgcolor = ft.colors.WHITE
            linha_pesquisa_field.read_only = False
            linha_pesquisa_field.bgcolor = ft.colors.WHITE
            email_field.read_only = False
            email_field.bgcolor = ft.colors.WHITE

            # Mantendo campos como somente leitura e definindo a cor de fundo como cinza claro
            nome_field.read_only = True
            nome_field.bgcolor = ft.colors.GREY_200
            orientador_field.read_only = True
            orientador_field.bgcolor = ft.colors.GREY_200
            curso_field.read_only = True
            curso_field.bgcolor = ft.colors.GREY_200
            polo_field.read_only = True
            polo_field.bgcolor = ft.colors.GREY_200
            nivel_curso_field.read_only = True
            nivel_curso_field.bgcolor = ft.colors.GREY_200
            vinculo_field.read_only = True
            vinculo_field.bgcolor = ft.colors.GREY_200
            uf_instituicao_field.read_only = True
            uf_instituicao_field.bgcolor = ft.colors.GREY_200
            ano_ingresso_field.read_only = True
            ano_ingresso_field.bgcolor = ft.colors.GREY_200
            ano_conclusao_field.read_only = True
            ano_conclusao_field.bgcolor = ft.colors.GREY_200
            bolsa_field.read_only = True
            bolsa_field.bgcolor = ft.colors.GREY_200
            tipo_bolsa_field.read_only = True
            tipo_bolsa_field.bgcolor = ft.colors.GREY_200
            situacao_field.read_only = True
            situacao_field.bgcolor = ft.colors.GREY_200
            instituicao_field.read_only = True
            instituicao_field.bgcolor = ft.colors.GREY_200
            matricula_field.read_only = True
            matricula_field.bgcolor = ft.colors.GREY_200
            doc_compromisso_field.read_only = True
            doc_compromisso_field.bgcolor = ft.colors.GREY_200
            situacao_matricula_field.read_only = True
            situacao_matricula_field.bgcolor = ft.colors.GREY_200

            # Alterando a visibilidade dos botões
            botao_atualizar_aluno.visible = False
            botao_salvar.visible = True
            page.update()

    # Função para abrir o diálogo de confirmação de atualização
    def save_aluno(e):
        """Abre o diálogo de confirmação de atualização de dados."""
        page.dialog = dlg_confirmacao_atualizar
        dlg_confirmacao_atualizar.open = True
        page.update()

    # Cria os botões de CRUD (apenas atualização neste caso)
    botao_atualizar_aluno = ft.ElevatedButton(text="Atualizar cadastro", width=180, height=40, bgcolor="#006BA0", color="WHITE", on_click=atualizar_aluno, style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)), visible=False)
    botao_salvar = ft.ElevatedButton(text="Salvar", width=180, height=40,bgcolor="#006BA0", color="WHITE", on_click=save_aluno, style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)), visible=False)

    # Cria a ListView para exibir as fases e os prazos do aluno
    fases_prazos_listview = ft.ListView(height=100)

    # Diálogo de confirmação para atualização de dados
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

    # Função para fechar o diálogo de confirmação de atualização
    def fechar_dialogo_atualizar(e):
        """Fecha o diálogo de confirmação de atualização."""
        dlg_confirmacao_atualizar.open = False

        # Resetando a cor de fundo de todos os campos para branco
        telefone_field.bgcolor = ft.colors.WHITE
        lattes_field.bgcolor = ft.colors.WHITE
        via_tcc_entregue_field.bgcolor = ft.colors.WHITE
        tipo_tcc_field.bgcolor = ft.colors.WHITE
        tema_field.bgcolor = ft.colors.WHITE
        grupo_pesquisa_field.bgcolor = ft.colors.WHITE
        linha_pesquisa_field.bgcolor = ft.colors.WHITE
        email_field.bgcolor = ft.colors.WHITE
        nome_field.bgcolor = ft.colors.WHITE
        orientador_field.bgcolor = ft.colors.WHITE
        curso_field.bgcolor = ft.colors.WHITE
        polo_field.bgcolor = ft.colors.WHITE
        nivel_curso_field.bgcolor = ft.colors.WHITE
        vinculo_field.bgcolor = ft.colors.WHITE
        uf_instituicao_field.bgcolor = ft.colors.WHITE
        ano_ingresso_field.bgcolor = ft.colors.WHITE
        ano_conclusao_field.bgcolor = ft.colors.WHITE
        bolsa_field.bgcolor = ft.colors.WHITE
        tipo_bolsa_field.bgcolor = ft.colors.WHITE
        situacao_field.bgcolor = ft.colors.WHITE
        instituicao_field.bgcolor = ft.colors.WHITE
        matricula_field.bgcolor = ft.colors.WHITE
        doc_compromisso_field.bgcolor = ft.colors.WHITE
        situacao_matricula_field.bgcolor = ft.colors.WHITE

        # Preenche os campos com os dados do aluno selecionado no dropdown
        preencher_campos(dropdown_alunos.value)

        page.update()

    # Função para atualizar os dados do aluno no banco de dados
    def atualizar_aluno_confirmado(e):
        """Atualiza os dados do aluno no banco de dados após a confirmação."""
        global aluno_id  # Acessa a variável global

        # Cria um dicionário com os dados do aluno a ser atualizado
        aluno_data = {
            "id": aluno_id,
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

        # Obtém os valores originais do aluno do banco de dados usando o nome
        valor_original_dict = db.get_pessoa_info(nome_field.value)

        # Gera uma string com as alterações para o log
        alteracoes = []
        for chave, valor in aluno_data.items():
            if chave != "id" and valor_original_dict:
                valor_original = valor_original_dict.get(chave)
                if valor != valor_original:
                    alteracoes.append(f"{chave}: {valor_original} -> {valor}")

        # Cria a mensagem de log com as informações do aluno e as alterações
        log_mensagem = f"Aluno: {aluno_data['nome']}"
        if alteracoes:
            log_mensagem += f" - Alterações: {', '.join(alteracoes)}"

        # Atualiza os dados do aluno no banco de dados
        db.update_pessoa(aluno_data)

        # Registra o log da atualização
        db.registrar_log(usuario, "atualizar_aluno", log_mensagem)

        # Fecha o diálogo de confirmação
        dlg_confirmacao_atualizar.open = False

        # Exibe uma mensagem de sucesso
        page.snack_bar = ft.SnackBar(ft.Text("Dados atualizados com sucesso!"))
        page.snack_bar.open = True

        # Define a visibilidade dos botões
        botao_atualizar_aluno.visible = True
        botao_salvar.visible = False

        # Define a visibilidade dos campos de texto (ativa)
        curso_field.visible = True
        polo_field.visible = True
        nivel_curso_field.visible = True
        vinculo_field.visible = True
        uf_instituicao_field.visible = True
        orientador_field.visible = True

        # Resetando a cor de fundo de todos os campos para branco
        telefone_field.bgcolor = ft.colors.WHITE
        lattes_field.bgcolor = ft.colors.WHITE
        via_tcc_entregue_field.bgcolor = ft.colors.WHITE
        tipo_tcc_field.bgcolor = ft.colors.WHITE
        tema_field.bgcolor = ft.colors.WHITE
        grupo_pesquisa_field.bgcolor = ft.colors.WHITE
        linha_pesquisa_field.bgcolor = ft.colors.WHITE
        email_field.bgcolor = ft.colors.WHITE
        nome_field.bgcolor = ft.colors.WHITE
        orientador_field.bgcolor = ft.colors.WHITE
        curso_field.bgcolor = ft.colors.WHITE
        polo_field.bgcolor = ft.colors.WHITE
        nivel_curso_field.bgcolor = ft.colors.WHITE
        vinculo_field.bgcolor = ft.colors.WHITE
        uf_instituicao_field.bgcolor = ft.colors.WHITE
        ano_ingresso_field.bgcolor = ft.colors.WHITE
        ano_conclusao_field.bgcolor = ft.colors.WHITE
        bolsa_field.bgcolor = ft.colors.WHITE
        tipo_bolsa_field.bgcolor = ft.colors.WHITE
        situacao_field.bgcolor = ft.colors.WHITE
        instituicao_field.bgcolor = ft.colors.WHITE
        matricula_field.bgcolor = ft.colors.WHITE
        doc_compromisso_field.bgcolor = ft.colors.WHITE
        situacao_matricula_field.bgcolor = ft.colors.WHITE

        # Preenche os campos com os dados do aluno selecionado no dropdown
        preencher_campos(nome_field.value)

        page.update()

    # Lista de textfields para ser inserido no container
    lista_textfields = [
        dropdown_alunos,
        ft.ResponsiveRow(controls=[botao_atualizar_aluno], width=800),
        ft.ResponsiveRow(controls=[botao_salvar], width=800),
        nome_field,
        ft.ResponsiveRow(controls=[telefone_field, telefone_icon], width=800),
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
        ft.ResponsiveRow(controls=[lattes_field, lattes_icon], width=800),
        situacao_matricula_field,
        grupo_pesquisa_field,
        linha_pesquisa_field,
        ft.ResponsiveRow(controls=[via_tcc_entregue_field, via_tcc_entregue_icon], width=800),
        ft.ResponsiveRow(controls=[fases_prazos_listview], width=800),
    ]

    # Título da seção
    nome_campo = ft.Text("DADOS CADASTRAIS - DISCENTE", size=16, color="#006BA0", font_family="Roboto", weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER)

    # Container principal da tela
    container_alunos = ft.Container(
        expand=True,
        content=ft.Column( 
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            scroll=ft.ScrollMode.ALWAYS,
            controls=[
                nome_campo,
                ft.Divider(),
                *lista_textfields,
            ]
        ), margin=ft.margin.only(bottom=50)
    )

    return container_alunos
