"""
Módulo de interface gráfica Tkinter para autenticação no sistema Canaimé.

Este módulo contém a implementação da interface gráfica usando Tkinter.
"""

import itertools
import time
import tkinter as tk
from threading import Thread
from typing import Any, Callable, Optional, Tuple

from playwright.sync_api import Page, sync_playwright

# URL de login do sistema Canaimé (ainda precisa disso para verificação de login)
URL_LOGIN_CANAIME = "https://canaime.com.br/sgp2rr/login/login_principal.php"


class LoginDialog:
    """
    Interface gráfica Tkinter para login no sistema Canaimé.
    
    Esta classe gerencia a interface de usuário e o processo de autenticação.
    """

    def __init__(self, root: tk.Tk) -> None:
        """
        Inicializa a aplicação de login.
        
        Args:
            root: A instância de tkinter.Tk para a janela principal
        """
        self.root = root
        self.configurar_janela()
        self.criar_widgets()

        # Variáveis para armazenar credenciais
        self.usuario: Optional[str] = None
        self.senha: Optional[str] = None

        # Animação e status
        self.rodando: bool = False

    def configurar_janela(self) -> None:
        """Configura a janela principal da aplicação."""
        self.root.title("Login Canaimé")
        largura_janela, altura_janela = 300, 225
        self.centralizar_janela(largura_janela, altura_janela)
        self.root.attributes("-topmost", True)

    def centralizar_janela(self, largura_janela: int, altura_janela: int) -> None:
        """
        Centraliza a janela na tela.
        
        Args:
            largura_janela: Largura da janela em pixels
            altura_janela: Altura da janela em pixels
        """
        largura_tela = self.root.winfo_screenwidth()
        altura_tela = self.root.winfo_screenheight()
        pos_x = (largura_tela - largura_janela) // 2
        pos_y = (altura_tela - altura_janela) // 2
        self.root.geometry(f"{largura_janela}x{altura_janela}+{pos_x}+{pos_y}")

    def criar_widgets(self) -> None:
        """Cria todos os widgets da interface."""
        self.label_usuario = tk.Label(self.root, text="Usuário:", anchor="w")
        self.label_usuario.pack(pady=(10, 2))

        self.entry_usuario = tk.Entry(self.root)
        self.entry_usuario.pack(pady=(0, 10))
        self.entry_usuario.focus_set()

        self.label_senha = tk.Label(self.root, text="Senha:", anchor="w")
        self.label_senha.pack(pady=(10, 2))

        self.entry_senha = tk.Entry(self.root, show="*")
        self.entry_senha.pack(pady=(0, 10))

        self.btn_login = tk.Button(self.root, text="Login", command=self.iniciar_login)
        self.btn_login.pack(pady=10)

        # Label para mostrar status (como animação de carregamento)
        self.label_status = tk.Label(self.root, text="")
        self.label_status.pack(pady=10)

        # Vincular o evento de pressionar Enter ao método de login
        self.root.bind("<Return>", self.on_enter)

    def iniciar_login(self) -> None:
        """Inicia o processo de login em uma thread separada."""
        self.btn_login.config(state=tk.DISABLED)
        self.label_status.config(text="Realizando login...")
        self.rodando = True

        # Iniciar animação e processo de login
        Thread(target=self.animar_bolinha).start()
        Thread(target=self.fazer_login).start()

    def animar_bolinha(self) -> None:
        """Anima indicador de carregamento enquanto o login está em andamento."""
        for frame in itertools.cycle(["◐", "◓", "◑", "◒"]):
            if not self.rodando:
                break
            self.label_status.config(text=f"Realizando login... {frame}")
            time.sleep(0.2)

    def on_enter(self, event: Any) -> None:
        """
        Método chamado quando a tecla Enter é pressionada.
        
        Args:
            event: Evento de tecla pressionada
        """
        self.iniciar_login()

    def fazer_login(self) -> None:
        """Executa o login utilizando Playwright em uma thread separada."""
        usuario = self.entry_usuario.get()
        senha = self.entry_senha.get()

        if not usuario or not senha:
            self.mostrar_erro("Usuário e senha são obrigatórios.")
            return

        try:
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=True)
                page = browser.new_page()
                self.realizar_login(page, usuario, senha)
                browser.close()

        except Exception as e:
            self.mostrar_erro(f"Erro de conexão: {str(e)}")

    def realizar_login(self, page: Page, usuario: str, senha: str) -> None:
        """
        Realiza o processo de login utilizando Playwright.
        
        Args:
            page: Instância de Page do Playwright
            usuario: Nome de usuário para login
            senha: Senha para login
        """
        page.goto(URL_LOGIN_CANAIME)
        page.fill("input[name='usuario']", usuario)
        page.fill("input[name='senha']", senha)
        page.press("input[name='senha']", "Enter")
        page.wait_for_timeout(5000)

        if page.locator("img").count() < 4:
            self.mostrar_erro("Usuário ou senha inválidos.")
        else:
            self.login_sucesso(usuario, senha)

    def login_sucesso(self, usuario: str, senha: str) -> None:
        """
        Atualiza a interface para mostrar sucesso no login.
        
        Args:
            usuario: Nome de usuário utilizado no login
            senha: Senha utilizada no login
        """
        self.usuario = usuario
        self.senha = senha
        self.rodando = False
        self.atualizar_interface(
            lambda: (
                self.label_status.config(text="Login efetuado com sucesso!"),
                self.root.after(1000, self.root.destroy),
            )
        )

    def mostrar_erro(self, mensagem: str) -> None:
        """
        Mostra mensagem de erro e habilita o botão de login novamente.
        
        Args:
            mensagem: Mensagem de erro a ser exibida
        """
        self.rodando = False
        self.atualizar_interface(
            lambda: (
                self.label_status.config(text=mensagem),
                self.btn_login.config(state=tk.NORMAL),
            )
        )

    def atualizar_interface(self, func: Callable) -> None:
        """
        Atualiza a interface da aplicação.
        
        Args:
            func: Função a ser executada na thread principal
        """
        self.root.after(0, func)

    def get_credentials(self) -> Tuple[Optional[str], Optional[str]]:
        """
        Retorna as credenciais de login (usuário e senha).
        
        Returns:
            Uma tupla contendo o usuário e a senha
        """
        return self.usuario, self.senha


def executar_login_dialog() -> Tuple[Optional[str], Optional[str]]:
    """
    Executa a aplicação de login e retorna as credenciais.
    
    Returns:
        Uma tupla contendo o usuário e a senha após o login
    """
    root = tk.Tk()
    app = LoginDialog(root)
    root.mainloop()
    return app.get_credentials() 