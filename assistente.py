import flet as ft
import google.generativeai as genai
from database import Database  # Importa a classe Database

# Configura a API key do Gemini
def configurar_genai(api_key: str):
    genai.configure(api_key=api_key)
    return genai.GenerativeModel('gemini-1.5-flash')

# Inicializa a configuração do banco de dados e o modelo de geração de conteúdo
db = Database()  # Crie a instância da classe Database aqui, fora de qualquer função
model = configurar_genai(api_key="AIzaSyDJyyS98jjloqMKgpXfPj4jL1FskXCr1jY")  # Substitua pela sua chave API

def gerar_insights_iniciais(page: ft.Page):
    """Gera insights iniciais com base nos dados do banco de dados."""
    insights = []

    # 1. Número de alunos e cursos
    num_alunos = len(db.get_db_assistente())
    num_cursos = len(db.get_db_assistente_curso())
    insights.append(f"No sistema de controle do CEPEP foram localizados {num_alunos} alunos e {num_cursos} cursos.")

    return insights

def atualizar_insights(pergunta: str, textfield_resposta, textfield_entrada):
    """Atualiza os insights do chatbot com base na entrada do usuário."""
    # Se não houver correspondência, use o Gemini
    response = model.generate_content(
        f"Analisando os dados da {pergunta} gere respostas citando referências preferencialmente acadêmicas, sempre que possível sugerindo boas práticas e dicas de como usar ia para melhorar pesquisas e trabalhos. Responda de forma concisa e com itens separados por pontos (.). **Não use negrito.**"
    )
    insights = response.text.split(".")

    # Limpa o TextField de resposta
    textfield_resposta.value = ''

    # Adiciona a pergunta ao TextField de resposta
    textfield_resposta.value = f"Pergunta:\n--------------------------------------------------\n{pergunta}\n\nResposta:\n--------------------------------------------------\n"

    # Adiciona os insights ao TextField de resposta
    for insight in insights:
        if insight.strip():  # Remove espaços em branco extras
            textfield_resposta.value += f"{insight.strip()}\n"
    
    # Atualiza a tela
    textfield_resposta.update()
    textfield_entrada.value = ''  # Limpa o TextField
    textfield_entrada.update()

def limpar_respostas(textfield_resposta, textfield_entrada):
    """Limpa o campo de respostas."""
    textfield_resposta.value = ''
    textfield_resposta.update()
    textfield_entrada.value = ''
    textfield_entrada.update()

def tela_assistente(page: ft.Page):
    """Cria a tela do chatbot com o Gemini."""

    # Título da tela
    titulo = ft.Text("Assistente de Produção Acadêmica (Em testes)", size=24, weight=ft.FontWeight.BOLD)

    # Mensagem de boas-vindas
    mensagem_boas_vindas = ft.Text(
        "Olá! Em que posso te ajudar?",
        size=16,
    )

    # Textfield para entrada do usuário
    textfield_entrada = ft.TextField(
        label="Digite sua pergunta",
        multiline=True,
        max_lines=5,  # Define a altura para cinco linhas
        expand=False,  # Remove expand para controlar a largura
        width=800,  # Define a largura
        height=150,  # Define a altura (ajuste para 5 linhas)
        border=ft.InputBorder.NONE,
        content_padding=ft.Padding(left=0, top=0, right=0, bottom=10),  # Corrigido para ft.Padding
        border_radius=ft.border_radius.all(0),
        border_color=ft.colors.BLUE_GREY,
    )

    # TextField para exibir a resposta
    textfield_resposta = ft.TextField(
        expand=False,
        width=800,
        height=400,
        multiline=True,
        border=ft.InputBorder.NONE,
        read_only=True,  # Define como read-only
    )

    # Botão "Enviar"
    botao_enviar = ft.ElevatedButton(
        text="Enviar",
        on_click=lambda e: atualizar_insights(textfield_entrada.value, textfield_resposta, textfield_entrada),  # Passa o TextField
        width=100,
        height=50,
        style=ft.ButtonStyle(  # Aplica o 'border_radius' ao style
            shape=ft.RoundedRectangleBorder(radius=10),
            elevation=4,
            bgcolor=ft.colors.BLUE_ACCENT_400,
            color=ft.colors.WHITE,
        ),
    )

    # Botão "Limpar"
    botao_limpar = ft.ElevatedButton(
        text="Limpar",
        on_click=lambda e: limpar_respostas(textfield_resposta, textfield_entrada),
        width=100,
        height=50,
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=10),
            elevation=4,
            bgcolor=ft.colors.RED_ACCENT_400,
            color=ft.colors.WHITE,
        ),
    )

    # Container principal da tela do chatbot
    container_assistente = ft.Container(
        expand=True,
        padding=20,
        content=ft.Column(
            controls=[
                titulo,
                ft.Divider(height=10),
                mensagem_boas_vindas,
                ft.Divider(height=10),
                ft.Row(
                    controls=[
                        textfield_entrada,
                        botao_enviar,  # Adiciona o botão "Enviar" na mesma linha
                        botao_limpar,  # Adiciona o botão "Limpar" na mesma linha
                    ],
                    spacing=10,
                ),
                ft.Divider(height=10),
                ft.Text("Insights:", weight=ft.FontWeight.BOLD),
                textfield_resposta,  # Exibe a resposta
            ],
            horizontal_alignment=ft.CrossAxisAlignment.START,
            spacing=10
        )
    )

    # Gera insights iniciais
    insights_iniciais = gerar_insights_iniciais(page)
    for insight in insights_iniciais:
        textfield_resposta.value += f"{insight.strip()}\n"

    page.update()

    return container_assistente
