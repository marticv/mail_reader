
import params 
import utils
from objects.MessageBody import MessageBody
from objects.ProductInfo import ProductInfo


text= """
Proveedor información: Delaviuda Alimentacion, S.A(8410223000008)
Productos OK: 8
Productos KO: 1


DETALLE:
RESULTADO DE LA CARGA DE INFORMACIÓN ALIMENTARIA

Mercado: 724

08431876345582: KO
        Filename:8410223000008-PRICAT2AME-FILE-20231219T18422904899834_20231219_184224.zip
Error:101012301 -  Unselectable classification
08431876345575: OK
08431876345360: OK
08431876345391: OK
08431876345384: OK
08431876346459: OK
08431876346442: OK
08431876345551: OK
08431876345377: OK

"""



num =utils.get_Mercado_number_from_text(text)

list = utils.get_product_infos_from_text(text)
#for item in list:
#    print(item)

body = MessageBody(num, list)
print(body)

