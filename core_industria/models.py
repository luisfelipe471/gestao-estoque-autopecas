from django.core.validators import MinValueValidator
from django.db import models

class Categoria(models.Model):
    # CharField para textos curtos. Max_length é obrigatório.
    nome = models.CharField(max_length=100)
    codigo_setor = models.CharField(max_length=20, unique=True)
    # Textfield para textos longos. blank=True e null=True permitem que o campo seja opcional.
    descricao = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.nome} ({self.codigo_setor})"
    
class Fabricante(models.Model):
    nome_empresa = models.CharField(max_length=150)
    pais_origem = models.CharField(max_length=100)
    site_oficial = models.URLField(blank=True, null=True) # Valida URLs automaticamente
    
    def __str__(self):
        return self.nome_empresa

class Peca(models.Model):
    nome = models.CharField(max_length=150)
    sku = models.CharField(max_length=50, unique=True)
    preco_custo = models.DecimalField(
        decimal_places=2,
        max_digits=10,
        validators=[MinValueValidator(0)],
    )
    preco_venda = models.DecimalField(
        decimal_places=2,
        max_digits=10,
        validators=[MinValueValidator(0)],
    )
    quantidade_estoque = models.PositiveIntegerField(default=0)
    data_fabricacao = models.DateField()
    # Relacinamentos (Chaves Estrangeiras)
    categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT, related_name='pecas')
    fabricante = models.ForeignKey(Fabricante, on_delete=models.PROTECT, related_name='pecas')
    
    def __str__(self):
        return f"{self.nome} - SKU: {self.sku}"

class MovimentacaoEstoque(models.Model):
    class Tipo(models.TextChoices):
        ENTRADA = 'entrada', 'Entrada'
        SAIDA = 'saida', 'Saída'

    peca = models.ForeignKey(
        Peca,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='movimentacoes',
    )
    nome_peca = models.CharField(max_length=150)
    sku_peca = models.CharField(max_length=50)
    tipo = models.CharField(max_length=7, choices=Tipo.choices)
    quantidade = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    observacao = models.CharField(max_length=250, blank=True)
    criada_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-criada_em', '-pk']
        verbose_name = 'movimentação de estoque'
        verbose_name_plural = 'movimentações de estoque'

    def __str__(self):
        return f'{self.get_tipo_display()} de {self.quantidade} un. - {self.nome_peca}'