import flet as ft
from database import Database

# Conexão com o banco de dados
db = Database()


def tela_submissoes(page: ft.Page, usuario):  # Passa o objeto page para a função

    # Diálogos de Confirmação
    dlg_confirmacao_excluir = ft.AlertDialog(
        modal=True,
        title=ft.Text("Confirmar Exclusão"),
        content=ft.Text("Tem certeza que deseja excluir esta submissão?"),
        actions=[
            ft.TextButton("Sim", on_click=lambda e: confirmar_exclusao_submissao(e)),
            ft.TextButton("Não", on_click=lambda e: fechar_dialogo(e)),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )
    dlg_confirmacao_novo = ft.AlertDialog(
        modal=True,
        title=ft.Text("Confirmar Cadastro"),
        content=ft.Text("Tem certeza que deseja cadastrar esta nova submissão?"),
        actions=[
            ft.TextButton("Sim", on_click=lambda e: confirmar_salvar_nova_submissao(e)),
            ft.TextButton("Não", on_click=lambda e: fechar_dialogo(e)),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )

    def fechar_dialogo(e):
        dlg_confirmacao_excluir.open = False
        dlg_confirmacao_novo.open = False
        page.update()

    def handle_change(e):
        lv.controls.clear()
        if e.data:
            for nome in nomes_alunos:
                if e.data.lower() in nome.lower():
                    lv.controls.append(
                        ft.ListTile(title=ft.Text(nome), on_click=close_anchor, data=nome)
                    )
        else:
            for nome in nomes_alunos:
                lv.controls.append(
                    ft.ListTile(title=ft.Text(nome), on_click=close_anchor, data=nome)
                )
        lv.update()

    def close_anchor(e):
        anchor.close_view(e.control.data)
        carregar_dados_submissao(e.control.data)
        anchor.value = e.control.data

        # Oculta campos de edição e mostra botões padrão
        container_campos.visible = False
        botao_salvar_novo.visible = False
        botao_nova_submissao.visible = True
        container_campos.update()
        container_botoes.update()

    def carregar_dados_submissao(nome_aluno):
        pessoa_id = db.get_pessoa_info(nome=nome_aluno).get('id')
        submissoes = db.get_submissoes_by_pessoa_id(pessoa_id)
        pessoa_info = db.get_pessoa_info(nome=nome_aluno)

        # Atualiza a tabela de submissões
        tabela_submissoes.rows.clear()
        for submissao in submissoes:
            # Cria a célula "Excluir" com a função de exclusão
            excluir_cell = ft.DataCell(
                ft.TextButton(
                    "Excluir",
                    on_click=lambda e, submissao_id=submissao['id']: confirmar_exclusao(e, submissao_id),
                    data=submissao['id']  # Armazena o ID da submissão na célula
                )
            )

            tabela_submissoes.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(submissao['link'])),
                        ft.DataCell(ft.Text(submissao['data_hora'])),
                        excluir_cell  # Adiciona a célula "Excluir"
                    ]
                )
            )
        tabela_submissoes.update()

        # Atualiza a tabela de informações do aluno
        tabela_info_aluno.rows.clear()
        tabela_info_aluno.rows.append(
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(pessoa_info.get('curso', ''))),
                    ft.DataCell(ft.Text(pessoa_info.get('orientador', '')))
                ]
            )
        )
        tabela_info_aluno.update()

    def excluir_submissao(submissao_id):
        """Exclui uma submissão e recarrega os dados da tabela."""
        db.excluir_submissao(submissao_id)
        db.registrar_log(usuario, "excluir_submissao", f"Submissão ID: {submissao_id}")  # Registra o log
        carregar_dados_submissao(anchor.value)  # Recarrega as submissões do aluno

    def confirmar_exclusao(e, submissao_id):
        page.dialog = dlg_confirmacao_excluir
        dlg_confirmacao_excluir.open = True
        page.update()
        global submissao_id_excluir  # Acessa a variável global
        submissao_id_excluir = submissao_id

    def confirmar_exclusao_submissao(e):
        """Exclui a submissão após a confirmação do usuário."""
        global submissao_id_excluir  # Acessa a variável global
        excluir_submissao(submissao_id_excluir)
        fechar_dialogo(e)

    def limpar_campos():
        link_field.value = ""

    def nova_submissao(e):
        limpar_campos()
        container_campos.visible = True
        tabela_submissoes.visible = True
        botao_salvar_novo.visible = True
        botao_nova_submissao.visible = False
        container_campos.update()
        tabela_submissoes.update()
        container_botoes.update()

    # Função para abrir o diálogo de confirmação para salvar uma nova submissão
    def salvar_nova_submissao(e):
        page.dialog = dlg_confirmacao_novo
        dlg_confirmacao_novo.open = True
        page.update()

    # Função chamada após confirmar a nova submissão no diálogo
    def confirmar_salvar_nova_submissao(e):
        pessoa_id = db.get_pessoa_info(nome=anchor.value).get('id')
        submissao_data = {
            'id_pessoa': pessoa_id,
            'link': link_field.value,
        }
        db.inserir_submissao(submissao_data)
        db.registrar_log(usuario, "inserir_submissao", f"Submissão para: {anchor.value}, Link: {submissao_data['link']}")  # Registra o log com o link
        carregar_dados_submissao(anchor.value)
        limpar_campos()
        container_campos.visible = False
        tabela_submissoes.visible = True
        botao_salvar_novo.visible = False
        botao_nova_submissao.visible = True
        container_campos.update()
        tabela_submissoes.update()
        container_botoes.update()
        fechar_dialogo(e)

    nomes_alunos = db.get_aluno()
    lv = ft.ListView()
    nomes_alunos = db.get_aluno()
    for i in range(0, len(nomes_alunos), 25):
        for nome in nomes_alunos[i:i+25]:
            lv.controls.append(ft.ListTile(title=ft.Text(nome), on_click=close_anchor, data=nome))
        page.update()

    anchor = ft.SearchBar(
        view_elevation=4,
        divider_color=ft.colors.AMBER,
        bar_hint_text="Buscar por nome do aluno.",
        view_hint_text="Escolha um aluno.",
        on_change=handle_change,
        controls=[lv],
    )

    # Tabela de submissões
    tabela_submissoes = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Container(ft.Text("Link"), alignment=ft.alignment.center)),
            ft.DataColumn(ft.Container(ft.Text("Data e Hora"), alignment=ft.alignment.center)),
            ft.DataColumn(ft.Container(ft.Text("Ação"), alignment=ft.alignment.center)),
        ],
        rows=[],
        border=ft.border.all(2, "black"),
        border_radius=ft.border_radius.all(10)
    )

    # Tabela de informações do aluno (curso e orientador)
    tabela_info_aluno = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Container(ft.Text("Curso"), alignment=ft.alignment.center)),
            ft.DataColumn(ft.Container(ft.Text("Orientador"), alignment=ft.alignment.center)),
        ],
        rows=[],
        border=ft.border.all(2, "black"),
        border_radius=ft.border_radius.all(10),
        width=1300
    )

    link_field = ft.TextField(label="Link", width=1200)

    container_campos = ft.Container(
        content=ft.Row(
            controls=[
                link_field,
            ],
            alignment=ft.MainAxisAlignment.CENTER
        ),
        visible=False
    )

    botao_nova_submissao = ft.ElevatedButton(
        text="Nova Submissão",
        width=300,
        height=40,
        elevation=4,
        bgcolor="#006BA0",
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
        color="WHITE",
        on_click=nova_submissao
    )
    botao_salvar_novo = ft.ElevatedButton(
        text="Salvar Nova Submissão",
        width=200,
        height=40,
        elevation=4,
        bgcolor="#006BA0",
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
        color="WHITE",
        on_click=salvar_nova_submissao,
        visible=False
    )
    container_botoes = ft.Container(
        content=ft.Row(
            controls=[
                botao_nova_submissao,
                botao_salvar_novo
            ],
            alignment=ft.MainAxisAlignment.CENTER
        )
    )

    container_submissoes = ft.Container(
        expand=True,
        content=ft.Column(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                container_botoes,
                anchor,
                tabela_info_aluno,  # Adiciona a tabela de informações do aluno
                container_campos,
                ft.Container(
                    width=1300,
                    content=tabela_submissoes,
                    margin=ft.margin.only(top=10)
                ),
            ]
        )
    )

    return container_submissoes