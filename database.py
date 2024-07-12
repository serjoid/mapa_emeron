import mysql.connector
import flet as ft
import pandas as pd
import hashlib
import datetime

class Database:
    def __init__(self):
        self.db_config = {
            'user': 'seu_usuario',       # substitua pelo seu usuário MySQL
            'password': 'sua_senha',     # substitua pela sua senha MySQL
            'host': 'seu_host',         # substitua pelo host do seu servidor MySQL
            'database': 'seu_banco_de_dados'      # substitua pelo nome do seu banco de dados
        }

    def get_db_assistente(self):
        with mysql.connector.connect(**self.db_config) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM pessoas WHERE perfil = 'Discente' ORDER BY nome")
            return cursor.fetchall()

    def get_db_assistente_prazos(self):
        with mysql.connector.connect(**self.db_config) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM prazos")
            return cursor.fetchall()
    
    def get_db_assistente_curso(self):
        with mysql.connector.connect(**self.db_config) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM cursos")
            return cursor.fetchall()

    def get_titulos_tcc(self):
        with mysql.connector.connect(**self.db_config) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT titulo_tcc FROM pessoas WHERE perfil = 'Discente' AND titulo_tcc IS NOT NULL")
            return [row[0] for row in cursor.fetchall()]

    def get_aluno(self):
        """Retorna uma lista de nomes de alunos."""
        with mysql.connector.connect(**self.db_config) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT nome FROM pessoas WHERE perfil = 'Discente' ORDER BY nome")
            return [row[0] for row in cursor.fetchall()]
        
    def get_aluno2(self):
        """Retorna uma lista de dicionários, cada um representando um aluno com 'id' e 'nome'."""
        with mysql.connector.connect(**self.db_config) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, nome FROM pessoas WHERE perfil = 'Discente' ORDER BY nome")
            return [{"id": row[0], "nome": row[1]} for row in cursor.fetchall()]
    
    def get_orientador(self):
        """Retorna uma lista de nomes de orientadores."""
        with mysql.connector.connect(**self.db_config) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT nome FROM pessoas WHERE perfil = 'Orientador' ORDER BY nome")
            return [row[0] for row in cursor.fetchall()]
        
    def get_curso(self):
        """Retorna uma lista de nomes de cursos."""
        with mysql.connector.connect(**self.db_config) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT DISTINCT nome_curso FROM cursos ORDER BY nome_curso")
            return [row[0] for row in cursor.fetchall()]
        
    def get_orientando(self, orientador):
        """Retorna os nomes dos orientandos de um orientador específico."""
        with mysql.connector.connect(**self.db_config) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                        SELECT nome
                        FROM pessoas WHERE orientador = %s""", (orientador,))
            rows = cursor.fetchall()
            return [row[0] for row in rows]
        
    def get_relatorio(self):
        """Retorna os dados para o DataTable, 
        exibindo apenas a fase da pesquisa mais recente de cada aluno.
        """
        with mysql.connector.connect(**self.db_config) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT 
                    p.nome, 
                    p.curso, 
                    p.orientador, 
                    p.polo, 
                    p.instituicao,
                    p.ano_ingresso,
                    p.situacao_aluno_curso, 
                    pz.fase_pesquisa,
                    pz.prazo_fase_pesquisa,
                    pz.situacao_fase_pesquisa
                FROM pessoas p
                LEFT JOIN prazos pz ON p.id = pz.id_pessoa 
                AND pz.id = (SELECT MAX(id) FROM prazos WHERE id_pessoa = p.id)
                WHERE p.perfil = 'Discente'
                ORDER BY p.nome
            """)
            dados_alunos = cursor.fetchall()
            rows = []
            for aluno in dados_alunos:
                cells = [
                    ft.DataCell(ft.Text(valor, size=10, selectable=True)) if valor is not None else ft.DataCell(ft.Text("", size=10, selectable=True))
                    for valor in aluno
                ]
                rows.append(ft.DataRow(cells=cells))
            return rows
            
    def get_relatorio_geral(self):
            """Retorna os dados para o DataFrame, 
            buscando a fase da pesquisa da tabela 'prazos'.
            """
            with mysql.connector.connect(**self.db_config) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT 
                        p.perfil, 
                        p.nome, 
                        p.telefone, 
                        p.email, 
                        p.lattes, 
                        p.matricula, 
                        p.orientador,
                        p.instituicao, 
                        p.uf_instituicao, 
                        p.curso, 
                        p.nivel_curso, 
                        p.situacao_aluno_curso, 
                        p.ano_ingresso, 
                        p.ano_conclusao,
                        p.titulo_tcc, 
                        p.tipo_tcc, 
                        pz.fase_pesquisa,  -- Busca a fase da pesquisa da tabela 'prazos'
                        pz.prazo_fase_pesquisa,  -- Busca o prazo da fase da pesquisa da tabela 'prazos'
                        pz.prazo_dias,
                        pz.prazo_situacao,
                        pz.situacao_fase_pesquisa,
                        p.situacao_matricula, 
                        p.grupo_pesquisa, 
                        p.linha_pesquisa,
                        p.bolsa, 
                        p.tipo_bolsa, 
                        p.vinculo, 
                        p.polo, 
                        p.doc_compromisso, 
                        p.via_tcc_entregue,
                        p.titulacao
                    FROM pessoas p
                    LEFT JOIN prazos pz ON p.id = pz.id_pessoa
                    AND pz.id = (SELECT MAX(id) FROM prazos WHERE id_pessoa = p.id) -- Busca o prazo mais recente
                    ORDER BY p.nome
                """)
                relatorio_geral = cursor.fetchall()

                colunas = [
                    "perfil", "nome", "telefone", "email", "lattes", "matricula", "orientador",
                    "instituicao", "uf_instituicao", "curso", "nivel_curso", "situacao_aluno_curso", 
                    "ano_ingresso", "ano_conclusao", "titulo_tcc", "tipo_tcc", 
                    "fase_pesquisa", "prazo_fase_pesquisa", "prazo_dias", "prazo_situacao", "situacao_fase_pesquisa",
                    "situacao_matricula", "grupo_pesquisa", "linha_pesquisa", "bolsa", "tipo_bolsa", 
                    "vinculo", "polo", "doc_compromisso", "via_tcc_entregue", "titulacao"
                ]
                df = pd.DataFrame(relatorio_geral, columns=colunas)
                return df
            
    def get_orientador_relatorio(self, orientador_filtrado):
        """Retorna as informações dos alunos de um orientador específico."""
        with mysql.connector.connect(**self.db_config) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT 
                    p.nome, 
                    p.curso, 
                    p.polo, 
                    p.instituicao,
                    p.ano_ingresso,
                    p.ano_conclusao,
                    p.situacao_aluno_curso, 
                    pz.fase_pesquisa,
                    pz.prazo_fase_pesquisa,
                    pz.situacao_fase_pesquisa
                FROM pessoas p
                LEFT JOIN prazos pz ON p.id = pz.id_pessoa 
                AND pz.id = (SELECT MAX(id) FROM prazos WHERE id_pessoa = p.id) -- condição para evitar duplicatas
                WHERE p.perfil = 'Discente' AND p.orientador = %s
                ORDER BY p.nome
            """, (orientador_filtrado,))
            dados_orientador = cursor.fetchall()

            # Cria as linhas do DataTable
            rows = []
            for data in dados_orientador:
                row = ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(str(valor), size=11, selectable=True)) 
                        for valor in data
                    ]
                )
                rows.append(row)
            return rows
                
    def get_curso_relatorio(self, curso_filtrado):
        """Retorna as informações dos alunos de um curso específico."""
        with mysql.connector.connect(**self.db_config) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT 
                    p.nome, 
                    p.curso, 
                    p.orientador, 
                    p.polo, 
                    p.instituicao,
                    p.ano_ingresso,
                    p.situacao_aluno_curso, 
                    pz.fase_pesquisa,
                    pz.prazo_fase_pesquisa,
                    pz.situacao_fase_pesquisa
                FROM pessoas p
                LEFT JOIN prazos pz ON p.id = pz.id_pessoa
                WHERE p.perfil = 'Discente' AND p.curso = %s
                ORDER BY p.nome
            """, (curso_filtrado,))
            dados_curso = cursor.fetchall()

            # Cria as linhas do DataTable
            rows = []
            for data in dados_curso:
                row = ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(str(valor), size=10, selectable=True)) 
                        for valor in data
                    ]
                )
                rows.append(row)
            return rows

    def get_pessoa_info(self, nome):
        """Retorna as informações de uma pessoa pelo nome."""
        with mysql.connector.connect(**self.db_config) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT 
                    p.id, 
                    p.perfil, 
                    p.nome, 
                    p.telefone, 
                    p.email, 
                    p.lattes, 
                    p.matricula,
                    p.orientador, 
                    p.instituicao, 
                    p.uf_instituicao, 
                    p.curso, 
                    p.sigla_curso,
                    p.tipo_curso, 
                    p.nivel_curso, 
                    p.situacao_aluno_curso, 
                    p.ano_ingresso,
                    p.ano_conclusao, 
                    p.titulo_tcc, 
                    p.tipo_tcc, 
                    p.prazo_tcc, 
                    p.prorrogacao_tcc,
                    p.situacao_tcc, 
                    p.situacao_matricula, 
                    p.grupo_pesquisa,
                    p.linha_pesquisa, 
                    p.bolsa, 
                    p.tipo_bolsa, 
                    p.vinculo, 
                    p.polo, 
                    p.doc_compromisso,
                    p.via_tcc_entregue, 
                    p.titulacao
                FROM pessoas p
                WHERE p.nome = %s
            """, (nome,))
            row = cursor.fetchone()
            if row is None:
                return {} 
            columns = [column[0] for column in cursor.description]
            pessoa_info = dict(zip(columns, row))
            return pessoa_info
        
    def get_pessoa_info_by_id(self, pessoa_id):
        """Retorna as informações de uma pessoa pelo ID."""
        with mysql.connector.connect(**self.db_config) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT 
                    p.id, 
                    p.perfil, 
                    p.nome, 
                    p.telefone, 
                    p.email, 
                    p.lattes, 
                    p.matricula,
                    p.orientador, 
                    p.instituicao, 
                    p.uf_instituicao, 
                    p.curso, 
                    p.sigla_curso,
                    p.tipo_curso, 
                    p.nivel_curso, 
                    p.situacao_aluno_curso, 
                    p.ano_ingresso,
                    p.ano_conclusao, 
                    p.titulo_tcc, 
                    p.tipo_tcc, 
                    p.prazo_tcc, 
                    p.prorrogacao_tcc,
                    p.situacao_tcc, 
                    p.situacao_matricula, 
                    p.grupo_pesquisa,
                    p.linha_pesquisa, 
                    p.bolsa, 
                    p.tipo_bolsa, 
                    p.vinculo, 
                    p.polo, 
                    p.doc_compromisso,
                    p.via_tcc_entregue, 
                    p.titulacao
                FROM pessoas p
                WHERE p.id = %s
            """, (pessoa_id,))
            row = cursor.fetchone()
            if row is None:
                return {} 
            columns = [column[0] for column in cursor.description]
            pessoa_info = dict(zip(columns, row))
            return pessoa_info
        
    def get_orientador_info(self, nome):
        """Retorna as informações de um aluno específico pelo nome."""
        with mysql.connector.connect(**self.db_config) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                        SELECT id, perfil, nome, telefone, email, lattes, matricula,
                        orientador, instituicao, uf_instituicao, curso, sigla_curso,
                        tipo_curso, nivel_curso, situacao_aluno_curso, ano_ingresso,
                        ano_conclusao, titulo_tcc, tipo_tcc, prazo_tcc, prorrogacao_tcc,
                        situacao_tcc, fase_pesquisa, situacao_matricula, grupo_pesquisa,
                        linha_pesquisa, bolsa, tipo_bolsa, vinculo, polo, doc_compromisso,
                        via_tcc_entregue, prazo_fase_pesquisa, titulacao
                FROM pessoas WHERE perfil = 'Orientador' and nome = %s""", (nome,))
            row = cursor.fetchone()
            if row is None:
                return {}  # Return an empty dictionary if no match is found
            columns = [column[0] for column in cursor.description]
            orientador_info = dict(zip(columns, row))
            if 'nome' in orientador_info:
                return orientador_info
            else:
                return {}

    def insert_pessoa(self, pessoa_data):
        """Insere uma nova pessoa na tabela."""
        with mysql.connector.connect(**self.db_config) as conn:
            cursor = conn.cursor()
            try:
                # Extraia os dados da pessoa para a tabela 'pessoas'
                pessoa_data_pessoas = {
                    k: v.upper() if k in ['nome', 'matricula', 'tipo_tcc', 'titulo_tcc', 'situacao_matricula',
                                        'grupo_pesquisa', 'linha_pesquisa', 'doc_compromisso'] else v
                    for k, v in pessoa_data.items()
                    if k in [
                        'perfil', 'nome', 'telefone', 'email', 'lattes', 'matricula',
                        'orientador', 'instituicao', 'uf_instituicao', 'curso',
                        'nivel_curso', 'situacao_aluno_curso',
                        'ano_ingresso', 'ano_conclusao', 'titulo_tcc', 'tipo_tcc',
                        'situacao_matricula', 'grupo_pesquisa', 'linha_pesquisa',
                        'bolsa', 'tipo_bolsa', 'vinculo', 'polo', 'doc_compromisso',
                        'via_tcc_entregue', 'titulacao'
                    ]
                }

                # Limpa o campo telefone, mantendo apenas dígitos numéricos
                pessoa_data_pessoas['telefone'] = ''.join(filter(str.isdigit, pessoa_data_pessoas['telefone']))

                # Verificar se o nome já existe na tabela
                cursor.execute("SELECT COUNT(*) FROM pessoas WHERE nome = %s", (pessoa_data_pessoas['nome'],))
                count = cursor.fetchone()[0]

                if count > 0:
                    pessoa_data_pessoas['nome'] += ' (2)'

                cursor.execute("""
                    INSERT INTO pessoas (
                        perfil, nome, telefone, email, lattes, matricula, orientador, instituicao,
                        uf_instituicao, curso, nivel_curso, situacao_aluno_curso, ano_ingresso,
                        ano_conclusao, titulo_tcc, tipo_tcc, situacao_matricula, grupo_pesquisa,
                        linha_pesquisa, bolsa, tipo_bolsa, vinculo, polo, doc_compromisso,
                        via_tcc_entregue, titulacao
                    ) VALUES (
                        %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
                    )""", (
                    pessoa_data_pessoas['perfil'], pessoa_data_pessoas['nome'], pessoa_data_pessoas['telefone'],
                    pessoa_data_pessoas['email'], pessoa_data_pessoas['lattes'], pessoa_data_pessoas['matricula'],
                    pessoa_data_pessoas['orientador'], pessoa_data_pessoas['instituicao'],
                    pessoa_data_pessoas['uf_instituicao'], pessoa_data_pessoas['curso'],
                    pessoa_data_pessoas['nivel_curso'],
                    pessoa_data_pessoas['situacao_aluno_curso'], pessoa_data_pessoas['ano_ingresso'],
                    pessoa_data_pessoas['ano_conclusao'],
                    pessoa_data_pessoas['titulo_tcc'], pessoa_data_pessoas['tipo_tcc'],
                    pessoa_data_pessoas['situacao_matricula'], pessoa_data_pessoas['grupo_pesquisa'],
                    pessoa_data_pessoas['linha_pesquisa'], pessoa_data_pessoas['bolsa'],
                    pessoa_data_pessoas['tipo_bolsa'], pessoa_data_pessoas['vinculo'], pessoa_data_pessoas['polo'],
                    pessoa_data_pessoas['doc_compromisso'], pessoa_data_pessoas['via_tcc_entregue'],
                    pessoa_data_pessoas['titulacao']
                ))
                conn.commit()
                print("Pessoa cadastrada com sucesso.")
            except Exception as e:
                print(f"Erro ao cadastrar pessoa: {e}")
                conn.rollback()  # Reverte a transação em caso de erro

    def update_pessoa(self, pessoa_data):
        """Atualiza os dados de uma pessoa existente."""
        with mysql.connector.connect(**self.db_config) as conn:
            cursor = conn.cursor()
            try:
                # Aplica upper() aos campos desejados
                pessoa_data['nome'] = pessoa_data['nome'].upper()
                pessoa_data['matricula'] = pessoa_data['matricula'].upper()
                pessoa_data['tipo_tcc'] = pessoa_data['tipo_tcc'].upper()
                pessoa_data['titulo_tcc'] = pessoa_data['titulo_tcc'].upper()
                pessoa_data['situacao_matricula'] = pessoa_data['situacao_matricula'].upper()
                pessoa_data['grupo_pesquisa'] = pessoa_data['grupo_pesquisa'].upper()
                pessoa_data['linha_pesquisa'] = pessoa_data['linha_pesquisa'].upper()
                pessoa_data['doc_compromisso'] = pessoa_data['doc_compromisso'].upper()

                # Limpa o campo telefone, mantendo apenas dígitos numéricos
                pessoa_data['telefone'] = ''.join(filter(str.isdigit, pessoa_data['telefone']))

                cursor.execute("""
                    UPDATE pessoas
                    SET perfil = %s, nome = %s, telefone = %s, email = %s, lattes = %s, matricula = %s, 
                        orientador = %s, instituicao = %s, uf_instituicao = %s, curso = %s, 
                        nivel_curso = %s, 
                        situacao_aluno_curso = %s, ano_ingresso = %s, ano_conclusao = %s, 
                        titulo_tcc = %s, tipo_tcc = %s,
                        situacao_matricula = %s, 
                        grupo_pesquisa = %s, linha_pesquisa = %s, bolsa = %s, tipo_bolsa = %s, 
                        vinculo = %s, polo = %s, doc_compromisso = %s, via_tcc_entregue = %s
                    WHERE id = %s
                """, (pessoa_data['perfil'], pessoa_data['nome'], pessoa_data['telefone'], pessoa_data['email'], 
                    pessoa_data['lattes'], pessoa_data['matricula'], pessoa_data['orientador'], 
                    pessoa_data['instituicao'], pessoa_data['uf_instituicao'], pessoa_data['curso'], 
                    pessoa_data['nivel_curso'], 
                    pessoa_data['situacao_aluno_curso'], pessoa_data['ano_ingresso'], pessoa_data['ano_conclusao'], 
                    pessoa_data['titulo_tcc'], pessoa_data['tipo_tcc'], 
                    pessoa_data['situacao_matricula'], pessoa_data['grupo_pesquisa'], pessoa_data['linha_pesquisa'], 
                    pessoa_data['bolsa'], pessoa_data['tipo_bolsa'], pessoa_data['vinculo'], pessoa_data['polo'], 
                    pessoa_data['doc_compromisso'], pessoa_data['via_tcc_entregue'],
                    pessoa_data['id']))
                conn.commit()
                print("Pessoa atualizada com sucesso.")
            except mysql.connector.Error as e:
                print(f"Erro ao atualizar pessoa: {e}")
            except KeyError as e:
                print(f"Chave ausente no dicionário: {e}")

    def get_curso_info(self, nome_curso):
        """Retorna as informações de um curso específico pelo nome."""
        with mysql.connector.connect(**self.db_config) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                        SELECT ID, nome_curso, sigla_curso, tipo_curso, area_curso, coordenador_curso
                        FROM cursos WHERE nome_curso = %s""", (nome_curso,))
            row = cursor.fetchone()
            if row is None:
                return {}  # Return an empty dictionary if no match is found
            columns = [column[0] for column in cursor.description]
            return dict(zip(columns, row))
            
    def insert_curso(self, curso_data):
        """Insere um novo curso na tabela."""
        with mysql.connector.connect(**self.db_config) as conn:
            cursor = conn.cursor()
            try:
                cursor.execute("""
                    INSERT INTO cursos (nome_curso, sigla_curso, tipo_curso, area_curso, coordenador_curso)
                    VALUES (%s, %s, %s, %s, %s)""",
                    (curso_data['nome_curso'], curso_data['sigla_curso'], curso_data['tipo_curso'], curso_data['area_curso'], curso_data['coordenador_curso']))
                conn.commit()
                print("Curso cadastrado com sucesso.")
            except mysql.connector.Error as e:
                print(f"Erro ao cadastrar curso: {e}")
            except KeyError as e:
                print(f"Chave ausente no dicionário: {e}")

    def update_curso(self, curso_data):
        """Atualiza os dados de um curso existente."""
        with mysql.connector.connect(**self.db_config) as conn:
            cursor = conn.cursor()
            try:
                cursor.execute("""
                    UPDATE cursos 
                    SET nome_curso = %s, sigla_curso = %s, tipo_curso = %s, area_curso = %s, coordenador_curso = %s
                    WHERE ID = %s
                """, (curso_data['nome_curso'], curso_data['sigla_curso'], curso_data['tipo_curso'], 
                    curso_data['area_curso'], curso_data['coordenador_curso'], curso_data['ID']))
                conn.commit()
                print("Curso atualizado com sucesso.")
            except mysql.connector.Error as e:
                print(f"Erro ao atualizar curso: {e}")
            except KeyError as e:
                print(f"Chave ausente no dicionário: {e}")

    def insert_orientador(self, orientador_data):
        """Insere um novo orientador na tabela."""
        with mysql.connector.connect(**self.db_config) as conn:
            cursor = conn.cursor()
            try:
                # Transforma nome, titulacao e instituicao em maiúsculas
                orientador_data['nome'] = orientador_data['nome'].upper()
                orientador_data['titulacao'] = orientador_data['titulacao'].upper()
                orientador_data['instituicao'] = orientador_data['instituicao'].upper()

                # Limpa o campo telefone, mantendo apenas dígitos numéricos
                orientador_data['telefone'] = ''.join(filter(str.isdigit, orientador_data['telefone']))

                cursor.execute("""
                    INSERT INTO pessoas (
                        perfil, nome, telefone, email, lattes, curso, titulacao, 
                        instituicao, vinculo, polo, uf_instituicao
                    ) VALUES (
                        %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
                    )
                """, (
                    'Orientador', orientador_data['nome'], orientador_data['telefone'], 
                    orientador_data['email'], orientador_data['lattes'], orientador_data['curso'],
                    orientador_data['titulacao'], 
                    orientador_data['instituicao'], orientador_data['vinculo'], orientador_data['polo'],
                    orientador_data['uf_instituicao']
                ))
                conn.commit()
                print("Orientador cadastrado com sucesso.")
            except mysql.connector.Error as e:
                print(f"Erro ao cadastrar orientador: {e}")
            except KeyError as e:
                print(f"Chave ausente no dicionário: {e}")

    def update_orientador(self, orientador_data):
        """Atualiza os dados de um orientador existente."""
        with mysql.connector.connect(**self.db_config) as conn:
            cursor = conn.cursor()
            try:
                # Transforma nome, titulacao e instituicao em maiúsculas
                orientador_data['nome'] = orientador_data['nome'].upper()
                orientador_data['titulacao'] = orientador_data['titulacao'].upper()
                orientador_data['instituicao'] = orientador_data['instituicao'].upper()

                # Limpa o campo telefone, mantendo apenas dígitos numéricos
                orientador_data['telefone'] = ''.join(filter(str.isdigit, orientador_data['telefone']))

                cursor.execute("""
                    UPDATE pessoas
                    SET nome = %s, telefone = %s, email = %s, curso = %s, titulacao = %s, 
                        instituicao = %s, vinculo = %s, polo = %s, uf_instituicao = %s, lattes = %s
                    WHERE id = %s
                """, (
                    orientador_data['nome'], orientador_data['telefone'], orientador_data['email'],
                    orientador_data['curso'], orientador_data['titulacao'],
                    orientador_data['instituicao'], orientador_data['vinculo'], orientador_data['polo'],
                    orientador_data['uf_instituicao'], orientador_data['lattes'], orientador_data['id']
                ))
                conn.commit()
                print("Orientador atualizado com sucesso.")
            except mysql.connector.Error as e:
                print(f"Erro ao atualizar orientador: {e}")
            except KeyError as e:
                print(f"Chave ausente no dicionário: {e}")

    def get_prazos_by_pessoa_id(self, pessoa_id):
            """Retorna todos os prazos de uma pessoa pelo ID."""
            with mysql.connector.connect(**self.db_config) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT id, fase_pesquisa, prazo_fase_pesquisa, prazo_dias, prazo_situacao, situacao_fase_pesquisa
                    FROM prazos
                    WHERE id_pessoa = %s
                """, (pessoa_id,))
                rows = cursor.fetchall()
                columns = [column[0] for column in cursor.description]
                return [dict(zip(columns, row)) for row in rows]

    def inserir_prazo(self, prazo_data):
        """Insere um novo prazo na tabela 'prazos'."""
        with mysql.connector.connect(**self.db_config) as conn:
            cursor = conn.cursor()
            
            # Define um valor padrão para prazo_fase_pesquisa se for nulo ou vazio
            prazo_fase_pesquisa = prazo_data['prazo_fase_pesquisa'] if prazo_data['prazo_fase_pesquisa'] else '01/01/2024'

            # Validação e definição de prazo_dias
            try:
                prazo_dias = int(prazo_data['prazo_dias'])
                if prazo_dias < 0 or prazo_dias > 730:
                    prazo_dias = 0
            except (ValueError, TypeError):
                prazo_dias = 0

            cursor.execute("""
                INSERT INTO prazos (id_pessoa, fase_pesquisa, prazo_fase_pesquisa, prazo_dias, prazo_situacao, situacao_fase_pesquisa)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (
                prazo_data['id_pessoa'],
                prazo_data['fase_pesquisa'],
                prazo_fase_pesquisa,
                prazo_dias,
                prazo_data['prazo_situacao'],
                prazo_data['situacao_fase_pesquisa']
            ))
            conn.commit()

    def atualizar_prazo(self, prazo_data):
        """Atualiza um prazo existente na tabela 'prazos'."""
        with mysql.connector.connect(**self.db_config) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE prazos
                SET 
                    fase_pesquisa = %s,
                    prazo_fase_pesquisa = %s,
                    prazo_dias = %s,
                    prazo_situacao = %s,
                    situacao_fase_pesquisa = %s
                WHERE id = %s 
            """, (
                prazo_data['fase_pesquisa'],
                prazo_data['prazo_fase_pesquisa'],
                prazo_data['prazo_dias'],
                prazo_data['prazo_situacao'],
                prazo_data['situacao_fase_pesquisa'],
                prazo_data['id'], # Certifique-se de ter o ID do prazo a ser atualizado
            ))
            conn.commit()

    def excluir_prazo(self, prazo_id):
        """Exclui um prazo da tabela 'prazos' pelo ID."""
        with mysql.connector.connect(**self.db_config) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM prazos WHERE id = %s", (prazo_id,))
            conn.commit()

    def deletar_pessoa(self, pessoa_id):
            """Deleta uma pessoa da tabela 'pessoas' pelo ID, fazendo backup antes."""
            with mysql.connector.connect(**self.db_config) as conn:
                cursor = conn.cursor()

                # Faz backup dos dados da pessoa em 'pessoas_excluidas'
                cursor.execute(
                    "INSERT INTO pessoas_excluidas SELECT * FROM pessoas WHERE id = %s",
                    (pessoa_id,),
                )

                # Exclui a pessoa da tabela 'pessoas'
                cursor.execute("DELETE FROM pessoas WHERE id = %s", (pessoa_id,))
                conn.commit()

    def deletar_curso(self, curso_id):
        """Deleta um curso da tabela 'cursos' pelo ID, fazendo backup antes."""
        with mysql.connector.connect(**self.db_config) as conn:
            cursor = conn.cursor()

            # Faz backup dos dados do curso em 'cursos_excluidos'
            cursor.execute(
                "INSERT INTO cursos_excluidos SELECT * FROM cursos WHERE ID = %s",
                (curso_id,),
            )

            # Exclui o curso da tabela 'cursos'
            cursor.execute("DELETE FROM cursos WHERE ID = %s", (curso_id,))
            conn.commit()

    def excluir_prazo(self, prazo_id):
        """Exclui um prazo da tabela 'prazos' pelo ID."""
        with mysql.connector.connect(**self.db_config) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM prazos WHERE id = %s", (prazo_id,))
            conn.commit()

    def get_alunos_por_curso(self):
        """Retorna o número de alunos por curso."""
        with mysql.connector.connect(**self.db_config) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT curso, COUNT(*) AS num_alunos FROM pessoas
                WHERE perfil = 'Discente'
                GROUP BY curso
                ORDER BY curso
            """)
            return cursor.fetchall()

    def get_alunos_por_orientador(self):
        """Retorna o número de alunos por orientador."""
        with mysql.connector.connect(**self.db_config) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT orientador, COUNT(*) AS num_alunos
                FROM pessoas
                WHERE perfil = 'Discente'
                GROUP BY orientador
                ORDER BY orientador
            """)
            return cursor.fetchall()

    def get_alunos_por_situacao_tcc(self):
        """Retorna o número de alunos por situação do TCC."""
        with mysql.connector.connect(**self.db_config) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT situacao_tcc, COUNT(*) AS num_alunos
                FROM pessoas
                WHERE perfil = 'Discente'
                GROUP BY situacao_tcc
                ORDER BY situacao_tcc
            """)
            return cursor.fetchall()
        
    def cadastrar_usuario(self, nome, email, usuario, senha, perfil):
        """Cadastra um novo usuário na tabela 'cadastro' com a senha em hash.

        Args:
            nome: Nome completo do usuário.
            email: Email do usuário.
            usuario: Nome de usuário para login.
            senha: Senha do usuário (em texto plano).
            perfil: Perfil do usuário (por exemplo, 'admin', 'usuario', etc.).
        """
        conn = mysql.connector.connect(**self.db_config)
        cursor = conn.cursor()

        # Gera o hash da senha usando SHA-256
        senha_hash = hashlib.sha256(senha.encode()).hexdigest()

        try:
            cursor.execute(
                "INSERT INTO cadastro (nome, email, usuario, senha, perfil) VALUES (%s, %s, %s, %s, %s)",
                (nome, email, usuario, senha_hash, perfil),
            )
            conn.commit()
            print(f"Usuário '{usuario}' cadastrado com sucesso!")
            return True  # Indica sucesso no cadastro
        except mysql.connector.IntegrityError:
            print(f"Erro: Já existe um usuário com o nome de usuário '{usuario}' ou email '{email}'.")
            return False  # Indica erro no cadastro
        finally:
            cursor.close()
            conn.close()

    def alterar_senha(self, usuario, senha_atual, nova_senha):
        """Altera a senha de um usuário existente na tabela 'cadastro'.

        Args:
            usuario: Nome de usuário do usuário a ser atualizado.
            senha_atual: Senha atual do usuário (em texto plano).
            nova_senha: Nova senha desejada (em texto plano).

        Returns:
            True se a senha foi alterada com sucesso, False caso contrário.
        """
        conn = mysql.connector.connect(**self.db_config)
        cursor = conn.cursor()

        # Gera o hash da senha atual
        senha_atual_hash = hashlib.sha256(senha_atual.encode()).hexdigest()

        try:
            # Verifica se o usuário e a senha atual correspondem
            cursor.execute(
                "SELECT 1 FROM cadastro WHERE usuario = %s AND senha = %s",
                (usuario, senha_atual_hash),
            )
            if cursor.fetchone() is None:
                print(f"Erro: Nome de usuário ou senha atual incorretos.")
                return False

            # Gera o hash da nova senha
            nova_senha_hash = hashlib.sha256(nova_senha.encode()).hexdigest()

            # Atualiza a senha no banco de dados
            cursor.execute(
                "UPDATE cadastro SET senha = %s WHERE usuario = %s",
                (nova_senha_hash, usuario),
            )
            conn.commit()
            print(f"Senha do usuário '{usuario}' alterada com sucesso!")
            return True

        except mysql.connector.Error as e:
            print(f"Erro ao alterar a senha: {e}")
            return False
        finally:
            cursor.close()
            conn.close()

    def verificar_credenciais(self, usuario, senha):
        """Verifica as credenciais do usuário no banco de dados.

        Args:
            usuario: Nome de usuário.
            senha: Senha em texto plano.

        Returns:
            Dicionário com os dados do usuário se as credenciais forem válidas, None caso contrário.
        """
        conn = mysql.connector.connect(**self.db_config)
        cursor = conn.cursor()

        # Gera o hash da senha
        senha_hash = hashlib.sha256(senha.encode()).hexdigest()

        try:
            # Seleciona explicitamente as colunas desejadas
            cursor.execute(
                "SELECT usuario, senha, perfil FROM cadastro WHERE usuario = %s AND senha = %s", 
                (usuario, senha_hash)
            )
            usuario_db = cursor.fetchone()

            if usuario_db:
                # Converte a tupla do resultado em um dicionário
                colunas = [column[0] for column in cursor.description]
                usuario_dict = dict(zip(colunas, usuario_db))
                return usuario_dict
            else:
                return None
        except mysql.connector.Error as e:
            print(f"Erro ao verificar as credenciais: {e}")
            return None
        finally:
            cursor.close()
            conn.close()
        

    def registrar_log(self, usuario, acao, detalhes=None):
        """Registra um novo log no banco de dados.

        Args:
            usuario: Nome de usuário que fez a ação.
            acao: Tipo de ação realizada (por exemplo, "login", "inserir_pessoa", etc.).
            detalhes: Informações adicionais sobre a ação (opcional).
        """
        data_hora = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with mysql.connector.connect(**self.db_config) as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO logs (data_hora, usuario, acao, detalhes) VALUES (%s, %s, %s, %s)",
                           (data_hora, usuario, acao, detalhes))
            conn.commit()

    def get_alunos_por_fase_pesquisa(self):
        """Retorna o número de alunos por fase de pesquisa, considerando apenas a fase de pesquisa mais recente de cada aluno."""
        with mysql.connector.connect(**self.db_config) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT 
                    fase_pesquisa, 
                    COUNT(*) AS num_alunos
                FROM (
                    SELECT 
                        pz.id_pessoa, 
                        pz.fase_pesquisa
                    FROM 
                        prazos pz
                    INNER JOIN (
                        SELECT 
                            id_pessoa, 
                            MAX(id) AS max_id
                        FROM 
                            prazos
                        GROUP BY 
                            id_pessoa
                    ) AS max_prazo
                    ON 
                        pz.id_pessoa = max_prazo.id_pessoa 
                        AND pz.id = max_prazo.max_id
                ) AS recentes
                GROUP BY 
                    fase_pesquisa
                ORDER BY 
                    fase_pesquisa;
            """)
            return cursor.fetchall()

    def get_submissoes_by_pessoa_id(self, pessoa_id):
        """Retorna todas as submissões de uma pessoa pelo ID."""
        with mysql.connector.connect(**self.db_config) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id, link, data_hora
                FROM submissoes
                WHERE id_pessoa = %s
            """, (pessoa_id,))
            rows = cursor.fetchall()
            columns = [column[0] for column in cursor.description]
            return [dict(zip(columns, row)) for row in rows]

    def inserir_submissao(self, submissao_data):
        """Insere uma nova submissão na tabela 'submissoes'."""
        with mysql.connector.connect(**self.db_config) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO submissoes (id_pessoa, link)
                VALUES (%s, %s)
            """, (
                submissao_data['id_pessoa'],
                submissao_data['link'],
            ))
            conn.commit()

    def excluir_submissao(self, submissao_id):
        """Exclui uma submissão da tabela 'submissoes' pelo ID."""
        with mysql.connector.connect(**self.db_config) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM submissoes WHERE id = %s", (submissao_id,))
            conn.commit()

    def get_orientador_info_por_usuario(self, usuario):
        """Retorna as informações do orientador pelo nome de usuário."""
        with mysql.connector.connect(**self.db_config) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT p.*  -- Selecionando apenas as colunas de 'pessoas'
                FROM pessoas p
                JOIN cadastro c ON p.nome = c.nome  
                WHERE c.usuario = %s AND p.perfil = 'Orientador' 
            """, (usuario,))
            row = cursor.fetchone()
            if row is not None:
                columns = [column[0] for column in cursor.description]
                return dict(zip(columns, row))
            else:
                return None
            
    def get_orientando_por_orientador_id(self, orientador_id):
        """Retorna os orientandos de um orientador específico pelo ID do orientador.

        Args:
            orientador_id: O ID do orientador.

        Returns:
            Uma lista de dicionários, onde cada dicionário representa um orientando 
            e contém suas informações (nome, etc.). 
            Retorna uma lista vazia se nenhum orientando for encontrado.
        """
        with mysql.connector.connect(**self.db_config) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT *
                FROM pessoas
                WHERE orientador = %s AND perfil = 'Discente'
            """, (orientador_id,))
            rows = cursor.fetchall()
            columns = [column[0] for column in cursor.description]
            return [dict(zip(columns, row)) for row in rows]
        
    def get_pessoa_info_por_usuario(self, usuario):
        """Retorna as informações de uma pessoa pelo nome de usuário."""
        with mysql.connector.connect(**self.db_config) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT p.*
                FROM pessoas p
                JOIN cadastro c ON p.nome = c.nome
                WHERE c.usuario = %s
            """, (usuario,))
            row = cursor.fetchone()
            if row is not None:
                columns = [column[0] for column in cursor.description]
                return dict(zip(columns, row))
            else:
                return None
    
    def get_relatorio_lista(self):
        """Retorna os dados do relatório em formato de lista."""
        with mysql.connector.connect(**self.db_config) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT 
                    p.nome, 
                    p.curso, 
                    p.orientador, 
                    p.polo, 
                    p.instituicao,
                    p.ano_ingresso,
                    p.situacao_aluno_curso, 
                    pz.fase_pesquisa,
                    pz.prazo_fase_pesquisa,
                    pz.situacao_fase_pesquisa
                FROM pessoas p
                LEFT JOIN prazos pz ON p.id = pz.id_pessoa 
                AND pz.id = (SELECT MAX(id) FROM prazos WHERE id_pessoa = p.id)
                WHERE p.perfil = 'Discente'
                ORDER BY p.nome
            """)
            dados_alunos = cursor.fetchall()
            return dados_alunos
        
    def get_perfil_usuario(self, usuario):
        with mysql.connector.connect(**self.db_config) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT perfil FROM cadastro WHERE usuario = %s", (usuario,)
            )
            row = cursor.fetchone()
            if row:
                return row[0]
            else:
                return None
            
    def get_orientador_relatorio_lista(self, orientador):
        """Retorna uma lista de alunos relacionados ao orientador."""
        with mysql.connector.connect(**self.db_config) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT 
                    p.nome, 
                    p.curso, 
                    p.polo, 
                    p.instituicao,
                    p.ano_ingresso,
                    p.ano_conclusao,
                    p.situacao_aluno_curso, 
                    pz.fase_pesquisa,
                    pz.prazo_fase_pesquisa,
                    pz.situacao_fase_pesquisa
                FROM pessoas p
                LEFT JOIN prazos pz ON p.id = pz.id_pessoa 
                AND pz.id = (SELECT MAX(id) FROM prazos WHERE id_pessoa = p.id)
                WHERE p.orientador = %s
                ORDER BY p.nome
            """, (orientador,))
            dados_orientador = cursor.fetchall()
            return dados_orientador
        
    def consultar_usuarios(self):
        """Consulta os dados de nome, email, usuário e perfil dos usuários cadastrados."""
        with mysql.connector.connect(**self.db_config) as conn:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT nome, email, usuario, perfil FROM cadastro")
            return cursor.fetchall()
        
    def excluir_usuario(self, usuario_excluido):
        """Exclui um usuário do banco de dados.

        Args:
            usuario_excluido: O nome de usuário do usuário a ser excluído.
        """
        with mysql.connector.connect(**self.db_config) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM cadastro WHERE usuario = %s", (usuario_excluido,))
            conn.commit()

    def consultar_logs(self):
        """Consulta os logs no banco de dados, excluindo 'login' e 'logout', ordenados por data_hora (descendente).

        Returns:
            Uma lista de dicionários contendo os logs.
        """
        with mysql.connector.connect(**self.db_config) as conn:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM logs WHERE acao NOT IN ('login', 'logout') ORDER BY data_hora DESC")
            logs = cursor.fetchall()
        return logs

