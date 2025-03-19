import asyncio
import io
import os
import re
import shutil
import warnings
from datetime import datetime, timedelta


import pyperclip
import pyautogui
from pywinauto.application import Application
from rich.console import Console
from dateutil.relativedelta import relativedelta
from pywinauto import Desktop

from worker_automate_hub.models.dto.rpa_historico_request_dto import RpaHistoricoStatusEnum, RpaRetornoProcessoDTO, RpaTagDTO, RpaTagEnum
from worker_automate_hub.models.dto.rpa_processo_entrada_dto import RpaProcessoEntradaDTO
from worker_automate_hub.utils.get_creds_gworkspace import GetCredsGworkspace
import win32clipboard
from googleapiclient.discovery import build
from worker_automate_hub.utils.logger import logger
from pywinauto_recorder import set_combobox
from worker_automate_hub.api.client import get_config_by_name, get_valor_remessa_cobranca, send_file, sync_get_config_by_name
from worker_automate_hub.utils.util import (
    create_temp_folder,
    delete_folder,
    kill_all_emsys,
    kill_process, 
    login_emsys,
    save_pdf_emsys, 
    type_text_into_field,
    worker_sleep,
    set_variable,
    )

pyautogui.PAUSE = 0.5
ASSETS_BASE_PATH = 'assets/fidc/'
PDF_SUFFIX = "_PDF.pdf"
console = Console()



async def exportacao_docs_portal_b2b(task: RpaProcessoEntradaDTO) -> RpaRetornoProcessoDTO:
    '''
       Processo FIDC - Remessa de Cobrança CNAB240
    '''
    try:
        #Setando tempo de timeout
        multiplicador_timeout = int(float(task.sistemas[0].timeout))
        set_variable("timeout_multiplicador", multiplicador_timeout)
        
        #Pegando nome do usuario
        nome_usuario = os.environ.get('USERNAME') or os.environ.get('USER')
        nome_pasta = f"{nome_usuario}_arquivos"

        #Delete temp folder
        await delete_folder(nome_pasta)
        #Cria Pasta temporaria
        temp_folder = await create_temp_folder()
        temp_folder = temp_folder +'\\'
        #Pega Config para logar no Emsys
        config = await get_config_by_name("login_emsys")
        folders_paths = await get_config_by_name("Folders_Fidc")
        #Abre um novo emsys
        await kill_all_emsys()
        app = Application(backend='win32').start("C:\\Rezende\\EMSys3\\EMSys3.exe")
        warnings.filterwarnings("ignore", category=UserWarning, message="32-bit application should be automated using 32-bit Python")
        console.print("\nEMSys iniciando...", style="bold green")
        return_login = await login_emsys(config.conConfiguracao, app, task)

        if return_login.sucesso == True:
            type_text_into_field('Envia Boleto por email', app['TFrmMenuPrincipal']['Edit'], True, '50')
            pyautogui.press('enter')
            await worker_sleep(1)
            pyautogui.press('enter')
            console.print(f"\nPesquisa: 'Envia Boleto por email' realizada com sucesso", style="bold green")
        else:
            logger.info(f"\nError Message: {return_login.retorno}")
            console.print(f"\nError Message: {return_login.retorno}", style="bold red")
            return return_login
        
        # # Identificando jenela principal
        app = Application().connect(class_name="TFrmEnviaEmailBoletaTitulo", backend="uia")
        main_window_envia_boletos = app["TFrmEnviaEmailBoletaTitulo"]
        main_window_envia_boletos.set_focus()


        #Seleciona "Sim" na fatura
        main_window_envia_boletos.child_window(class_name="TRadioButton", title="Sim").click()

        #Seleciona tipo de cobrança
        main_window_envia_boletos.child_window(class_name="TDBIEditCode", found_index=1).type_keys("4044{TAB}")

        #Selecionando Modelo
        main_window_envia_boletos.child_window(class_name="TDBIComboBox", found_index=0).click()
        pyautogui.press("down", presses=7, interval=0.1)
        pyautogui.hotkey("enter")
        pyautogui.hotkey("tab")

        #Selecionando "Somente Não Enviados"
        main_window_envia_boletos.child_window(class_name="TDBICheckBox", found_index=6).click()
        #Selecionando "Enviar XML e PDF do NF-e"
        main_window_envia_boletos.child_window(class_name="TDBICheckBox", found_index=3).click()
        #Selecionando "Cupom Fiscal"
        main_window_envia_boletos.child_window(class_name="TDBICheckBox", found_index=13).click()

        #Selecionando "Enviar Resumo da Fatura"
        main_window_envia_boletos.child_window(class_name="TDBICheckBox", found_index=5).click()
        
        await worker_sleep(6)
        try:
            app = Application().connect(class_name="TMessageForm", backend="uia", title="Confirm")
            window_template = app["TMessageForm"]
            window_template.set_focus()
            await worker_sleep(2)
            #Clica em "No" no aviso
            window_template.child_window(title="&No", class_name="TButton").click()
            pyautogui.click(1002, 561)
            await worker_sleep(2)
            #Clica em Detalhamento da Fatura
            pyautogui.click(916, 457)
            await worker_sleep(2)
            #Clica em Ok na janelinha de detalhamento
            pyautogui.click(1046, 556)
            await worker_sleep(2)
        except Exception as ex:
            log_msg = f"Erro ao identificar a janela Resumo da fatura: {str(ex)}"
            console.print(log_msg, style="bold red")
            return RpaRetornoProcessoDTO(sucesso=False, retorno=log_msg, status=RpaHistoricoStatusEnum.Falha, tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)])
        

        #Digita Periodo de Emissão
        # Data atual
        data_atual = datetime.now()
        # Data(8 dias atrás)
        start_date = data_atual - timedelta(days=8)
        # start_date = '10/01/2024'
        # end_date = '01/02/2025'
        # Data(1 dia atrás)
        end_date = data_atual - timedelta(days=1)
        main_window_envia_boletos.child_window(class_name="TDBIEditDate", found_index=1).type_keys(f"{start_date:%d/%m/%Y}")
        # main_window_envia_boletos.child_window(class_name="TDBIEditDate", found_index=1).set_edit_text("")
        await worker_sleep(1)
        # main_window_envia_boletos.child_window(class_name="TDBIEditDate", found_index=1).type_keys(f"{start_date}", pause=0.2)
        # pyautogui.hotkey("tab")
        main_window_envia_boletos.child_window(class_name="TDBIEditDate", found_index=0).type_keys(f"{end_date:%d/%m/%Y}")
        # main_window_envia_boletos.child_window(class_name="TDBIEditDate", found_index=0).set_edit_text("")
        # main_window_envia_boletos.child_window(class_name="TDBIEditDate", found_index=0).type_keys(f"{end_date}", pause=0.2) 
        await worker_sleep(2)   

        #Clica em Pesquisar
        pyautogui.click(602, 588)
        await worker_sleep(5)

        #Deseja selecionar as empresas para pesquisa?
        try:
            app = Application().connect(class_name="TMessageForm", backend="uia", title="Confirm")
            window_company_select = app["TMessageForm"]
            window_company_select.set_focus()
            window_company_select.child_window(title="&Yes", class_name="TButton").click()
            await worker_sleep(5)

            app = Application().connect(class_name="TFrmSelecionaEmpresas", backend="uia", title="Seleção de Empresas")
            window_company_select = app["TFrmSelecionaEmpresas"]
            if window_company_select.exists():
                window_company_select.set_focus()
                pyautogui.click(720, 623)
                await worker_sleep(5)
                pyautogui.click(1092, 658)
                await worker_sleep(2)
        except Exception as ex:
            log_msg = f"Erro ao identificar a janela de empresas: {str(ex)}"
            console.print(log_msg, style="bold red")
            return RpaRetornoProcessoDTO(sucesso=False, retorno=log_msg, status=RpaHistoricoStatusEnum.Falha, tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)])
        
        #Aguarda botão pesqiusar inativar
        current_try = 0
        max_try = 10
        while current_try < max_try:
            try:
                pyautogui.locateOnScreen(ASSETS_BASE_PATH + 'envio_docs_b2b_pesquisar_desabilitado.png', confidence=0.9)
                break
            except Exception as e:
                await worker_sleep(20)
                current_try += 1
                continue
        
        if current_try >= max_try:
            log_msg = f"Numero máximo de tentativas para verificar o botão pesquisar desabilitado excedidas"
            console.print(log_msg, style="bold red")
            return RpaRetornoProcessoDTO(sucesso=False, retorno=log_msg, status=RpaHistoricoStatusEnum.Falha, tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)])

        # #Clica em Pesquisar
        # pyautogui.click(602, 588)
        # await worker_sleep(5)   

        #Desmarca titulos sem Nosso Número gerado
        #Clica para selecionar todos registros
        pyautogui.click(970,580)

        #Filtra registros para aparecerem em ordem
        pyautogui.click(700,680)
        await worker_sleep(2)

        pyautogui.click(615, 700)
        #Vai para o primeiro item
        with pyautogui.hold('ctrl'):
            pyautogui.hotkey('home')
        pyautogui.hotkey('home')

        pyautogui.PAUSE = 0.3
        while True:
            try:
                console.print("[green]Copiando Linha")
                with pyautogui.hold('ctrl'):
                    pyautogui.press('c')

                win32clipboard.OpenClipboard()
                actual_line = win32clipboard.GetClipboardData()
                win32clipboard.CloseClipboard()

                if actual_line.split('\n')[1].split('\t')[2] == '':
                    console.print("[yellow]Desmarcando item para envio")
                    pyautogui.press('space')
                else:
                    console.print("[red]Encerrando o Loop")
                    break

                console.print("[yellow]Seguindo para próxima linha")
                pyautogui.press('down')

            except Exception as ex:
                log_msg = f"Erro ao marcar item: {str(ex)}"
                console.print(log_msg, style="bold red")
        
        #Envaindo emails
        pyautogui.click(700, 585)

        #Deseja enviar boletos por email?
        await worker_sleep(15)
        try:
            app = Application().connect(class_name="TMessageForm", backend="uia", title="Information")
            window_boleto_email = app["TMessageForm"]
            window_boleto_email.set_focus()
            window_boleto_email.child_window(title="&Yes", class_name="TButton").click()
            #pyautogui.click(915, 560)
            await worker_sleep(12)
        except Exception as ex:
            log_msg = f"Erro ao achar janela de confirmação de envio de emails: {str(ex)}"
            console.print(log_msg, style="bold red")
            return RpaRetornoProcessoDTO(sucesso=False, retorno=log_msg, status=RpaHistoricoStatusEnum.Falha, tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)])
        
        #Deseja marcar boletos enviados como impressos
        try: 
            app = Application().connect(class_name="TMessageForm", backend="uia", title="Confirm")
            window_boleto_email = app["TMessageForm"]
            window_boleto_email.set_focus()
            window_boleto_email.child_window(title="&Yes", class_name="TButton").click()
            pyautogui.click(915, 560)
            await worker_sleep(12)
        except Exception as ex:
            log_msg = f"Erro ao achar janela de confirmação de envio de emails: {str(ex)}"
            console.print(log_msg, style="bold red")
            return RpaRetornoProcessoDTO(sucesso=False, retorno=log_msg, status=RpaHistoricoStatusEnum.Falha, tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)])
        
        await worker_sleep(15)
        sucesso = False
        while True:
            desktop = Desktop(backend="uia")
            try:
                # Tenta localizar a janela com o título que contém "Aguarde"
                window = desktop.window(title_re="Aguarde...")
                # Se a janela existe, continua monitorando
                if window.exists():
                    console.print(f"Janela 'Aguarde...' ainda aberta", style="bold yellow")
                    await worker_sleep(20)
                    continue
                else:
                    await worker_sleep(5)
                    # console.print(
                    #     f"Janela '{window_name}' foi fechada.", style="bold green"
                    # )
                    try:
                        # window_information = desktop.window(title_re="Infromation")
                        app = Application().connect(class_name="TMessageForm", backend="uia", title="Information")
                        window_information = app["TMessageForm"]
                        window_information.set_focus()
                        if window_information.exists():
                            console.print(f"Janela 'Information' aberta, processo finalizado.", style="bold yellow")
                            sucesso = True
                            break
                        else:
                            continue
                    except:
                        console.print(f"Janela 'Aguarde...' não existe mais.", style="bold green")
                        await worker_sleep(5)
                        break
                
                # return False  # Retorna falso pois a janela esta fechada
                # await worker_sleep(30)  # Espera 2 (* o multiplicador) segundos antes de verificar novamente
            except Exception as ex:
                log_msg= f"Erro ao verificar janela 'Aguarde...': {str(ex)}"
                console.print(log_msg, style="bold red")
                return RpaRetornoProcessoDTO(sucesso=False, retorno=log_msg, status=RpaHistoricoStatusEnum.Falha, tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)])

        if sucesso:
            return RpaRetornoProcessoDTO(sucesso=True, retorno="Processo de exportação dos documentos do portal B2B finalizado", status=RpaHistoricoStatusEnum.Sucesso)
        else:
            return RpaRetornoProcessoDTO(sucesso=False, retorno="Ocorreu um erro ao finalizar o processo de exportação dos documentos do portal B2B", status=RpaHistoricoStatusEnum.Falha, tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)])
    except Exception as ex:
        log_msg = f"Erro Processo Exportacao Docs Portal B2B: {str(ex)}"
        console.print(log_msg, style="bold red")
        return RpaRetornoProcessoDTO(
        sucesso=False, retorno=log_msg, status=RpaHistoricoStatusEnum.Falha, tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)])
    