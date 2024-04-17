from objects.ProductInfo import ProductInfo
#classe que tiene un atributo Mercado y una lista de objetos ProductInfo
class MessageBody:
    def __init__(self, mercado: int, product_infos: list['ProductInfo']):
        self.mercado = mercado
        self.product_infos = product_infos
    
    #tostring devuelve un texto de una o mas lineas, y cada linea tiene el formato "mercado + | + ProductInfo"
    def __str__(self):
        text:str = ""
        for product_info in self.product_infos:
            text += str(self.mercado) + " | " + product_info.__str__()+"\n"

        return text