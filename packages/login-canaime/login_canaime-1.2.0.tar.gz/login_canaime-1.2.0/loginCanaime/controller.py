"""
Módulo controller
-----------------
Conecta a View com o Model, controlando o fluxo de login.
Utiliza asyncio para executar o login de forma assíncrona e manter a interface responsiva.
"""

import asyncio
import logging
from PySide6.QtCore import QTimer, Slot
from PySide6.QtWidgets import QApplication
from .model import CanaimeLoginModel

class CanaimeLoginController:
    """
    Controller que gerencia o fluxo de login, conectando a interface (View) com a lógica de negócio (Model).
    """

    def __init__(self, view, test_mode: bool = False) -> None:
        self.view = view
        self.model = CanaimeLoginModel(test_mode=test_mode)
        self._bind_events()
        self.login_task = None  # Para armazenar a task assíncrona e evitar vazamentos de memória

    def _bind_events(self) -> None:
        self.view.login_btn.clicked.connect(self.start_login_process)
        self.view.password_input.returnPressed.connect(self.start_login_process)

    @Slot()
    def start_login_process(self) -> None:
        username = self.view.get_username().strip()
        password = self.view.get_password().strip()
        if not username or not password:
            self.view.set_status_message("Por favor, digite usuário e senha.")
            self.view.enable_login_button()
            self.view.stop_loading_animation()
            return

        self.view.disable_login_button()
        self.view.set_status_message("Realizando login...")
        self.view.start_loading_animation()

        if self.login_task:
            self.login_task.cancel()

        self.login_task = asyncio.create_task(self._login(username, password))

    async def _login(self, username: str, password: str) -> None:
        try:
            print("Executando login assíncrono...")
            success, full_name, page = await self.model.perform_login(username, password)
            print(f"Resultado do login: success={success}, user={full_name}, page={bool(page)}")
            self._on_login_finished(success, full_name, page)
        except Exception as e:
            print(f"Erro no login: {e}")
            self._on_login_error(str(e))

    @Slot(bool, str, object)
    def _on_login_finished(self, success: bool, full_name: str, page: object) -> None:
        self.view.stop_loading_animation()
        if success:
            self.view._login_result = page
            QTimer.singleShot(2000, self._finalize_success)
        else:
            self.view.set_status_message("Usuário ou senha inválidos. Tente novamente.")
            self.view._login_result = None
            self.view.enable_login_button()

    @Slot(str)
    def _on_login_error(self, message: str) -> None:
        logging.error(f"Erro no login: {message}")
        self.view.stop_loading_animation()
        self.view.set_status_message(message)
        self.view.enable_login_button()

    def _finalize_success(self):
        if self.view._login_result is not None:
            self.view.close()
