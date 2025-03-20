# Login Canaimé

**Login Canaimé** é uma biblioteca Python que fornece uma interface gráfica moderna para realizar o login no Sistema Canaimé, um sistema desenvolvido para gerenciar unidades prisionais e facilitar o controle de dados de reeducandos, dados administrativos, visitantes e acesso em tempo real a informações para órgãos como a Justiça, Defensoria Pública e Ministério Público.

A biblioteca integra o **Model**, **View** e **Controller** para fornecer um fluxo de login robusto e reutilizável. Além disso, ela utiliza o **PySide6** para a interface gráfica e o **Playwright** para automatizar o processo de login, permitindo a execução em modo headless (para produção) ou não-headless (para testes).

## Instalação

### Via pip

```bash
pip install login-canaime
```

Após a instalação, instale também os navegadores necessários para o Playwright:

```bash
playwright install
```

## Como usar

### Como Biblioteca em Seu Código

#### API Síncrona (modo padrão)

```python
# Método 1: Obter a página logada para automação
import asyncio
from loginCanaime import Login

# Obter a página já logada para automação com Playwright (método síncrono)
page = Login.get_page(test_mode=False)

# Agora você pode usar a página para navegar e automatizar tarefas
async def run_operations():
    if page:
        # Use a API assíncrona do Playwright
        await page.goto("https://canaime.com.br/sgp2rr/areas/unidades/alguma_pagina.php")
        # Realize suas operações...
    
    # Quando terminar, limpe os recursos
    Login.cleanup()

# Execute a função assíncrona
asyncio.run(run_operations())
```

```python
# Método 2: Apenas obter as credenciais (útil para desenvolvimento)
from loginCanaime import Login

credentials = Login.get_credentials(test_mode=False)
if credentials:
    print(f"Usuário: {credentials['username']}")
    print(f"Senha: {credentials['password']}")

# Limpe os recursos quando terminar
Login.cleanup()
```

#### API Assíncrona (para uso em funções assíncronas)

```python
# Método 1: Obter a página logada para automação (versão assíncrona)
import asyncio
from loginCanaime import Login

async def run_login_and_operations():
    # Obter a página já logada usando a API assíncrona
    page = await Login.get_page_async(test_mode=False)
    
    if page:
        # Use a API assíncrona do Playwright
        await page.goto("https://canaime.com.br/sgp2rr/areas/unidades/alguma_pagina.php")
        # Realize suas operações...
    
    # Quando terminar, limpe os recursos
    Login.cleanup()

# Execute a função assíncrona
asyncio.run(run_login_and_operations())
```

```python
# Método 2: Obter credenciais de forma assíncrona
import asyncio
from loginCanaime import Login

async def get_user_credentials():
    credentials = await Login.get_credentials_async(test_mode=False)
    if credentials:
        print(f"Usuário: {credentials['username']}")
        print(f"Senha: {credentials['password']}")
    
    # Limpe os recursos quando terminar
    Login.cleanup()

# Execute a função assíncrona
asyncio.run(get_user_credentials())
```

### Integração com Aplicações Qt Existentes

O Login Canaimé detecta automaticamente se já existe uma instância de QApplication em execução e a utiliza em vez de criar uma nova. Isso facilita a integração com aplicações Qt existentes:

```python
from PySide6.QtWidgets import QApplication, QMainWindow
import sys
from loginCanaime import Login

# Crie sua aplicação Qt
app = QApplication(sys.argv)
main_window = QMainWindow()
main_window.show()

# O Login Canaimé usará a instância de QApplication existente
page = Login.get_page(test_mode=True)

# Continue com sua aplicação
app.exec()
```

### Via Linha de Comando

Após instalar o pacote, você pode usá-lo diretamente da linha de comando:

```bash
# Login padrão, abre interface gráfica e retorna página logada
canaime-login

# Executar em modo de teste (navegador visível)
canaime-login --test

# Apenas obter credenciais sem iniciar navegador
canaime-login --credentials-only

# Usar a API assíncrona (útil para scripts que dependem de asyncio)
canaime-login --async
```

## Características

 1. **Interface moderna e personalizável:**
	  - Janela sem borda e fundo translúcido;
     - Campos de e-mail e senha (este último com caracteres ocultos);
     - Ícone personalizado (baixado a partir de uma URL);
     - Spinner de carregamento (GIF animado) durante o processo de login;
     - Janela arrastável (mesmo sem borda);

 2. **Fluxo de login assíncrono:**  
	 - Utiliza o QThread (via subclassificação de QThread) para executar o processo de login sem travar a interface;
	 - Oferece APIs síncronas e assíncronas para diferentes contextos de uso;

 3. **Retorno do resultado:**  
	 - Retorna o objeto `Page` logado (do Playwright) para uso em aplicações reais;
	 - Permite também, em modo de desenvolvimento, obter as credenciais digitadas;

 4. **Integração com outros sistemas:**
	 - Detecta e utiliza instâncias existentes de QApplication;
	 - Tratamento adequado de erros e exceções;
	 - Gerenciamento automático de recursos.

## Estrutura do Projeto

```markdown
📦 login-canaime_project/        # Diretório raiz do projeto
├── ⚙️ setup.py                  # Configuração para instalação via pip
├── 📋 requirements.txt          # Lista de dependências do projeto
├── 🛡️ LICENSE                   # Arquivo de licença do projeto
├── 📖 README.md                 # Documentação do projeto
├── 📝 MANIFEST.in               # Controle de arquivos incluídos no pacote
└── 📦 loginCanaime/             # Pacote principal
    ├── 📄 __init__.py           # Inicializa o pacote e expõe a classe Login
    ├── 📄 __main__.py           # Ponto de entrada do pacote loginCanaime
    ├── 📄 model.py              # Lógica de negócio (Model, utilizando Playwright)
    ├── 📄 view.py               # Interface gráfica (View, utilizando PySide6)
    ├── 📄 controller.py         # Controle de fluxo (Controller, utilizando QThread)
    ├── 📄 main.py               # Funções principais para login
    └── 📁 resources/            # Recursos estáticos (imagens, ícones)
   ```

## Funcionamento Interno

-   **Model:**  
    O módulo `model.py` utiliza o Playwright para abrir o navegador, navegar até a página de login e preencher os campos de usuário e senha.  
    Ele utiliza uma heurística baseada no conteúdo de um elemento específico da página para confirmar o sucesso do login e retorna uma tupla `(True, full_name, page)` ou `(False, "", None)`.
    
-   **View:**  
    O módulo `view.py` implementa a interface gráfica com PySide6, contendo campos para e-mail e senha, botão de login, label de status e um spinner de carregamento (GIF).  
    A interface é configurada sem borda, com um ícone personalizado (baixado de uma URL) e permite arrastar a janela.
    
-   **Controller:**  
    O módulo `controller.py` conecta a View e o Model. Utiliza um QThread (via subclassificação de QThread na classe `LoginThread`) para executar o login de forma assíncrona, mantendo a interface responsiva.  
    O Controller finaliza o aplicativo automaticamente assim que o login é concluído, retornando o objeto `Page` logado.
    

## Contribuição

Contribuições são bem-vindas! Se você deseja melhorar o código, adicione novas funcionalidades ou corrigir problemas, sinta-se à vontade para abrir _issues_ ou enviar _pull requests_.



## Contato

Anderson Assunção – andersongomesrr@hotmail.com  
Projeto disponível em: [https://github.com/A-Assuncao/login-canaime_project](https://github.com/A-Assuncao/login-canaime_project)

## Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENÇA](LICENSE) para mais detalhes.  
  
----------  
**Desenvolvido com ♥ e Python.**