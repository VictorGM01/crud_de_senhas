import sqlite3
from cryptography.fernet import Fernet

from CRUD.excecoes import DelecaoInvalida


conexao = sqlite3.connect("Senhas.bd")
c = conexao.cursor()


def criptografa_file():
    with open(
            r'C:\Users\victo\PycharmProjects\cybersecurity\criptografia\criptografar_arquivo\chave_simetrica.txt', 'rb'
    ) as f:
        cr = f.read()

    f = Fernet(cr)

    with open('Senhas.bd', 'rb') as arquivo:
        arquivo_original = arquivo.read()

    with open('Senhas.bd', 'wb') as cript:
        cript.write(f.encrypt(arquivo_original))


def descriptografa_file():
    with open(
            r'C:\Users\victo\PycharmProjects\cybersecurity\criptografia\criptografar_arquivo\chave_simetrica.txt', 'rb'
    ) as f:
        cr = f.read()

    f = Fernet(cr)

    with open('Senhas.bd', 'rb') as arquivo:
        criptografado = arquivo.read()

    with open('Senhas.bd', 'wb') as cript:
        cript.write(f.decrypt(criptografado))


# Cria tabela para armazenar informações do usuário
try:
    c.execute('CREATE TABLE IF NOT EXISTS usuario (nome_user text PRIMARY KEY, senha_user text)')
    conexao.commit()
except sqlite3.Error:
    print(f'Erro: {sqlite3.Error}')

# Cria tabela para armazenar o nome do programa e a senha
try:
    c.execute('''CREATE TABLE IF NOT EXISTS dados (nome_usuario text, programa text primary key, senha text,
    CONSTRAINT fk_usuario FOREIGN KEY(nome_usuario) REFERENCES usuario(nome_user))''')
    conexao.commit()
except sqlite3.Error:
    print(f'Erro: {sqlite3.Error}')


# função para criar novo usuário (útil para a GUI)
def cria_usuario(nome: str, senha: str):
    try:
        c.execute(f'INSERT INTO usuario VALUES ("{nome}", "{senha}")')
        conexao.commit()
    except sqlite3.Error as erro_sql:
        print(f'Não foi possível criar o usuário. Erro: {erro_sql}')


# função para mudança de senha do usuário
def atualiza_senha_usuario(nome: str, nova_senha: str):
    try:
        c.execute(f'UPDATE usuario SET senha_user = "{nova_senha}" WHERE nome_user = "{nome}"')
        conexao.commit()
    except sqlite3.Error:
        print(f'Erro: {sqlite3.Error}')


# função para criar/inserir nova senha
def insere_valores(usuario: str, programa: str, senha: str):
    c.execute('SELECT programa FROM dados')
    programas = c.fetchall()

    lista_de_programas = []
    for i in programas:
        lista_de_programas.append(i[0])

    if programa not in lista_de_programas:
        c.execute(f'INSERT INTO dados VALUES ("{usuario}", "{programa}", "{senha}")')
        conexao.commit()
        print('Senha cadastrada com sucesso')

    else:
        print(f'A senha para "{programa}" já está cadastrada!')


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
        print('Exclusão realizada')

    else:
        raise DelecaoInvalida('Não foi possível concluir a deleção')


# função para atualizar a senha por meio do nome do programa
def atualiza_valores(programa: str, nova_senha: str):
    try:
        c.execute(f'UPDATE dados SET senha = "{nova_senha}" WHERE programa = "{programa}"')
        conexao.commit()
    except sqlite3.Error:
        print(f'Erro: {sqlite3.Error}')


# função que possibilita a viisualização da senha do programa informado
def leitura_de_valores_especificos(programa: str):
    try:
        c.execute(f'SELECT senha FROM dados WHERE programa = "{programa}"')
        resultado = c.fetchall()
        print(resultado[0][0])

    except sqlite3.Error:
        print(f'Erro: {sqlite3.Error}')


# função que retorna todos os dados armazenados no banco de dados
def leitura_de_todas_as_senhas():
    try:
        c.execute('SELECT * FROM dados')
        resultado = c.fetchall()

        for dados in resultado:
            print(f'Programa: {dados[1]} - Senha: {dados[2]}')

    except sqlite3.Error:
        print(f'Erro: {sqlite3.Error}')


# Acesso ao banco
def acessar_banco():
    print('''Opções:
    1) Cadastrar usuário
    2) Acessar banco de dados''')

    escolha = int(input('Opção escolhida: '))

    if escolha == 1:
        nome = input('Digite o nome do usuário: ')
        senha = input('Digite sua senha: ')

        cria_usuario(nome, senha)

        print('Usuário cadastrado!')

    elif escolha == 2:
        nome = input('Digite o nome do seu usuário: ')
        senha = input('Digite a sua senha: ')

        c.execute(f'SELECT nome_user FROM usuario WHERE nome_user = "{nome}"')
        nome_bd = c.fetchall()

        if len(nome_bd) == 0:
            print('\033[91m' + 'Acesso negado - Usuário não cadastrado')

        elif nome == nome_bd[0][0]:
            c.execute(f'SELECT senha_user FROM usuario WHERE nome_user = "{nome}"')
            senha_bd = c.fetchall()

            if senha == senha_bd[0][0]:
                while True:
                    print('*******************************************************************************************')
                    print('1) Inserir valores')
                    print('2) Excluir valores')
                    print('3) Atualizar valores')
                    print('4) Acessar informações')
                    print('5) Fechar')

                    opcao = int(input('Opção escolhida: '))

                    if opcao == 1:
                        programa = input('Insira o nome do programa/software: ')
                        senha = input('Insira a senha do respectivo programa/software: ')
                        insere_valores(nome, programa, senha)
                        sair_continuar = int(input('1) Sair / 2) Continuar navegando: '))
                        if sair_continuar == 1:
                            break
                        elif sair_continuar == 2:
                            continue

                    elif opcao == 2:
                        programa = input('Insira o nome do programa/software: ')
                        exclui_valores(programa)
                        sair_continuar = int(input('1) Sair / 2) Continuar navegando: '))
                        if sair_continuar == 1:
                            break
                        elif sair_continuar == 2:
                            continue

                    elif opcao == 3:
                        programa = input('Insira o nome do programa/software: ')
                        nova_senha = input('Digite a nova senha para atualização: ')
                        atualiza_valores(programa, nova_senha)
                        sair_continuar = int(input('1) Sair / 2) Continuar navegando: '))
                        if sair_continuar == 1:
                            break
                        elif sair_continuar == 2:
                            continue

                    elif opcao == 4:
                        print('1) Ler senha específica / 2) Ler todas as senhas salvas')
                        opcao_escolhida = int(input('Resposta: '))
                        if opcao_escolhida == 1:
                            programa = input('Insira o nome do programa/software: ')
                            leitura_de_valores_especificos(programa)
                            sair_continuar = int(input('1) Sair / 2) Continuar navegando: '))
                            if sair_continuar == 1:
                                break
                            elif sair_continuar == 2:
                                continue

                        elif opcao_escolhida == 2:
                            leitura_de_todas_as_senhas()

                            sair_continuar = int(input('1) Sair / 2) Continuar navegando: '))
                            if sair_continuar == 1:
                                break
                            elif sair_continuar == 2:
                                continue

            else:
                print('\033[91m' + 'Acessso Negado - Senha incorreta!')


acessar_banco()