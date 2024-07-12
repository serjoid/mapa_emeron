import home
import alunos
import cursos
import orientadores
import relatorios
import prazos
import submissoes
import cadastro
import alterar_senha
import orientador_logado
import relatorios_orientador_logado
import prazos_orientador_logado
import submissoes_orientador_logado
import alunos_orientador
import prazos_alunos
import alunos_logado
import submissoes_aluno_logado
import orientador_aluno_logado
import assistente
import acesso
import tela_logs
from database import Database
import flet as ft

db = Database()

def navegar(e, usuario, page, perfil_usuario):  # Recebe perfil_usuario como argumento
    """Função para navegar entre as telas do aplicativo."""
    global searchbar
    searchbar = None

    texto_controle = (
        e.control.text if hasattr(e, "control") and hasattr(e.control, "text") else ""
    )

    # Encontre o conteudo_container na página
    conteudo_container = next(
        (
            control
            for control in page.controls[0].content.controls[0].controls
            if isinstance(control, ft.Container) and control.expand
        ),
        None,
    )

    if not conteudo_container:
        return

    # Limpa apenas o conteúdo do conteudo_container
    conteudo_container.content = None

    if texto_controle == "Início":
        conteudo_container.content = home.tela_inicial(page)
    elif texto_controle == "Cursos":
        conteudo_container.content = cursos.tela_cursos(page, usuario)
    elif texto_controle == "Orientadores":
        if perfil_usuario == "Orientador":  # Utiliza perfil_usuario para redirecionamento
            conteudo_container.content = orientador_logado.tela_orientador_logado(page, usuario)
        elif perfil_usuario == "Aluno":
            conteudo_container.content = orientador_aluno_logado.orientador_aluno_logado(page, usuario)
        else:
            conteudo_container.content = orientadores.tela_orientadores(page, usuario)
    elif texto_controle == "Alunos":
        if perfil_usuario == "Orientador":
            conteudo_container.content = alunos_orientador.tela_alunos_orientador_logado(page, usuario)
        elif perfil_usuario == "Aluno":
            conteudo_container.content = alunos_logado.tela_alunos_logado(page, usuario)
        else:
            conteudo_container.content = alunos.tela_alunos(page, usuario)
    elif texto_controle == "Relatórios":
        if perfil_usuario == "Orientador":
            conteudo_container.content = relatorios_orientador_logado.relatorios_orientador_logado(page, usuario)
        else:
            conteudo_container.content = relatorios.tela_relatorios(page)
    elif texto_controle == "Andamento da Pesquisa":
        if perfil_usuario == "Orientador":
            conteudo_container.content = prazos_orientador_logado.prazos_orientador_logado(page, usuario)
        elif perfil_usuario == "Aluno":
            aluno_info = db.get_pessoa_info_por_usuario(usuario)
            aluno_id = aluno_info["id"]
            nome_aluno = aluno_info["nome"]
            conteudo_container.content = prazos_alunos.tela_prazos_alunos(page, aluno_id, nome_aluno)
        else:
            conteudo_container.content = prazos.tela_prazos(page, usuario)
    elif texto_controle == "Submissões":
        if perfil_usuario == "Orientador":
            conteudo_container.content = submissoes_orientador_logado.submissoes_orientador_logado(page, usuario)
        elif perfil_usuario == "Aluno":
            conteudo_container.content = submissoes_aluno_logado.submissoes_aluno_logado(page, usuario)
        else:
            conteudo_container.content = submissoes.tela_submissoes(page, usuario)
    elif texto_controle == "Cadastro":
        conteudo_container.content = cadastro.tela_cadastro(page, usuario)
    elif texto_controle == "Senha":
        conteudo_container.content = alterar_senha.def_alterar_senha(page, usuario)
    elif texto_controle == "Assistente":
        conteudo_container.content = assistente.tela_assistente(page)
    elif texto_controle == "Logs":
        conteudo_container.content = tela_logs.tela_logs(page)
    else:
        conteudo_container.content = ft.Text("Em construção...")

    page.update()