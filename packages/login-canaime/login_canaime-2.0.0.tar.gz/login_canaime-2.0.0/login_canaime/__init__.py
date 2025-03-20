"""
Biblioteca para autenticação no sistema Canaimé.

Esta biblioteca oferece uma interface para login no sistema Canaimé
e retorna a página logada para manipulação com Playwright.
"""

from login_canaime.auth import Login
from login_canaime.autenticador import (
    Autenticador, 
    AutenticadorGUI, 
    AutenticadorArgs, 
    AutenticadorEnv
)

__version__ = "2.0.0"

__all__ = [
    # Classe principal
    "Login",
    
    # Autenticadores
    "Autenticador", 
    "AutenticadorGUI", 
    "AutenticadorArgs", 
    "AutenticadorEnv",
] 