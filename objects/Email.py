#crea la classe email, que tiene un campo sender (texto), un campo asumto (texto) y un campo body (texto)
class Email:
    """Clase que tiene un campo sender (texto), un campo asunto (texto) y un campo body (texto)"""
    def __init__(self, sender: str, asunto: str, body: str):
        self.sender = sender
        self.asunto = asunto
        self.body = body        

    def __str__(self):
        return f"{self.sender}\n{self.asunto}\n{self.body}"