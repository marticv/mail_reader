#classe que tiene 3 campos, reference (string), state (string) y errorname (string)
class ProductInfo:
    def __init__(self, reference: int, state: str, errorname: str):
        self.reference = reference
        self.state = state
        self.errorname = errorname

    #añade una funcion tostring
    def __str__(self):
        return f"{self.reference},{self.state},{self.errorname}"