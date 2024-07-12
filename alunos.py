import flet as ft
from database import Database

# Inicializa a conexão com o banco de dados
db = Database()

# Define uma variável global para armazenar as informações do aluno selecionado
aluno_info = None

def tela_alunos(page: ft.Page, usuario):
    """
    Cria a tela de gerenciamento de alunos.

    Args:
        page (ft.Page): A página onde a tela será exibida.
        usuario (str): O nome de usuário do usuário atualmente logado.

    Returns:
        ft.Container: Um container com os elementos da tela de alunos.
    """

    # Obtém listas de orientadores, alunos e cursos do banco de dados
    orientadores = db.get_orientador()
    alunos = db.get_aluno()
    cursos = db.get_curso()

    # Define uma variável global para armazenar o ID do aluno selecionado
    global aluno_id

    # Função para preencher os campos da tela com as informações do aluno selecionado
    def preencher_campos():
        """Preenche os campos da tela com as informações do aluno selecionado."""
        
        global aluno_info, aluno_id # Acessa as variáveis globais

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

            # Preenche o dropdown de orientador
            orientador_dropdown.value = aluno_info["orientador"]
            # Preenche o dropdown de curso
            curso_dropdown.value = aluno_info["curso"]
            # Preenche o dropdown de nível do curso
            nivel_curso_dropdown.value = aluno_info["nivel_curso"]
            # Preenche o dropdown de vínculo
            vinculo_dropdown.value = aluno_info["vinculo"]
            # Preenche o dropdown de polo
            polo_dropdown.value = aluno_info["polo"]
            # Preenche o dropdown de UF da instituição
            uf_instituicao_dropdown.value = aluno_info["uf_instituicao"]

            # Preenche a ListView com os prazos do aluno
            prazos_aluno = db.get_prazos_by_pessoa_id(aluno_info["id"])
            fases_prazos_listview.controls.clear()
            for prazo in prazos_aluno:
                fase = prazo.get("fase_pesquisa", "N/A")
                prazo_str = prazo.get("prazo_fase_pesquisa", "N/A")
                fases_prazos_listview.controls.append(ft.ListTile(title=ft.Text(f"{fase}: {prazo_str}")))

            # Define a visibilidade dos botões
            botao_atualizar_aluno.visible = True
            botao_novo_aluno.visible = False
            botao_cadastrar.visible = False
            botao_excluir_aluno.visible = False
            botao_salvar.visible = False

            # Define a visibilidade dos campos de texto (ativa)
            curso_field.visible = True
            polo_field.visible = True
            nivel_curso_field.visible = True
            vinculo_field.visible = True
            uf_instituicao_field.visible = True
            orientador_field.visible = True

            # Define a visibilidade dos dropdowns (inativa)
            curso_dropdown.visible = False
            polo_dropdown.visible = False
            nivel_curso_dropdown.visible = False
            vinculo_dropdown.visible = False
            uf_instituicao_dropdown.visible = False
            orientador_dropdown.visible = False

            # Define os campos de texto como somente leitura
            for field in lista_textfields:
                field.read_only = True
            telefone_field.read_only = True
            lattes_field.read_only = True
            via_tcc_entregue_field.read_only = True

            # Atualiza a página
            page.update()

    # Cria uma ListView para exibir os alunos
    lv = ft.ListView(expand=True, spacing=10, item_extent=50)

    # Função para carregar os alunos na ListView
    def carregar_alunos():
        """Carrega todos os alunos na ListView."""
        lv.controls.clear() # Limpa a lista antes de carregar os alunos
        for aluno in alunos:
            lv.controls.append(
                ft.ListTile(
                    title=ft.Text(aluno),
                    on_click=lambda e, aluno=aluno: selecionar_aluno(e, aluno) # Define a função a ser executada quando um aluno for clicado
                )
            )
        page.update()

    # Função para filtrar alunos na SearchBar
    def handle_change(e):
        """Filtra os alunos na ListView de acordo com o texto digitado na SearchBar."""

        coluna_alunos.controls.clear()  # Limpa os itens existentes na coluna
        if e.data: # Se houver texto na SearchBar
            for aluno in alunos:
                if e.data.lower() in aluno.lower(): # Verifica se o texto digitado está presente no nome do aluno (case insensitive)
                    coluna_alunos.controls.append(
                        ft.ListTile(
                            title=ft.Text(aluno),
                            on_click=lambda e, aluno=aluno: selecionar_aluno(e, aluno)
                        )
                    )
        else: # Se a SearchBar estiver vazia
            carregar_alunos() # Carrega todos os alunos na ListView
        page.update()

    # Função para lidar com a seleção de um aluno na SearchBar
    def selecionar_aluno(e, aluno_selecionado):
        """
        Manipula a seleção de um aluno na SearchBar.

        Args:
            e (ft.Event): O evento que acionou a função.
            aluno_selecionado (str): O nome do aluno selecionado na SearchBar.
        """
        global aluno_id, aluno_info # Acessa as variáveis globais
        aluno_info = db.get_pessoa_info(aluno_selecionado) # Obtém as informações do aluno selecionado no banco de dados
        aluno_id = aluno_info.get("id") # Define o ID do aluno selecionado
        preencher_campos() # Preenche os campos da tela com as informações do aluno
        sb_alunos.close_view(aluno_selecionado) # Fecha a SearchBar
        page.update()

    # Cria uma coluna para conter os ListTiles dos alunos
    coluna_alunos = ft.Column([lv])

    # Cria a SearchBar para buscar alunos pelo nome
    sb_alunos = ft.SearchBar(
        view_elevation=4,
        divider_color=ft.colors.AMBER,
        bar_hint_text="Buscar por nome.",
        view_hint_text="Escolha um aluno.",
        on_submit=lambda e: selecionar_aluno(e, e.control.value), # Define a função a ser executada quando um aluno for selecionado na SearchBar
        controls=[
            coluna_alunos # Adiciona a coluna de alunos à SearchBar
        ],
        on_change=handle_change, # Define a função a ser executada quando o texto da SearchBar for alterado
    )

    # Carrega os alunos na ListView ao iniciar a tela
    carregar_alunos()

    # Função para abrir o WhatsApp com o número de telefone do aluno
    def abrir_whatsapp(telefone):
        """
        Abre o WhatsApp Web com o número de telefone fornecido.

        Args:
            telefone (str): O número de telefone do aluno.
        """
        if telefone:
            page.launch_url(f"https://wa.me/55{telefone.replace(' ', '').replace('-', '')}") # Abre o link do WhatsApp Web com o número de telefone

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
    situacao_field = ft.TextField(label="Situação do aluno", width=800, height=50, read_only=True, bgcolor="WHITE")
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

    # Cria os dropdowns da tela
    orientador_dropdown = ft.Dropdown( width=800, label="Orientador(a)", options=[ft.dropdown.Option(key=orientador) for orientador in orientadores], visible=False, bgcolor="WHITE")
    curso_dropdown = ft.Dropdown(width=800, label="Curso", options=[ft.dropdown.Option(key=curso) for curso in cursos], visible=False, bgcolor="WHITE")
    nivel_curso_dropdown = ft.Dropdown(width=800, label="Nível do curso", options=[ft.dropdown.Option("Especialização"), ft.dropdown.Option("Mestrado"), ft.dropdown.Option("Doutorado")], visible=False, bgcolor="WHITE")
    vinculo_dropdown = ft.Dropdown(width=800, label="Vínculo", options=[ft.dropdown.Option("Servidor"), ft.dropdown.Option("Magistrado"), ft.dropdown.Option("Externo")], visible=False, bgcolor="WHITE")
    polo_dropdown = ft.Dropdown(width=800, label="Polo", options=[ft.dropdown.Option("Porto Velho"), ft.dropdown.Option("Cacoal"), ft.dropdown.Option("N/A")], visible=False, bgcolor="WHITE")
    uf_instituicao_dropdown = ft.Dropdown(width=800, label="UF da instituição", options=[ft.dropdown.Option(uf) for uf in ["RO", "AC", "AM", "RR", "PA", "AP", "TO", "MA", "PI", "CE", "RN", "PB", "PE", "AL", "SE", "BA", "MG", "ES", "RJ", "SP", "PR", "SC", "RS", "MS", "MT", "GO", "DF"]], visible=False, bgcolor="WHITE")
    situacao_dropdown = ft.Dropdown(width=800, label="Situação do Aluno", options=[ft.dropdown.Option("Cursando"), ft.dropdown.Option("Concluído"), ft.dropdown.Option("Desistente"), ft.dropdown.Option("Reprovado"), ft.dropdown.Option("Outros")], visible=False, bgcolor="WHITE")

    # Funções para lidar com os eventos dos botões de CRUD

    def novo_aluno(e):
        """
        Prepara a tela para o cadastro de um novo aluno.

        Args:
            e (ft.Event): O evento que acionou a função (clique no botão "Novo aluno").
        """

        # Torna os campos de texto editáveis e limpa seus valores
        for field in lista_textfields:
            field.read_only = False
        telefone_field.read_only = False
        lattes_field.read_only = False
        
        for field in lista_textfields:
            field.value = ""
        telefone_field.value = ""
        lattes_field.value = ""

        # Define a visibilidade dos botões
        botao_cadastrar.visible = True
        botao_novo_aluno.visible = False
        botao_atualizar_aluno.visible = False
        botao_excluir_aluno.visible = False
        botao_salvar.visible = False

        # Define a visibilidade dos campos de texto (inativa)
        curso_field.visible = False
        polo_field.visible = False
        nivel_curso_field.visible = False
        vinculo_field.visible = False
        uf_instituicao_field.visible = False
        orientador_field.visible = False
        situacao_field.visible = False
        via_tcc_entregue_field.visible = False
        via_tcc_entregue_icon.visible = False

        # Define a visibilidade dos dropdowns (ativa)
        curso_dropdown.visible = True
        polo_dropdown.visible = True
        nivel_curso_dropdown.visible = True
        vinculo_dropdown.visible = True
        uf_instituicao_dropdown.visible = True
        orientador_dropdown.visible = True
        situacao_dropdown.visible = True

        # Define a visibilidade da SearchBar (inativa)
        sb_alunos.visible = False

        # Define os valores padrão dos dropdowns
        uf_instituicao_dropdown.value = "RO"
        polo_dropdown.value = "Porto Velho"

        # Define a função para atualizar os campos de acordo com o curso selecionado
        def atualizar_campos_curso(e):
            """Atualiza os campos de nível do curso e instituição de acordo com o curso selecionado."""
            curso = curso_dropdown.value
            if curso in ["ESPECIALIZAÇÃO EM DIREITO PARA CARREIRA DA MAGISTRATURA", "MBA EM DIREITO PROCESSUAL CIVIL", "PÓS-GRADUAÇÃO LATO SENSU GESTÃO EM SEGURANÇA PÚBLICA"]:
                nivel_curso_dropdown.value = "Especialização"
                instituicao_field.value = "EMERON"
                tipo_tcc_field.value = "MONOGRAFIA"
            elif curso == "MESTRADO EM DIREITO PENAL":
                nivel_curso_dropdown.value = "Mestrado"
                instituicao_field.value = "UERJ"
                tipo_tcc_field.value = "DISSERTAÇÃO"
            elif curso == "DIREITOS HUMANOS E DESENVOLVIMENTO DA JUSTIÇA - DHJUS":
                nivel_curso_dropdown.value = "Mestrado"
                instituicao_field.value = "UNIR"
                tipo_tcc_field.value = "DISSERTAÇÃO"
            nivel_curso_dropdown.update()
            instituicao_field.update()

        # Define a função atualizar_campos_curso como a função a ser executada quando o valor do dropdown de curso for alterado
        curso_dropdown.on_change = atualizar_campos_curso
        atualizar_campos_curso(None)  # Executa a função uma vez no início

        # Atualiza a página
        page.update()

    def atualizar_aluno(e):
        """
        Prepara a tela para a atualização das informações de um aluno.

        Args:
            e (ft.Event): O evento que acionou a função (clique no botão "Atualizar cadastro").
        """

        global aluno_id # Acessa a variável global

        if aluno_id:
            # Torna os campos de texto editáveis
            for field in lista_textfields:
                field.read_only = False
            telefone_field.read_only = False
            lattes_field.read_only = False
            via_tcc_entregue_field.read_only = False

            # Define a visibilidade dos campos de texto (inativa)
            uf_instituicao_field.visible = False
            polo_field.visible = False
            vinculo_field.visible = False
            orientador_field.visible = False
            curso_field.visible = False
            nivel_curso_field.visible = False
            situacao_field.visible = False

            # Define a visibilidade dos dropdowns (ativa)
            situacao_dropdown.visible = True
            orientador_dropdown.visible = True
            curso_dropdown.visible = True
            polo_dropdown.visible = True
            nivel_curso_dropdown.visible = True
            vinculo_dropdown.visible = True
            uf_instituicao_dropdown.visible = True

            # Obtém as informações do aluno do banco de dados
            aluno_info = db.get_pessoa_info_by_id(aluno_id)

            # Preenche os dropdowns com as informações do aluno
            orientador_dropdown.value = aluno_info.get("orientador")
            curso_dropdown.value = aluno_info.get("curso")
            nivel_curso_dropdown.value = aluno_info.get("nivel_curso")
            vinculo_dropdown.value = aluno_info.get("vinculo")
            polo_dropdown.value = aluno_info.get("polo")
            uf_instituicao_dropdown.value = aluno_info.get("uf_instituicao")
            situacao_dropdown.value = aluno_info.get("situacao_aluno_curso")

            # Define a visibilidade do botão "Novo aluno" (inativo)
            botao_novo_aluno.visible = False

            # Define a função para atualizar os campos de acordo com o curso selecionado
            def atualizar_campos_curso(e):
                """Atualiza os campos de nível do curso, instituição e tipo de TCC de acordo com o curso selecionado."""
                curso = curso_dropdown.value
                if curso in ["ESPECIALIZAÇÃO EM DIREITO PARA CARREIRA DA MAGISTRATURA", "MBA EM DIREITO PROCESSUAL CIVIL", "PÓS-GRADUAÇÃO LATO SENSU GESTÃO EM SEGURANÇA PÚBLICA"]:
                    nivel_curso_dropdown.value = "Especialização"
                    instituicao_field.value = "EMERON"
                    tipo_tcc_field.value = "MONOGRAFIA"
                elif curso == "MESTRADO EM DIREITO PENAL":
                    nivel_curso_dropdown.value = "Mestrado"
                    instituicao_field.value = "UERJ"
                    tipo_tcc_field.value = "DISSERTAÇÃO"
                elif curso == "DIREITOS HUMANOS E DESENVOLVIMENTO DA JUSTIÇA - DHJUS":
                    nivel_curso_dropdown.value = "Mestrado"
                    instituicao_field.value = "UNIR"
                    tipo_tcc_field.value = "DISSERTAÇÃO"
                page.update()

            # Define a função atualizar_campos_curso como a função a ser executada quando o valor do dropdown de curso for alterado
            curso_dropdown.on_change = atualizar_campos_curso
            atualizar_campos_curso(None)  # Executa a função uma vez no início

        # Define a visibilidade dos botões
        botao_atualizar_aluno.visible = False
        botao_cadastrar.visible = False
        botao_excluir_aluno.visible = True
        botao_salvar.visible = True
        page.update()

    # Funções para exibir os diálogos de confirmação

    def insert_new_aluno(e):
        """Exibe o diálogo de confirmação para inserir um novo aluno."""
        page.dialog = dlg_confirmacao_novo
        dlg_confirmacao_novo.open = True
        page.update()

    def save_aluno(e):
        """Exibe o diálogo de confirmação para salvar as alterações de um aluno."""
        page.dialog = dlg_confirmacao_atualizar
        dlg_confirmacao_atualizar.open = True
        page.update()

    def confirmar_exclusao(e):
        """Exibe o diálogo de confirmação para excluir um aluno."""
        page.dialog = dlg_confirmacao_excluir
        dlg_confirmacao_excluir.open = True
        page.update()

    # Cria os botões de CRUD
    botao_novo_aluno = ft.ElevatedButton(text="Novo aluno", width=180, height=40, bgcolor="#006BA0", color="WHITE", on_click=novo_aluno, style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)))
    botao_cadastrar = ft.ElevatedButton(text="Cadastrar", width=180, height=40, bgcolor="#006BA0", color="WHITE", on_click=insert_new_aluno, style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)), visible=False)
    botao_atualizar_aluno = ft.ElevatedButton(text="Atualizar cadastro", width=180, height=40, bgcolor="#006BA0", color="WHITE", on_click=atualizar_aluno, style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)), visible=False)
    botao_salvar = ft.ElevatedButton(text="Salvar", width=180, height=40,bgcolor="#006BA0", color="WHITE", on_click=save_aluno, style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)), visible=False)
    botao_excluir_aluno = ft.ElevatedButton(text="Excluir", width=180, height=40, bgcolor="#006BA0", color="WHITE", on_click=confirmar_exclusao, style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)), visible=False) 

    # Cria a ListView para exibir as fases e os prazos do aluno
    fases_prazos_listview = ft.ListView(height=100)

    # Cria os diálogos de confirmação
    dlg_confirmacao_novo = ft.AlertDialog(
        modal=True,
        title=ft.Text("Confirmar Cadastro"),
        content=ft.Text("Tem certeza que deseja cadastrar este novo aluno?"),
        actions=[
            ft.TextButton("Sim", on_click=lambda e: cadastrar_aluno_confirmado(e)),
            ft.TextButton("Não", on_click=lambda e: fechar_dialogo_novo(e)),
        ],
        actions_alignment=ft.MainAxisAlignment.END
    )

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

    dlg_confirmacao_excluir = ft.AlertDialog(
        modal=True,
        title=ft.Text("Confirmar Exclusão"),
        content=ft.Text("Tem certeza que deseja excluir este aluno?"),
        actions=[
            ft.TextButton("Sim", on_click=lambda e: deletar_aluno_confirmado(aluno_id)),
            ft.TextButton("Não", on_click=lambda e: fechar_dialogo_excluir(e)),
        ],
        actions_alignment=ft.MainAxisAlignment.END
    )

    # Funções para fechar os diálogos de confirmação sem realizar nenhuma ação

    def fechar_dialogo_novo(e):
        """Fecha o diálogo de confirmação de novo aluno."""
        dlg_confirmacao_novo.open = False
        page.update()

    def fechar_dialogo_atualizar(e):
        """Fecha o diálogo de confirmação de atualização de aluno."""
        dlg_confirmacao_atualizar.open = False
        preencher_campos()
        page.update()

    def fechar_dialogo_excluir(e):
        """Fecha o diálogo de confirmação de exclusão de aluno."""
        dlg_confirmacao_excluir.open = False
        page.update()

    def fechar_dialogo(dlg):
        """Fecha um diálogo genérico."""
        dlg.open = False
        page.update()

    # Funções para executar as ações de CRUD após a confirmação

    def deletar_aluno_confirmado(aluno_id):
        """
        Exclui um aluno do banco de dados.

        Args:
            aluno_id (int): O ID do aluno a ser excluído.
        """

        # Exclui o aluno do banco de dados
        db.deletar_pessoa(aluno_id)

        # Registra o log da exclusão
        db.registrar_log(usuario, "excluir_aluno", f"Aluno: {nome_field.value}")

        # Fecha o diálogo de confirmação
        dlg_confirmacao_excluir.open = False

        # Exibe uma mensagem de sucesso
        page.snack_bar = ft.SnackBar(ft.Text("Aluno excluído com sucesso!"))
        page.snack_bar.open = True

        # Redefine a visibilidade dos elementos da tela
        sb_alunos.visible = True
        sb_alunos.value = ""
        
        for item in lista_textfields:
            if isinstance(item, ft.TextField):
                item.bgcolor = "WHITE"
                item.value = ""
                item.read_only = True
            elif isinstance(item, ft.Dropdown):
                item.value = ""
                item.visible = False

        telefone_field.value = ""
        lattes_field.value = ""
        via_tcc_entregue_field.value = ""
        situacao_field.value = ""
        telefone_field.bgcolor = "WHITE"
        lattes_field.bgcolor = "WHITE"
        via_tcc_entregue_field.bgcolor = "WHITE"
        situacao_field.bgcolor = "WHITE"
        telefone_field.read_only = True
        lattes_field.read_only = True
        via_tcc_entregue_field.read_only = True
        situacao_dropdown.visible = False

        botao_excluir_aluno.visible = False
        botao_salvar.visible = False
        page.update()

    def cadastrar_aluno_confirmado(e):
        """
        Cadastra um novo aluno no banco de dados.

        Args:
            e (ft.Event): O evento que acionou a função (clique no botão "Sim" do diálogo de confirmação).
        """

        # Define os campos obrigatórios
        campos_obrigatorios = [
            nome_field,
            curso_dropdown,
            nivel_curso_dropdown,
            ano_ingresso_field,
            instituicao_field,
            uf_instituicao_dropdown,
            polo_dropdown,
        ]

        # Verifica se todos os campos obrigatórios estão preenchidos
        campos_nao_preenchidos = [campo for campo in campos_obrigatorios if not campo.value]

        if campos_nao_preenchidos:
            # Destacar campos não preenchidos
            for campo in campos_nao_preenchidos:
                campo.bgcolor = ft.colors.RED_ACCENT_100

            # Mostrar alerta
            dlg = ft.AlertDialog(
                title=ft.Text("Campos Obrigatórios"),
                content=ft.Text("Preencha todos os campos obrigatórios."),
                actions=[ft.TextButton("Ok", on_click=lambda e: fechar_dialogo(dlg))]
            )
            page.dialog = dlg
            dlg.open = True
            page.update()
        else:
            # Cria um dicionário com os dados do novo aluno
            aluno_data = {
                "perfil": "Discente",
                "nome": nome_field.value,
                "telefone": telefone_field.value if telefone_field.value else "Não informado",
                "email": email_field.value if email_field.value else "Não informado",
                "orientador": orientador_dropdown.value if orientador_dropdown.value else "A definir",
                "curso": curso_dropdown.value,
                "nivel_curso": nivel_curso_dropdown.value,
                "ano_ingresso": ano_ingresso_field.value,
                "ano_conclusao": ano_conclusao_field.value,
                "situacao_aluno_curso": situacao_dropdown.value if situacao_dropdown.value else "Não informado",
                "instituicao": instituicao_field.value,
                "tipo_tcc": tipo_tcc_field.value if tipo_tcc_field.value else "Não informado",
                "titulo_tcc": tema_field.value if tema_field.value else "A definir",
                "bolsa": bolsa_field.value if bolsa_field.value else "Não informado",
                "tipo_bolsa": tipo_bolsa_field.value if tipo_bolsa_field.value else "Não informado",
                "vinculo": vinculo_dropdown.value if vinculo_dropdown.value else "Não informado",
                "polo": polo_dropdown.value,
                "matricula": matricula_field.value if matricula_field.value else "Não informado",
                "doc_compromisso": doc_compromisso_field.value if doc_compromisso_field.value else "Não informado",
                "uf_instituicao": uf_instituicao_dropdown.value if uf_instituicao_dropdown.value else "Não informado",
                "lattes": lattes_field.value if lattes_field.value else "Não informado",
                "situacao_matricula": situacao_matricula_field.value if situacao_matricula_field.value else "Não informado",
                "grupo_pesquisa": grupo_pesquisa_field.value if grupo_pesquisa_field.value else "N/A",
                "linha_pesquisa": linha_pesquisa_field.value if linha_pesquisa_field.value else "N/A",
                "via_tcc_entregue": via_tcc_entregue_field.value if via_tcc_entregue_field.value else "Após conclusão do curso",
                "titulacao": "",
            }

            # Insere o aluno no banco de dados
            db.insert_pessoa(aluno_data)

            # Registra o log do cadastro
            db.registrar_log(usuario, "inserir_aluno", f"Aluno: {aluno_data['nome']}")

            # Fecha o diálogo de confirmação
            dlg_confirmacao_novo.open = False

            # Exibe uma mensagem de sucesso
            page.snack_bar = ft.SnackBar(ft.Text("Aluno cadastrado com sucesso!"))
            page.snack_bar.open = True
            page.update()

            # Atualiza a lista de alunos
            global alunos
            alunos = db.get_aluno()
            lv.controls.clear()
            for nome in alunos:
                lv.controls.append(
                    ft.ListTile(title=ft.Text(nome), on_click=selecionar_aluno, data=nome)
                )

            # Define os campos de texto como somente leitura
            for field in lista_textfields:
                field.read_only = True
            telefone_field.read_only = True
            lattes_field.read_only = True
            via_tcc_entregue_field.read_only = True

            # Define a visibilidade dos botões
            botao_atualizar_aluno.visible = False
            botao_novo_aluno.visible = True
            botao_cadastrar.visible = False
            botao_excluir_aluno.visible = False
            botao_salvar.visible = False

            # Define a visibilidade dos campos de texto (ativa)
            curso_field.visible = True
            polo_field.visible = True
            nivel_curso_field.visible = True
            vinculo_field.visible = True
            uf_instituicao_field.visible = True
            orientador_field.visible = True
            situacao_field.visible = True

            # Define a visibilidade dos dropdowns (inativa)
            curso_dropdown.visible = False
            polo_dropdown.visible = False
            nivel_curso_dropdown.visible = False
            vinculo_dropdown.visible = False
            uf_instituicao_dropdown.visible = False
            orientador_dropdown.visible = False
            situacao_dropdown.visible = False

            # Define a cor de fundo dos campos de texto como branco
            ano_ingresso_field.bgcolor = "WHITE"
            situacao_field.bgcolor = "WHITE"
            instituicao_field.bgcolor = "WHITE"
            page.update()

    def atualizar_aluno_confirmado(e):
        """
        Atualiza as informações de um aluno no banco de dados.

        Args:
            e (ft.Event): O evento que acionou a função (clique no botão "Sim" do diálogo de confirmação).
        """

        global aluno_id # Acessa a variável global

        # Cria um dicionário com os dados do aluno a ser atualizado
        aluno_data = {
            "id": aluno_id,
            'perfil': 'Discente',
            'nome': nome_field.value,
            'telefone': telefone_field.value,
            'email': email_field.value,
            'orientador': orientador_dropdown.value,
            'curso': curso_dropdown.value,
            'nivel_curso': nivel_curso_dropdown.value,
            'ano_ingresso': ano_ingresso_field.value,
            'ano_conclusao': ano_conclusao_field.value,
            'situacao_aluno_curso': situacao_dropdown.value,
            'instituicao': instituicao_field.value,
            'tipo_tcc': tipo_tcc_field.value,
            'titulo_tcc': tema_field.value,
            'bolsa': bolsa_field.value,
            'tipo_bolsa': tipo_bolsa_field.value,
            'vinculo': vinculo_field.value,
            'polo': polo_dropdown.value,
            'matricula': matricula_field.value,
            'doc_compromisso': doc_compromisso_field.value,
            'uf_instituicao': uf_instituicao_dropdown.value,
            'lattes': lattes_field.value,
            'situacao_matricula': situacao_matricula_field.value,
            'grupo_pesquisa': grupo_pesquisa_field.value,
            'linha_pesquisa': linha_pesquisa_field.value,
            'via_tcc_entregue': via_tcc_entregue_field.value,
        }

        # Obtém os valores originais do aluno do banco de dados
        valor_original_dict = db.get_pessoa_info(nome_field.value) 

        # Cria uma lista com as alterações feitas nas informações do aluno
        alteracoes = []
        for chave, valor in aluno_data.items():
            if chave != "id" and valor_original_dict:
                valor_original = valor_original_dict.get(chave)
                if valor != valor_original:
                    alteracoes.append(f"{chave}: {valor_original} -> {valor}")

        # Cria uma mensagem para o log com as informações do aluno e as alterações feitas
        log_mensagem = f"Aluno: {aluno_data['nome']}"
        if alteracoes:
            log_mensagem += f" - Alterações: {', '.join(alteracoes)}"

        # Atualiza as informações do aluno no banco de dados
        db.update_pessoa(aluno_data)

        # Registra o log da atualização
        db.registrar_log(usuario, "atualizar_aluno", log_mensagem) 

        # Fecha o diálogo de confirmação
        dlg_confirmacao_atualizar.open = False

        # Exibe uma mensagem de sucesso
        page.snack_bar = ft.SnackBar(ft.Text("Dados atualizados com sucesso!"))
        page.snack_bar.open = True

        # Define os campos de texto como somente leitura
        for field in lista_textfields:
            field.read_only = True
        telefone_field.read_only = True
        lattes_field.read_only = True
        via_tcc_entregue_field.read_only = True
        situacao_field.read_only = True

        # Define a visibilidade dos botões
        botao_atualizar_aluno.visible = True
        botao_novo_aluno.visible = False
        botao_cadastrar.visible = False
        botao_excluir_aluno.visible = False
        botao_salvar.visible = False

        # Define a visibilidade dos campos de texto (ativa)
        curso_field.visible = True
        polo_field.visible = True
        nivel_curso_field.visible = True
        vinculo_field.visible = True
        uf_instituicao_field.visible = True
        orientador_field.visible = True
        situacao_field.visible = True

        # Define a visibilidade dos dropdowns (inativa)
        curso_dropdown.visible = False
        polo_dropdown.visible = False
        nivel_curso_dropdown.visible = False
        vinculo_dropdown.visible = False
        uf_instituicao_dropdown.visible = False
        orientador_dropdown.visible = False
        situacao_dropdown.visible = False

        # Preenche os campos da tela com as informações do aluno atualizado
        preencher_campos()
        page.update()

    # Cria uma lista com os campos de texto da tela
    lista_textfields = [
        sb_alunos,
        ft.ResponsiveRow(controls=[botao_novo_aluno], width=800),
        ft.ResponsiveRow(controls=[botao_cadastrar], width=800),
        ft.ResponsiveRow(controls=[botao_atualizar_aluno], width=800),
        ft.ResponsiveRow(controls=[botao_salvar], width=800),
        ft.ResponsiveRow(controls=[botao_excluir_aluno], width=800),
        nome_field,
        ft.ResponsiveRow(controls=[telefone_field, telefone_icon], width=800),
        email_field,
        orientador_dropdown,
        orientador_field,
        curso_field,
        curso_dropdown,
        nivel_curso_dropdown,
        nivel_curso_field,
        ano_ingresso_field,
        ano_conclusao_field,
        situacao_dropdown,
        situacao_field,
        instituicao_field,
        tipo_tcc_field,
        tema_field,
        bolsa_field,
        tipo_bolsa_field,
        vinculo_dropdown,
        vinculo_field,
        polo_dropdown,
        polo_field,
        matricula_field,
        doc_compromisso_field,
        uf_instituicao_dropdown,
        uf_instituicao_field,
        ft.ResponsiveRow(controls=[lattes_field, lattes_icon], width=800),
        situacao_matricula_field,
        grupo_pesquisa_field,
        linha_pesquisa_field,
        ft.ResponsiveRow(controls=[via_tcc_entregue_field, via_tcc_entregue_icon], width=800),
        ft.ResponsiveRow(controls=[fases_prazos_listview], width=800),
    ]

    # Cria um divisor visual
    divisor = ft.ResponsiveRow(controls=[ft.Divider()], width=800)

    # Cria o título da tela
    nome_campo = ft.Text("DADOS CADASTRAIS - DISCENTE", size=16, color="#006BA0", font_family="Roboto", weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER)

    # Cria o container principal da tela
    container_alunos = ft.Container(
        expand=True,
        content=ft.Column( 
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.START,
            scroll=ft.ScrollMode.ALWAYS,
            controls=[
                nome_campo,
                divisor,
                *lista_textfields,
            ]
        ), margin=ft.margin.only(bottom=50)
    )

    return container_alunos
                
