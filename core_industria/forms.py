from django import forms
from .models import Peca, Categoria, Fabricante, MovimentacaoEstoque

# Criando um ModelFrom para simplificar o cadastro de Peças
class PecaForm(forms.ModelForm):
    class Meta:
        model = Peca
        fields = '__all__' # Inclui todos os campos do modelo no formulário

class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = '__all__'

class FabricanteForm(forms.ModelForm):
    class Meta:
        model = Fabricante
        fields = '__all__'


class MovimentacaoEstoqueForm(forms.ModelForm):
    class Meta:
        model = MovimentacaoEstoque
        fields = ('peca', 'tipo', 'quantidade', 'observacao')
        labels = {
            'peca': 'Peça',
            'tipo': 'Tipo de movimentação',
            'quantidade': 'Quantidade',
            'observacao': 'Observação',
        }
        widgets = {
            'observacao': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['peca'].queryset = Peca.objects.order_by('nome')
        self.fields['quantidade'].min_value = 1
        self.fields['observacao'].required = False