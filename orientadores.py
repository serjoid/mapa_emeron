import flet as ft  # Importa a biblioteca Flet
from database import Database  # Importa a classe Database do arquivo database.py

# Inicializa a conexão com o banco de dados
db = Database()

# Obtém a lista de nomes dos orientadores do banco de dados
nomes_orientadores = db.get_orientador()
# Obtém a lista de nomes dos cursos do banco de dados
cursos = db.get_curso()

# Define a função para exibir a tela de orientadores
def tela_orientadores(page: ft.Page, usuario):
    """
    Cria a tela de gerenciamento de orientadores.

    Args:
        page (ft.Page): A página Flet atual.
        usuario (str): O nome de usuário do usuário logado.
    """

    # Função para lidar com as mudanças no texto da SearchBar
    def handle_change(e):
        """Filtra a lista de orientadores na ListView de acordo com o texto digitado na SearchBar."""
        print(f"handle_change e.data: {e.data}")
        lv.controls.clear()  # Limpa a lista de orientadores na ListView
        if e.data:  # Se houver texto na SearchBar, filtra a lista de orientadores
            for nome in nomes_orientadores:
                if e.data.lower() in nome.lower():  # Verifica se o texto digitado está presente no nome do orientador (case insensitive)
                    lv.controls.append(
                        ft.ListTile(title=ft.Text(nome), on_click=close_anchor, data=nome)  # Adiciona o orientador à ListView
                    )
        else:  # Se não houver texto na SearchBar, exibe todos os orientadores
            for nome in nomes_orientadores:
                lv.controls.append(
                    ft.ListTile(title=ft.Text(nome), on_click=close_anchor, data=nome)  # Adiciona o orientador à ListView
                )
        lv.update()  # Atualiza a ListView

    # Função para fechar a view da SearchBar quando um orientador é selecionado
    def close_anchor(e):
        """Fecha a view da SearchBar e preenche os campos com as informações do orientador selecionado."""
        print(f"Fechando a view do orientador {e.control.data}")
        anchor.close_view(e.control.data)  # Fecha a view da SearchBar
        sbvalue(e.control.data)  # Chama a função para preencher os campos com as informações do orientador

    # Função para preencher os campos de texto com as informações do orientador selecionado
    def sbvalue(nome):
        """Preenche os campos de texto com as informações do orientador selecionado na SearchBar."""
        global orientador_id  # Declara a variável global orientador_id para armazenar o ID do orientador selecionado
        orientador_info = db.get_orientador_info(anchor.value)  # Obtém as informações do orientador do banco de dados a partir do nome selecionado na SearchBar

        # Se o orientador for encontrado no banco de dados
        if orientador_info:
            # Preenche os campos de texto com as informações do orientador
            nome_field.value = orientador_info["nome"]
            telefone_field.value = orientador_info["telefone"]
            email_field.value = orientador_info["email"]
            curso_field.value = orientador_info["curso"]
            titulacao_field.value = orientador_info["titulacao"]
            instituicao_field.value = orientador_info["instituicao"]
            vinculo_field.value = orientador_info["vinculo"]
            polo_field.value = orientador_info["polo"]
            uf_instituicao_field.value = orientador_info["uf_instituicao"]
            lattes_field.value = orientador_info["lattes"]
            orientador_id = orientador_info["id"]  # Armazena o ID do orientador na variável global

            # Define os valores dos dropdowns com as informações do orientador
            curso_dropdown.value = orientador_info["curso"]
            vinculo_dropdown.value = orientador_info["vinculo"]
            polo_dropdown.value = orientador_info["polo"]
            uf_instituicao_dropdown.value = orientador_info["uf_instituicao"]

            # Torna os campos de texto somente leitura
            for field in lista_textfields:
                field.read_only = True

            # Define a visibilidade dos campos de texto e dropdowns
            curso_field.visible = True
            vinculo_field.visible = True
            polo_field.visible = True
            uf_instituicao_field.visible = True
            curso_dropdown.visible = False
            vinculo_dropdown.visible = False
            polo_dropdown.visible = False
            uf_instituicao_dropdown.visible = False

            # Define a visibilidade dos botões
            botao_novo_orientador.visible = False
            botao_atualizar_orientador.visible = True
            botao_excluir_orientador.visible = False

            # Atualiza a página para exibir as alterações
            page.update()
        else:
            # Se o orientador não for encontrado no banco de dados, oculta os botões "Atualizar" e "Excluir"
            botao_atualizar_orientador.visible = False
            botao_excluir_orientador.visible = False

            # Limpa os campos de texto
            for field in lista_textfields:
                telefone_field.value = ""
                lattes_field.value = ""
                field.value = ""

        # Atualiza a lista de orientandos do orientador selecionado
        atualizar_orientandos(anchor.value)
        page.update()

    # Função para limpar os campos de texto e redefinir a visibilidade dos botões
    def clrsbvalue(nome):
        """Limpa os campos de texto e redefine a visibilidade dos botões."""
        # Limpa os campos de texto
        for field in lista_textfields:
            telefone_field.value = ""
            lattes_field.value = ""
            field.value = ""
            field.read_only = True

        # Define a visibilidade dos botões
        botao_salvar.visible = False
        botao_novo_orientador.visible = True
        botao_atualizar_orientador.visible = False
        botao_excluir_orientador.visible = False

        # Define a visibilidade dos campos de texto e dropdowns
        curso_field.visible = True
        vinculo_field.visible = True
        polo_field.visible = True
        uf_instituicao_field.visible = True
        curso_dropdown.visible = False
        vinculo_dropdown.visible = False
        polo_dropdown.visible = False
        uf_instituicao_dropdown.visible = False

        # Limpa a lista de orientandos
        orientandos_view.controls.clear()

        # Atualiza a página para exibir as alterações
        page.update()

    # Cria os campos de texto para exibir as informações do orientador
    nome_field = ft.TextField(label="Nome", width=800, height=50, read_only=True, bgcolor="WHITE")
    telefone_field = ft.TextField(
        label="Telefone (Com DDD, somente números)",
        width=650,
        height=75,
        read_only=True,
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
    email_field = ft.TextField(label="Email", width=800, height=50, read_only=True, bgcolor="WHITE")
    curso_field = ft.TextField(label="Curso", width=800, height=50, read_only=True, bgcolor="WHITE")
    titulacao_field = ft.TextField(label="Titulação", width=800, height=50, read_only=True, bgcolor="WHITE")
    instituicao_field = ft.TextField(label="Instituição", width=800, height=50, read_only=True, bgcolor="WHITE")
    vinculo_field = ft.TextField(label="Vínculo", width=800, height=50, read_only=True, bgcolor="WHITE")
    polo_field = ft.TextField(label="Polo", width=800, height=50, read_only=True, bgcolor="WHITE")
    uf_instituicao_field = ft.TextField(label="UF da instituição", width=800, height=50, read_only=True, bgcolor="WHITE")
    lattes_field = ft.TextField(
        label="Lattes",
        width=650,
        height=50,
        read_only=True,
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

    # Cria os dropdowns para os campos Curso, Vínculo, Polo e UF da instituição
    curso_dropdown = ft.Dropdown(
        width=800,
        label="Curso",
        options=[ft.dropdown.Option(key=curso) for curso in cursos],  # Define as opções do dropdown com base na lista de cursos
        visible=False,  # O dropdown é inicialmente invisível
        bgcolor="WHITE"
    )
    vinculo_dropdown = ft.Dropdown(
        width=800,
        label="Vínculo",
        options=[
            ft.dropdown.Option("Servidor"),
            ft.dropdown.Option("Magistrado"),
            ft.dropdown.Option("Externo"),
        ],  # Define as opções do dropdown
        visible=False,  # O dropdown é inicialmente invisível
        bgcolor="WHITE"
    )
    polo_dropdown = ft.Dropdown(
        width=800,
        label="Polo",
        options=[ft.dropdown.Option("Porto Velho"), ft.dropdown.Option("Cacoal"), ft.dropdown.Option("N/A")],  # Define as opções do dropdown
        visible=False,  # O dropdown é inicialmente invisível
        bgcolor="WHITE"
    )
    uf_instituicao_dropdown = ft.Dropdown(
        width=800,
        label="UF da instituição",
        options=[
            ft.dropdown.Option("RO"),
            ft.dropdown.Option("AC"),
            ft.dropdown.Option("AM"),
            ft.dropdown.Option("RR"),
            ft.dropdown.Option("PA"),
            ft.dropdown.Option("AP"),
            ft.dropdown.Option("TO"),
            ft.dropdown.Option("MA"),
            ft.dropdown.Option("PI"),
            ft.dropdown.Option("CE"),
            ft.dropdown.Option("RN"),
            ft.dropdown.Option("PB"),
            ft.dropdown.Option("PE"),
            ft.dropdown.Option("AL"),
            ft.dropdown.Option("SE"),
            ft.dropdown.Option("BA"),
            ft.dropdown.Option("MG"),
            ft.dropdown.Option("ES"),
            ft.dropdown.Option("RJ"),
            ft.dropdown.Option("SP"),
            ft.dropdown.Option("PR"),
            ft.dropdown.Option("SC"),
            ft.dropdown.Option("RS"),
            ft.dropdown.Option("MS"),
            ft.dropdown.Option("MT"),
            ft.dropdown.Option("GO"),
            ft.dropdown.Option("DF"),
        ],  # Define as opções do dropdown
        visible=False,  # O dropdown é inicialmente invisível
        bgcolor="WHITE"
    )

    # Cria uma lista com os campos de texto para facilitar a manipulação
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
        curso_dropdown,
        vinculo_dropdown,
        polo_dropdown,
        uf_instituicao_dropdown
    ]

    # Cria a ListView para exibir os orientadores
    lv = ft.ListView()

    # Adiciona todos os orientadores à ListView quando a tela é criada
    for nome in nomes_orientadores:
        lv.controls.append(
            ft.ListTile(title=ft.Text(nome), on_click=close_anchor, data=nome)  # Adiciona o orientador à ListView
        )

    # Cria a SearchBar para buscar orientadores
    anchor = ft.SearchBar(
        view_elevation=4,
        divider_color=ft.colors.AMBER,
        bar_hint_text="Buscar orientador",
        view_hint_text="Selecione um nome",
        on_change=handle_change,  # Define a função a ser chamada quando o texto da SearchBar for alterado
        on_submit=sbvalue,  # Define a função a ser chamada quando um orientador for selecionado na SearchBar
        on_tap=clrsbvalue,  # Define a função a ser chamada quando a SearchBar for clicada
        controls=[lv],  # Adiciona a ListView à SearchBar
    )

    # Cria a ListView para exibir os orientandos do orientador selecionado
    orientandos_view = ft.ListView()

    # Define a função para atualizar a lista de orientandos do orientador selecionado
    def atualizar_orientandos(orientador):
        """Atualiza a lista de orientandos do orientador selecionado na ListView."""
        orientando_info = db.get_orientando(orientador)  # Obtém a lista de orientandos do banco de dados
        orientandos_view.controls.clear()  # Limpa a lista de orientandos na ListView
        if orientando_info:
            for nome in orientando_info:
                orientandos_view.controls.append(ft.ListTile(title=ft.Text(nome)))  # Adiciona o orientando à ListView
        orientandos_view.update()  # Atualiza a ListView

    # Cria os diálogos de confirmação para exclusão, cadastro e atualização de orientadores
    dlg_confirmacao_excluir = ft.AlertDialog(
        modal=True,
        title=ft.Text("Confirmar Exclusão"),
        content=ft.Text("Tem certeza que deseja excluir este orientador?"),
        actions=[
            ft.TextButton(
                "Sim", on_click=lambda e: deletar_orientador_confirmado(orientador_id)  # Define a função a ser chamada quando o botão "Sim" for clicado
            ),
            ft.TextButton("Não", on_click=lambda e: fechar_dialogo_excluir(e)),  # Define a função a ser chamada quando o botão "Não" for clicado
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )

    dlg_confirmacao_novo = ft.AlertDialog(
        modal=True,
        title=ft.Text("Confirmar Cadastro"),
        content=ft.Text("Tem certeza que deseja cadastrar este novo orientador?"),
        actions=[
            ft.TextButton("Sim", on_click=lambda e: cadastrar_orientador_confirmado(e)),  # Define a função a ser chamada quando o botão "Sim" for clicado
            ft.TextButton("Não", on_click=lambda e: fechar_dialogo_novo(e)),  # Define a função a ser chamada quando o botão "Não" for clicado
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )

    dlg_confirmacao_atualizar = ft.AlertDialog(
        modal=True,
        title=ft.Text("Confirmar Atualização"),
        content=ft.Text("Tem certeza que deseja atualizar este orientador?"),
        actions=[
            ft.TextButton("Sim", on_click=lambda e: atualizar_orientador_confirmado(e)),  # Define a função a ser chamada quando o botão "Sim" for clicado
            ft.TextButton("Não", on_click=lambda e: fechar_dialogo_atualizar(e)),  # Define a função a ser chamada quando o botão "Não" for clicado
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )

    # Define as funções para fechar os diálogos de confirmação
    def fechar_dialogo_excluir(e):
        """Fecha o diálogo de confirmação de exclusão."""
        dlg_confirmacao_excluir.open = False
        page.update()

    def fechar_dialogo_novo(e):
        """Fecha o diálogo de confirmação de novo orientador."""
        dlg_confirmacao_novo.open = False
        page.update()

    def fechar_dialogo_atualizar(e):
        """Fecha o diálogo de confirmação de atualização de orientador."""
        dlg_confirmacao_atualizar.open = False
        page.update()

    # Define a função para excluir um orientador do banco de dados após a confirmação
    def deletar_orientador_confirmado(orientador_id):
        """Exclui um orientador do banco de dados após a confirmação."""
        # Exclui o orientador do banco de dados
        db.deletar_pessoa(orientador_id)

        # Registra a ação no log do sistema
        db.registrar_log(
            usuario, "excluir_orientador", f"Orientador: {nome_field.value}"
        )

        # Fecha o diálogo de confirmação
        dlg_confirmacao_excluir.open = False

        # Exibe uma mensagem de sucesso
        page.snack_bar = ft.SnackBar(ft.Text("Orientador excluído com sucesso!"))
        page.snack_bar.open = True

        # Limpa a SearchBar e atualiza a tela
        anchor.value = ""
        sbvalue(anchor.value)
        page.update()

        # Atualiza a lista de orientadores na ListView
        global nomes_orientadores
        nomes_orientadores = db.get_orientador()
        lv.controls.clear()
        for nome in nomes_orientadores:
            lv.controls.append(
                ft.ListTile(title=ft.Text(nome), on_click=close_anchor, data=nome)
            )
        lv.update()

        # Limpa os campos de texto
        for field in lista_textfields:
            field.value = ""
            lattes_field.value = ""
            telefone_field.value = ""
            field.update()

        # Limpa a lista de orientandos
        orientandos_view.controls.clear()
        page.update()

    # Define a função para abrir o diálogo de confirmação de exclusão
    def confirmar_exclusao(e):
        """Abre o diálogo de confirmação de exclusão de orientador."""
        page.dialog = dlg_confirmacao_excluir
        dlg_confirmacao_excluir.open = True
        page.update()

    # Define a função para preparar a tela para o cadastro de um novo orientador
    def novo_orientador(e):
        """Prepara a tela para o cadastro de um novo orientador."""
        # Torna os campos de texto editáveis e limpa seus valores
        for field in lista_textfields:
            field.read_only = False
            lattes_field.read_only = False
            telefone_field.read_only = False
            lattes_field.value = ""
            telefone_field.value = ""
            field.value = ""
            field.update()

        # Define a visibilidade dos campos de texto e dropdowns
        curso_field.visible = False
        vinculo_field.visible = False
        polo_field.visible = False
        uf_instituicao_field.visible = False
        curso_dropdown.visible = True
        vinculo_dropdown.visible = True
        polo_dropdown.visible = True
        uf_instituicao_dropdown.visible = True

        # Limpa a lista de orientandos
        orientandos_view.controls.clear()

        # Define a visibilidade dos botões
        botao_salvar.visible = False
        botao_cadastrar.visible = True
        botao_atualizar_orientador.visible = False
        botao_excluir_orientador.visible = False
        botao_novo_orientador.visible = False

        # Limpa a SearchBar e a torna invisível
        anchor.value = ""
        anchor.visible = False
        anchor.update()

        # Atualiza a página para exibir as alterações
        page.update()

    # Define a função para preparar a tela para a atualização das informações de um orientador
    def atualizar_orientador(e):
        """Prepara a tela para a atualização das informações de um orientador."""
        global orientador_id  # Acessa a variável global orientador_id

        # Define a visibilidade dos campos de texto e dropdowns
        curso_field.visible = False
        vinculo_field.visible = False
        polo_field.visible = False
        uf_instituicao_field.visible = False
        curso_dropdown.visible = True
        vinculo_dropdown.visible = True
        polo_dropdown.visible = True
        uf_instituicao_dropdown.visible = True

        # Atualiza a página para exibir as alterações
        page.update()

        # Preenche os dropdowns com as informações do orientador
        orientador_info = db.get_orientador_info(anchor.value)
        curso_dropdown.value = orientador_info["curso"]
        vinculo_dropdown.value = orientador_info["vinculo"]
        polo_dropdown.value = orientador_info["polo"]
        uf_instituicao_dropdown.value = orientador_info["uf_instituicao"]

        # Torna os campos de texto editáveis
        if orientador_id:
            for field in lista_textfields:
                field.read_only = False
                lattes_field.read_only = False
                telefone_field.read_only = False
                field.update()

        # Define a visibilidade dos botões
        botao_salvar.visible = True
        botao_novo_orientador.visible = False
        botao_atualizar_orientador.visible = False
        botao_excluir_orientador.visible = True

        # Atualiza a página para exibir as alterações
        page.update()

    # Define a função para abrir o diálogo de confirmação de cadastro
    def insert_new_orientador(e):
        """Abre o diálogo de confirmação de cadastro de orientador."""
        page.dialog = dlg_confirmacao_novo
        dlg_confirmacao_novo.open = True
        page.update()

    # Define a função para abrir o diálogo de confirmação de atualização
    def save_orientador(e):
        """Abre o diálogo de confirmação de atualização de orientador."""
        page.dialog = dlg_confirmacao_atualizar
        dlg_confirmacao_atualizar.open = True
        page.update()

    # Define a função para cadastrar um novo orientador após a confirmação
    def cadastrar_orientador_confirmado(e):
        """Cadastra um novo orientador no banco de dados após a confirmação."""

        # Verifica se os campos obrigatórios estão preenchidos
        campos_obrigatorios = [
            nome_field,
            instituicao_field,
            vinculo_dropdown,
        ]
        campos_nao_preenchidos = [campo for campo in campos_obrigatorios if not campo.value]

        # Se houver campos não preenchidos
        if campos_nao_preenchidos:
            # Destaca os campos não preenchidos em vermelho
            for campo in campos_nao_preenchidos:
                campo.bgcolor = ft.colors.RED_ACCENT_100

            # Exibe um alerta informando que os campos obrigatórios devem ser preenchidos
            dlg = ft.AlertDialog(
                title=ft.Text("Campos Obrigatórios"),
                content=ft.Text("Preencha todos os campos obrigatórios."),
                actions=[ft.TextButton("Ok", on_click=lambda e: fechar_dialogo(dlg))]
            )
            page.dialog = dlg
            dlg.open = True
            page.update()
        # Se todos os campos obrigatórios estiverem preenchidos
        else:
            # Cria um dicionário com os dados do novo orientador
            orientador_data = {
                "nome": nome_field.value,
                "telefone": telefone_field.value if telefone_field.value else "Não informado",  # Define "Não informado" se o campo estiver vazio
                "email": email_field.value if email_field.value else "Não informado",  # Define "Não informado" se o campo estiver vazio
                "curso": curso_dropdown.value if curso_dropdown.value else "Não informado",  # Define "Não informado" se o campo estiver vazio
                "titulacao": titulacao_field.value if titulacao_field.value else "Não informado",  # Define "Não informado" se o campo estiver vazio
                "instituicao": instituicao_field.value,
                "vinculo": vinculo_dropdown.value,
                "polo": polo_dropdown.value,
                "uf_instituicao": uf_instituicao_dropdown.value,
                "lattes": lattes_field.value if lattes_field.value else "Não informado",  # Define "Não informado" se o campo estiver vazio
            }
            # Insere o novo orientador no banco de dados
            db.insert_orientador(orientador_data)

            # Registra a ação no log do sistema
            db.registrar_log(
                usuario,
                "inserir_orientador",
                f"Orientador: {orientador_data['nome']}",
            )

            # Fecha o diálogo de confirmação
            dlg_confirmacao_novo.open = False

            # Exibe uma mensagem de sucesso
            page.snack_bar = ft.SnackBar(ft.Text("Orientador cadastrado com sucesso!"))
            page.snack_bar.open = True
            page.update()

            # Atualiza a lista de orientadores na ListView
            global nomes_orientadores
            nomes_orientadores = db.get_orientador()
            lv.controls.clear()
            for nome in nomes_orientadores:
                lv.controls.append(
                    ft.ListTile(title=ft.Text(nome), on_click=close_anchor, data=nome)
                )
            lv.update()

            # Retorna os campos para o estado inicial (somente leitura e vazios)
            for field in lista_textfields:
                field.read_only = True
                field.value = ''

            # Define a visibilidade dos campos de texto e dropdowns
            curso_field.visible = True
            vinculo_field.visible = True
            polo_field.visible = True
            uf_instituicao_field.visible = True
            curso_dropdown.visible = False
            vinculo_dropdown.visible = False
            polo_dropdown.visible = False
            uf_instituicao_dropdown.visible = False

            # Define a visibilidade dos botões
            botao_novo_orientador.visible = True
            botao_salvar.visible = False
            botao_cadastrar.visible = False

            # Torna a SearchBar visível
            anchor.visible = True

            # Define a cor de fundo do campo "Instituição" como branco
            instituicao_field.bgcolor = "WHITE"

            # Atualiza a página para exibir as alterações
            page.update()

    # Define a função para fechar um diálogo genérico
    def fechar_dialogo(dlg):
        """Fecha o diálogo."""
        dlg.open = False
        page.update()

    # Define a função para atualizar um orientador no banco de dados após a confirmação
    def atualizar_orientador_confirmado(e):
        """Atualiza um orientador no banco de dados após a confirmação."""
        # Cria um dicionário com os dados do orientador a ser atualizado
        orientador_data = {
            "nome": nome_field.value,
            "telefone": telefone_field.value,
            "email": email_field.value,
            "curso": curso_dropdown.value,
            "titulacao": titulacao_field.value,
            "instituicao": instituicao_field.value,
            "vinculo": vinculo_dropdown.value,
            "polo": polo_dropdown.value,
            "uf_instituicao": uf_instituicao_dropdown.value,
            "lattes": lattes_field.value,
            "id": orientador_id,
        }

        # Atualiza o orientador no banco de dados
        db.update_orientador(orientador_data)

        # Registra a ação no log do sistema
        db.registrar_log(
            usuario,
            "atualizar_orientador",
            f"Orientador: {orientador_data['nome']}",
        )

        # Fecha o diálogo de confirmação
        dlg_confirmacao_atualizar.open = False

        # Exibe uma mensagem de sucesso
        page.snack_bar = ft.SnackBar(ft.Text("Orientador atualizado com sucesso!"))
        page.snack_bar.open = True

        # Torna os campos de texto somente leitura
        for field in lista_textfields:
            field.read_only = True
            lattes_field.read_only = True
            telefone_field.read_only = True

        # Atualiza a tela com as informações do orientador atualizado
        sbvalue(anchor.value)

        # Define a visibilidade dos botões
        botao_atualizar_orientador.visible = True
        botao_cadastrar.visible = False
        botao_excluir_orientador.visible = False
        botao_salvar.visible = False

        # Define a visibilidade dos campos de texto e dropdowns
        curso_field.visible = True
        vinculo_field.visible = True
        polo_field.visible = True
        uf_instituicao_field.visible = True
        curso_dropdown.visible = False
        vinculo_dropdown.visible = False
        polo_dropdown.visible = False
        uf_instituicao_dropdown.visible = False

        # Atualiza a página para exibir as alterações
        page.update()

    # Define a função para abrir o WhatsApp com o número de telefone do orientador
    def abrir_whatsapp(telefone):
        """Abre o WhatsApp Web com o número de telefone fornecido."""
        if telefone:
            page.launch_url(
                f"https://wa.me/55{telefone.replace(' ', '').replace('-', '')}"
            )

    # Cria os botões da tela
    botao_novo_orientador = ft.ElevatedButton(
        text="Novo orientador",
        width=185,
        height=40,
        bgcolor="#006BA0",
        color="WHITE",
        on_click=novo_orientador,  # Define a função a ser chamada quando o botão for clicado
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
    )
    botao_atualizar_orientador = ft.ElevatedButton(
        text="Atualizar cadastro",
        width=185,
        height=40,
        bgcolor="#006BA0",
        color="WHITE",
        on_click=atualizar_orientador,  # Define a função a ser chamada quando o botão for clicado
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
        visible=False,  # O botão é inicialmente invisível
    )
    botao_salvar = ft.ElevatedButton(
        text="Salvar",
        width=185,
        height=40,
        bgcolor="#006BA0",
        color="WHITE",
        on_click=save_orientador,  # Define a função a ser chamada quando o botão for clicado
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
        visible=False,  # O botão é inicialmente invisível
    )
    botao_cadastrar = ft.ElevatedButton(
        text="Cadastrar",
        width=185,
        height=40,
        bgcolor="#006BA0",
        color="WHITE",
        on_click=insert_new_orientador,  # Define a função a ser chamada quando o botão for clicado
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
        visible=False,  # O botão é inicialmente invisível
    )
    botao_excluir_orientador = ft.ElevatedButton(
        text="Excluir",
        width=185,
        height=40,
        bgcolor="#006BA0",
        color="WHITE",
        on_click=confirmar_exclusao,  # Define a função a ser chamada quando o botão for clicado
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
        visible=False,  # O botão é inicialmente invisível
    )

    # Cria um container para organizar os botões
    container_botoes = ft.Container(
        width=800,
        content=ft.ResponsiveRow(
            alignment=ft.MainAxisAlignment.END,
            controls=[
                botao_novo_orientador,
                botao_atualizar_orientador,
                botao_salvar,
                botao_cadastrar,
                botao_excluir_orientador,
            ],
        ),
    )

    # Cria um container para a ListView de orientandos
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

    # Cria o título da tela
    nome_campo = ft.Text("DADOS CADASTRAIS - ORIENTADORES", size=16, color="#006BA0", font_family="Roboto", weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER)

    # Cria o container principal da tela
    container_orientador = ft.Container(
        expand=True,  # Permite que o container se expanda para preencher o espaço disponível
        content=ft.Column(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,  # Alinha o conteúdo horizontalmente ao centro
            scroll=ft.ScrollMode.AUTO,  # Habilita a rolagem automática quando o conteúdo excede o tamanho do container
            controls=[
                ft.Container(
                    width=800,  # Define a largura do container interno
                    content=ft.Column(
                        scroll=ft.ScrollMode.ALWAYS,  # Habilita a rolagem vertical quando o conteúdo excede o tamanho do container
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,  # Alinha o conteúdo horizontalmente ao centro
                        controls=[
                            nome_campo,  # Título da tela
                            ft.Divider(),  # Divisor visual
                            anchor,  # SearchBar para buscar orientadores
                            container_botoes,  # Container com os botões
                            nome_field,  # Campo de texto para o nome
                            ft.ResponsiveRow(controls=[telefone_field, telefone_icon]),  # Linha responsiva com o campo de telefone e o ícone do WhatsApp
                            email_field,  # Campo de texto para o email
                            curso_dropdown,  # Dropdown para selecionar o curso
                            curso_field,  # Campo de texto para o curso (visível quando o dropdown estiver oculto)
                            titulacao_field,  # Campo de texto para a titulação
                            instituicao_field,  # Campo de texto para a instituição
                            vinculo_dropdown,  # Dropdown para selecionar o vínculo
                            vinculo_field,  # Campo de texto para o vínculo (visível quando o dropdown estiver oculto)
                            polo_dropdown,  # Dropdown para selecionar o polo
                            polo_field,  # Campo de texto para o polo (visível quando o dropdown estiver oculto)
                            uf_instituicao_dropdown,  # Dropdown para selecionar a UF da instituição
                            uf_instituicao_field,  # Campo de texto para a UF da instituição (visível quando o dropdown estiver oculto)
                            ft.ResponsiveRow(controls=[lattes_field, lattes_icon]),  # Linha responsiva com o campo do Lattes e o ícone de link
                            container_listview,  # Container com a ListView de orientandos
                        ],
                    ),
                ),
            ],
        ),
        margin=ft.margin.only(bottom=20),  # Define a margem inferior do container principal
    )

    # Retorna o container principal da tela
    return container_orientador
