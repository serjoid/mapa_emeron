import flet as ft
from database import Database

# Conexão com o banco de dados
db = Database()


def submissoes_aluno_logado(page: ft.Page, usuario):
    """
    Exibe e gerencia as submissões do aluno logado.

    Args:
        page (ft.Page): A página Flet atual.
        usuario (str): O nome de usuário do aluno logado.
    """

    # Obtém o ID e o nome do aluno a partir do nome de usuário
    aluno_info = db.get_pessoa_info_por_usuario(usuario)
    aluno_id = aluno_info['id']
    nome_aluno = aluno_info['nome']

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

    # Funções para gerenciar submissões (movidas para cima)
    def carregar_dados_submissao():
        """Carrega as submissões do aluno logado na tabela."""
        submissoes = db.get_submissoes_by_pessoa_id(aluno_id)

        # Preenche as linhas da tabela
        tabela_submissoes.rows.clear()  # Limpa as linhas existentes (se houver)
        for submissao in submissoes:
            excluir_cell = ft.DataCell(
                ft.TextButton(
                    "Excluir",
                    on_click=lambda e, submissao_id=submissao['id']: confirmar_exclusao(
                        e, submissao_id
                    ),
                    data=submissao['id'],  # Armazena o ID da submissão na célula
                )
            )
            tabela_submissoes.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(submissao['link'])),
                        ft.DataCell(ft.Text(submissao['data_hora'])),
                        excluir_cell,  # Adiciona a célula "Excluir"
                    ]
                )
            )
        page.update()  # Atualiza a página

    def confirmar_exclusao(e, submissao_id):
        """Abre o diálogo de confirmação de exclusão."""
        page.dialog = dlg_confirmacao_excluir
        dlg_confirmacao_excluir.open = True
        page.update()
        global submissao_id_excluir  # Acessa a variável global
        submissao_id_excluir = submissao_id

    def confirmar_exclusao_submissao(e):
        """Exclui a submissão após a confirmação do usuário."""
        global submissao_id_excluir  # Acessa a variável global
        db.excluir_submissao(submissao_id_excluir)
        db.registrar_log(usuario, "excluir_submissao", f"Submissão ID: {submissao_id_excluir}")  # Registra o log
        carregar_dados_submissao()  # Recarrega as submissões do aluno
        fechar_dialogo(e)

    def limpar_campos():
        """Limpa o campo de link."""
        link_field.value = ""
        page.update()  # Atualiza a página

    def nova_submissao(e):  # Função movida para cima
        """Prepara a interface para uma nova submissão."""
        limpar_campos()
        container_campos.visible = True
        tabela_submissoes.visible = True
        botao_salvar_novo.visible = True
        botao_nova_submissao.visible = False
        page.update()  # Atualiza a página

    def salvar_nova_submissao(e):
        """Abre o diálogo de confirmação para salvar a submissão."""
        page.dialog = dlg_confirmacao_novo
        dlg_confirmacao_novo.open = True
        page.update()

    def confirmar_salvar_nova_submissao(e):
        """Salva a nova submissão após a confirmação do usuário."""
        submissao_data = {
            'id_pessoa': aluno_id,
            'link': link_field.value,
        }
        db.inserir_submissao(submissao_data)
        db.registrar_log(
            usuario, "inserir_submissao", f"Submissão para: {nome_aluno}, Link: {submissao_data['link']}"
        )  # Registra o log com o link
        carregar_dados_submissao()
        limpar_campos()
        container_campos.visible = False
        tabela_submissoes.visible = True
        botao_salvar_novo.visible = False
        botao_nova_submissao.visible = True
        
        # Fecha o diálogo de confirmação
        dlg_confirmacao_novo.open = False 
        page.update()  # Atualiza a página

    # Tabela de submissões (criada com linhas vazias)
    tabela_submissoes = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Container(ft.Text("Link"), alignment=ft.alignment.center)),
            ft.DataColumn(ft.Container(ft.Text("Data e Hora"), alignment=ft.alignment.center)),
            ft.DataColumn(ft.Container(ft.Text("Ação"), alignment=ft.alignment.center)),
        ],
        rows=[],  # Linhas vazias inicialmente
        border=ft.border.all(2, "black"),
        border_radius=ft.border_radius.all(10)
    )

    link_field = ft.TextField(label="Link", width=1200)

    # Container para o link_field com largura máxima de 1300 pixels
    container_campos = ft.Container(
        width=1300,  # Largura máxima do container
        content=ft.ResponsiveRow(
            controls=[
                link_field,
            ],
            alignment=ft.MainAxisAlignment.CENTER
        ),
        visible=False
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
        on_click=nova_submissao  # Agora a função já está definida
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

    # Container para os botões com largura máxima de 1300 pixels
    container_botoes = ft.Container(
        width=1300,  # Largura máxima do container
        content=ft.ResponsiveRow(
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
                ft.Text(f"Submissões de {nome_aluno}", size=20),
                container_botoes,  # Container para os botões
                container_campos,  # Container para o link_field
                ft.Container(
                    width=1300,
                    content=tabela_submissoes,
                    margin=ft.margin.only(top=10)
                ),
            ]
        )
    )

    # Carrega os dados da submissão imediatamente
    carregar_dados_submissao()

    return container_submissoes