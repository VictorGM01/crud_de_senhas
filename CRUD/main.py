import sqlite3

from CRUD.excecoes import DelecaoInvalida


conexao = sqlite3.connect("Senhas.bd")
c = conexao.cursor()

# Cria tabela para armazenar o nome do programa e a senha
c.execute('CREATE TABLE IF NOT EXISTS dados (programa text primary key, senha text)')

# salva
conexao.commit()


# função para criar/inserir nova senha
def insere_valores(programa: str, senha: str):
    c.execute(f'INSERT INTO dados VALUES ("{programa}", "{senha}")')
    conexao.commit()


# função para excluir uma senha armazenada por meio do nome do programa
def exclui_valores(programa: str):
    c.execute('SELECT programa FROM dados')
    resultado = c.fetchall()

    resultados = []
    for res in resultado:
        resultados.append(res[0])

    if programa in resultados:
        c.execute(f'DELETE FROM dados WHERE programa = "{programa}"')
        conexao.commit()

    else:
        raise DelecaoInvalida('Não foi possível concluir a deleção')


# função para atualizar a senha por meio do nome do programa
def atualiza_valores(programa: str, nova_senha: str):
    try:
        c.execute(f'UPDATE dados SET senha = "{nova_senha}" WHERE programa = "{programa}"')
        conexao.commit()
    except sqlite3.Error as erro:
        print(erro)
