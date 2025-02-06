# Projeto E-Commerce

Repositório criado com intuito de estudar tecnologias como Python, Django, HTML E CSS.

## Requisitos

Antes de iniciar, certifique-se de ter instalado:
- Python 3.x
- Git
- Virtualenv

## Tecnologias Utilizadas

O projeto utiliza as seguintes tecnologias e frameworks:
- **Django** - Framework web em Python para desenvolvimento do backend.
- **Django REST Framework** - Para criação de APIs RESTful.
- **SQLite** - Banco de dados padrão do Django.
- **Bootstrap** - Framework CSS para estilização das páginas.
- **JavaScript e jQuery** - Para interatividade no frontend.
- **HTML e CSS** - Para estruturação e design das páginas.

## Instalação e Execução

Siga os passos abaixo para clonar e rodar o projeto em sua máquina local:

```sh
# Clone o repositório
git clone https://github.com/vitorgsantoss/e-commerce.git

# Acesse o diretório do projeto
cd e-commerce

# Instale as dependências
pip install -r requirements.txt

# Aplique as migrações do banco de dados
python manage.py migrate

# Inicie o servidor de desenvolvimento
python manage.py runserver
```

Após rodar o servidor, o projeto estará disponível em: `http://127.0.0.1:8000/`

## Estrutura do Projeto

- `ecommerce/` - Diretório principal do projeto Django.
- `manage.py` - Script para gerenciar o projeto.
- `requirements.txt` - Lista de dependências do projeto.
- `loja` - Diretório de configuração do projeto.
- `pedido` -  App para gerenciamento de pedidos.
- `perfil` -  App para gerenciamento de perfis.
- `produto` -  App para gerenciamento de produtos.
- `templates` -  Diretório onde constam todos os templates e arquivos estáticos da aplicação.


## Contribuição

Sinta-se à vontade para sugerir melhorias e novas funcionalidades através do e-mail: vitor.santos800411@gmail.com

