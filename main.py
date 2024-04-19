import utils
from objects.MessageBody import MessageBody
import params
import time

"""
To use this script, you need to install the following libraries:
- win32com:
    pip install win32com
- Outlook with a connected account:
"""


"""
TODO:
- Filtrar solo correos necesarios (solo los que contengan mercado) -> done
- Filtrar por fecha
- Marcar como leido despues de leer
- Conecar sin necesidad de outlook
"""

emailList = utils.get_text_from_email()

for email in emailList:
    
    mercado_num= utils.get_Mercado_number_from_text(email)

    if mercado_num>0: #get only useful mails
        list=utils.get_product_infos_from_text(email)
        body = MessageBody(mercado_num, list)
        utils.create_file_from_MessageBody(body, params.DESTINATION_FOLDER)
        time.sleep(1) #wait 1 second to avoid rewriting the file
