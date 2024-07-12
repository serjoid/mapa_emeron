import flet as ft  # Importa a biblioteca Flet para a criação da interface
from database import Database  # Importa a classe Database para interagir com o banco de dados

def tela_logs(page: ft.Page):
    """
    Cria a tela de visualização de logs do sistema.

    Args:
        page (ft.Page): A página Flet atual.
    """

    # Inicializa a conexão com o banco de dados
    db = Database()
    logs = []  # Lista para armazenar os logs do sistema

    # Campo de pesquisa para filtrar os logs
    txt_pesquisa = ft.TextField(label="Pesquisar nos logs", width=300)

    # Função para carregar os logs do banco de dados
    def carregar_logs(e):
        """
        Carrega os logs do banco de dados e os exibe na tela.
        """
        nonlocal logs  # Declara a variável 'logs' como nonlocal para poder modificá-la dentro da função
        logs = db.consultar_logs()  # Obtém os logs do banco de dados
        filtrar_logs()  # Filtra os logs de acordo com o termo de pesquisa

    # Função para filtrar os logs de acordo com o termo de pesquisa
    def filtrar_logs(e=None):
        """
        Filtra os logs de acordo com o termo de pesquisa e os exibe na tela.
        """
        termo_pesquisa = txt_pesquisa.value.lower() if txt_pesquisa.value else ""  # Obtém o termo de pesquisa do campo de texto e o converte para minúsculas
        coluna_logs.controls.clear()  # Limpa os logs exibidos na coluna

        # Itera sobre os logs
        for log in logs:
            acao = log.get('acao', 'N/A')  # Obtém a ação do log
            data = log.get('data_hora', 'N/A')  # Obtém a data e hora do log
            usuario = log.get('usuario', 'N/A')  # Obtém o usuário que realizou a ação
            detalhes = log.get('detalhes', 'N/A')  # Obtém os detalhes da ação

            # Verifica se o termo de pesquisa está presente nas informações do log (case insensitive)
            if termo_pesquisa in str(log).lower():
                # Cria um texto com as informações do log formatadas
                log_texto = ft.SelectionArea(  # Cria uma área de seleção para o texto
                    content=ft.Text(
                        f"Ação: {acao}\nData e hora: {data}\nUsuário: {usuario}\nDetalhes: {detalhes}\n-------------------"
                    )
                )
                # Adiciona o texto do log à coluna
                coluna_logs.controls.append(log_texto)

        # Atualiza a coluna de logs e a página
        coluna_logs.update()
        page.update()

    # Botão para carregar os logs do banco de dados
    botao_carregar_logs = ft.ElevatedButton(
        text="Carregar Logs",  # Texto do botão
        on_click=carregar_logs,  # Define a função 'carregar_logs' para ser chamada quando o botão for clicado
        width=200,  # Largura do botão
        height=40,  # Altura do botão
        elevation=4,  # Elevação do botão
        bgcolor="#006BA0",  # Cor de fundo do botão
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),  # Estilo do botão (borda arredondada)
        color="WHITE",  # Cor do texto do botão
    )

    # Coluna para exibir os logs
    coluna_logs = ft.Column()

    # Divisor visual
    divisor = ft.ResponsiveRow(controls=[ft.Divider()], width=800)

    # Título da tela
    nome_campo = ft.Text("Logs do sistema", size=16, color="#006BA0", font_family="Roboto", weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER)

    # Container principal da tela
    container = ft.Container(
        content=ft.Column(
            [
                nome_campo,  # Título da tela
                divisor,  # Divisor visual
                txt_pesquisa,  # Campo de pesquisa para filtrar os logs
                botao_carregar_logs,  # Botão para carregar os logs do banco de dados
                ft.ResponsiveRow(controls=[coluna_logs], width=800),  # Linha responsiva com a coluna de logs
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,  # Alinha o conteúdo horizontalmente ao centro
            scroll=ft.ScrollMode.ALWAYS,  # Habilita a rolagem vertical na tela
        ),
    )

    return container  # Retorna o container principal da tela
