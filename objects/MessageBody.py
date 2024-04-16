from objects.ProductInfo import ProductInfo
#classe que tiene un atributo Mercado y una lista de objetos ProductInfo
class MessageBody:
    def __init__(self, mercado: int, product_infos: list['ProductInfo']):
        self.mercado = mercado
        self.product_infos = product_infos

    def __str__(self):
        return f"mercado: {self.mercado}, productuctos: {self.print_products}"