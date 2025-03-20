"""
Pacote loginCanaime
--------------------
Este pacote fornece as funcionalidades para o login no Sistema Canaimé,
integrando Model, View e Controller em uma interface simples e reutilizável.

Uso básico como biblioteca:
    # Modo 1: Obter a página logada para automação
    import asyncio
    from loginCanaime import Login
    
    # Obter a página já logada para automação com Playwright
    page = Login.get_page(test_mode=False)
    
    # Agora você pode usar a página para navegar de forma assíncrona
    async def run_operations():
        if page:
            await page.goto("https://canaime.com.br/sgp2rr/areas/unidades/alguma_pagina.php")
            # Realize suas operações...
            
            # Quando terminar, limpe os recursos
            Login.cleanup()
    
    # Execute a função assíncrona
    asyncio.run(run_operations())
        
    # Modo 2: Apenas obter as credenciais (útil para desenvolvimento)
    from loginCanaime import Login
    
    credentials = Login.get_credentials(test_mode=False)
    if credentials:
        print(f"Usuário: {credentials['username']}")
        print(f"Senha: {credentials['password']}")

Uso via linha de comando (após instalar o pacote):
    # Login padrão
    canaime-login
    
    # Executar em modo de teste
    canaime-login --test
    
    # Apenas obter credenciais sem iniciar navegador
    canaime-login --credentials-only

Nota: A biblioteca gerencia internamente o loop de eventos asyncio e a instância da aplicação Qt.
Se estiver integrando com uma aplicação Qt existente, certifique-se de usar o QApplication.instance()
existente em vez de criar uma nova instância.
"""

__version__ = "1.0.1"

# Importa a classe Login do módulo main.py
from .main import Login
