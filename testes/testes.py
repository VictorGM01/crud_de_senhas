from unittest import TestCase

from CRUD.main import insere_valores, exclui_valores, atualiza_valores, leitura_de_valores_especificos, \
    leitura_de_todas_as_senhas, cria_usuario
from CRUD.excecoes import DelecaoInvalida


class TesteCrud(TestCase):

    # define cenário de testes
    def setUp(self) -> None:
        self.senha = "123456789"
        self.programa = "github"

    def test_deve_permitir_criar_novo_usuario(self):
        cria_usuario('Teste', 'abcdefjh')

    def test_deve_inserir_uma_nova_senha_quando_a_funcao_insere_valores_for_chamada(self):
        insere_valores('Victor', self.programa, self.senha)
        insere_valores('Victor', self.programa, self.senha)
        insere_valores('Victor', 'Facebook', '123456')

    def test_deve_excluir_uma_senha_quando_a_funcao_exclui_valores_for_chamada(self):
        exclui_valores(self.programa)

    def test_nao_deve_permitir_delecao_quando_o_programa_nao_for_encontrado(self):
        with self.assertRaises(DelecaoInvalida):
            exclui_valores('SATURNO')
            exclui_valores(3)

    def test_deve_permitir_atualizacao_de_senha_quando_a_funcao_atualiza_valores_for_chamada(self):
        atualiza_valores(self.programa, '141598')

    def test_deve_permitir_visualizar_uma_senha_por_meio_do_nome_de_um_programa_no_banco(self):
        leitura_de_valores_especificos('Facebook')

    def test_deve_retornar_todas_as_senhas_armazenadas(self):
        leitura_de_todas_as_senhas()
