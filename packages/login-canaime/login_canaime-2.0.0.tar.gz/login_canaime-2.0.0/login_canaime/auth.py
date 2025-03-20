"""
Módulo de autenticação para o sistema Canaimé.

Este módulo oferece uma interface para autenticação no sistema Canaimé.
"""

import time
from typing import Optional, Tuple, Dict, Any

from playwright.sync_api import Page, Browser, BrowserContext, sync_playwright

from login_canaime.autenticador import Autenticador, AutenticadorGUI

# URL de login do sistema Canaimé
URL_LOGIN_CANAIME = "https://canaime.com.br/sgp2rr/login/login_principal.php"


class Login:
    """
    Classe principal para autenticação e manipulação da página do sistema Canaimé.
    
    Esta classe encapsula toda a funcionalidade de login e manipulação da página.
    
    Exemplo de uso:
        ```python
        from login_canaime import Login
        
        # Criar uma instância e fazer login
        login = Login()
        
        # Opção 1: Obter apenas as credenciais
        usuario, senha = login.obter_credenciais()
        print(f"Credenciais: {usuario} / {senha}")
        
        # Opção 2: Obter a página logada
        page = login.obter_pagina()
        
        # Manipular a página
        if page:
            print(f"Título da página: {page.title()}")
            page.screenshot(path="screenshot.png")
            
            # Lembre-se de fechar quando terminar
            login.fechar()
        ```
    """
    
    def __init__(self, autenticador: Optional[Autenticador] = None):
        """
        Inicializa a classe Login.
        
        Args:
            autenticador: Implementação de Autenticador a ser usada.
                          Se None, usa AutenticadorGUI por padrão.
        """
        self.autenticador = autenticador or AutenticadorGUI()
        self.usuario: Optional[str] = None
        self.senha: Optional[str] = None
        self.page: Optional[Page] = None
        self.browser: Optional[Browser] = None
        self.context: Optional[BrowserContext] = None
        self.playwright = None
    
    def obter_credenciais(self, **kwargs: Any) -> Tuple[Optional[str], Optional[str]]:
        """
        Obtém apenas as credenciais de login usando o autenticador configurado.
        
        Args:
            **kwargs: Argumentos adicionais para o autenticador.
        
        Returns:
            Tupla contendo usuário e senha, ou (None, None) se falhar.
        """
        self.usuario, self.senha = self.autenticador.obter_credenciais(**kwargs)
        return self.usuario, self.senha
    
    def obter_pagina(
        self,
        headless: bool = False,
        browser_type: str = "chromium",
        viewport: Dict[str, int] = {"width": 1280, "height": 720},
        timeout: int = 30000,
        **kwargs: Any
    ) -> Optional[Page]:
        """
        Obtém credenciais e retorna a página logada para manipulação.
        
        Args:
            headless: Se True, o navegador não será exibido visualmente. Padrão: False.
            browser_type: Tipo do navegador a ser usado. Padrão: "chromium".
            viewport: Dimensões da janela do navegador. Padrão: 1280x720.
            timeout: Tempo limite em ms para operações de navegação. Padrão: 30000ms.
            **kwargs: Argumentos adicionais para o autenticador.
            
        Returns:
            Instância da Page do Playwright já logada, ou None se falhar.
        """
        # Primeiro obtém as credenciais se ainda não tiver
        if not self.usuario or not self.senha:
            self.obter_credenciais(**kwargs)
            
            if not self.usuario or not self.senha:
                print("Falha ao obter credenciais.")
                return None
        
        try:
            # Inicia o Playwright e cria o navegador
            self.playwright = sync_playwright().start()
            
            # Configura argumentos adicionais para o navegador para permitir navegação entre domínios
            browser_args = [
                "--disable-web-security",  # Desabilita restrições de segurança entre domínios
                "--disable-site-isolation-trials",
                "--no-sandbox",
                "--disable-features=IsolateOrigins,site-per-process"
            ]
            
            # Seleciona o tipo de navegador com as configurações adicionais
            if browser_type.lower() == "firefox":
                self.browser = self.playwright.firefox.launch(
                    headless=headless,
                    firefox_user_prefs={"privacy.webrtc.legacyGlobalIndicator": False}
                )
            elif browser_type.lower() == "webkit":
                self.browser = self.playwright.webkit.launch(headless=headless)
            else:
                self.browser = self.playwright.chromium.launch(
                    headless=headless, 
                    args=browser_args
                )
            
            # Configura o contexto com permissões adicionais para todos os sites
            self.context = self.browser.new_context(
                viewport=viewport,
                bypass_csp=True,  # Ignora políticas de segurança de conteúdo
                permissions=["geolocation"]  # Adiciona permissões que podem ser necessárias
            )
            
            # Ignora erros de certificado e HTTPS
            self.context.set_default_navigation_timeout(timeout)
            
            # Cria a página
            self.page = self.context.new_page()
            self.page.set_default_timeout(timeout)
            
            # Navega para a página de login
            self.page.goto(URL_LOGIN_CANAIME)
            
            # Preenche o formulário de login
            self.page.fill("input[name='usuario']", self.usuario)
            self.page.fill("input[name='senha']", self.senha)
            self.page.press("input[name='senha']", "Enter")
            
            # Aguarda a navegação completa
            self.page.wait_for_load_state("networkidle")
            
            # Verifica se o login foi bem-sucedido (ajuste conforme necessário)
            if self.page.locator('img').count() < 4:
                print("Falha no login: parece que as credenciais não foram aceitas.")
                self.fechar()
                return None
            
            return self.page
            
        except Exception as e:
            print(f"Erro ao obter página logada: {str(e)}")
            self.fechar()
            return None
    
    def fechar(self) -> None:
        """Fecha o navegador e libera recursos."""
        if self.browser:
            self.browser.close()
            self.browser = None
        
        if self.playwright:
            self.playwright.stop()
            self.playwright = None
    
    def __enter__(self):
        """Suporte para uso com 'with'."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Garante que os recursos sejam liberados ao sair do bloco 'with'."""
        self.fechar() 