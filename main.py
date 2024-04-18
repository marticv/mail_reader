import utils
from objects.MessageBody import MessageBody
import params
import time

emailList = utils.get_text_from_email()

for email in emailList:
    list=utils.get_product_infos_from_text(email)
    num= utils.get_Mercado_number_from_text(email)
    body = MessageBody(num, list)
    utils.create_file_from_MessageBody(body, params.DESTINATION_FOLDER)
    time.sleep(1) #wait 1 second to avoid rewriting the file
