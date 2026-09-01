from pathlib import Path
from time import sleep

import openpyxl
import pyautogui
import pyperclip
import schedule
from playwright.sync_api import sync_playwright


CUSTO_PRODUTO = 200
HORARIO_EXECUCAO = "22:06"
GRUPO_WHATSAPP = "compras T.I"

ARQUIVO_EXCEL = Path("margem de lucro.xlsx")
ARQUIVO_TXT = Path("margem_lucro.txt")
PERFIL_NAVEGADOR = Path("./automacao_web")

PRODUTOS = [
    {
        "site": "Kabum",
        "url": "https://www.kabum.com.br/produto/383893/memoria-ram-rise-mode-z-8gb-3200mhz-ddr4-cl19-branco-rm-d4-8g-3200zw",
        "seletor_preco": '//*[@id="main-content"]/div[1]/div[1]/div[1]/div[3]/div[3]/h4',
    },
    {
        "site": "Amazon",
        "url": "https://www.amazon.com.br/Mem%C3%B3ria-3200MHz-Rise-Mode-Diamond/dp/B01B95BDRS/ref=sr_1_5?__mk_pt_BR=%C3%85M%C3%85%C5%BD%C3%95%C3%91&crid=2P3ER3D525L1K&dib=eyJ2IjoiMSJ9.pIhF620oH7DBHeXj3Fg6nRlXbmEHuk2zy5n-gsomnP-vY2IArEXaB2CPNftUapbuqXSwZeh7FSysSys4B5p-nyHUcIL7lMwNvIlbs-hJ6qEu7T-fEc5_wRXEFdcsvQu7HvtjqpW7jQemDyX37TMwAv8NGCnJZttE7ocsEswLDPu7k235S9H0J5C0K1nl0kfiN3AmC9qN5j0zUY7ZqG7Vjl2jS6tktCk1OoSZfHKIjbQvJmmZrbRtViIhH9MxyOFRi5cCE_JlXjH59pX9f1tzoqPOay8ahl1nWlpgl8_Pgbs.S87q9eM5LBjYQ5-EleaYZInTdpuUBDMwHHRLDBLbN6Q&dib_tag=se&keywords=memoria+ram+16gb&qid=1780701161&sprefix=memoria+ram+16gb%2Caps%2C269&sr=8-5&ufe=app_do%3Aamzn1.fos.25548f35-0de7-44b3-b28e-0f56f3f96147",
        "seletor_preco": '//*[@id="corePriceDisplay_desktop_feature_div"]/div[1]',
    },
]


def converter_preco_para_float(texto_preco):
    """Transforma textos como 'R$ 159,90' em numero decimal: 159.90."""
    preco_limpo = (
        texto_preco.replace("R$", "")
        .replace(".", "")
        .replace(",", ".")
        .strip()
        .split()[0]
    )
    return float(preco_limpo)


def buscar_precos(produtos):
    precos = []

    with sync_playwright() as playwright:
        navegador = playwright.chromium.launch_persistent_context(
            user_data_dir=str(PERFIL_NAVEGADOR),
            headless=False,
            locale="pt-BR",
        )

        pagina = navegador.new_page()
        pagina.set_default_timeout(30000)
        pagina.set_default_navigation_timeout(60000)

        for produto in produtos:
            pagina.goto(produto["url"])
            texto_preco = pagina.locator(produto["seletor_preco"]).inner_text()
            preco = converter_preco_para_float(texto_preco)

            precos.append(
                {
                    "site": produto["site"],
                    "url": produto["url"],
                    "preco": preco,
                }
            )

            sleep(4)

        navegador.close()

    return precos


def gerar_relatorio(precos, custo, arquivo_excel, arquivo_txt):
    workbook = openpyxl.Workbook()
    sheet = workbook.active
    sheet.title = "margem_lucro"
    sheet.append(["Site", "Custo", "Preco", "Lucro"])

    for item in precos:
        lucro = item["preco"] - custo
        sheet.append([item["site"], custo, item["preco"], lucro])

    workbook.save(arquivo_excel)

    linhas_relatorio = [
        f"{linha[0].value}, {linha[1].value}, {linha[2].value}, {linha[3].value}"
        for linha in sheet.iter_rows(min_row=1)
    ]
    texto_relatorio = "\n".join(linhas_relatorio)
    arquivo_txt.write_text(texto_relatorio, encoding="utf-8")

    return texto_relatorio


def enviar_relatorio_whatsapp(nome_grupo, texto_relatorio):
    # Usa a area de transferencia para enviar textos grandes e com quebras de linha.
    pyperclip.copy(texto_relatorio)

    pyautogui.hotkey("win")
    sleep(5)

    pyautogui.write("whatsapp")
    sleep(10)
    pyautogui.press("enter")
    sleep(20)

    pyautogui.press("tab", presses=2, interval=1)
    pyautogui.press("enter")
    sleep(3)

    pyautogui.write(nome_grupo)
    pyautogui.press("tab", presses=2, interval=1)
    pyautogui.press("enter")
    sleep(2)

    pyautogui.hotkey("ctrl", "v")
    sleep(2)
    pyautogui.press("enter")


def executar_automacao(produtos, custo, grupo_whatsapp, arquivo_excel, arquivo_txt):
    precos = buscar_precos(produtos)
    relatorio = gerar_relatorio(precos, custo, arquivo_excel, arquivo_txt)
    enviar_relatorio_whatsapp(grupo_whatsapp, relatorio)


def iniciar_agendamento():
    schedule.every().day.at(HORARIO_EXECUCAO).do(
        executar_automacao,
        produtos=PRODUTOS,
        custo=CUSTO_PRODUTO,
        grupo_whatsapp=GRUPO_WHATSAPP,
        arquivo_excel=ARQUIVO_EXCEL,
        arquivo_txt=ARQUIVO_TXT,
    )

    while True:
        schedule.run_pending()
        sleep(1)


if __name__ == "__main__":
    iniciar_agendamento()
