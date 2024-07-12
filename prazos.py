import flet as ft  # Importa a biblioteca Flet
from database import Database  # Importa a classe Database do módulo 'database.py'
from datetime import date, timedelta  # Importa as classes date e timedelta do módulo datetime
import datetime  # Importa o módulo datetime

# Inicializa a conexão com o banco de dados
db = Database()

# Define a função para exibir a tela de prazos
def tela_prazos(page: ft.Page, usuario, nome_aluno=None, mostrar_botao_voltar=False):
    """
    Cria a tela de gerenciamento de prazos.

    Args:
        page (ft.Page): A página Flet atual.
        usuario (str): O nome de usuário do usuário logado.
        nome_aluno (str, optional): O nome do aluno para o qual os prazos devem ser exibidos. Defaults to None.
        mostrar_botao_voltar (bool, optional): Indica se o botão "Voltar" deve ser exibido. Defaults to False.
    """

    # Define a variável global para armazenar os dados da tabela de prazos
    global dados_tabela_prazos
    dados_tabela_prazos = []

    # Obtém a lista de nomes dos alunos do banco de dados
    nomes_alunos = db.get_aluno()

    # Se o nome do aluno for fornecido, carrega os dados do prazo do aluno
    if nome_aluno:
        carregar_dados_prazo(nome_aluno)
        anchor.value = nome_aluno

    # Cria os diálogos de confirmação para exclusão, cadastro e atualização de prazos
    dlg_confirmacao_excluir = ft.AlertDialog(
        modal=True,
        title=ft.Text("Confirmar Exclusão"),
        content=ft.Text("Tem certeza que deseja excluir este prazo?"),
        actions=[
            ft.TextButton("Sim", on_click=lambda e: confirmar_exclusao_prazo(e)),
            ft.TextButton("Não", on_click=lambda e: fechar_dialogo(e)),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )
    dlg_confirmacao_novo = ft.AlertDialog(
        modal=True,
        title=ft.Text("Confirmar Cadastro"),
        content=ft.Text("Tem certeza que deseja cadastrar este novo prazo?"),
        actions=[
            ft.TextButton("Sim", on_click=lambda e: confirmar_salvar_novo_prazo(e)),
            ft.TextButton("Não", on_click=lambda e: fechar_dialogo(e)),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )
    dlg_confirmacao_atualizar = ft.AlertDialog(
        modal=True,
        title=ft.Text("Confirmar Atualização"),
        content=ft.Text("Tem certeza que deseja atualizar este prazo?"),
        actions=[
            ft.TextButton("Sim", on_click=lambda e: confirmar_salvar_prazo(e)),
            ft.TextButton("Não", on_click=lambda e: fechar_dialogo(e)),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )

    # Define a função para fechar os diálogos de confirmação
    def fechar_dialogo(e):
        """Fecha os diálogos de confirmação."""
        dlg_confirmacao_excluir.open = False
        dlg_confirmacao_novo.open = False
        dlg_confirmacao_atualizar.open = False
        page.update()

    # Define a função para lidar com as mudanças no texto da SearchBar
    def handle_change(e):
        """Filtra a lista de alunos na ListView de acordo com o texto digitado na SearchBar."""
        lv.controls.clear()  # Limpa a lista de alunos na ListView
        if e.data:  # Se houver texto na SearchBar, filtra a lista de alunos
            for nome in nomes_alunos:
                if e.data.lower() in nome.lower():  # Verifica se o texto digitado está presente no nome do aluno (case insensitive)
                    lv.controls.append(
                        ft.ListTile(title=ft.Text(nome), on_click=close_anchor, data=nome)  # Adiciona o aluno à ListView
                    )
        else:  # Se não houver texto na SearchBar, exibe todos os alunos
            for nome in nomes_alunos:
                lv.controls.append(
                    ft.ListTile(title=ft.Text(nome), on_click=close_anchor, data=nome)  # Adiciona o aluno à ListView
                )
        lv.update()  # Atualiza a ListView

    # Define a função para fechar a view da SearchBar quando um aluno é selecionado
    def close_anchor(e):
        """Fecha a view da SearchBar e carrega os dados do prazo do aluno selecionado."""
        anchor.close_view(e.control.data)  # Fecha a view da SearchBar
        carregar_dados_prazo(e.control.data)  # Carrega os dados do prazo do aluno selecionado
        anchor.value = e.control.data  # Define o valor da SearchBar como o nome do aluno selecionado

        # Define o valor dos campos de texto com as informações do aluno selecionado
        nome_aluno.value = "Nome: " + f"{db.get_pessoa_info(nome=anchor.value).get('nome', '')}"
        curso.value = "Curso: " + f"{db.get_pessoa_info(nome=anchor.value).get('curso', '')}"
        orientador.value = "Orientador: " + f"{db.get_pessoa_info(nome=anchor.value).get('orientador', '')}"
        tema.value = "Tema: " + f"{db.get_pessoa_info(nome=anchor.value).get('titulo_tcc', '')}"

        # Limpa os controles existentes no container de informações dos prazos
        container_info_prazos.controls.clear()

        # Exibe a tabela de prazos se a tela for maior que 1024 pixels de largura
        if page.width >= 1024:
            tabela_prazos.visible = True

        # Oculta os campos de edição e exibe os botões padrão
        container_campos.visible = False
        container_dropdown.visible = False
        botao_salvar.visible = False
        botao_salvar_novo.visible = False
        botao_novo.visible = True
        botao_atualizar.visible = True

        # Atualiza os containers e a página
        container_campos.update()
        container_dropdown.update()
        container_info_prazos.update()
        atualizar_visualizacao_dados(page)  # Atualiza a visualização dos dados (tabela ou lista)
        page.update()

    # Define a função para carregar os dados do prazo do aluno selecionado
    def carregar_dados_prazo(nome_aluno):
        """Carrega os dados do prazo do aluno selecionado."""
        global dados_tabela_prazos  # Acessa a variável global dados_tabela_prazos
        dados_tabela_prazos = []  # Limpa a lista de dados da tabela
        pessoa_id = db.get_pessoa_info(nome=nome_aluno).get("id")  # Obtém o ID do aluno a partir do nome
        prazos = db.get_prazos_by_pessoa_id(pessoa_id)  # Obtém a lista de prazos do aluno a partir do ID

        # Ordena a lista de prazos pela data do prazo, colocando os prazos sem data no final
        prazos.sort(
            key=lambda prazo: datetime.datetime.strptime(
                prazo["prazo_fase_pesquisa"], "%d/%m/%Y"
            ).date()
            if prazo["prazo_fase_pesquisa"]
            else datetime.date.max
        )

        # Adiciona os prazos à lista de dados da tabela
        dados_tabela_prazos = prazos
        atualizar_visualizacao_dados(page)  # Atualiza a visualização dos dados (tabela ou lista)

    # Define a função para excluir um prazo do banco de dados
    def excluir_prazo(prazo_id, fase_pesquisa):
        """Exclui um prazo e recarrega os dados da tabela."""
        db.excluir_prazo(prazo_id)  # Exclui o prazo do banco de dados
        db.registrar_log(
            usuario, "excluir_prazo", f"Prazo ID: {prazo_id}, Fase: {fase_pesquisa}"
        )  # Registra o log da exclusão
        carregar_dados_prazo(anchor.value)  # Recarrega os prazos do aluno selecionado

    # Define a função para abrir o diálogo de confirmação de exclusão
    def confirmar_exclusao(e, prazo_id, fase):
        """Abre o diálogo de confirmação de exclusão de prazo."""
        page.dialog = dlg_confirmacao_excluir
        dlg_confirmacao_excluir.open = True
        page.update()
        global prazo_id_excluir, fase_pesquisa  # Acessa as variáveis globais
        prazo_id_excluir = prazo_id  # Define o ID do prazo a ser excluído
        fase_pesquisa = fase  # Define a fase do prazo a ser excluído

    # Define a função para confirmar a exclusão de um prazo
    def confirmar_exclusao_prazo(e):
        """Exclui o prazo após a confirmação do usuário."""
        global prazo_id_excluir, fase_pesquisa  # Acessa as variáveis globais
        excluir_prazo(
            prazo_id_excluir, fase_pesquisa
        )  # Chama a função para excluir o prazo do banco de dados
        fechar_dialogo(e)  # Fecha o diálogo de confirmação

    # Define a função para limpar os campos de edição de prazo
    def limpar_campos():
        """Limpa os campos de edição de prazo."""
        prazo_fase_pesquisa_field.value = ""  # Limpa o campo de data do prazo
        prazo_dias_field.value = ""  # Limpa o campo de prazo em dias
        prazo_situacao_field.value = ""  # Limpa o campo de situação do prazo
        situacao_fase_pesquisa_dropdown.value = None  # Limpa o dropdown de situação da fase
        dropdown_fases.value = None  # Limpa o dropdown de fases para atualização
        dropdown_fases_registro.value = None  # Limpa o dropdown de fases para registro

    # Define a função para preencher os campos de edição de prazo com as informações de um prazo existente
    def preencher_campos(prazo):
        """Preenche os campos de edição de prazo com as informações de um prazo existente."""
        prazo_fase_pesquisa_field.value = prazo.get("prazo_fase_pesquisa", "")  # Define a data do prazo
        prazo_dias_field.value = str(prazo.get("prazo_dias", ""))  # Define o prazo em dias
        prazo_situacao_field.value = prazo.get("prazo_situacao", "")  # Define a situação do prazo
        situacao_fase_pesquisa_dropdown.value = prazo.get(
            "situacao_fase_pesquisa", ""
        )  # Define a situação da fase

    # Define a função para preparar a tela para o cadastro de um novo prazo
    def novo_prazo(e):
        """Prepara a tela para o cadastro de um novo prazo."""
        # Verifica se o dropdown de fases para registro está vazio e, se estiver, o preenche com as opções de fases
        if not dropdown_fases_registro.options:
            dropdown_fases_registro.options = [
                ft.dropdown.Option("01 - Definição de Orientador"),
                ft.dropdown.Option("02 - Escolha do Tema"),
                ft.dropdown.Option("03 - Elaboração do projeto de Pesquisa"),
                ft.dropdown.Option("04 - Encaminhamento do projeto ao CEP"),
                ft.dropdown.Option("05 - Aprovação do CEP"),
                ft.dropdown.Option("06 - Coleta de Dados ou Materiais"),
                ft.dropdown.Option("07 - Análise de Resultados"),
                ft.dropdown.Option("08 - Escrita do TCC"),
                ft.dropdown.Option("09 - Submissão do TCC para defesa"),
                ft.dropdown.Option("10 - Qualificação"),
                ft.dropdown.Option("11 - Data da Defesa"),
                ft.dropdown.Option("12 - Adequação do TCC"),
                ft.dropdown.Option(
                    "13 - TCC finalizado e enviada a biblioteca"
                ),
                ft.dropdown.Option("14 - Certificado"),
                ft.dropdown.Option("Desistente"),
                ft.dropdown.Option("Reprovado"),
                ft.dropdown.Option("Outras situações"),
            ]

        # Limpa os campos de edição de prazo
        limpar_campos()

        # Define a visibilidade dos containers e botões
        container_campos.visible = True
        botao_salvar.visible = False
        botao_salvar_novo.visible = True
        botao_novo.visible = False
        botao_atualizar.visible = False

        # Atualiza os containers e a página
        container_campos.update()
        page.update()

    # Define a função para abrir o diálogo de confirmação de cadastro de novo prazo
    def salvar_novo_prazo(e):
        """Abre o diálogo de confirmação de cadastro de novo prazo."""
        page.dialog = dlg_confirmacao_novo
        dlg_confirmacao_novo.open = True
        page.update()

    # Define a função para confirmar o cadastro de um novo prazo
    def confirmar_salvar_novo_prazo(e):
        """Cadastra um novo prazo no banco de dados após a confirmação."""
        pessoa_id = db.get_pessoa_info(nome=anchor.value).get("id")  # Obtém o ID do aluno a partir do nome
        # Cria um dicionário com os dados do novo prazo
        prazo_data = {
            "id_pessoa": pessoa_id,
            "fase_pesquisa": dropdown_fases_registro.value,
            "prazo_fase_pesquisa": prazo_fase_pesquisa_field.value,
            "prazo_dias": prazo_dias_field.value,
            "prazo_situacao": prazo_situacao_field.value,
            "situacao_fase_pesquisa": situacao_fase_pesquisa_dropdown.value,
        }
        # Insere o novo prazo no banco de dados
        db.inserir_prazo(prazo_data)

        # Registra a ação no log do sistema
        campos_log = [
            f"{chave}: {valor}" for chave, valor in prazo_data.items() if chave != "id_pessoa"
        ]
        log_mensagem = f"Prazo incluído para: {anchor.value}, {', '.join(campos_log)}"
        db.registrar_log(usuario, "inserir_prazo", log_mensagem)

        # Recarrega os dados do prazo do aluno selecionado
        carregar_dados_prazo(anchor.value)

        # Limpa os campos de edição de prazo
        limpar_campos()

        # Define a visibilidade dos containers e botões
        container_campos.visible = False
        botao_salvar_novo.visible = False
        botao_novo.visible = True
        botao_atualizar.visible = True

        # Atualiza os containers e fecha o diálogo de confirmação
        container_campos.update()
        fechar_dialogo(e)

    # Define a função para abrir o diálogo de confirmação de atualização de prazo
    def salvar_prazo(e):
        """Abre o diálogo de confirmação de atualização de prazo."""
        page.dialog = dlg_confirmacao_atualizar
        dlg_confirmacao_atualizar.open = True
        page.update()

    # Define a função para confirmar a atualização de um prazo
    def confirmar_salvar_prazo(e):
        """Atualiza um prazo no banco de dados após a confirmação."""
        # Obtém a fase selecionada no dropdown
        fase_selecionada = dropdown_fases.value
        # Obtém o ID do aluno a partir do nome
        pessoa_id = db.get_pessoa_info(nome=anchor.value).get("id")
        # Obtém a lista de prazos do aluno
        prazos = db.get_prazos_by_pessoa_id(pessoa_id)
        # Encontra o prazo a ser atualizado na lista de prazos
        prazo_a_atualizar = next(
        (p for p in prazos if p["fase_pesquisa"] == fase_selecionada), None
        )
        # Se o prazo for encontrado
        if prazo_a_atualizar:
            # Cria um dicionário com os dados do prazo a ser atualizado
            prazo_data = {
                "id": prazo_a_atualizar["id"],  # Define o ID do prazo a ser atualizado
                "fase_pesquisa": fase_selecionada,
                "prazo_fase_pesquisa": prazo_fase_pesquisa_field.value,
                "prazo_dias": prazo_dias_field.value,
                "prazo_situacao": prazo_situacao_field.value,
                "situacao_fase_pesquisa": situacao_fase_pesquisa_dropdown.value,
            }
        # Atualiza o prazo no banco de dados
        db.atualizar_prazo(prazo_data)

        # Registra a ação no log do sistema
        campos_log = [
            f"{chave}: {valor}" for chave, valor in prazo_data.items() if chave != "id_pessoa"
        ]
        log_mensagem = f"Prazo alterado para: {anchor.value}, {', '.join(campos_log)}"
        db.registrar_log(usuario, "inserir_prazo", log_mensagem)

        # Recarrega os dados do prazo do aluno selecionado
        carregar_dados_prazo(anchor.value)

        # Limpa os campos de edição de prazo
        limpar_campos()

        # Define a visibilidade dos containers e botões
        container_campos.visible = False
        botao_salvar_novo.visible = False
        botao_novo.visible = True
        botao_atualizar.visible = True

        # Atualiza os containers e fecha o diálogo de confirmação
        container_campos.update()
        fechar_dialogo(e)

    # Define a função para preparar a tela para a atualização de um prazo existente
    def atualizar_prazo(e):
        """Prepara a tela para a atualização de um prazo existente."""
        pessoa_id = db.get_pessoa_info(nome=anchor.value).get("id")  # Obtém o ID do aluno a partir do nome
        prazos = db.get_prazos_by_pessoa_id(pessoa_id)  # Obtém a lista de prazos do aluno

        # Se houver prazos para o aluno selecionado
        if prazos:
            # Cria as opções do dropdown de fases com base nos prazos existentes
            opcoes_fases = [
                ft.dropdown.Option(prazo["fase_pesquisa"]) for prazo in prazos
            ]
            # Define as opções do dropdown
            dropdown_fases.options = opcoes_fases
            # Define o valor do dropdown como None para forçar o usuário a selecionar uma fase
            dropdown_fases.value = None

            # Define a visibilidade dos containers e botões
            container_campos.visible = False
            container_dropdown.visible = True
            botao_salvar.visible = True
            botao_salvar_novo.visible = False
            botao_novo.visible = False
            botao_atualizar.visible = False

            # Atualiza os containers e a página
            container_campos.update()
            container_dropdown.update()
            page.update()
        else:
            print("Nenhum prazo encontrado para este aluno.")

    # Define a função para preencher os campos de edição com base na fase selecionada no dropdown
    def preencher_campos_edicao(e):
        """Preenche os campos de edição com base na fase selecionada."""
        fase_selecionada = dropdown_fases.value  # Obtém a fase selecionada no dropdown
        pessoa_id = db.get_pessoa_info(nome=anchor.value).get("id")  # Obtém o ID do aluno a partir do nome
        prazos = db.get_prazos_by_pessoa_id(pessoa_id)  # Obtém a lista de prazos do aluno
        # Encontra o prazo correspondente à fase selecionada
        prazo_selecionado = next(
            (p for p in prazos if p["fase_pesquisa"] == fase_selecionada), None
        )

        # Se o prazo for encontrado, preenche os campos de edição com suas informações
        if prazo_selecionado:
            preencher_campos(prazo_selecionado)
            container_campos.visible = True
            page.update()

    # Define a função para calcular a data do prazo e atualizar a situação do prazo
    def calcular_prazo(e):
        """Calcula a data do prazo e atualiza a situação."""
        # Se a situação da fase for "Concluído"
        if situacao_fase_pesquisa_dropdown.value == "Concluído":
            # Define o prazo em dias como 0
            prazo_dias_field.value = 0
            # Limpa o campo de data do prazo
            prazo_fase_pesquisa_field.value = ""
            # Define a situação do prazo como "Concluído"
            prazo_situacao_field.value = "Concluído"
            # Atualiza a página
            page.update()
        else:
            try:
                # Verifica se o campo de prazo em dias está vazio
                if prazo_dias_field.value == "":
                    # Limpa o campo de data do prazo
                    prazo_fase_pesquisa_field.value = ""
                    # Atualiza a página
                    page.update()
                    return

                # Converte o prazo em dias para inteiro
                dias = int(prazo_dias_field.value)

                # Verifica se o número de dias é negativo
                if dias < 0:
                    raise ValueError("Número de dias não pode ser negativo.")

                # Calcula a data do prazo
                data_atual = date.today()
                data_prazo = data_atual + timedelta(days=dias)
                prazo_fase_pesquisa_field.value = data_prazo.strftime("%d/%m/%Y")
                page.update()
            except ValueError:
                prazo_fase_pesquisa_field.value = "Número de dias inválido."
                page.update()
        page.update()

    # --- Criação dos Componentes da Interface ---

    # Dropdown para selecionar a fase do prazo ao registrar um novo prazo
    dropdown_fases_registro = ft.Dropdown(
        width=250,
        label="Fase de Pesquisa",
        bgcolor="WHITE",
        options=[],  # Inicialmente vazio, será preenchido na função 'novo_prazo'
    )

    # Cria a ListView para exibir a lista de alunos
    lv = ft.ListView()

    # Obtém a lista de nomes dos alunos do banco de dados
    nomes_alunos = db.get_aluno()

    # Adiciona os alunos à ListView em grupos de 25 para melhorar o desempenho
    for i in range(0, len(nomes_alunos), 25):
        for nome in nomes_alunos[i : i + 25]:
            lv.controls.append(
                ft.ListTile(title=ft.Text(nome), on_click=close_anchor, data=nome)  # Adiciona o aluno à ListView
            )
        page.update()  # Atualiza a página para exibir os alunos adicionados

    # Cria a SearchBar para buscar alunos pelo nome
    anchor = ft.SearchBar(
        view_elevation=4,
        divider_color=ft.colors.AMBER,
        bar_hint_text="Buscar por nome do aluno.",
        view_hint_text="Escolha um aluno.",
        on_change=handle_change,  # Define a função a ser chamada quando o texto da SearchBar for alterado
        controls=[lv],  # Adiciona a ListView à SearchBar
    )

    # Cria os campos de texto para exibir as informações do aluno selecionado
    nome_aluno = ft.Text("", size=14)  # Nome do aluno
    curso = ft.Text("", size=14)  # Curso do aluno
    orientador = ft.Text("", size=14)  # Orientador do aluno
    tema = ft.Text("", size=14)  # Tema do TCC do aluno

    # --- Criação da Tabela de Prazos e dos Campos de Texto para os Prazos ---

    # Define as colunas da tabela de prazos
    colunas_tabela_prazos = [
        ft.DataColumn(
            ft.Container(ft.Text("Fase de Pesquisa"), alignment=ft.alignment.center)
        ),
        ft.DataColumn(
            ft.Container(ft.Text("Prazo Fase Pesquisa"), alignment=ft.alignment.center)
        ),
        ft.DataColumn(
            ft.Container(ft.Text("Prazo em Dias"), alignment=ft.alignment.center)
        ),
        ft.DataColumn(
            ft.Container(ft.Text("Situação do Prazo"), alignment=ft.alignment.center)
        ),
        ft.DataColumn(
            ft.Container(ft.Text("Situação da Fase"), alignment=ft.alignment.center)
        ),
        ft.DataColumn(
            ft.Container(
                ft.Text("Tempo Restante (dias)"), alignment=ft.alignment.center
            )
        ),
        ft.DataColumn(ft.Container(ft.Text("Ação"), alignment=ft.alignment.center)),  # Coluna para os botões de ação
    ]

    # Cria a tabela de prazos (visível apenas em telas maiores que 1024 pixels de largura)
    tabela_prazos = ft.DataTable(
        columns=colunas_tabela_prazos,  # Define as colunas da tabela
        rows=[],  # Inicialmente, a tabela não possui linhas
        border=ft.border.all(2, "black"),  # Define a borda da tabela
        border_radius=ft.border_radius.all(10),  # Define o raio de borda da tabela
        width=1300,  # Define a largura da tabela
        bgcolor="WHITE",  # Define a cor de fundo da tabela
        visible=False,  # A tabela é inicialmente invisível
    )

    # Cria o container para os campos de texto dos prazos (visível apenas em telas menores que 1024 pixels de largura)
    container_info_prazos = ft.Column(
        spacing=5,  # Define o espaçamento entre os campos de texto
        width=1300,  # Define a largura do container
        visible=False,  # O container é inicialmente invisível
    )

    # --- Criação dos Containers ---

    # Dropdown para selecionar a fase do prazo a ser atualizado
    dropdown_fases = ft.Dropdown(
        width=200,
        bgcolor="WHITE",
        label="Selecione a fase para edição",
        options=[],  # Inicialmente vazio, será preenchido na função 'atualizar_prazo'
        on_change=preencher_campos_edicao,  # Define a função a ser chamada quando o valor do dropdown for alterado
    )

    # Container para o dropdown de fases para atualização
    container_dropdown = ft.Container(
        content=ft.ResponsiveRow(
            controls=[dropdown_fases],  # Adiciona o dropdown ao container
            alignment=ft.MainAxisAlignment.CENTER,  # Alinha o dropdown ao centro
            width=800,  # Define a largura do container
        ),
        visible=False,  # O container é inicialmente invisível
    )

    # Cria os campos de texto para edição de prazo
    prazo_fase_pesquisa_field = ft.TextField(
        label="Data do prazo - DD/MM/AAAA", width=200, read_only=False, bgcolor="WHITE", max_length=10  # Define o campo de data do prazo
    )
    prazo_dias_field = ft.TextField(
        label="Prazo em Dias",
        width=200,
        bgcolor="WHITE",
        on_change=calcular_prazo,  # Define a função a ser chamada quando o valor do campo for alterado
        keyboard_type=ft.KeyboardType.NUMBER,  # Define o tipo de teclado como numérico
    )
    prazo_situacao_field = ft.Dropdown(
        label="Situação do Prazo",
        width=800,
        bgcolor="WHITE",
        options=[
            ft.dropdown.Option("Vigente"),
            ft.dropdown.Option("Vencido"),
            ft.dropdown.Option("Concluído"),
            ft.dropdown.Option("Suspenso"),
        ],  # Define as opções do dropdown
    )
    situacao_fase_pesquisa_dropdown = ft.Dropdown(
        label="Situação da Fase",
        width=800,
        bgcolor="WHITE",
        on_change=calcular_prazo,  # Define a função a ser chamada quando o valor do dropdown for alterado
        options=[
            ft.dropdown.Option("Em andamento"),
            ft.dropdown.Option("Suspenso"),
            ft.dropdown.Option("Concluído"),
            ft.dropdown.Option("Outras Situações"),
        ],  # Define as opções do dropdown
    )

    # Container para os campos de edição de prazo
    container_campos = ft.Container(
        content=ft.ResponsiveRow(
            controls=[
                dropdown_fases_registro,  # Dropdown para selecionar a fase do prazo ao registrar um novo prazo
                situacao_fase_pesquisa_dropdown,  # Dropdown para selecionar a situação da fase
                prazo_dias_field,  # Campo de texto para o prazo em dias
                prazo_fase_pesquisa_field,  # Campo de texto para a data do prazo
                prazo_situacao_field,  # Dropdown para selecionar a situação do prazo
            ],
            alignment=ft.MainAxisAlignment.CENTER,  # Alinha os campos ao centro
        ),
        visible=False,  # O container é inicialmente invisível
        width=1300,  # Define a largura do container
    )

    # --- Criação dos Botões ---

    # Botão para adicionar um novo prazo
    botao_novo = ft.ElevatedButton(
        text="Novo",
        width=800,
        height=40,
        elevation=4,
        bgcolor="#006BA0",
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),  # Define o estilo do botão (borda arredondada)
        color="WHITE",
        on_click=novo_prazo,  # Define a função a ser chamada quando o botão for clicado
        visible=False,  # O botão é inicialmente invisível
    )

    # Botão para atualizar um prazo existente
    botao_atualizar = ft.ElevatedButton(
        text="Atualizar",
        width=800,
        height=40,
        elevation=4,
        bgcolor="#006BA0",
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),  # Define o estilo do botão (borda arredondada)
        color="WHITE",
        on_click=atualizar_prazo,  # Define a função a ser chamada quando o botão for clicado
        visible=False,  # O botão é inicialmente invisível
    )

    # Botão para salvar um novo prazo
    botao_salvar_novo = ft.ElevatedButton(
        text="Salvar Novo",
        width=800,
        height=40,
        elevation=4,
        bgcolor="#006BA0",
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),  # Define o estilo do botão (borda arredondada)
        color="WHITE",
        on_click=salvar_novo_prazo,  # Define a função a ser chamada quando o botão for clicado
        visible=False,  # O botão é inicialmente invisível
    )

    # Botão para salvar as alterações de um prazo existente
    botao_salvar = ft.ElevatedButton(
        text="Salvar",
        width=800,
        height=40,
        elevation=4,
        bgcolor="#006BA0",
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),  # Define o estilo do botão (borda arredondada)
        color="WHITE",
        on_click=salvar_prazo,  # Define a função a ser chamada quando o botão for clicado
        visible=False,  # O botão é inicialmente invisível
    )

    # Container para os botões
    container_botoes = ft.Container(
        width=1300,
        content=ft.ResponsiveRow(
            controls=[botao_novo, botao_atualizar, botao_salvar, botao_salvar_novo],  # Adiciona os botões ao container
            alignment=ft.MainAxisAlignment.CENTER,  # Alinha os botões ao centro
        ),
    )

    # --- Criação do Container Principal ---

    # Cria o título da tela
    nome_campo = ft.Text(
        "ANDAMENTO DA PESQUISA",
        size=16,
        color="#006BA0",
        font_family="Roboto",
        weight=ft.FontWeight.BOLD,  # Define o peso da fonte como negrito
        text_align=ft.TextAlign.CENTER,  # Alinha o texto ao centro
    )

    # Cria o container principal da tela
    container_prazos = ft.Container(
        expand=True,  # Permite que o container se expanda para preencher o espaço disponível
        content=ft.Column(
            scroll=ft.ScrollMode.ALWAYS,  # Habilita a rolagem vertical quando o conteúdo excede o tamanho do container
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,  # Alinha o conteúdo horizontalmente ao centro
            controls=[
                nome_campo,  # Título da tela
                ft.Divider(),  # Divisor visual
                anchor,  # SearchBar para buscar alunos
                ft.Column(  # Coluna para as informações do aluno selecionado
                    controls=[
                        nome_aluno,  # Nome do aluno
                        curso,  # Curso do aluno
                        orientador,  # Orientador do aluno
                        tema,  # Tema do TCC do aluno
                    ]
                ),
                ft.ResponsiveRow(controls=[container_botoes], width=800),  # Linha responsiva com o container de botões
                container_dropdown,  # Container com o dropdown de fases para atualização
                tabela_prazos,  # Tabela de prazos (visível apenas em telas maiores que 1024 pixels de largura)
                container_info_prazos,  # Container com os campos de texto dos prazos (visível apenas em telas menores que 1024 pixels de largura)
                container_campos,  # Container com os campos de edição de prazo
            ],
        ),
    )

    # --- Funções para atualizar a visualização ---

    # Define a função para atualizar a visualização dos dados (tabela ou lista)
    def atualizar_visualizacao_dados(page):
        """
        Atualiza a visualização dos dados de acordo com a largura da tela.

        Args:
            page (ft.Page): A página Flet atual.
        """
        global dados_tabela_prazos  # Acessa a variável global dados_tabela_prazos

        # Se a largura da tela for menor que 1024 pixels e um aluno estiver selecionado
        if page.width < 1024 and anchor.value is not None:
            # Limpa os controles existentes no container de informações dos prazos
            container_info_prazos.controls.clear()

            # Define o tamanho da fonte dos campos de texto para 12 pixels
            nome_aluno.size = 12
            curso.size = 12
            orientador.size = 12
            tema.size = 12

            # Itera sobre os prazos do aluno selecionado
            for prazo in dados_tabela_prazos:
                # Calcula o tempo restante em dias para o prazo
                prazo_fase_pesquisa_date = (
                    datetime.datetime.strptime(
                        prazo["prazo_fase_pesquisa"], "%d/%m/%Y"
                    ).date()
                    if prazo["prazo_fase_pesquisa"]
                    else None
                )
                tempo_restante = (
                    (prazo_fase_pesquisa_date - date.today()).days
                    if prazo_fase_pesquisa_date
                    else "N/A"  # Define "N/A" se a data do prazo não estiver definida
                )
                # Se a situação da fase for "Concluído", o tempo restante é definido como 0
                if prazo["situacao_fase_pesquisa"] == "Concluído":
                    tempo_restante = 0

                # Adiciona os campos de texto com as informações do prazo ao container de informações dos prazos
                container_info_prazos.controls.append(
                    ft.Text(f"Fase de Pesquisa: {prazo['fase_pesquisa']}", size=12)  # Fase da pesquisa
                )
                container_info_prazos.controls.append(
                    ft.Text(f"Data do Prazo: {prazo['prazo_fase_pesquisa']}", size=12)  # Data do prazo
                )
                container_info_prazos.controls.append(
                    ft.Text(f"Prazo em Dias: {prazo['prazo_dias']}", size=12)  # Prazo em dias
                )
                container_info_prazos.controls.append(
                    ft.Text(f"Situação do Prazo: {prazo['prazo_situacao']}", size=12)  # Situação do prazo
                )
                container_info_prazos.controls.append(
                    ft.Text(
                        f"Situação da Fase: {prazo['situacao_fase_pesquisa']}", size=12  # Situação da fase
                    )
                )
                container_info_prazos.controls.append(
                    ft.Text(f"Tempo Restante (dias): {tempo_restante}", size=12)  # Tempo restante em dias
                )

                # Adiciona um botão "Excluir" para cada prazo
                container_info_prazos.controls.append(
                    ft.TextButton(
                        "Excluir",
                        on_click=lambda e, prazo_id=prazo[
                            "id"
                        ], fase=prazo[
                            "fase_pesquisa"
                        ]: confirmar_exclusao(  # Define a função a ser chamada quando o botão for clicado
                            e, prazo_id, fase  # Passa o ID do prazo e a fase como argumentos para a função
                        ),
                        data=prazo["fase_pesquisa"],
                    )
                )

                # Adiciona um divisor visual após cada prazo
                container_info_prazos.controls.append(ft.Divider())

            # Oculta a tabela de prazos e exibe o container de informações dos prazos
            tabela_prazos.visible = False
            container_info_prazos.visible = True
        # Se a largura da tela for maior ou igual a 1024 pixels
        else:
            # Limpa as linhas da tabela de prazos
            tabela_prazos.rows.clear()

            # Define o tamanho da fonte dos campos de texto para 14 pixels
            nome_aluno.size = 14
            curso.size = 14
            orientador.size = 14
            tema.size = 14

            # Se um aluno estiver selecionado
            if anchor.value is not None:
                # Itera sobre os prazos do aluno selecionado
                for prazo in dados_tabela_prazos:
                    # Calcula o tempo restante em dias para o prazo
                    prazo_fase_pesquisa_date = (
                        datetime.datetime.strptime(
                            prazo["prazo_fase_pesquisa"], "%d/%m/%Y"
                        ).date()
                        if prazo["prazo_fase_pesquisa"]
                        else None
                    )
                    tempo_restante = (
                        (prazo_fase_pesquisa_date - date.today()).days
                        if prazo_fase_pesquisa_date
                        else "N/A"  # Define "N/A" se a data do prazo não estiver definida
                    )
                    # Se a situação da fase for "Concluído", o tempo restante é definido como 0
                    if prazo["situacao_fase_pesquisa"] == "Concluído":
                        tempo_restante = 0

                    # Cria o botão "Excluir" para o prazo
                    excluir_cell = ft.DataCell(
                        ft.TextButton(
                            "Excluir",
                            on_click=lambda e, prazo_id=prazo[
                                "id"
                            ], fase=prazo[
                                "fase_pesquisa"
                            ]: confirmar_exclusao(  # Define a função a ser chamada quando o botão for clicado
                                e, prazo_id, fase  # Passa o ID do prazo e a fase como argumentos para a função
                            ),
                            data=prazo["fase_pesquisa"],
                        )
                    )

                    # Cria a célula com o tempo restante em dias para o prazo
                    tempo_restante_cell = ft.DataCell(
                        ft.Text(str(tempo_restante))  # Converte o tempo restante para string
                    )

                    # Adiciona uma nova linha à tabela de prazos com as informações do prazo
                    tabela_prazos.rows.append(
                        ft.DataRow(
                            cells=[
                                ft.DataCell(ft.Text(prazo["fase_pesquisa"])),  # Fase da pesquisa
                                ft.DataCell(
                                    ft.Text(prazo["prazo_fase_pesquisa"])  # Data do prazo
                                ),
                                ft.DataCell(ft.Text(str(prazo["prazo_dias"]))),  # Prazo em dias (convertido para string)
                                ft.DataCell(ft.Text(prazo["prazo_situacao"])),  # Situação do prazo
                                ft.DataCell(
                                    ft.Text(prazo["situacao_fase_pesquisa"])  # Situação da fase
                                ),
                                tempo_restante_cell,  # Célula com o tempo restante em dias
                                excluir_cell,  # Célula com o botão "Excluir"
                            ]
                        )
                    )

            # Exibe a tabela de prazos e oculta o container de informações dos prazos
            tabela_prazos.visible = True
            container_info_prazos.visible = False

        # Atualiza a página para exibir as alterações
        page.update()

    # Define a função para redimensionar os containers quando a tela for redimensionada
    def resize_containers(e):
        """Redimensiona os containers de acordo com a largura da tela."""
        # Se um aluno estiver selecionado, recarrega os dados do prazo
        if anchor.value is not None:
            carregar_dados_prazo(anchor.value)
        # Atualiza a visualização dos dados (tabela ou lista)
        atualizar_visualizacao_dados(page)

    # Chama a função 'resize_containers' uma vez no início para configurar a interface corretamente
    resize_containers(None)

    # Define a função 'resize_containers' como a função a ser chamada quando a tela for redimensionada
    page.on_resize = resize_containers

    # Retorna o container principal da tela
    return container_prazos
