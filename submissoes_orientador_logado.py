import flet as ft
from database import Database

# Conexão com o banco de dados
db = Database()


def submissoes_orientador_logado(page: ft.Page, usuario):  # Passa o objeto page para a função

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

    # Função para carregar os dados da submissão com base no aluno selecionado no dropdown
    def carregar_dados_submissao_dropdown(e):
        nome_aluno = dropdown_alunos.value
        if nome_aluno:
            carregar_dados_submissao(nome_aluno)

            # Oculta campos de edição e mostra botões padrão
            container_campos.visible = False
            botao_salvar_novo.visible = False
            botao_nova_submissao.visible = True
            page.update() # Atualização da página

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
        page.update() # Atualização da página

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
        page.update() # Atualização da página

    def excluir_submissao(submissao_id):
        """Exclui uma submissão e recarrega os dados da tabela."""
        db.excluir_submissao(submissao_id)
        db.registrar_log(usuario, "excluir_submissao", f"Submissão ID: {submissao_id}")  # Registra o log
        carregar_dados_submissao(dropdown_alunos.value)  # Recarrega as submissões do aluno

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
        page.update() # Atualização da página

    # Função para abrir o diálogo de confirmação para salvar uma nova submissão
    def salvar_nova_submissao(e):
        page.dialog = dlg_confirmacao_novo
        dlg_confirmacao_novo.open = True
        page.update()

    # Função chamada após confirmar a nova submissão no diálogo
    def confirmar_salvar_nova_submissao(e):
        pessoa_id = db.get_pessoa_info(nome=dropdown_alunos.value).get('id')
        submissao_data = {
            'id_pessoa': pessoa_id,
            'link': link_field.value,
        }
        db.inserir_submissao(submissao_data)
        db.registrar_log(usuario, "inserir_submissao", f"Submissão para: {dropdown_alunos.value}, Link: {submissao_data['link']}")  # Registra o log com o link
        carregar_dados_submissao(dropdown_alunos.value)
        limpar_campos()
        container_campos.visible = False
        tabela_submissoes.visible = True
        botao_salvar_novo.visible = False
        botao_nova_submissao.visible = True
        page.update() # Atualização da página
        fechar_dialogo(e)
    
    # Obtém o nome do orientador a partir do usuário logado
    orientador = db.get_orientador_info_por_usuario(usuario)['nome']

    # Obtém os nomes dos alunos que têm o orientador logado
    nomes_alunos = db.get_orientando(orientador)

    # Cria o dropdown com os nomes dos alunos
    dropdown_alunos = ft.Dropdown(
        width=800,
        options=[ft.dropdown.Option(nome) for nome in nomes_alunos],
        on_change=carregar_dados_submissao_dropdown,
    )

    # Botões (agora criados depois da definição das funções)
    botao_nova_submissao = ft.ElevatedButton(
        text="Nova Submissão",
        width=150,
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

    # Container para o dropdown e botões com largura máxima de 1300 pixels
    container_dropdown_botoes = ft.Container(
        width=1300,
        content=ft.ResponsiveRow(
            controls=[
                dropdown_alunos,
                botao_nova_submissao,
                botao_salvar_novo
            ],
            alignment=ft.MainAxisAlignment.START,
        )
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
        width=1300, # Largura máxima do container
        content=ft.ResponsiveRow(
            controls=[
                link_field,
            ],
            alignment=ft.MainAxisAlignment.CENTER
        ),
        visible=False
    )

    container_submissoes = ft.Container(
        expand=True,
        content=ft.Column(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                container_dropdown_botoes, # Container para dropdown e botões
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