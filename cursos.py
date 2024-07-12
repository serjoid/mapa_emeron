import flet as ft
from database import Database

# Inicializa a conexão com o banco de dados
db = Database()

# Obtém a lista de nomes dos cursos do banco de dados
nomes_cursos = db.get_curso()

# Define a função para exibir a tela de gerenciamento de cursos
def tela_cursos(page: ft.Page, usuario):
    """
    Exibe a tela de gerenciamento de cursos.

    Args:
        page (ft.Page): A página Flet atual.
        usuario (str): O nome de usuário do usuário logado.
    """

    # Função para lidar com as mudanças no texto da SearchBar
    def handle_change(e):
        """Filtra a lista de cursos na ListView de acordo com o texto digitado na SearchBar."""
        print(f"handle_change e.data: {e.data}")
        lv.controls.clear()  # Limpa a lista de cursos na ListView
        if e.data:  # Se houver texto na SearchBar, filtra a lista de cursos
            for nome in nomes_cursos:
                if e.data.lower() in nome.lower():  # Verifica se o texto digitado está presente no nome do curso (case insensitive)
                    lv.controls.append(
                        ft.ListTile(
                            title=ft.Text(nome), on_click=close_anchor, data=nome  # Adiciona o curso à ListView
                        )
                    )
        else:  # Se não houver texto na SearchBar, exibe todos os cursos
            for nome in nomes_cursos:
                lv.controls.append(
                    ft.ListTile(
                        title=ft.Text(nome), on_click=close_anchor, data=nome  # Adiciona o curso à ListView
                    )
                )
        lv.update()  # Atualiza a ListView

    # Função para fechar a view da SearchBar quando um curso é selecionado
    def close_anchor(e):
        """Fecha a view da SearchBar e preenche os campos com as informações do curso selecionado."""
        print(f"Fechando a view do curso {e.control.data}")
        anchor.close_view(e.control.data)  # Fecha a view da SearchBar

        # Preenche os campos de texto com as informações do curso selecionado
        sbvalue(e.data)

    # Função para preencher os campos de texto com as informações do curso selecionado
    def sbvalue(nome):
        """Preenche os campos de texto com as informações do curso selecionado na SearchBar."""
        global curso_id  # Declara a variável global curso_id para armazenar o ID do curso selecionado
        curso_info = db.get_curso_info(anchor.value)  # Obtém as informações do curso do banco de dados a partir do nome selecionado na SearchBar

        # Se o curso for encontrado no banco de dados
        if curso_info:
            # Preenche os campos de texto com as informações do curso
            nome_curso_field.value = curso_info["nome_curso"]
            sigla_curso_field.value = curso_info["sigla_curso"]
            tipo_curso_field.value = curso_info["tipo_curso"]
            area_curso_field.value = curso_info["area_curso"]
            coordenador_curso_field.value = curso_info["coordenador_curso"]
            curso_id = curso_info["ID"]  # Armazena o ID do curso na variável global

            # Torna os botões "Atualizar" e "Excluir" visíveis
            botao_atualizar_curso.visible = True
            botao_excluir_curso.visible = True

            # Atualiza a página para exibir as alterações
            page.update()
        else:
            # Se o curso não for encontrado no banco de dados, oculta os botões "Atualizar" e "Excluir"
            botao_atualizar_curso.visible = False
            botao_excluir_curso.visible = False

        # Atualiza a página para exibir as alterações na visibilidade dos botões
        page.update()

    # Função para limpar os campos de texto e redefinir a visibilidade dos botões
    def clrsbvalue(nome):
        """Limpa os campos de texto e redefine a visibilidade dos botões."""
        # Limpa os campos de texto
        for field in [
            nome_curso_field,
            sigla_curso_field,
            tipo_curso_field,
            area_curso_field,
            coordenador_curso_field,
        ]:
            field.value = ""

        # Define a visibilidade dos botões
        botao_atualizar_curso.visible = False
        botao_cadastrar.visible = False
        botao_excluir_curso.visible = False
        botao_salvar.visible = False
        botao_novo_curso.visible = True

        # Atualiza a página para exibir as alterações
        page.update()

    # Cria a ListView para exibir os cursos
    lv = ft.ListView()

    # Adiciona todos os cursos à ListView quando a tela é criada
    for nome in nomes_cursos:
        lv.controls.append(
            ft.ListTile(title=ft.Text(nome), on_click=close_anchor, data=nome)  # Adiciona o curso à ListView
        )

    # Cria os campos de texto para exibir as informações do curso
    nome_curso_field = ft.TextField(
        label="Nome do curso", width=800, height=50, read_only=True, bgcolor="WHITE"
    )
    sigla_curso_field = ft.TextField(
        label="Sigla do curso", width=800, height=50, read_only=True, bgcolor="WHITE"
    )
    tipo_curso_field = ft.TextField(
        label="Tipo de curso", width=800, height=50, read_only=True, bgcolor="WHITE"
    )
    area_curso_field = ft.TextField(
        label="Área do curso", width=800, height=50, read_only=True, bgcolor="WHITE"
    )
    coordenador_curso_field = ft.TextField(
        label="Coordenador", width=800, height=50, read_only=True, bgcolor="WHITE"
    )

    # Cria uma lista com os campos de texto para facilitar a manipulação
    lista_textfields = [
        nome_curso_field,
        sigla_curso_field,
        tipo_curso_field,
        area_curso_field,
        coordenador_curso_field,
    ]

    # Cria a SearchBar para buscar cursos
    anchor = ft.SearchBar(
        view_elevation=4,
        divider_color=ft.colors.AMBER,
        bar_hint_text="Buscar por curso",
        view_hint_text="Escolha um curso",
        on_change=handle_change,  # Define a função a ser chamada quando o texto da SearchBar for alterado
        on_submit=sbvalue,  # Define a função a ser chamada quando um curso for selecionado na SearchBar
        on_tap=clrsbvalue,  # Define a função a ser chamada quando a SearchBar for clicada
        controls=[lv],  # Adiciona a ListView à SearchBar
    )

    # Diálogos de confirmação para exclusão, cadastro e atualização de cursos
    dlg_confirmacao_excluir = ft.AlertDialog(
        modal=True,
        title=ft.Text("Confirmar Exclusão"),
        content=ft.Text("Tem certeza que deseja excluir este curso?"),
        actions=[
            ft.TextButton(
                "Sim", on_click=lambda e: deletar_curso_confirmado(curso_id)  # Define a função a ser chamada quando o botão "Sim" for clicado
            ),
            ft.TextButton("Não", on_click=lambda e: fechar_dialogo_excluir(e)),  # Define a função a ser chamada quando o botão "Não" for clicado
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )

    dlg_confirmacao_novo = ft.AlertDialog(
        modal=True,
        title=ft.Text("Confirmar Cadastro"),
        content=ft.Text("Tem certeza que deseja cadastrar este novo curso?"),
        actions=[
            ft.TextButton("Sim", on_click=lambda e: cadastrar_curso_confirmado(e)),  # Define a função a ser chamada quando o botão "Sim" for clicado
            ft.TextButton("Não", on_click=lambda e: fechar_dialogo_novo(e)),  # Define a função a ser chamada quando o botão "Não" for clicado
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )

    dlg_confirmacao_atualizar = ft.AlertDialog(
        modal=True,
        title=ft.Text("Confirmar Atualização"),
        content=ft.Text("Tem certeza que deseja atualizar este curso?"),
        actions=[
            ft.TextButton("Sim", on_click=lambda e: atualizar_curso_confirmado(e)),  # Define a função a ser chamada quando o botão "Sim" for clicado
            ft.TextButton("Não", on_click=lambda e: fechar_dialogo_atualizar(e)),  # Define a função a ser chamada quando o botão "Não" for clicado
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )

    # Funções para fechar os diálogos de confirmação

    def fechar_dialogo_excluir(e):
        """Fecha o diálogo de confirmação de exclusão."""
        dlg_confirmacao_excluir.open = False
        page.update()

    def fechar_dialogo_novo(e):
        """Fecha o diálogo de confirmação de novo curso."""
        dlg_confirmacao_novo.open = False
        page.update()

    def fechar_dialogo_atualizar(e):
        """Fecha o diálogo de confirmação de atualização de curso."""
        dlg_confirmacao_atualizar.open = False
        page.update()

    # Função para excluir um curso do banco de dados após a confirmação
    def deletar_curso_confirmado(curso_id):
        """Exclui um curso do banco de dados após a confirmação."""
        # Exclui o curso do banco de dados
        db.deletar_curso(curso_id)

        # Registra a ação no log do sistema
        db.registrar_log(usuario, "excluir_curso", f"Curso ID: {curso_id}")

        # Fecha o diálogo de confirmação
        dlg_confirmacao_excluir.open = False

        # Exibe uma mensagem de sucesso
        page.snack_bar = ft.SnackBar(ft.Text("Curso excluído com sucesso!"))
        page.snack_bar.open = True
        page.update()

        # Atualiza a lista de cursos
        global nomes_cursos
        nomes_cursos = db.get_curso()
        lv.controls.clear()
        for nome in nomes_cursos:
            lv.controls.append(
                ft.ListTile(title=ft.Text(nome), on_click=close_anchor, data=nome)
            )
        lv.update()

        # Limpa os campos de texto
        for field in lista_textfields:
            field.value = ""
            
        page.update()

    # Função para abrir o diálogo de confirmação de exclusão
    def confirmar_exclusao(e):
        """Abre o diálogo de confirmação de exclusão de curso."""
        page.dialog = dlg_confirmacao_excluir
        dlg_confirmacao_excluir.open = True
        page.update()
        
    # Funções para lidar com os eventos dos botões
    def novo_curso(e):
        """Prepara a tela para o cadastro de um novo curso."""
        # Torna os campos de texto editáveis e limpa seus valores
        for field in lista_textfields:
            field.read_only = False
            field.value = ""
            
        # Define a visibilidade dos botões
        botao_novo_curso.visible = False
        botao_salvar.visible = False
        botao_excluir_curso.visible = False
        botao_atualizar_curso.visible = False
        botao_cadastrar.visible = True

        # Limpa a SearchBar e a torna invisível
        anchor.value = ""
        anchor.visible = False
        
        page.update()

    def atualizar_curso(e):
        """Prepara a tela para a atualização das informações de um curso."""
        global curso_id  # Acessa a variável global curso_id

        # Torna os campos de texto editáveis
        for field in lista_textfields:
            field.read_only = False

        # Define a visibilidade dos botões
        botao_atualizar_curso.visible = False    
        botao_novo_curso.visible = False
        botao_salvar.visible = True
        
        page.update()

    def insert_new_curso(e):
        """Abre o diálogo de confirmação para cadastrar um novo curso."""
        # Abre o diálogo de confirmação
        page.dialog = dlg_confirmacao_novo
        dlg_confirmacao_novo.open = True

        # Define a visibilidade dos botões
        botao_atualizar_curso.visible = False
        botao_novo_curso.visible = False
        botao_cadastrar.visible = True
        
        page.update()

    def save_curso(e):
        """Abre o diálogo de confirmação para salvar as alterações de um curso."""
        # Abre o diálogo de confirmação
        page.dialog = dlg_confirmacao_atualizar
        dlg_confirmacao_atualizar.open = True

        # Define a visibilidade dos botões
        botao_atualizar_curso.visible = False
        botao_cadastrar.visible = False
        botao_excluir_curso.visible = False
        botao_cadastrar.visible = True

        page.update()

    # Função para cadastrar um novo curso após a confirmação
    def cadastrar_curso_confirmado(e):
        """Cadastra um novo curso no banco de dados após a confirmação."""
        # Cria um dicionário com as informações do novo curso
        curso_data = {
            "nome_curso": nome_curso_field.value,
            "sigla_curso": sigla_curso_field.value,
            "tipo_curso": tipo_curso_field.value,
            "area_curso": area_curso_field.value,
            "coordenador_curso": coordenador_curso_field.value,
        }

        # Insere o novo curso no banco de dados
        db.insert_curso(curso_data)

        # Registra a ação no log do sistema
        db.registrar_log(usuario, "inserir_curso", f"Curso: {curso_data['nome_curso']}")

        # Fecha o diálogo de confirmação
        dlg_confirmacao_novo.open = False

        # Exibe uma mensagem de sucesso
        page.snack_bar = ft.SnackBar(ft.Text("Curso cadastrado com sucesso!"))
        page.snack_bar.open = True

        # Define a visibilidade dos botões
        botao_novo_curso.visible = True
        botao_atualizar_curso.visible = False
        botao_excluir_curso.visible = False
        botao_salvar.visible = False
        botao_cadastrar.visible = False

        # Atualiza a página para exibir as alterações
        page.update()

        # Atualiza a lista de cursos na ListView
        global nomes_cursos  # Acessa a variável global
        nomes_cursos = db.get_curso()
        lv.controls.clear()
        for nome in nomes_cursos:
            lv.controls.append(
                ft.ListTile(title=ft.Text(nome), on_click=close_anchor, data=nome)
            )
        lv.update()

        # Retorna os campos de texto para somente leitura e limpa seus valores
        for field in lista_textfields:
            field.read_only = True
            field.value = ""

        # Torna a SearchBar visível
        anchor.visible = True
        
        page.update()

    # Função para atualizar um curso no banco de dados após a confirmação
    def atualizar_curso_confirmado(e):
        """Atualiza um curso no banco de dados após a confirmação."""
        global curso_id  # Acessa a variável global curso_id

        # Cria um dicionário com as informações do curso a ser atualizado
        curso_data = {
            "nome_curso": nome_curso_field.value,
            "sigla_curso": sigla_curso_field.value,
            "tipo_curso": tipo_curso_field.value,
            "area_curso": area_curso_field.value,
            "coordenador_curso": coordenador_curso_field.value,
            "ID": curso_id,  # Inclui o ID do curso para a atualização
        }

        # Atualiza o curso no banco de dados
        db.update_curso(curso_data)

        # Registra a ação no log do sistema
        db.registrar_log(usuario, "atualizar_curso", f"Curso ID: {curso_id}")

        # Fecha o diálogo de confirmação
        dlg_confirmacao_atualizar.open = False

        # Exibe uma mensagem de sucesso
        page.snack_bar = ft.SnackBar(ft.Text("Curso atualizado com sucesso!"))
        page.snack_bar.open = True
        page.update()

        # Retorna os campos de texto para somente leitura e limpa seus valores
        for field in lista_textfields:
            field.read_only = True
            field.value = ""
            
        # Define a visibilidade dos botões
        botao_novo_curso.visible = True
        botao_salvar.visible = False
        botao_cadastrar.visible = False
        botao_excluir_curso.visible = False
        botao_atualizar_curso.visible = False
        
        page.update()

        # Atualiza a lista de cursos na ListView
        global nomes_cursos
        nomes_cursos = db.get_curso()
        lv.controls.clear()
        for nome in nomes_cursos:
            lv.controls.append(
                ft.ListTile(title=ft.Text(nome), on_click=close_anchor, data=nome)
            )
        lv.update()

        # Limpa a SearchBar
        anchor.value = ""
        
        page.update()

    # Cria os botões da tela
    botao_novo_curso = ft.ElevatedButton(
        text="Novo curso",
        width=200,
        height=40,
        bgcolor="#006BA0",
        color=ft.colors.WHITE,
        on_click=novo_curso,  # Define a função a ser chamada quando o botão for clicado
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
    )
    botao_atualizar_curso = ft.ElevatedButton(
        text="Atualizar cadastro",
        width=200,
        height=40,
        bgcolor="#006BA0",
        color=ft.colors.WHITE,
        on_click=atualizar_curso,  # Define a função a ser chamada quando o botão for clicado
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
        visible=False,  # O botão é inicialmente invisível
    )
    botao_salvar = ft.ElevatedButton(
        text="Salvar",
        width=200,
        height=40,
        bgcolor="#006BA0",
        color=ft.colors.WHITE,
        on_click=save_curso,  # Define a função a ser chamada quando o botão for clicado
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
        visible=False,  # O botão é inicialmente invisível
    )
    botao_cadastrar = ft.ElevatedButton(
        text="Cadastrar",
        width=200,
        height=40,
        bgcolor="#006BA0",
        color=ft.colors.WHITE,
        on_click=insert_new_curso,  # Define a função a ser chamada quando o botão for clicado
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
        visible=False,  # O botão é inicialmente invisível
    )
    botao_excluir_curso = ft.ElevatedButton(
        text="Excluir",
        width=200,
        height=40,
        bgcolor="#006BA0",
        color=ft.colors.WHITE,
        on_click=confirmar_exclusao,  # Define a função a ser chamada quando o botão for clicado
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
        visible=False,  # O botão é inicialmente invisível
    )

    # Cria um container para organizar os botões
    botoes = ft.Container(
        width=800,
        content=ft.ResponsiveRow(
            alignment=ft.MainAxisAlignment.END,
            controls=[
                botao_novo_curso,
                botao_atualizar_curso,
                botao_salvar,
                botao_cadastrar,
                botao_excluir_curso,
            ],
        ),
    )

    # Cria o título da tela
    nome_campo = ft.Text("CURSOS", size=16, color="#006BA0", font_family="Roboto", weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER)

    # Cria o container principal da tela
    container_cursos = ft.Container(
        expand=True,
        content=ft.Column(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Container(
                    width=800,
                    content=ft.ResponsiveRow(
                        vertical_alignment=ft.CrossAxisAlignment.START,
                        controls=[
                            ft.Column(
                                expand=True,
                                scroll=ft.ScrollMode.ALWAYS,  # Habilita a rolagem vertical
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                controls=[
                                    nome_campo,  # Título da tela
                                    ft.Divider(),  # Divisor visual
                                    anchor,  # SearchBar para buscar cursos
                                    botoes,  # Container com os botões
                                    *lista_textfields,  # Campos de texto para exibir as informações do curso
                                ]
                            )
                        ],
                    ),
                )
            ],
        ),
    )

    # Retorna o container principal da tela
    return container_cursos
