"""
Módulo de interfaces para autenticação no sistema Canaimé.

Este módulo define interfaces abstratas para diferentes métodos de autenticação.
"""

from abc import ABC, abstractmethod
from typing import Optional, Tuple, Dict, Any


class Autenticador(ABC):
    """
    Interface abstrata para diferentes métodos de autenticação.
    
    Qualquer classe que queira fornecer um mecanismo de autenticação
    deve implementar esta interface.
    """
    
    @abstractmethod
    def obter_credenciais(self, **kwargs: Dict[str, Any]) -> Tuple[Optional[str], Optional[str]]:
        """
        Obtém as credenciais de login.
        
        Returns:
            Tuple[Optional[str], Optional[str]]: Uma tupla contendo o usuário e a senha.
        """
        pass


class AutenticadorGUI(Autenticador):
    """
    Implementação concreta do autenticador que usa interface gráfica Tkinter.
    
    Esta é a implementação padrão que usa a interface Tkinter.
    """
    
    def obter_credenciais(self, **kwargs: Dict[str, Any]) -> Tuple[Optional[str], Optional[str]]:
        """
        Exibe uma interface gráfica Tkinter para o usuário inserir suas credenciais.
        
        Returns:
            Tuple[Optional[str], Optional[str]]: Credenciais fornecidas pelo usuário.
        """
        from login_canaime.ui.tkinter_ui import executar_login_dialog
        return executar_login_dialog()


class AutenticadorArgs(Autenticador):
    """
    Implementação do autenticador que usa argumentos fornecidos diretamente.
    
    Esta implementação é útil para testes ou quando as credenciais são
    fornecidas programaticamente.
    """
    
    def obter_credenciais(self, **kwargs: Dict[str, Any]) -> Tuple[Optional[str], Optional[str]]:
        """
        Usa as credenciais fornecidas diretamente como argumentos.
        
        Args:
            **kwargs: Deve conter 'usuario' e 'senha'.
        
        Returns:
            Tuple[Optional[str], Optional[str]]: Credenciais fornecidas.
        """
        usuario = kwargs.get("usuario")
        senha = kwargs.get("senha")
        return usuario, senha


class AutenticadorEnv(Autenticador):
    """
    Implementação do autenticador que obtém credenciais de variáveis de ambiente.
    
    Esta implementação é útil para ambientes automatizados como CI/CD.
    """
    
    def obter_credenciais(self, **kwargs: Dict[str, Any]) -> Tuple[Optional[str], Optional[str]]:
        """
        Obtém credenciais de variáveis de ambiente.
        
        Returns:
            Tuple[Optional[str], Optional[str]]: Credenciais das variáveis de ambiente.
        """
        import os
        usuario = os.environ.get("CANAIME_USUARIO")
        senha = os.environ.get("CANAIME_SENHA")
        return usuario, senha 