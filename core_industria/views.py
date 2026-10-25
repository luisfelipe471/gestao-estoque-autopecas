from decimal import Decimal

from django.db import transaction
from django.db.models.deletion import ProtectedError
from django.db.models import F, Sum
from django.shortcuts import get_object_or_404, render, redirect
from django.views.decorators.http import require_http_methods

from .forms import (
    CategoriaForm,
    FabricanteForm,
    MovimentacaoEstoqueForm,
    PecaForm,
)
from .models import Categoria, Fabricante, MovimentacaoEstoque, Peca

LOW_STOCK_THRESHOLD = 5

#View para index
def index(request):
    return render(request, 'index.html')


def painel(request):
    totais = Peca.objects.aggregate(
        unidades=Sum('quantidade_estoque'),
        valor_venda=Sum(F('preco_venda') * F('quantidade_estoque')),
    )
    pecas_baixo_estoque = Peca.objects.filter(
        quantidade_estoque__lte=LOW_STOCK_THRESHOLD
    ).select_related('categoria', 'fabricante')
    return render(request, 'painel.html', {
        'total_pecas': Peca.objects.count(),
        'total_categorias': Categoria.objects.count(),
        'total_fabricantes': Fabricante.objects.count(),
        'total_unidades': totais['unidades'] or 0,
        'valor_em_estoque': totais['valor_venda'] or Decimal('0.00'),
        'pecas_baixo_estoque': pecas_baixo_estoque[:5],
        'movimentacoes': MovimentacaoEstoque.objects.select_related('peca')[:5],
        'limite_estoque_baixo': LOW_STOCK_THRESHOLD,
    })


def relatorio_estoque(request):
    pecas_baixo_estoque = Peca.objects.filter(
        quantidade_estoque__lte=LOW_STOCK_THRESHOLD
    ).select_related('categoria', 'fabricante')
    return render(request, 'relatorio_estoque.html', {
        'pecas': pecas_baixo_estoque,
        'limite_estoque_baixo': LOW_STOCK_THRESHOLD,
        'total_sem_estoque': pecas_baixo_estoque.filter(quantidade_estoque=0).count(),
    })


def listar_pecas(request):
    pecas = Peca.objects.select_related('categoria', 'fabricante')
    return render(request, 'peca_list.html', {'pecas': pecas})


def detalhe_peca(request, pk):
    peca = get_object_or_404(
        Peca.objects.select_related('categoria', 'fabricante'),
        pk=pk,
    )
    return render(request, 'peca_detail.html', {
        'peca': peca,
        'movimentacoes': peca.movimentacoes.all()[:10],
    })


def cadastrar_peca(request):
    if request.method == 'POST':
        form = PecaForm(request.POST)
        if form.is_valid():
            form.save() # Salva no banco
            return redirect('listar_pecas') # Redireciona para a lista
    else:
        form = PecaForm()
    return render(request, 'peca_form.html', {'form': form})

def editar_peca(request, pk):
    peca = get_object_or_404(Peca, pk=pk)
    if request.method == 'POST':
        form = PecaForm(request.POST, instance=peca)
        if form.is_valid():
            form.save()
            return redirect('listar_pecas')
    else:
        form = PecaForm(instance=peca)
    return render(request, 'peca_form.html', {'form': form})

@require_http_methods(['GET', 'POST'])
def excluir_peca(request, pk):
    peca = get_object_or_404(Peca, pk=pk)
    if request.method == 'POST':
        peca.delete()
        return redirect('listar_pecas')
    return render(request, 'peca_confirm_delete.html', {'peca': peca})

def listar_categorias(request):
    categorias = Categoria.objects.all()
    return render(request, 'categoria_list.html', {'categorias': categorias})

def cadastrar_categoria(request):
    if request.method == 'POST':
        form = CategoriaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_categorias')
    else:
        form = CategoriaForm()
    return render(request, 'categoria_form.html', {'form': form})

def editar_categoria(request, pk):
    categoria = get_object_or_404(Categoria, pk=pk)
    if request.method == 'POST':
        form = CategoriaForm(request.POST, instance=categoria)
        if form.is_valid():
            form.save()
            return redirect('listar_categorias')
    else:
        form = CategoriaForm(instance=categoria)
    return render(request, 'categoria_form.html', {'form': form})

@require_http_methods(['GET', 'POST'])
def excluir_categoria(request, pk):
    categoria = get_object_or_404(Categoria, pk=pk)
    pecas_vinculadas = categoria.pecas.count()
    exclusao_bloqueada = False
    if request.method == 'POST':
        try:
            categoria.delete()
        except ProtectedError:
            exclusao_bloqueada = True
            pecas_vinculadas = categoria.pecas.count()
        else:
            return redirect('listar_categorias')
    return render(request, 'categoria_confirm_delete.html', {
        'categoria': categoria,
        'pecas_vinculadas': pecas_vinculadas,
        'exclusao_bloqueada': exclusao_bloqueada,
    }, status=409 if exclusao_bloqueada else 200)

def listar_fabricante(request):
    fabricantes = Fabricante.objects.all()
    return render(request, 'fabricante_list.html', {'fabricantes': fabricantes})

def cadastrar_fabricante(request):
    if request.method == 'POST':
        form = FabricanteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_fabricantes')
    else:
        form = FabricanteForm()
    return render(request, 'fabricante_form.html', {'form': form})

def editar_fabricante(request, pk):
    fabricante = get_object_or_404(Fabricante, pk=pk)
    if request.method == 'POST':
        form = FabricanteForm(request.POST, instance=fabricante)
        if form.is_valid():
            form.save()
            return redirect('listar_fabricantes')
    else:
        form = FabricanteForm(instance=fabricante)
    return render(request, 'fabricante_form.html', {'form': form})

@require_http_methods(['GET', 'POST'])
def excluir_fabricante(request, pk):
    fabricante = get_object_or_404(Fabricante, pk=pk)
    pecas_vinculadas = fabricante.pecas.count()
    exclusao_bloqueada = False
    if request.method == 'POST':
        try:
            fabricante.delete()
        except ProtectedError:
            exclusao_bloqueada = True
            pecas_vinculadas = fabricante.pecas.count()
        else:
            return redirect('listar_fabricantes')
    return render(request, 'fabricante_confirm_delete.html', {
        'fabricante': fabricante,
        'pecas_vinculadas': pecas_vinculadas,
        'exclusao_bloqueada': exclusao_bloqueada,
    }, status=409 if exclusao_bloqueada else 200)


def movimentacoes_estoque(request):
    if request.method == 'POST':
        form = MovimentacaoEstoqueForm(request.POST)
        if form.is_valid():
            movimentacao = form.save(commit=False)
            peca = movimentacao.peca
            alteracao = movimentacao.quantidade
            if movimentacao.tipo == MovimentacaoEstoque.Tipo.SAIDA:
                alteracao = -alteracao

            with transaction.atomic():
                estoque = Peca.objects.filter(pk=peca.pk)
                if alteracao < 0:
                    estoque = estoque.filter(quantidade_estoque__gte=-alteracao)
                atualizadas = estoque.update(
                    quantidade_estoque=F('quantidade_estoque') + alteracao
                )
                if not atualizadas:
                    form.add_error(
                        None,
                        'Não há estoque suficiente para registrar essa saída.',
                    )
                else:
                    movimentacao.nome_peca = peca.nome
                    movimentacao.sku_peca = peca.sku
                    movimentacao.save()
                    return redirect('movimentacoes_estoque')
    else:
        form = MovimentacaoEstoqueForm()

    movimentacoes = MovimentacaoEstoque.objects.select_related('peca')
    return render(request, 'movimentacoes_estoque.html', {
        'form': form,
        'movimentacoes': movimentacoes[:30],
    })