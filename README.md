# Gestão de Estoque de Autopeças

Sistema web desenvolvido com **Python e Django** para gerenciar o estoque de peças automotivas, organizar categorias e fabricantes e registrar movimentações de entrada e saída.

## Funcionalidades

- Cadastro, edição, listagem e exclusão de peças, categorias e fabricantes;
- Registro de entradas e saídas com histórico das movimentações;
- Validação de quantidade disponível antes de baixar o estoque;
- Painel com indicadores de produtos, unidades em estoque e valor estimado de venda;
- Relatórios e identificação de peças com estoque baixo;
- Interface web responsiva.

## Tecnologias

- Python
- Django
- HTML, CSS e Bootstrap
- SQLite (ambiente local)

## Como executar localmente

1. Clone o repositório:

   ```bash
   git clone https://github.com/luisfelipe471/gestao-estoque-autopecas.git
   cd gestao-estoque-autopecas
   ```

2. Crie e ative um ambiente virtual:

   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

3. Instale as dependências:

   ```bash
   pip install -r requirements.txt
   ```

4. Configure as variáveis de ambiente. No PowerShell:

   ```powershell
   $env:DJANGO_SECRET_KEY = "substitua-por-uma-chave-segura"
   $env:DJANGO_DEBUG = "True"
   $env:DJANGO_ALLOWED_HOSTS = "127.0.0.1,localhost"
   ```

5. Crie as tabelas e execute o servidor:

   ```bash
   python manage.py migrate
   python manage.py runserver
   ```

Acesse `http://127.0.0.1:8000/`. O banco SQLite é criado localmente e **não faz parte do repositório**.

## Testes

```bash
python manage.py test
```

## Observações de segurança

Este repositório é uma demonstração acadêmica. Não coloque dados pessoais ou credenciais reais no banco de demonstração. Antes de hospedar publicamente o sistema para uso real, revise autenticação, permissões, configurações de produção e banco persistente.

## Autor

Desenvolvido por **Luis Felipe** — estudante de Desenvolvimento de Sistemas.
