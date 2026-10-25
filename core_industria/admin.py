from django.contrib import admin
from .models import Categoria, Fabricante, MovimentacaoEstoque, Peca

admin.site.register(Peca)
admin.site.register(Categoria)
admin.site.register(Fabricante)
admin.site.register(MovimentacaoEstoque)