from django.contrib import admin
from django.urls import path
from core_industria import views

urlpatterns = [
    # Url para a página inicial
    path('', views.index, name='index'),
    path('painel/', views.painel, name='painel'),
    path('relatorios/estoque/', views.relatorio_estoque, name='relatorio_estoque'),
    path('movimentacoes/', views.movimentacoes_estoque, name='movimentacoes_estoque'),
    # Urls para Peças
    path('pecas/', views.listar_pecas, name='listar_pecas'),
    path('pecas/cadastrar/', views.cadastrar_peca, name='cadastrar_peca'),
    path('pecas/<int:pk>/', views.detalhe_peca, name='detalhe_peca'),
    path('pecas/<int:pk>/editar/', views.editar_peca, name='editar_peca'),
    path('pecas/<int:pk>/excluir/', views.excluir_peca, name='excluir_peca'),
    # Urls para Categorias
    path('categorias/', views.listar_categorias, name='listar_categorias'),
    path('categorias/cadastrar/', views.cadastrar_categoria, name='cadastrar_categoria'),
    path('categorias/<int:pk>/editar/', views.editar_categoria, name='editar_categoria'),
    path('categorias/<int:pk>/excluir/', views.excluir_categoria, name='excluir_categoria'),
    # Urls para Fabricantes
    path('fabricantes/', views.listar_fabricante, name='listar_fabricantes'),
    path('fabricantes/cadastrar/', views.cadastrar_fabricante, name='cadastrar_fabricante'),
    path('fabricantes/<int:pk>/editar/', views.editar_fabricante, name='editar_fabricante'),
    path('fabricantes/<int:pk>/excluir/', views.excluir_fabricante, name='excluir_fabricante')
]