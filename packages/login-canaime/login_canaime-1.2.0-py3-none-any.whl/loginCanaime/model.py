"""
Módulo model
------------
Contém a lógica de negócio (regras e acessos externos) para login no Canaimé.
Utiliza a API assíncrona do Playwright para automatizar o fluxo de login.
"""

from typing import Tuple, Optional
from playwright.async_api import async_playwright, Browser, Page

# URL de login do sistema Canaimé
LOGIN_URL: str = "https://canaime.com.br/sgp2rr/login/login_principal.php"

class CanaimeLoginModel:
    """
    Classe responsável por encapsular a lógica de login utilizando a API assíncrona do Playwright.
    """

    def __init__(self, test_mode: bool = False) -> None:
        self.test_mode: bool = test_mode
        self.browser: Optional[Browser] = None
        self.page: Optional[Page] = None
        self.playwright = None  # Será inicializado de forma assíncrona

    async def perform_login(self, username: str, password: str) -> Tuple[bool, str, Optional[Page]]:
        """
        Executa o processo de login de forma assíncrona.

        Args:
            username (str): Nome de usuário.
            password (str): Senha.

        Returns:
            Tuple[bool, str, Optional[Page]]:
                - (True, full_name, page) se o login for bem-sucedido;
                - (False, "", None) caso contrário.
        """
        try:
            if not username or not password:
                raise ValueError("Os campos de usuário e senha são obrigatórios para efetuar o login.")

            self.playwright = await async_playwright().start()
            self.browser = await self.playwright.chromium.launch(headless=not self.test_mode)

            context = await self.browser.new_context(java_script_enabled=False, bypass_csp=True)

            # Bloquear imagens
            await context.route("**/*", lambda route: route.abort() if route.request.resource_type == "image" else route.continue_())

            self.page = await context.new_page()
            await self.page.goto(LOGIN_URL)
            await self.page.fill("input[name='usuario']", username)
            await self.page.fill("input[name='senha']", password)
            await self.page.press("input[name='senha']", "Enter")

            await self.page.wait_for_load_state("load")  # Aguarda a página carregar completamente

            if self.page.url == "https://canaime.com.br/sgp2rr/index.php":
                return False, "", None

            frame = self.page.frame(name="areas")
            if not frame:
                return False, "", None

            locator = frame.locator(".tituloAmarelo")
            text = await locator.text_content()
            if not text:
                return False, "", None

            text = text.strip()
            parts = text.splitlines()
            if len(parts) < 2:
                return False, "", None

            full_name = parts[0].strip()
            login_obtained = parts[1].strip()

            return (True, full_name, self.page) if login_obtained == username else (False, "", None)

        except Exception as e:
            print(f"Erro durante login: {e}")
            return False, "", None
