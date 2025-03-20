"""
Módulo __main__
----------------
Exemplo de uso do pacote loginCanaime.
Este script executa um fluxo completo de login, navegação e fechamento do navegador.
"""

from asyncio import run
from loginCanaime import Login

async def main():
    # Obtém a página logada
    page = Login.get_page(test_mode=True)

    # Manipula a página como quiser
    if page:
        await page.goto("https://canaime.com.br/sgp2rr/areas/unidades/Ficha_Preso_index.php?id_cad_preso=62131")
        await page.wait_for_load_state("load")

        # Obtém o nome interno
        nome = await page.locator("tr:nth-child(3) .titulobk").text_content()
        print(f"Nome interno: {nome}")

    # Finaliza tudo corretamente
    Login.cleanup()

# Executa a função assíncrona
run(main())
