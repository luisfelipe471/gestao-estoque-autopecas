from datetime import date

from django.test import TestCase
from django.urls import reverse

from .forms import MovimentacaoEstoqueForm, PecaForm
from .models import Categoria, Fabricante, MovimentacaoEstoque, Peca


class EstoqueViewsTests(TestCase):
    def setUp(self):
        self.categoria = Categoria.objects.create(
            nome='Freios',
            codigo_setor='FR',
        )
        self.fabricante = Fabricante.objects.create(
            nome_empresa='Bosch',
            pais_origem='Brasil',
        )
        self.peca = Peca.objects.create(
            nome='Pastilha de freio',
            sku='PA-101',
            preco_custo='40.00',
            preco_venda='90.00',
            quantidade_estoque=4,
            data_fabricacao=date(2026, 1, 1),
            categoria=self.categoria,
            fabricante=self.fabricante,
        )

    def test_painel_e_relatorio_exibem_pecas_com_estoque_baixo(self):
        painel = self.client.get(reverse('painel'))
        relatorio = self.client.get(reverse('relatorio_estoque'))

        self.assertContains(painel, 'Painel de gestão')
        self.assertContains(painel, 'Pastilha de freio')
        self.assertContains(relatorio, 'Relatório de estoque baixo')
        self.assertContains(relatorio, 'Pastilha de freio')

    def test_detalhe_da_peca_exibe_informacoes_e_historico(self):
        response = self.client.get(reverse('detalhe_peca', args=[self.peca.pk]))

        self.assertContains(response, 'PA-101')
        self.assertContains(response, 'R$ 90,00')
        self.assertContains(response, 'Histórico de movimentações')

    def test_entrada_atualiza_saldo_e_registra_historico(self):
        response = self.client.post(reverse('movimentacoes_estoque'), {
            'peca': self.peca.pk,
            'tipo': MovimentacaoEstoque.Tipo.ENTRADA,
            'quantidade': 3,
            'observacao': 'Reposição',
        })

        self.peca.refresh_from_db()
        self.assertRedirects(response, reverse('movimentacoes_estoque'))
        self.assertEqual(self.peca.quantidade_estoque, 7)
        self.assertEqual(MovimentacaoEstoque.objects.get().nome_peca, 'Pastilha de freio')

    def test_saida_atualiza_saldo_e_registra_historico(self):
        response = self.client.post(reverse('movimentacoes_estoque'), {
            'peca': self.peca.pk,
            'tipo': MovimentacaoEstoque.Tipo.SAIDA,
            'quantidade': 2,
            'observacao': 'Venda',
        })

        self.peca.refresh_from_db()
        self.assertRedirects(response, reverse('movimentacoes_estoque'))
        self.assertEqual(self.peca.quantidade_estoque, 2)
        self.assertEqual(
            MovimentacaoEstoque.objects.get().tipo,
            MovimentacaoEstoque.Tipo.SAIDA,
        )

    def test_saida_nao_pode_deixar_estoque_negativo(self):
        response = self.client.post(reverse('movimentacoes_estoque'), {
            'peca': self.peca.pk,
            'tipo': MovimentacaoEstoque.Tipo.SAIDA,
            'quantidade': 5,
            'observacao': '',
        })

        self.peca.refresh_from_db()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.peca.quantidade_estoque, 4)
        self.assertEqual(MovimentacaoEstoque.objects.count(), 0)
        self.assertContains(response, 'Não há estoque suficiente')

    def test_formulario_rejeita_preco_negativo(self):
        form = PecaForm(data={
            'nome': 'Filtro de óleo',
            'sku': 'FO-202',
            'preco_custo': '-1.00',
            'preco_venda': '10.00',
            'quantidade_estoque': 1,
            'data_fabricacao': '2026-01-01',
            'categoria': self.categoria.pk,
            'fabricante': self.fabricante.pk,
        })

        self.assertFalse(form.is_valid())
        self.assertIn('preco_custo', form.errors)
        self.assertEqual(Peca.objects.count(), 1)

    def test_formulario_rejeita_movimentacao_com_quantidade_zero(self):
        form = MovimentacaoEstoqueForm(data={
            'peca': self.peca.pk,
            'tipo': MovimentacaoEstoque.Tipo.ENTRADA,
            'quantidade': 0,
            'observacao': '',
        })

        self.assertFalse(form.is_valid())
        self.assertIn('quantidade', form.errors)

    def test_exclusao_de_categoria_com_pecas_e_bloqueada(self):
        url = reverse('excluir_categoria', args=[self.categoria.pk])

        resposta_metodo_nao_permitido = self.client.delete(url)
        response = self.client.post(url)

        self.assertEqual(resposta_metodo_nao_permitido.status_code, 405)
        self.assertTrue(Categoria.objects.filter(pk=self.categoria.pk).exists())
        self.assertEqual(response.status_code, 409)
        self.assertContains(response, 'não pode ser excluída', status_code=409)
        self.assertTrue(Categoria.objects.filter(pk=self.categoria.pk).exists())
        self.assertTrue(Peca.objects.filter(pk=self.peca.pk).exists())

    def test_exclusao_de_fabricante_com_pecas_e_bloqueada(self):
        url = reverse('excluir_fabricante', args=[self.fabricante.pk])

        response = self.client.post(url)

        self.assertEqual(response.status_code, 409)
        self.assertContains(response, 'não pode ser excluído', status_code=409)
        self.assertTrue(Fabricante.objects.filter(pk=self.fabricante.pk).exists())
        self.assertTrue(Peca.objects.filter(pk=self.peca.pk).exists())

    def test_exclusao_de_categoria_e_fabricante_sem_pecas_funciona(self):
        self.peca.delete()

        resposta_categoria = self.client.post(
            reverse('excluir_categoria', args=[self.categoria.pk]),
        )
        resposta_fabricante = self.client.post(
            reverse('excluir_fabricante', args=[self.fabricante.pk]),
        )

        self.assertRedirects(resposta_categoria, reverse('listar_categorias'))
        self.assertRedirects(resposta_fabricante, reverse('listar_fabricantes'))
        self.assertFalse(Categoria.objects.filter(pk=self.categoria.pk).exists())
        self.assertFalse(Fabricante.objects.filter(pk=self.fabricante.pk).exists())

    def test_exclusao_de_peca_preserva_historico_de_movimentacao(self):
        movimentacao = MovimentacaoEstoque.objects.create(
            peca=self.peca,
            nome_peca=self.peca.nome,
            sku_peca=self.peca.sku,
            tipo=MovimentacaoEstoque.Tipo.ENTRADA,
            quantidade=1,
        )

        response = self.client.post(
            reverse('excluir_peca', args=[self.peca.pk]),
        )

        movimentacao.refresh_from_db()
        self.assertRedirects(response, reverse('listar_pecas'))
        self.assertIsNone(movimentacao.peca)
        self.assertEqual(movimentacao.nome_peca, 'Pastilha de freio')

    def test_edicao_de_peca_inexistente_retorna_404(self):
        response = self.client.get(reverse('editar_peca', args=[9999]))

        self.assertEqual(response.status_code, 404)
