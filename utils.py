from objects.ProductInfo import ProductInfo
import win32com.client
import params
import datetime
from objects.MessageBody import MessageBody

def get_Mercado_number_from_text(text: str) -> int:
    # Split the text into lines. If line starts with "Mercado:", return the number after ":"
    lines = text.splitlines()
    for line in lines:
        if line.startswith('Mercado:'):
            try:
                return int(line.split(':')[1].strip())
            except (ValueError, IndexError, Exception):
                return -1
    return -1
            
def get_product_infos_from_text(text: str) -> list['ProductInfo']:
    #Spit the text in lines. If line start number return a ProductInfo
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



def get_text_from_email()->list[str]:
#Get the conection
    outlook = win32com.client.Dispatch("Outlook.Application").GetNamespace("MAPI")
    inbox = outlook.GetDefaultFolder(6)  # 6 for inbox

    messages = inbox.Items
    unread_messages = messages.Restrict("[Unread]=True")  # getting only unread messages

    messages_count= len(unread_messages)

    list = []

    if messages_count>0:
        for message in unread_messages:
            if message.SenderEmailAddress == params.SENDER:
                print("Subject:", message.Subject)
                print("Sender:", message.SenderName)
                print("Received Time:", message.ReceivedTime)
                print("senderMail:", message.SenderEmailAddress)
                print("-----------------------------------")
                list.append(message.body)
    else:
        print("no hay mensajes pendientes ")
    
    return list

#crea una funcion que pase un objeto MessageBody a un archivo .txt en la carpeta especificada  
def create_file_from_MessageBody(messageBody: MessageBody, destination_folder: str):
    #get the date and pass it to text
    
    now = datetime.datetime.now()
    date_text = now.strftime("%Y-%m-%d_%H%M%S")
    filename = f"mail_{date_text}.txt"

    #create the file
    with open(f"{destination_folder}/{filename}", "w") as file:
        file.write(messageBody.__str__())
    