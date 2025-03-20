"""
Interface de linha de comando para a biblioteca login-canaime.

Este módulo fornece uma interface para usar a biblioteca via linha de comando.
"""

import argparse
import sys
from typing import List, NoReturn, Optional

from login_canaime import __version__, Login


def parse_args(args: Optional[List[str]] = None) -> argparse.Namespace:
    """
    Analisa os argumentos da linha de comando.

    Args:
        args: Lista de argumentos da linha de comando

    Returns:
        Namespace contendo os argumentos analisados
    """
    parser = argparse.ArgumentParser(
        description="Ferramenta de autenticação no sistema Canaimé"
    )

    parser.add_argument(
        "--version", action="version", version=f"%(prog)s {__version__}"
    )

    return parser.parse_args(args)


def main(args: Optional[List[str]] = None) -> NoReturn:
    """
    Função principal da interface de linha de comando.

    Args:
        args: Lista de argumentos da linha de comando
    """
    parse_args(args)

    login = Login()
    usuario, senha = login.obter_credenciais()

    if usuario and senha:
        print(f"Usuário: {usuario}")
        print(f"Senha: {senha}")
        sys.exit(0)
    else:
        print("Autenticação cancelada ou falhou.", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
