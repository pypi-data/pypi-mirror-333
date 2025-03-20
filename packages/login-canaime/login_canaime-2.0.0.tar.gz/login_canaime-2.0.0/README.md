# login-canaime

Biblioteca para autenticação no sistema Canaimé e manipulação da página logada.

## Instalação

```bash
pip install login-canaime
```

## Uso como biblioteca

A biblioteca `login-canaime` oferece duas funcionalidades principais:

### 1. Obter apenas as credenciais

```python
from login_canaime import Login

# Criar uma instância da classe Login
login = Login()

# Obter apenas as credenciais
usuario, senha = login.obter_credenciais()

if usuario and senha:
    print(f"Login bem-sucedido! Usuário: {usuario}")
    
    # Usar as credenciais em outro sistema
    # outro_sistema.login(usuario, senha)
```

### 2. Obter e manipular a página logada

```python
from login_canaime import Login
import time

# Criar uma instância da classe Login
login = Login()

# Obter a página logada
page = login.obter_pagina(headless=False)

if page:
    try:
        print(f"Login realizado como: {login.usuario}")
        
        # Manipular a página com Playwright
        print(f"Título da página: {page.title()}")
        
        # Capturar screenshot
        page.screenshot(path="screenshot.png")
        
        # Navegar para outra página
        page.goto("https://www.google.com")
        
        # Aguardar visualização
        time.sleep(5)
        
    finally:
        # Sempre feche o navegador ao terminar
        login.fechar()
```

### 3. Uso com gerenciador de contexto

```python
from login_canaime import Login
import time

# Usando com o gerenciador de contexto 'with'
with Login() as login:
    # Obter a página logada
    page = login.obter_pagina()
    
    if page:
        print(f"Título da página: {page.title()}")
        
        # Fazer operações...
        
        # Aguardar visualização
        time.sleep(5)
    
# O navegador será fechado automaticamente ao sair do bloco 'with'
```

## Autenticadores alternativos

A biblioteca suporta diferentes métodos de autenticação:

```python
from login_canaime import Login, AutenticadorArgs, AutenticadorEnv

# 1. Usando credenciais em argumentos
auth_args = AutenticadorArgs()
login1 = Login(autenticador=auth_args)
page = login1.obter_pagina(usuario="usuario_exemplo", senha="senha_exemplo")

# 2. Usando variáveis de ambiente (CANAIME_USUARIO e CANAIME_SENHA)
auth_env = AutenticadorEnv()
login2 = Login(autenticador=auth_env)
page = login2.obter_pagina()
```

## Licença

MIT 