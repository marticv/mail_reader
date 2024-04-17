import utils
from objects.MessageBody import MessageBody
from objects.ProductInfo import ProductInfo
import params




list = utils.get_text_from_email()

for item in list:
    num =utils.get_Mercado_number_from_text(item)
    lista = utils.get_product_infos_from_text(item)
    body = MessageBody(num, lista)
    

    print("Mercado: "+str(num))
    for list_item in lista:
        print(list_item)
    

    utils.create_file_from_MessageBody(body, params.DESTINATION_FOLDER)

