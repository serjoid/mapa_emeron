-- Criação da tabela `cursos`
CREATE TABLE `cursos` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nome_curso` text,
  `sigla_curso` text,
  `tipo_curso` text,
  `area_curso` text,
  `coordenador_curso` text,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Criação da tabela `cadastro`
CREATE TABLE `cadastro` (
  `usuario` text,
  `senha` text,
  `nome` text,
  `email` text,
  `perfil` text,
  `usuario_id` int NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`usuario_id`)
) ENGINE=InnoDB AUTO_INCREMENT=37 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Criação da tabela `pessoas`
CREATE TABLE `pessoas` (
  `id` int NOT NULL AUTO_INCREMENT,
  `perfil` text,
  `nome` text,
  `telefone` text,
  `email` text,
  `lattes` text,
  `matricula` text,
  `orientador` text,
  `instituicao` text,
  `uf_instituicao` text,
  `curso` text,
  `sigla_curso` text,
  `tipo_curso` text,
  `nivel_curso` text,
  `situacao_aluno_curso` text,
  `ano_ingresso` text,
  `ano_conclusao` text,
  `titulo_tcc` text,
  `tipo_tcc` text,
  `prazo_tcc` text,
  `prorrogacao_tcc` text,
  `situacao_tcc` text,
  `fase_pesquisa` text,
  `situacao_matricula` text,
  `grupo_pesquisa` text,
  `linha_pesquisa` text,
  `bolsa` text,
  `tipo_bolsa` text,
  `vinculo` text,
  `polo` text,
  `doc_compromisso` text,
  `via_tcc_entregue` text,
  `prazo_fase_pesquisa` text,
  `titulacao` text,
  `prazo_dias` int DEFAULT NULL,
  `prazo_situacao` text,
  `situacao_fase_pesquisa` text,
  `id_curso` int, -- Coluna para a chave estrangeira
  PRIMARY KEY (`id`),
  FOREIGN KEY (`id_curso`) REFERENCES `cursos`(`id`) -- Definindo a chave estrangeira
) ENGINE=InnoDB AUTO_INCREMENT=654 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Criação da tabela `prazos`
CREATE TABLE `prazos` (
  `id` int NOT NULL AUTO_INCREMENT,
  `id_pessoa` int DEFAULT NULL,
  `fase_pesquisa` text,
  `prazo_fase_pesquisa` text,
  `prazo_dias` int DEFAULT NULL,
  `prazo_situacao` text,
  `situacao_fase_pesquisa` text,
  PRIMARY KEY (`id`),
  FOREIGN KEY (`id_pessoa`) REFERENCES `pessoas`(`id`) -- Definindo a chave estrangeira
) ENGINE=InnoDB AUTO_INCREMENT=1564 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Criação da tabela `cursos_excluidos`
CREATE TABLE `cursos_excluidos` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nome_curso` text,
  `sigla_curso` text,
  `tipo_curso` text,
  `area_curso` text,
  `coordenador_curso` text,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Criação da tabela `pessoas_excluidas`
CREATE TABLE `pessoas_excluidas` (
  `id` int NOT NULL AUTO_INCREMENT,
  `perfil` text,
  `nome` text,
  `telefone` text,
  `email` text,
  `lattes` text,
  `matricula` text,
  `orientador` text,
  `instituicao` text,
  `uf_instituicao` text,
  `curso` text,
  `sigla_curso` text,
  `tipo_curso` text,
  `nivel_curso` text,
  `situacao_aluno_curso` text,
  `ano_ingresso` text,
  `ano_conclusao` text,
  `titulo_tcc` text,
  `tipo_tcc` text,
  `prazo_tcc` text,
  `prorrogacao_tcc` text,
  `situacao_tcc` text,
  `fase_pesquisa` text,
  `situacao_matricula` text,
  `grupo_pesquisa` text,
  `linha_pesquisa` text,
  `bolsa` text,
  `tipo_bolsa` text,
  `vinculo` text,
  `polo` text,
  `doc_compromisso` text,
  `via_tcc_entregue` text,
  `prazo_fase_pesquisa` text,
  `titulacao` text,
  `prazo_dias` int DEFAULT NULL,
  `prazo_situacao` text,
  `situacao_fase_pesquisa` text,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=654 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Criação da tabela `logs`
CREATE TABLE `logs` (
  `id` int NOT NULL AUTO_INCREMENT,
  `data_hora` text,
  `usuario` text,
  `acao` text,
  `detalhes` text,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2720 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
