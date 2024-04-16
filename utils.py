from objects.ProductInfo import ProductInfo
import win32com.client

def get_Mercado_number_from_text(text: str) -> int:
    """Funcion que devuelve el mercado de un texto"""
    lines = text.splitlines()
    for line in lines:
        if line.startswith('Mercado:'):
            return int(line.split(':')[1])
        
def get_product_infos_from_text(text: str) -> list['ProductInfo']:
    """Funcion que devuelve una lista de objetos ProductInfo de un texto"""
    lines = text.splitlines()

    product_infos = []
    for line in lines:
        try:
            reference, state= line.split(':')
            reference = reference.strip()
            state = state.strip().split()[0]
            if state == 'OK':  # Get the first word (OK or KO)
                product_infos.append(ProductInfo(int(reference), state, None))
            else:
                errorname = "error no definido"
                product_infos.append(ProductInfo(int(reference), state, errorname))
        finally:
            continue
    return product_infos





def get_text_from_email():
#Get the conection
    outlook = win32com.client.Dispatch("Outlook.Application").GetNamespace("MAPI")
    inbox = outlook.GetDefaultFolder(6)  # 6 for inbox

    messages = inbox.Items
    unread_messages = messages.Restrict("[Unread]=True")  # getting only unread messages

    messages_count= len(unread_messages)

    if messages_count>0:
        for message in unread_messages:
                if message.SenderEmailAddress == params.SENDER:
                    print("Subject:", message.Subject)
                    print("Sender:", message.SenderName)
                    print("Received Time:", message.ReceivedTime)
                    print("senderMail:", message.SenderEmailAddress)

                    print("-----------------------------------")
            #        message.UnRead =False
    else:
        print("no hay mensajes pendientes ")


