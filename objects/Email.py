class Email:
    """Clase que tiene un campo sender (texto), un campo asunto (texto) y un campo body (texto)"""
    def __init__(self, sender: str, subject: str, date:str, body: str):
        self.sender = sender
        self.asunto = subject
        self.fecha = date
        self.body = body        

    def __str__(self):
        return f"{self.sender}\n{self.asunto}\n{self.body}"
