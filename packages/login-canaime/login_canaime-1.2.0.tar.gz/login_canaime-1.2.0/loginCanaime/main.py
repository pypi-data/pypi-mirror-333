import sys
import asyncio
from typing import Optional, Dict, Any
from PySide6.QtWidgets import QApplication
from qasync import QEventLoop
from playwright.async_api import Page
from .view import CanaimeLoginView
from .controller import CanaimeLoginController


class Login:
    """
    Classe principal para realizar login no Canaimé e fornecer uma página logada ou credenciais verificadas.
    """

    _app = None
    _loop = None
    _page = None
    _credentials = None
    _initialized = False

    @staticmethod
    def _ensure_initialized():
        """
        Garante que os componentes Qt e asyncio estejam inicializados.
        Tenta usar instâncias existentes quando disponíveis.
        """
        if not Login._initialized:
            # Tenta usar uma instância existente de QApplication, ou cria uma nova
            Login._app = QApplication.instance()
            if not Login._app:
                Login._app = QApplication(sys.argv)
                print("Nova instância de QApplication criada")
            else:
                print("Usando instância existente de QApplication")
            
            # Configura o loop de eventos
            try:
                Login._loop = QEventLoop(Login._app)
                asyncio.set_event_loop(Login._loop)
                print("Loop de eventos Qt configurado")
            except Exception as e:
                print(f"Erro ao configurar loop de eventos: {e}")
                raise
            
            Login._initialized = True

    @staticmethod
    def get_page(test_mode: bool = False) -> Optional[Page]:
        """
        Inicia o fluxo de login e retorna uma página logada para manipulação.
        O navegador permanecerá aberto até que `Login.cleanup()` seja chamado.

        Args:
            test_mode (bool): Se True, executa o navegador no modo visível.

        Returns:
            Page: Página logada do Playwright pronta para uso.
        """
        Login._ensure_initialized()

        view = CanaimeLoginView()
        view._login_result = None
        controller = CanaimeLoginController(view, test_mode=test_mode)
        view.show()

        async def _run():
            try:
                while view._login_result is None:
                    if not view.isVisible():
                        return None
                    await asyncio.sleep(0.1)
                return view._login_result
            except Exception as e:
                print(f"Erro durante o processo de login: {e}")
                return None

        try:
            Login._page = Login._loop.run_until_complete(_run())
            return Login._page
        except Exception as e:
            print(f"Falha ao executar o loop de eventos: {e}")
            return None

    @staticmethod
    async def get_page_async(test_mode: bool = False) -> Optional[Page]:
        """
        Versão assíncrona do método get_page. Use esta versão se estiver 
        dentro de uma função assíncrona ou com asyncio.

        Args:
            test_mode (bool): Se True, executa o navegador no modo visível.

        Returns:
            Page: Página logada do Playwright pronta para uso.
        """
        Login._ensure_initialized()

        view = CanaimeLoginView()
        view._login_result = None
        controller = CanaimeLoginController(view, test_mode=test_mode)
        view.show()

        try:
            while view._login_result is None:
                if not view.isVisible():
                    return None
                await asyncio.sleep(0.1)
            
            Login._page = view._login_result
            return Login._page
        except Exception as e:
            print(f"Erro durante o processo de login assíncrono: {e}")
            return None

    @staticmethod
    def get_credentials(test_mode: bool = False) -> Optional[Dict[str, str]]:
        """
        Inicia o fluxo de login e retorna as credenciais verificadas.
        O navegador permanecerá aberto até que `Login.cleanup()` seja chamado.

        Args:
            test_mode (bool): Se True, executa o navegador no modo visível.

        Returns:
            Dict[str, str]: Dicionário contendo 'username' e 'password' verificados no sistema após o login.
        """
        Login._ensure_initialized()

        view = CanaimeLoginView()
        view._login_result = None
        controller = CanaimeLoginController(view, test_mode=test_mode)
        view.show()

        async def _run():
            try:
                while view._login_result is None:
                    if not view.isVisible():
                        return None
                    await asyncio.sleep(0.1)
                return {"username": view.get_username(), "password": view.get_password()}
            except Exception as e:
                print(f"Erro ao obter credenciais: {e}")
                return None

        try:
            Login._credentials = Login._loop.run_until_complete(_run())
            return Login._credentials
        except Exception as e:
            print(f"Falha ao executar o loop de eventos para credenciais: {e}")
            return None

    @staticmethod
    async def get_credentials_async(test_mode: bool = False) -> Optional[Dict[str, str]]:
        """
        Versão assíncrona do método get_credentials. Use esta versão se estiver 
        dentro de uma função assíncrona ou com asyncio.

        Args:
            test_mode (bool): Se True, executa o navegador no modo visível.

        Returns:
            Dict[str, str]: Dicionário contendo 'username' e 'password' verificados no sistema após o login.
        """
        Login._ensure_initialized()

        view = CanaimeLoginView()
        view._login_result = None
        controller = CanaimeLoginController(view, test_mode=test_mode)
        view.show()

        try:
            while view._login_result is None:
                if not view.isVisible():
                    return None
                await asyncio.sleep(0.1)
            
            Login._credentials = {"username": view.get_username(), "password": view.get_password()}
            return Login._credentials
        except Exception as e:
            print(f"Erro ao obter credenciais de forma assíncrona: {e}")
            return None

    @staticmethod
    def cleanup():
        """
        Encerra corretamente a aplicação Qt, o navegador e o loop de eventos.
        """
        if Login._page and not Login._page.is_closed():
            context = Login._page.context
            browser = context.browser
            try:
                Login._loop.run_until_complete(context.close())
                Login._loop.run_until_complete(browser.close())
                print("Navegador fechado.")
            except Exception as e:
                print(f"Erro ao fechar o navegador: {e}")

        # Não finaliza o QApplication se foi obtido de uma instância existente
        if Login._app and Login._app == QApplication.instance():
            print("Preservando instância existente de QApplication")
        elif Login._app:
            Login._app.quit()
            print("Qt encerrado.")

        if Login._loop:
            try:
                Login._loop.stop()
                print("Asyncio encerrado.")
            except Exception as e:
                print(f"Erro ao encerrar o loop de eventos: {e}")

        Login._app = None
        Login._loop = None
        Login._page = None
        Login._credentials = None
        Login._initialized = False

def cli_main():
    """Função principal para execução via linha de comando.
    Esta função é chamada quando o pacote é executado via 'canaime-login' após instalação.
    """
    import argparse
    import asyncio
    
    parser = argparse.ArgumentParser(description="Sistema de login Canaimé")
    parser.add_argument("--test", action="store_true", help="Executar em modo de teste")
    parser.add_argument("--credentials-only", action="store_true", help="Apenas retornar as credenciais sem abrir navegador")
    parser.add_argument("--async", action="store_true", help="Usar API assíncrona", dest="use_async")
    args = parser.parse_args()
    
    if args.credentials_only:
        if args.use_async:
            async def get_creds_async():
                credentials = await Login.get_credentials_async(test_mode=args.test)
                if credentials:
                    print(f"Usuário: {credentials['username']}")
                    print(f"Senha: {credentials['password']}")
                else:
                    print("Falha ao obter credenciais ou operação cancelada pelo usuário.")
                Login.cleanup()
            
            asyncio.run(get_creds_async())
        else:
            credentials = Login.get_credentials(test_mode=args.test)
            if credentials:
                print(f"Usuário: {credentials['username']}")
                print(f"Senha: {credentials['password']}")
            else:
                print("Falha ao obter credenciais ou operação cancelada pelo usuário.")
            Login.cleanup()
    else:
        async def run_login():
            try:
                if args.use_async:
                    page = await Login.get_page_async(test_mode=args.test)
                else:
                    page = Login.get_page(test_mode=args.test)
                
                if page:
                    print("Login realizado com sucesso!")
                    print("Pressione Ctrl+C para encerrar...")
                    try:
                        # Mantém o programa rodando até Ctrl+C
                        while True:
                            await asyncio.sleep(1)
                    except KeyboardInterrupt:
                        print("Encerrando...")
                    finally:
                        Login.cleanup()
                else:
                    print("Falha no login ou operação cancelada pelo usuário.")
                    Login.cleanup()
            except Exception as e:
                print(f"Erro durante o login: {e}")
                Login.cleanup()
        
        asyncio.run(run_login())

if __name__ == "__main__":
    cli_main()
