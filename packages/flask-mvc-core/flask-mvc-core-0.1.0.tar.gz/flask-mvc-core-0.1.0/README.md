# Flask MVC Core

**Flask MVC Core** é uma extensão para o framework Flask que facilita a implementação da arquitetura MVC (Model-View-Controller) em suas aplicações. Ele permite a definição modular de rotas e facilita o carregamento dinâmico de controllers, proporcionando uma estrutura mais limpa e escalável para seus projetos Flask.

## Recursos

- **Arquitetura MVC**: Separação clara entre modelo, visão e controlador.
- **Roteamento Modular**: Permite o registro de rotas por meio de decorators personalizados.
- **Carregamento Dinâmico de Controllers**: Carregamento automático dos controllers com base na estrutura de diretórios.
- **Suporte a vários métodos HTTP**: Suporta GET, POST, PUT, DELETE, PATCH, OPTIONS, HEAD, e TRACE.
- **Integração com Waitress**: Para servir a aplicação em produção.

## Instalação

Você pode instalar o `flask-mvc-core` diretamente do PyPI:

```bash
pip install flask-mvc-core
```

Se preferir, pode instalar a partir do código-fonte:

1. Clone o repositório:

   ```bash
   git clone https://github.com/seuusuario/flask-mvc-core.git
   cd flask-mvc-core
   ```

2. Instale o pacote:

   ```bash
   pip install .
   ```

## Como Usar

Aqui está um exemplo simples de como usar o `FlaskMVC` em sua aplicação.

### Estrutura de Diretórios

Sua aplicação pode ser estruturada da seguinte forma:

```
myapp/
├── app/
│   ├── controllers/
│   │   ├── home_controller.py
│   │   └── outro_controller.py
│   ├── views/
│   └── models/
├── routes/
│   └── __init__.py
│   └── web.py
├── main.py
└── requirements.txt
```

### 1. Definindo o `main.py`

No arquivo `main.py`, você irá configurar a aplicação FlaskMVC e registrar as rotas:

```python
from waitress import serve
from flask_mvc_core import FlaskMVC, Register
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

# Criando a instância da aplicação FlaskMVC
app = FlaskMVC(__name__)

# Registrando as rotas definidas em 'routes/web.py'
Register.routes(app)

if __name__ == "__main__":
    # Servindo a aplicação usando Waitress
    serve(app, host="localhost", port=80, _quiet=True)
```

### 2. Definindo as Rotas em `routes/web.py`

No arquivo `routes/web.py`, você define as rotas da sua aplicação. A biblioteca `flask-mvc-core` permite que você registre rotas com uma sintaxe simples e modular.

```python
from flask_mvc_core.register import register

@register
def web(app):
    # Definindo uma rota GET para a página inicial
    app.get("/", "HomeController@index")

    # Definindo uma rota POST
    app.post("/submit", "FormController@submit")
```

### 3. Criando um Controller

Agora, crie um controller que será chamado para processar as rotas. Por exemplo, para a rota `"/"`, o controller seria `HomeController`.

Crie o arquivo `app/controllers/home_controller.py`:

```python
from flask_mvc_core import Request, Response

class HomeController:
    def index(self, request: Request, response: Response):
        # Retornando uma resposta simples
        return response.json({"message": "Bem-vindo à aplicação Flask MVC!"})
```

Neste exemplo, o método `index` da classe `HomeController` será executado quando a rota `"HomeController@index"` for acessada.

### 4. Criando o Controller com Métodos Diferentes

Você também pode definir controllers com outros métodos para manipular diferentes tipos de requisições:

```python
class FormController:
    def submit(self, request: Request, response: Response):
        # Processa os dados do formulário
        form_data = request.json
        return response.json({"status": "sucesso", "data": form_data})
```

### 5. Rodando a Aplicação

Com tudo configurado, basta rodar a aplicação com o seguinte comando:

```bash
python main.py
```

Isso irá iniciar a aplicação no endereço `http://localhost` e você poderá acessar as rotas definidas.

## Como Funciona

### `FlaskMVC`

A classe `FlaskMVC` estende o Flask e adiciona funcionalidades específicas para o padrão MVC:

- **Prefixos de Rota**: O método `prefix` permite adicionar prefixos e caminhos às suas rotas.
- **Métodos HTTP**: Métodos como `get`, `post`, `put`, `delete`, etc., são usados para registrar as rotas de acordo com o método HTTP.
- **Carregamento Dinâmico de Controllers**: Os controllers são carregados dinamicamente a partir do diretório correto com base na estrutura de pastas e nomes de classes.

### `Register`

O decorador `@register` é usado para registrar as rotas dentro de um arquivo específico. Você pode criar arquivos como `routes/web.py` para manter suas rotas organizadas.

## Exemplos de Uso

### Exemplo 1: Rota Simples

```python
@app.get("/hello", "HelloController@index")
```

### Exemplo 2: Rota com parâmetros

```python
@app.get("/user/<int:id>", "UserController@show")
```

### Exemplo 3: Definindo métodos POST

```python
@app.post("/login", "AuthController@login")
```

## Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](LICENSE) para mais detalhes.
