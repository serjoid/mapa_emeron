import flet as ft
from database import Database

db = Database()
nomes_cursos = db.get_curso()
def tela_cursos(page: ft.Page, usuario): # Passa o objeto page para a função
    def handle_change(e):
        print(f"handle_change e.data: {e.data}")
        lv.controls.clear()
        if e.data:  # Se há texto na SearchBar, filtre a lista de alunos
            for nome in nomes_cursos:
                if e.data.lower() in nome.lower():
                    lv.controls.append(
                        ft.ListTile(
                            title=ft.Text(nome), on_click=close_anchor, data=nome
                        )
                    )
        else:  # Se não há texto na SearchBar, exiba todos os alunos
            for nome in nomes_cursos:
                lv.controls.append(
                    ft.ListTile(
                        title=ft.Text(nome), on_click=close_anchor, data=nome
                    )
                )
        lv.update()

    def close_anchor(e):
        print(f"Fechando a view do curso {e.control.data}")
        anchor.close_view(e.control.data)

        # Chamar sbvalue para atualizar os TextFields
        sbvalue(e.data)

    def sbvalue(nome):
        global curso_id  # Declaração da variável global curso_id
        curso_info = db.get_curso_info(anchor.value)
        if curso_info:
            nome_curso_field.value = curso_info["nome_curso"]
            sigla_curso_field.value = curso_info["sigla_curso"]
            tipo_curso_field.value = curso_info["tipo_curso"]
            area_curso_field.value = curso_info["area_curso"]
            coordenador_curso_field.value = curso_info["coordenador_curso"]
            curso_id = curso_info["ID"]

            # Make the "Atualizar" button visible
            botao_atualizar_curso.visible = True
            botao_excluir_curso.visible = True  # Torna o botão Excluir visível

            # Atualiza todos os campos de texto
            page.update()
        else:
            # If no course is found, hide the "Atualizar" button
            botao_atualizar_curso.visible = False
            botao_excluir_curso.visible = False  # Torna o botão Excluir invisível

        # Update the button visibility
        page.update()

    def clrsbvalue(nome):
        for field in [
            nome_curso_field,
            sigla_curso_field,
            tipo_curso_field,
            area_curso_field,
            coordenador_curso_field,
        ]:
            field.value = ""
        botao_atualizar_curso.visible = False
        botao_cadastrar.visible = False
        botao_excluir_curso.visible = False
        botao_salvar.visible = False
        botao_novo_curso.visible = True
        page.update()

    lv = ft.ListView()
    # Adicione todos os alunos ao ListView quando a tela de alunos é criada
    for nome in nomes_cursos:
        lv.controls.append(
            ft.ListTile(title=ft.Text(nome), on_click=close_anchor, data=nome)
        )
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

    lista_textfields = [
        nome_curso_field,
        sigla_curso_field,
        tipo_curso_field,
        area_curso_field,
        coordenador_curso_field,
    ]

    anchor = ft.SearchBar(
        view_elevation=4,
        divider_color=ft.colors.AMBER,
        bar_hint_text="Buscar por curso",
        view_hint_text="Escolha um curso",
        on_change=handle_change,
        on_submit=sbvalue,
        on_tap=clrsbvalue,
        controls=[lv],
    )

    # Diálogos de Confirmação
    dlg_confirmacao_excluir = ft.AlertDialog(
        modal=True,
        title=ft.Text("Confirmar Exclusão"),
        content=ft.Text("Tem certeza que deseja excluir este curso?"),
        actions=[
            ft.TextButton(
                "Sim", on_click=lambda e: deletar_curso_confirmado(curso_id)
            ),
            ft.TextButton("Não", on_click=lambda e: fechar_dialogo_excluir(e)),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )

    dlg_confirmacao_novo = ft.AlertDialog(
        modal=True,
        title=ft.Text("Confirmar Cadastro"),
        content=ft.Text("Tem certeza que deseja cadastrar este novo curso?"),
        actions=[
            ft.TextButton("Sim", on_click=lambda e: cadastrar_curso_confirmado(e)),  # Passa 'e' aqui
            ft.TextButton("Não", on_click=lambda e: fechar_dialogo_novo(e)),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )

    dlg_confirmacao_atualizar = ft.AlertDialog(
        modal=True,
        title=ft.Text("Confirmar Atualização"),
        content=ft.Text("Tem certeza que deseja atualizar este curso?"),
        actions=[
            ft.TextButton("Sim", on_click=lambda e: atualizar_curso_confirmado(e)),  # Passa 'e' aqui
            ft.TextButton("Não", on_click=lambda e: fechar_dialogo_atualizar(e)),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )

    def fechar_dialogo_excluir(e):
        dlg_confirmacao_excluir.open = False
        page.update()

    def fechar_dialogo_novo(e):
        dlg_confirmacao_novo.open = False
        page.update()

    def fechar_dialogo_atualizar(e):
        dlg_confirmacao_atualizar.open = False
        page.update()

    def deletar_curso_confirmado(curso_id):
        db.deletar_curso(curso_id)
        db.registrar_log(usuario, "excluir_curso", f"Curso ID: {curso_id}") # Registra o log
        dlg_confirmacao_excluir.open = False
        page.snack_bar = ft.SnackBar(ft.Text("Curso excluído com sucesso!"))
        page.snack_bar.open = True
        page.update()

        # Atualizar a lista de cursos e os campos
        global nomes_cursos
        nomes_cursos = db.get_curso()
        lv.controls.clear()
        for nome in nomes_cursos:
            lv.controls.append(
                ft.ListTile(title=ft.Text(nome), on_click=close_anchor, data=nome)
            )
        lv.update()

        # Limpar os campos
        for field in lista_textfields:
            field.value = ""
            
        page.update()

    # Função para abrir o diálogo de confirmação
    def confirmar_exclusao(e):
        page.dialog = dlg_confirmacao_excluir
        dlg_confirmacao_excluir.open = True
        page.update()
        
    # Funções dos botões
    def novo_curso(e):
        for field in lista_textfields:
            field.read_only = False
            field.value = ""
            
        botao_novo_curso.visible = False
        botao_salvar.visible = False
        botao_excluir_curso.visible = False
        botao_atualizar_curso.visible = False
        botao_cadastrar.visible = True
        anchor.value = ""
        anchor.visible = False
        
        page.update()

    def atualizar_curso(e):
        global curso_id  # Acessa a variável global curso_id
        for field in lista_textfields:
            field.read_only = False
        botao_atualizar_curso.visible = False    
        botao_novo_curso.visible = False
        botao_salvar.visible = True
        
        page.update()

    def insert_new_curso(e):
        # Abre o diálogo de confirmação
        page.dialog = dlg_confirmacao_novo
        dlg_confirmacao_novo.open = True
        # Oculta botão atualizar
        botao_atualizar_curso.visible = False
        botao_novo_curso.visible = False
        botao_cadastrar.visible = True
        
        page.update() 

    def save_curso(e):
        # Abre o diálogo de confirmação
        page.dialog = dlg_confirmacao_atualizar
        dlg_confirmacao_atualizar.open = True
        # Oculta botão atualizar
        botao_atualizar_curso.visible = False
        botao_cadastrar.visible = False
        botao_excluir_curso.visible = False
        botao_cadastrar.visible = True
        page.update()

    def cadastrar_curso_confirmado(e):  # Função movida para fora
        curso_data = {
            "nome_curso": nome_curso_field.value,
            "sigla_curso": sigla_curso_field.value,
            "tipo_curso": tipo_curso_field.value,
            "area_curso": area_curso_field.value,
            "coordenador_curso": coordenador_curso_field.value,
        }
        # Chamar o método de atualização da DAO
        db.insert_curso(curso_data)
        db.registrar_log(usuario, "inserir_curso", f"Curso: {curso_data['nome_curso']}") # Registra o log
        dlg_confirmacao_novo.open = False  # Fecha o diálogo
        page.snack_bar = ft.SnackBar(ft.Text("Curso cadastrado com sucesso!"))
        page.snack_bar.open = True
        # Visibilidade
        botao_novo_curso.visible = True
        botao_atualizar_curso.visible = False
        botao_excluir_curso.visible = False
        botao_salvar.visible = False
        botao_cadastrar.visible = False
        page.update()
        # Refresh the 'nomes_cursos' list
        global nomes_cursos  # Access the global variable
        nomes_cursos = db.get_curso()
        # Update the ListView
        lv.controls.clear()
        for nome in nomes_cursos:
            lv.controls.append(
                ft.ListTile(title=ft.Text(nome), on_click=close_anchor, data=nome)
            )
        lv.update()
        # retorna os campos para somente leitura
        for field in lista_textfields:
            field.read_only = True
            field.value = ""
        anchor.visible = True
        
        page.update()

    def atualizar_curso_confirmado(e):  # Função movida para fora
        # Coletar dados dos TextField
        curso_data = {
            "nome_curso": nome_curso_field.value,
            "sigla_curso": sigla_curso_field.value,
            "tipo_curso": tipo_curso_field.value,
            "area_curso": area_curso_field.value,
            "coordenador_curso": coordenador_curso_field.value,
            "ID": curso_id,  # Inclui o ID do curso
        }
        # Chamar o método de atualização da DAO
        db.update_curso(curso_data)
        db.registrar_log(usuario, "atualizar_curso", f"Curso ID: {curso_id}") # Registra o log

        dlg_confirmacao_atualizar.open = False  # Fecha o diálogo
        page.snack_bar = ft.SnackBar(ft.Text("Curso atualizado com sucesso!"))
        page.snack_bar.open = True
        page.update()

        for field in lista_textfields:
            field.read_only = True
            field.value = ""
            
        botao_novo_curso.visible = True
        botao_salvar.visible = False
        botao_cadastrar.visible = False
        botao_excluir_curso.visible = False
        botao_atualizar_curso.visible = False
        
        page.update()

        # Atualizar a ListView
        global nomes_cursos
        nomes_cursos = db.get_curso()
        lv.controls.clear()
        for nome in nomes_cursos:
            lv.controls.append(
                ft.ListTile(title=ft.Text(nome), on_click=close_anchor, data=nome)
            )
        lv.update()

        # Atualizar a SearchBar (opcional)
        anchor.value = ""
        
        page.update()

    # Botões
    botao_novo_curso = ft.ElevatedButton(
        text="Novo curso",
        width=200,
        height=40,
        bgcolor="#006BA0",
        color=ft.colors.WHITE,
        on_click=novo_curso,
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
    )
    botao_atualizar_curso = ft.ElevatedButton(
        text="Atualizar cadastro",
        width=200,
        height=40,
        bgcolor="#006BA0",
        color=ft.colors.WHITE,
        on_click=atualizar_curso,
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
        visible=False,
    )
    botao_salvar = ft.ElevatedButton(
        text="Salvar",
        width=200,
        height=40,
        bgcolor="#006BA0",
        color=ft.colors.WHITE,
        on_click=save_curso,
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
        visible=False,
    )
    botao_cadastrar = ft.ElevatedButton(
        text="Cadastrar",
        width=200,
        height=40,
        bgcolor="#006BA0",
        color=ft.colors.WHITE,
        on_click=insert_new_curso,
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
        visible=False,
    )
    botao_excluir_curso = ft.ElevatedButton(
        text="Excluir",
        width=200,
        height=40,
        bgcolor="#006BA0",
        color=ft.colors.WHITE,
        on_click=confirmar_exclusao,
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
        visible=False,
    )

    botoes = ft.Container(
        width=800,
        content=ft.ResponsiveRow(
            alignment=ft.MainAxisAlignment.END,
            controls=[
                botao_novo_curso,
                botao_atualizar_curso,
                botao_salvar,
                botao_cadastrar,
                botao_excluir_curso,  # Adicione o botão Excluir aqui
            ],
        ),
    )

    nome_campo = ft.Text("CURSOS", size=16, color="#006BA0", font_family="Roboto", weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER)

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
                                scroll=ft.ScrollMode.ALWAYS,
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                controls=[
                                    nome_campo,
                                    ft.Divider(),
                                    anchor,
                                    botoes,
                                    *lista_textfields,
                                ]
                            )
                        ],
                    ),
                )
            ],
        ),
    )

    return container_cursos