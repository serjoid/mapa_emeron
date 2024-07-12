import home  # Importa o módulo 'home.py' (tela inicial)
import alunos  # Importa o módulo 'alunos.py' (tela de alunos - admin)
import cursos  # Importa o módulo 'cursos.py' (tela de cursos)
import orientadores  # Importa o módulo 'orientadores.py' (tela de orientadores - admin)
import relatorios  # Importa o módulo 'relatorios.py' (tela de relatórios - admin)
import prazos  # Importa o módulo 'prazos.py' (tela de prazos - admin)
import submissoes  # Importa o módulo 'submissoes.py' (tela de submissões - admin)
import cadastro  # Importa o módulo 'cadastro.py' (tela de cadastro de usuários)
import alterar_senha  # Importa o módulo 'alterar_senha.py' (tela de alteração de senha)
import orientador_logado  # Importa o módulo 'orientador_logado.py' (tela de informações do orientador logado)
import relatorios_orientador_logado  # Importa o módulo 'relatorios_orientador_logado.py' (tela de relatórios do orientador logado)
import prazos_orientador_logado  # Importa o módulo 'prazos_orientador_logado.py' (tela de prazos do orientador logado)
import submissoes_orientador_logado  # Importa o módulo 'submissoes_orientador_logado.py' (tela de submissões do orientador logado)
import alunos_orientador  # Importa o módulo 'alunos_orientador.py' (tela de alunos do orientador logado)
import prazos_alunos  # Importa o módulo 'prazos_alunos.py' (tela de prazos do aluno logado)
import alunos_logado  # Importa o módulo 'alunos_logado.py' (tela de informações do aluno logado)
import submissoes_aluno_logado  # Importa o módulo 'submissoes_aluno_logado.py' (tela de submissões do aluno logado)
import orientador_aluno_logado  # Importa o módulo 'orientador_aluno_logado.py' (tela de informações do orientador do aluno logado)
import assistente  # Importa o módulo 'assistente.py' (tela do assistente)
import acesso  # Importa o módulo 'acesso.py' (tela de login)
import tela_logs  # Importa o módulo 'tela_logs.py' (tela de logs do sistema)
from database import Database  # Importa a classe 'Database' do módulo 'database.py'
import flet as ft  # Importa a biblioteca Flet

# Inicializa a conexão com o banco de dados
db = Database()

# Define a função para navegar entre as telas do aplicativo
def navegar(e, usuario, page, perfil_usuario):
    """
    Função para navegar entre as telas do aplicativo.

    Args:
        e (ft.Event): O evento que acionou a função (clique no botão).
        usuario (str): O nome de usuário do usuário logado.
        page (ft.Page): A página Flet atual.
        perfil_usuario (str): O perfil do usuário logado.
    """
    global searchbar
    searchbar = None

    # Obtém o texto do controle que acionou o evento
    texto_controle = (
        e.control.text if hasattr(e, "control") and hasattr(e.control, "text") else ""
    )

    # Encontra o container de conteúdo na página
    conteudo_container = next(
        (
            control
            for control in page.controls[0].content.controls[0].controls
            if isinstance(control, ft.Container) and control.expand
        ),
        None,
    )

    # Verifica se o container de conteúdo foi encontrado
    if not conteudo_container:
        return

    # Limpa o conteúdo do container de conteúdo
    conteudo_container.content = None

    # Navega para a tela correspondente ao botão clicado
    if texto_controle == "Início":
        conteudo_container.content = home.tela_inicial(page)  # Tela inicial
    elif texto_controle == "Cursos":
        conteudo_container.content = cursos.tela_cursos(page, usuario)  # Tela de cursos
    elif texto_controle == "Orientadores":
        # Redireciona para a tela correta de acordo com o perfil do usuário
        if perfil_usuario == "Orientador":
            conteudo_container.content = orientador_logado.tela_orientador_logado(page, usuario)  # Tela de informações do orientador logado
        elif perfil_usuario == "Aluno":
            conteudo_container.content = orientador_aluno_logado.orientador_aluno_logado(page, usuario)  # Tela de informações do orientador do aluno logado
        else:
            conteudo_container.content = orientadores.tela_orientadores(page, usuario)  # Tela de orientadores (admin)
    elif texto_controle == "Alunos":
        # Redireciona para a tela correta de acordo com o perfil do usuário
        if perfil_usuario == "Orientador":
            conteudo_container.content = alunos_orientador.tela_alunos_orientador_logado(page, usuario)  # Tela de alunos do orientador logado
        elif perfil_usuario == "Aluno":
            conteudo_container.content = alunos_logado.tela_alunos_logado(page, usuario)  # Tela de informações do aluno logado
        else:
            conteudo_container.content = alunos.tela_alunos(page, usuario)  # Tela de alunos (admin)
    elif texto_controle == "Relatórios":
        # Redireciona para a tela correta de acordo com o perfil do usuário
        if perfil_usuario == "Orientador":
            conteudo_container.content = relatorios_orientador_logado.relatorios_orientador_logado(page, usuario)  # Tela de relatórios do orientador logado
        else:
            conteudo_container.content = relatorios.tela_relatorios(page)  # Tela de relatórios (admin)
    elif texto_controle == "Andamento da Pesquisa":
        # Redireciona para a tela correta de acordo com o perfil do usuário
        if perfil_usuario == "Orientador":
            conteudo_container.content = prazos_orientador_logado.prazos_orientador_logado(page, usuario)  # Tela de prazos do orientador logado
        elif perfil_usuario == "Aluno":
            aluno_info = db.get_pessoa_info_por_usuario(usuario)  # Obtém as informações do aluno logado
            aluno_id = aluno_info["id"]  # Obtém o ID do aluno logado
            nome_aluno = aluno_info["nome"]  # Obtém o nome do aluno logado
            conteudo_container.content = prazos_alunos.tela_prazos_alunos(page, aluno_id, nome_aluno)  # Tela de prazos do aluno logado
        else:
            conteudo_container.content = prazos.tela_prazos(page, usuario)  # Tela de prazos (admin)
    elif texto_controle == "Submissões":
        # Redireciona para a tela correta de acordo com o perfil do usuário
        if perfil_usuario == "Orientador":
            conteudo_container.content = submissoes_orientador_logado.submissoes_orientador_logado(page, usuario)  # Tela de submissões do orientador logado
        elif perfil_usuario == "Aluno":
            conteudo_container.content = submissoes_aluno_logado.submissoes_aluno_logado(page, usuario)  # Tela de submissões do aluno logado
        else:
            conteudo_container.content = submissoes.tela_submissoes(page, usuario)  # Tela de submissões (admin)
    elif texto_controle == "Cadastro":
        conteudo_container.content = cadastro.tela_cadastro(page, usuario)  # Tela de cadastro de usuários
    elif texto_controle == "Senha":
        conteudo_container.content = alterar_senha.def_alterar_senha(page, usuario)  # Tela de alteração de senha
    elif texto_controle == "Assistente":
        conteudo_container.content = assistente.tela_assistente(page)  # Tela do assistente
    elif texto_controle == "Logs":
        conteudo_container.content = tela_logs.tela_logs(page)  # Tela de logs do sistema
    else:
        conteudo_container.content = ft.Text("Em construção...")  # Mensagem padrão para telas em construção

    # Atualiza a página para exibir o novo conteúdo
    page.update()
