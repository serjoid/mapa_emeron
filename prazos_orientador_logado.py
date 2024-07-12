import flet as ft  # Importa a biblioteca Flet
from database import Database  # Importa a classe Database do módulo 'database.py'
from datetime import date, timedelta  # Importa as classes date e timedelta do módulo datetime
import datetime  # Importa o módulo datetime

# Inicializa a conexão com o banco de dados
db = Database()

# Define a função para exibir a tela de prazos do orientador logado
def prazos_orientador_logado(page: ft.Page, usuario):
    """
    Cria a tela de gerenciamento de prazos para o orientador logado.

    Args:
        page (ft.Page): A página Flet atual.
        usuario (str): O nome de usuário do orientador logado.
    """

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

    # Define a função para carregar os dados do prazo com base no aluno selecionado no dropdown
    def carregar_dados_prazo_dropdown(e):
        """Carrega os dados do prazo do aluno selecionado no dropdown."""
        nome_aluno = dropdown_alunos.value  # Obtém o nome do aluno selecionado no dropdown
        if nome_aluno:  # Se um aluno for selecionado
            carregar_dados_prazo(nome_aluno)  # Carrega os dados do prazo do aluno
            resize_containers(e)  # Ajusta a visualização dos dados de acordo com a largura da tela

    # Define a função para carregar os dados do prazo do aluno
    def carregar_dados_prazo(nome_aluno):
        """Carrega os dados do prazo do aluno e atualiza a tabela de prazos e as informações do aluno."""
        pessoa_id = db.get_pessoa_info(nome=nome_aluno).get("id")  # Obtém o ID do aluno a partir do nome
        prazos = db.get_prazos_by_pessoa_id(pessoa_id)  # Obtém a lista de prazos do aluno a partir do ID
        pessoa_info = db.get_pessoa_info(nome=nome_aluno)  # Obtém as informações do aluno a partir do nome

        # Ordena a lista de prazos pela data do prazo, colocando os prazos sem data no final
        prazos.sort(
            key=lambda prazo: datetime.datetime.strptime(
                prazo["prazo_fase_pesquisa"], "%d/%m/%Y"
            ).date()
            if prazo["prazo_fase_pesquisa"]
            else datetime.date.max
        )

        # Define as variáveis globais com os dados do prazo e as informações do aluno
        global dados_tabela_prazos, dados_info_aluno
        dados_tabela_prazos = prazos
        dados_info_aluno = [pessoa_info]  # Transforma as informações do aluno em uma lista para manter a compatibilidade com a função 'atualizar_visualizacao_info_aluno'

        # Define a visibilidade dos botões "Novo" e "Atualizar"
        botao_novo.visible = True
        botao_atualizar.visible = True

        # Atualiza a visualização dos dados e das informações do aluno
        atualizar_visualizacao_dados(page)
        atualizar_visualizacao_info_aluno(page)

    # Define a função para excluir um prazo do banco de dados
    def excluir_prazo(prazo_id, fase_pesquisa):
        """Exclui um prazo e recarrega os dados do prazo do aluno selecionado."""
        db.excluir_prazo(prazo_id)  # Exclui o prazo do banco de dados
        db.registrar_log(
            usuario, "excluir_prazo", f"Prazo ID: {prazo_id}, Fase: {fase_pesquisa}"
        )  # Registra o log da exclusão
        carregar_dados_prazo(dropdown_alunos.value)  # Recarrega os dados do prazo do aluno selecionado

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
        excluir_prazo(prazo_id_excluir, fase_pesquisa)  # Chama a função para excluir o prazo do banco de dados
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
        page.update()

    # Define a função para preencher os campos de edição de prazo com as informações de um prazo existente
    def preencher_campos(prazo):
        """Preenche os campos de edição de prazo com as informações de um prazo existente."""
        prazo_fase_pesquisa_field.value = prazo.get("prazo_fase_pesquisa", "")  # Define a data do prazo
        prazo_dias_field.value = str(prazo.get("prazo_dias", ""))  # Define o prazo em dias
        prazo_situacao_field.value = prazo.get("prazo_situacao", "")  # Define a situação do prazo
        situacao_fase_pesquisa_dropdown.value = prazo.get(
            "situacao_fase_pesquisa", ""
        )  # Define a situação da fase
        page.update()

    # Define a função para preparar a tela para o cadastro de um novo prazo
    def novo_prazo(e):
        """Prepara a tela para o cadastro de um novo prazo."""
        limpar_campos()  # Limpa os campos de edição de prazo
        # Define a visibilidade dos containers e botões
        container_campos.visible = True  # Torna o container de campos de edição de prazo visível
        container_dropdown.visible = False  # Oculta o container de dropdown de fases para atualização
        botao_salvar.visible = False  # Oculta o botão "Salvar"
        botao_salvar_novo.visible = True  # Exibe o botão "Salvar Novo"
        botao_novo.visible = False  # Oculta o botão "Novo"
        botao_atualizar.visible = False  # Oculta o botão "Atualizar"
        page.update()  # Atualiza a página

    # Define a função para abrir o diálogo de confirmação de cadastro de novo prazo
    def salvar_novo_prazo(e):
        """Abre o diálogo de confirmação de cadastro de novo prazo."""
        page.dialog = dlg_confirmacao_novo
        dlg_confirmacao_novo.open = True
        page.update()

    # Define a função para confirmar o cadastro de um novo prazo
    def confirmar_salvar_novo_prazo(e):
        """Cadastra um novo prazo no banco de dados após a confirmação."""
        pessoa_id = db.get_pessoa_info(nome=dropdown_alunos.value).get("id")  # Obtém o ID do aluno a partir do nome
        # Cria um dicionário com os dados do novo prazo
        prazo_data = {
            "id_pessoa": pessoa_id,  # ID do aluno
            "fase_pesquisa": dropdown_fases_registro.value,  # Fase da pesquisa selecionada no dropdown
            "prazo_fase_pesquisa": prazo_fase_pesquisa_field.value,  # Data do prazo
            "prazo_dias": prazo_dias_field.value,  # Prazo em dias
            "prazo_situacao": prazo_situacao_field.value,  # Situação do prazo selecionada no dropdown
            "situacao_fase_pesquisa": situacao_fase_pesquisa_dropdown.value,  # Situação da fase selecionada no dropdown
        }
        # Insere o novo prazo no banco de dados
        db.inserir_prazo(prazo_data)

        # Registra a ação no log do sistema
        db.registrar_log(
            usuario,
            "inserir_prazo",
            f"Prazo para: {dropdown_alunos.value}, Fase: {prazo_data['fase_pesquisa']}",
        )

        # Recarrega os dados do prazo do aluno selecionado
        carregar_dados_prazo(dropdown_alunos.value)

        # Limpa os campos de edição de prazo
        limpar_campos()

        # Define a visibilidade dos containers e botões
        container_campos.visible = False  # Oculta o container de campos de edição de prazo
        botao_salvar_novo.visible = False  # Oculta o botão "Salvar Novo"
        botao_novo.visible = True  # Exibe o botão "Novo"
        botao_atualizar.visible = True  # Exibe o botão "Atualizar"

        # Atualiza a página e fecha o diálogo de confirmação
        page.update()
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
        fase_selecionada = dropdown_fases.value  # Obtém a fase selecionada no dropdown
        pessoa_id = db.get_pessoa_info(nome=dropdown_alunos.value).get("id")  # Obtém o ID do aluno a partir do nome
        prazos = db.get_prazos_by_pessoa_id(pessoa_id)  # Obtém a lista de prazos do aluno
        # Encontra o prazo a ser atualizado na lista de prazos
        prazo_a_atualizar = next(
            (p for p in prazos if p["fase_pesquisa"] == fase_selecionada), None
        )

        # Se o prazo for encontrado
        if prazo_a_atualizar:
            # Cria um dicionário com os dados do prazo a ser atualizado
            prazo_data = {
                "id": prazo_a_atualizar["id"],  # ID do prazo
                "fase_pesquisa": fase_selecionada,  # Fase da pesquisa
                "prazo_fase_pesquisa": prazo_fase_pesquisa_field.value,  # Data do prazo
                "prazo_dias": prazo_dias_field.value,  # Prazo em dias
                "prazo_situacao": prazo_situacao_field.value,  # Situação do prazo
                "situacao_fase_pesquisa": situacao_fase_pesquisa_dropdown.value,  # Situação da fase
            }
            # Atualiza o prazo no banco de dados
            db.atualizar_prazo(prazo_data)

            # Registra a ação no log do sistema
            db.registrar_log(
                usuario,
                "atualizar_prazo",
                f"Prazo ID: {prazo_a_atualizar['id']}, Fase: {fase_selecionada}",
            )

            # Recarrega os dados do prazo do aluno selecionado
            carregar_dados_prazo(dropdown_alunos.value)

            # Limpa os campos de edição de prazo
            limpar_campos()

            # Define a visibilidade dos containers e botões
            container_campos.visible = False  # Oculta o container de campos de edição de prazo
            container_dropdown.visible = False  # Oculta o container de dropdown de fases para atualização
            botao_salvar.visible = False  # Oculta o botão "Salvar"
            botao_novo.visible = True  # Exibe o botão "Novo"
            botao_atualizar.visible = True  # Exibe o botão "Atualizar"

            # Atualiza a página e fecha o diálogo de confirmação
            page.update()
            fechar_dialogo(e)
        else:
            print(f"Nenhum prazo encontrado para a fase '{fase_selecionada}'.")

    # Define a função para preparar a tela para a atualização de um prazo existente
    def atualizar_prazo(e):
        """Prepara a tela para a atualização de um prazo existente."""
        pessoa_id = db.get_pessoa_info(nome=dropdown_alunos.value).get("id")  # Obtém o ID do aluno a partir do nome
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
            container_campos.visible = False  # Oculta o container de campos de edição de prazo
            container_dropdown.visible = True  # Exibe o container de dropdown de fases para atualização
            botao_salvar.visible = True  # Exibe o botão "Salvar"
            botao_salvar_novo.visible = False  # Oculta o botão "Salvar Novo"
            botao_novo.visible = False  # Oculta o botão "Novo"
            botao_atualizar.visible = False  # Oculta o botão "Atualizar"

            # Atualiza a página
            page.update()
        else:
            print("Nenhum prazo encontrado para este aluno.")

    # Define a função para preencher os campos de edição com base na fase selecionada no dropdown
    def preencher_campos_edicao(e):
        """Preenche os campos de edição com base na fase selecionada no dropdown."""
        fase_selecionada = dropdown_fases.value  # Obtém a fase selecionada no dropdown
        pessoa_id = db.get_pessoa_info(nome=dropdown_alunos.value).get("id")  # Obtém o ID do aluno a partir do nome
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

    # ---- Componentes da interface ----

    # Cria o dropdown para selecionar a fase do prazo ao registrar um novo prazo
    dropdown_fases_registro = ft.Dropdown(
        width=250,
        label="Fase de Pesquisa",
        bgcolor="WHITE",
        options=[
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
            ft.dropdown.Option("13 - TCC finalizado e enviada a biblioteca"),
            ft.dropdown.Option("14 - Certificado"),
            ft.dropdown.Option("Desistente"),
            ft.dropdown.Option("Reprovado"),
            ft.dropdown.Option("Outras situações"),
        ],
    )

    # Obtém o nome do orientador logado a partir do usuário
    orientador = db.get_orientador_info_por_usuario(usuario)["nome"]

    # Obtém a lista de nomes dos alunos orientandos do orientador logado
    nomes_alunos = db.get_orientando(orientador)

    # Cria o dropdown para selecionar o aluno
    dropdown_alunos = ft.Dropdown(
        width=1300,
        options=[ft.dropdown.Option(nome) for nome in nomes_alunos],  # Define as opções do dropdown com os nomes dos alunos
        on_change=carregar_dados_prazo_dropdown,  # Define a função a ser chamada quando o valor do dropdown for alterado
        bgcolor="WHITE",
    )

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
        ft.DataColumn(ft.Container(ft.Text("Ação"), alignment=ft.alignment.center)),
    ]

    # Define a variável global para armazenar os dados da tabela de prazos
    global dados_tabela_prazos
    dados_tabela_prazos = []

    # Cria a tabela de prazos (inicialmente invisível)
    tabela_prazos = ft.DataTable(
        columns=colunas_tabela_prazos,  # Define as colunas da tabela
        rows=[],  # Inicialmente, a tabela não possui linhas
        border=ft.border.all(2, "black"),  # Define a borda da tabela
        border_radius=ft.border_radius.all(10),  # Define o raio de borda da tabela
        bgcolor="WHITE",  # Define a cor de fundo da tabela
        visible=False,  # A tabela é inicialmente invisível
    )

    # Cria a ListView para exibir os prazos (inicialmente invisível)
    lista_prazos = ft.ListView(
        expand=True,  # Permite que a ListView se expanda para preencher o espaço disponível
        spacing=10,  # Define o espaçamento entre os itens da ListView
        padding=10,  # Define o espaçamento interno da ListView
        visible=False,  # A ListView é inicialmente invisível
    )

    # Cria a ListView para exibir as informações do aluno (inicialmente invisível)
    lista_info_aluno = ft.ListView(
        expand=True,  # Permite que a ListView se expanda para preencher o espaço disponível
        spacing=10,  # Define o espaçamento entre os itens da ListView
        padding=10,  # Define o espaçamento interno da ListView
        visible=False,  # A ListView é inicialmente invisível
    )

    # Define a variável global para armazenar as informações do aluno
    global dados_info_aluno
    dados_info_aluno = []

    # Cria o dropdown para selecionar a fase do prazo a ser atualizado
    dropdown_fases = ft.Dropdown(
        width=200,
        label="Selecione a fase para edição",
        options=[],  # Inicialmente vazio, será preenchido na função 'atualizar_prazo'
        on_change=preencher_campos_edicao,  # Define a função a ser chamada quando o valor do dropdown for alterado
        bgcolor="WHITE",
    )

    # Cria o container para o dropdown de fases para atualização
    container_dropdown = ft.Container(
        width=1300,  # Define a largura do container
        content=ft.ResponsiveRow(
            controls=[dropdown_fases],  # Adiciona o dropdown ao container
            alignment=ft.MainAxisAlignment.CENTER  # Alinha o dropdown ao centro
        ),
        visible=False,  # O container é inicialmente invisível
    )

    # Cria os campos de texto para edição de prazo
    prazo_fase_pesquisa_field = ft.TextField(
        label="Data do prazo", width=200, read_only=False, bgcolor="WHITE"  # Campo de texto para a data do prazo
    )
    prazo_dias_field = ft.TextField(
        label="Prazo em Dias",
        width=200,
        on_change=calcular_prazo,  # Define a função a ser chamada quando o valor do campo for alterado
        keyboard_type=ft.KeyboardType.NUMBER,  # Define o tipo de teclado como numérico
        bgcolor="WHITE",
    )
    prazo_situacao_field = ft.Dropdown(
        label="Situação do Prazo",
        width=200,
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
        width=200,
        bgcolor="WHITE",
        on_change=calcular_prazo,  # Define a função a ser chamada quando o valor do dropdown for alterado
        options=[
            ft.dropdown.Option("Em andamento"),
            ft.dropdown.Option("Suspenso"),
            ft.dropdown.Option("Concluído"),
            ft.dropdown.Option("Outras Situações"),
        ],  # Define as opções do dropdown
    )

    # Cria o container para os campos de edição de prazo
    container_campos = ft.Container(
        width=1300,  # Define a largura do container
        content=ft.ResponsiveRow(
            controls=[
                dropdown_fases_registro,  # Dropdown para selecionar a fase do prazo ao registrar um novo prazo
                situacao_fase_pesquisa_dropdown,  # Dropdown para selecionar a situação da fase
                prazo_dias_field,  # Campo de texto para o prazo em dias
                prazo_fase_pesquisa_field,  # Campo de texto para a data do prazo
                prazo_situacao_field,  # Dropdown para selecionar a situação do prazo
            ],
            alignment=ft.MainAxisAlignment.CENTER  # Alinha os campos ao centro
        ),
        visible=False,  # O container é inicialmente invisível
    )

    # Cria os botões da tela
    botao_novo = ft.ElevatedButton(
        text="Novo",
        width=150,
        height=40,
        elevation=4,
        bgcolor="#006BA0",
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),  # Define o estilo do botão (borda arredondada)
        color="WHITE",
        on_click=novo_prazo,  # Define a função a ser chamada quando o botão for clicado
        visible=False,  # O botão é inicialmente invisível
    )
    botao_atualizar = ft.ElevatedButton(
        text="Atualizar",
        width=150,
        height=40,
        elevation=4,
        bgcolor="#006BA0",
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),  # Define o estilo do botão (borda arredondada)
        color="WHITE",
        on_click=atualizar_prazo,  # Define a função a ser chamada quando o botão for clicado
        visible=False,  # O botão é inicialmente invisível
    )
    botao_salvar_novo = ft.ElevatedButton(
        text="Salvar Novo",
        width=150,
        height=40,
        elevation=4,
        bgcolor="#006BA0",
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),  # Define o estilo do botão (borda arredondada)
        color="WHITE",
        on_click=salvar_novo_prazo,  # Define a função a ser chamada quando o botão for clicado
        visible=False,  # O botão é inicialmente invisível
    )
    botao_salvar = ft.ElevatedButton(
        text="Salvar",
        width=150,
        height=40,
        elevation=4,
        bgcolor="#006BA0",
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),  # Define o estilo do botão (borda arredondada)
        color="WHITE",
        on_click=salvar_prazo,  # Define a função a ser chamada quando o botão for clicado
        visible=False,  # O botão é inicialmente invisível
    )

    # Cria o container para os botões
    container_botoes = ft.Container(
        width=1300,  # Define a largura do container
        content=ft.ResponsiveRow(
            controls=[botao_novo, botao_atualizar, botao_salvar, botao_salvar_novo],  # Adiciona os botões ao container
            alignment=ft.MainAxisAlignment.CENTER  # Alinha os botões ao centro
        ),
    )

    # Cria o título da tela
    nome_campo = ft.Text(
        "ANDAMENTO DA PESQUISA",
        size=16,
        color="#006BA0",
        font_family="Roboto",
        weight=ft.FontWeight.BOLD,  # Define o peso da fonte como negrito
        text_align=ft.TextAlign.CENTER,  # Alinha o texto ao centro
    )

    # Container principal para os dados da tabela ou da lista
    container_dados = ft.Container(
        width=1300,  # Define a largura do container
        content=None,  # O conteúdo do container será definido dinamicamente
        margin=ft.margin.only(bottom=10),  # Define a margem inferior do container como 10 pixels
    )

    # Container para as informações do aluno
    container_info_aluno = ft.Container(
        width=1300,  # Define a largura do container
        content=ft.Column(
            [
                ft.Text(  # Texto "Nome:" em negrito
                    "Nome:",
                    size=14,
                    weight=ft.FontWeight.BOLD,
                ),
                ft.Text(  # Campo de texto para o nome do aluno, inicialmente vazio
                    "",
                    size=14,
                ),
                ft.Text(  # Texto "Curso:" em negrito
                    "Curso:",
                    size=14,
                    weight=ft.FontWeight.BOLD,
                ),
                ft.Text(  # Campo de texto para o curso do aluno, inicialmente vazio
                    "",
                    size=14,
                ),
                ft.Text(  # Texto "Orientador:" em negrito
                    "Orientador:",
                    size=14,
                    weight=ft.FontWeight.BOLD,
                ),
                ft.Text(  # Campo de texto para o orientador do aluno, inicialmente vazio
                    "",
                    size=14,
                ),
            ]
        ),
        margin=ft.margin.only(top=10),  # Define a margem superior do container como 10 pixels
    )

    # Cria o container principal da tela
    container_prazos = ft.Container(
        expand=True,  # Permite que o container se expanda para preencher o espaço disponível
        content=ft.Column(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,  # Alinha o conteúdo horizontalmente ao centro
            scroll=ft.ScrollMode.ALWAYS,  # Habilita a rolagem vertical quando o conteúdo excede o tamanho do container
            controls=[
                nome_campo,  # Título da tela
                ft.Divider(),  # Divisor visual
                ft.ResponsiveRow(controls=[dropdown_alunos], width=800),  # Dropdown para selecionar o aluno
                ft.ResponsiveRow(controls=[container_botoes], width=800),  # Container com os botões
                ft.ResponsiveRow(controls=[container_info_aluno], width=800),  # Container com as informações do aluno
                ft.ResponsiveRow(controls=[ft.Divider()], width=800),  # Divisor visual
                container_dropdown,  # Container com o dropdown de fases para atualização
                container_campos,  # Container com os campos de edição de prazo
                container_dados,  # Container principal para os dados da tabela ou da lista
            ],
            alignment="START",  # Alinha o conteúdo ao início do container
        ),
    )

    # Define a função para atualizar a visualização dos dados (tabela ou lista)
    def atualizar_visualizacao_dados(page):
        """Atualiza a visualização dos dados de acordo com a largura da tela."""
        global dados_tabela_prazos  # Acessa a variável global dados_tabela_prazos

        # Se a largura da tela for menor que 1024 pixels, exibe a ListView de prazos
        if page.width < 1024:
            lista_prazos.controls.clear()  # Limpa a ListView de prazos
            for prazo in dados_tabela_prazos:
                lista_prazos.controls.append(criar_lista_prazos.controls.append(criar_item_lista_prazo(prazo))  # Adiciona um item à ListView para cada prazo
            container_dados.content = lista_prazos  # Define o conteúdo do container principal como a ListView de prazos
            lista_prazos.visible = True  # Torna a ListView de prazos visível
            tabela_prazos.visible = False  # Oculta a tabela de prazos
        # Se a largura da tela for maior ou igual a 1024 pixels, exibe a tabela de prazos
        else:
            tabela_prazos.rows.clear()  # Limpa as linhas da tabela de prazos
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

                # Cria a célula com o botão "Excluir" para o prazo
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
                tempo_restante_cell = ft.DataCell(ft.Text(str(tempo_restante)))

                # Adiciona uma nova linha à tabela de prazos com as informações do prazo
                tabela_prazos.rows.append(
                    ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Text(prazo["fase_pesquisa"])),  # Fase da pesquisa
                            ft.DataCell(ft.Text(prazo["prazo_fase_pesquisa"])),  # Data do prazo
                            ft.DataCell(ft.Text(str(prazo["prazo_dias"]))),  # Prazo em dias (convertido para string)
                            ft.DataCell(ft.Text(prazo["prazo_situacao"])),  # Situação do prazo
                            ft.DataCell(ft.Text(prazo["situacao_fase_pesquisa"])),  # Situação da fase
                            tempo_restante_cell,  # Célula com o tempo restante em dias
                            excluir_cell,  # Célula com o botão "Excluir"
                        ]
                    )
                )
            container_dados.content = tabela_prazos  # Define o conteúdo do container principal como a tabela de prazos
            tabela_prazos.visible = True  # Torna a tabela de prazos visível
            lista_prazos.visible = False  # Oculta a ListView de prazos
        page.update()  # Atualiza a página

    # Define a função para atualizar a visualização das informações do aluno
    def atualizar_visualizacao_info_aluno(page):
        """Atualiza a visualização das informações do aluno."""
        global dados_info_aluno  # Acessa a variável global dados_info_aluno

        # Se houver informações do aluno, preenche os campos de texto com os dados do aluno
        if dados_info_aluno:
            pessoa_info = dados_info_aluno[0]  # Obtém as informações do aluno da lista
            container_info_aluno.content.controls[1].value = pessoa_info.get(
                "nome", ""
            )  # Define o nome do aluno
            container_info_aluno.content.controls[3].value = pessoa_info.get(
                "curso", ""
            )  # Define o curso do aluno
            container_info_aluno.content.controls[5].value = pessoa_info.get(
                "orientador", ""
            )  # Define o orientador do aluno
        page.update()  # Atualiza a página

    # Define a função para criar um item da ListView de prazos
    def criar_item_lista_prazo(prazo):
        """Cria um item da ListView de prazos com as informações do prazo."""
        # Calcula o tempo restante em dias para o prazo
        prazo_fase_pesquisa_date = (
            datetime.datetime.strptime(prazo["prazo_fase_pesquisa"], "%d/%m/%Y").date()
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

        # Retorna um ListTile com as informações do prazo e um botão "Excluir"
        return ft.ListTile(
            title=ft.Text(prazo["fase_pesquisa"]),  # Define o título do ListTile como a fase da pesquisa
            subtitle=ft.Column(  # Define o subtítulo do ListTile como uma coluna com as informações do prazo
                [
                    ft.Row(  # Linha com a data do prazo
                        [ft.Text("Prazo:"), ft.Text(prazo["prazo_fase_pesquisa"])]  # Texto "Prazo:" e a data do prazo
                    ),
                    ft.Row(  # Linha com o prazo em dias
                        [ft.Text("Dias:"), ft.Text(str(prazo["prazo_dias"]))]  # Texto "Dias:" e o prazo em dias (convertido para string)
                    ),
                    ft.Row(  # Linha com a situação do prazo
                        [ft.Text("Situação Prazo:"), ft.Text(prazo["prazo_situacao"])]  # Texto "Situação Prazo:" e a situação do prazo
                    ),
                    ft.Row(  # Linha com a situação da fase
                        [
                            ft.Text("Situação Fase:"),
                            ft.Text(prazo["situacao_fase_pesquisa"]),  # Texto "Situação Fase:" e a situação da fase
                        ]
                    ),
                    ft.Row(  # Linha com o tempo restante em dias
                        [ft.Text("Tempo Restante:"), ft.Text(str(tempo_restante))]  # Texto "Tempo Restante:" e o tempo restante em dias (convertido para string)
                    ),
                ]
            ),
            trailing=ft.IconButton(  # Define o botão "Excluir" no final do ListTile
                icon=ft.icons.DELETE,
                on_click=lambda e, prazo_id=prazo["id"], fase=prazo[
                    "fase_pesquisa"
                ]: confirmar_exclusao(  # Define a função a ser chamada quando o botão for clicado
                    e, prazo_id, fase  # Passa o ID do prazo e a fase como argumentos para a função
                ),
            ),
        )

    # Define a função para redimensionar os containers quando a tela for redimensionada
    def resize_containers(e):
        """Redimensiona os containers de acordo com a largura da tela."""
        atualizar_visualizacao_dados(page)  # Atualiza a visualização dos dados (tabela ou lista)
        atualizar_visualizacao_info_aluno(page)  # Atualiza a visualização das informações do aluno

    # Chama a função 'resize_containers' uma vez no início para configurar a interface corretamente
    resize_containers(None)

    # Define a função 'resize_containers' como a função a ser chamada quando a tela for redimensionada
    page.on_resize = resize_containers

    # Retorna o container principal da tela
    return container_prazos
