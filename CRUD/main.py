import sqlite3


conexao = sqlite3.connect("Senhas.bd")
c = conexao.cursor()

# Cria tabela para armazenar o nome do programa e a senha
c.execute('CREATE TABLE IF NOT EXISTS dados (programa text, senha text)')

# salva
conexao.commit()