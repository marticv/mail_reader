from objects.ProductInfo import ProductInfo
import win32com.client
import params
import datetime
from objects.MessageBody import MessageBody

def get_Mercado_number_from_text(text: str) -> int:
    """
    Get the Mercado number from the given text.

    Parameters:
        text (str): The text to extract the Mercado number from.

    Returns:
        int: The Mercado number extracted from the text. Returns -1 if no Mercado number is found.
    """
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
    lines= clean_emprty_lines_from_text(text)

    lines = lines.splitlines()

    product_infos = []
    reference = None
    state = None
    error_lines = []

    for line in lines:
        line= line.strip()
        if ':' in line:
            key, value = [elem.strip() for elem in line.split(':', 1)]
            if key.isdigit():
                if state == 'KO' and error_lines:
                    # Add the concatenated error message to the previous product info
                    product_infos[-1].errorname = ' '.join(error_lines)
                    error_lines = []

                reference = int(key)
                state = value.split()[0]
                if state == 'OK':
                    product_infos.append(ProductInfo(reference, state, None))
                else:
                    errorname = "error no definido"
                    product_infos.append(ProductInfo(reference, state, errorname))
            else:
                # Check if it's an error line following a 'KO'
                if state == 'KO':
                    error_lines.append(line.strip())
        elif state == 'KO' and error_lines:
            # Add the last error line to the previous product info
            error_lines.append(line.strip())
            product_infos[-1].errorname = ' '.join(error_lines)
            error_lines = []
    
    #if the last product info is still 'KO', add the 2 last error lines to it
    if product_infos and product_infos[-1].state == 'KO':
        product_infos[-1].errorname = ' '.join(error_lines[-2:])

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
            emails_json = []

            if message.SenderEmailAddress == params.SENDER:
                print("Subject:", message.Subject)
                print("Sender:", message.SenderName)
                print("Received Time:", message.ReceivedTime)
                print(message.body)
                print("-----------------------------------")
                list.append(str(message.body))

    else:
        print("no hay mensajes pendientes ")
    
    return list

def clean_emprty_lines_from_text(text: str) -> str:
    return '\n'.join([line for line in text.splitlines() if line.strip()])

#crea una funcion que pase un objeto MessageBody a un archivo .txt en la carpeta especificada  
def create_file_from_MessageBody(messageBody: MessageBody, destination_folder: str):
    #get the date and pass it to text
    
    now = datetime.datetime.now()
    date_text = now.strftime("%Y-%m-%d_%H%M%S")
    filename = f"mail_{date_text}.txt"

    #create the file
    with open(f"{destination_folder}/{filename}", "w") as file:
        file.write(messageBody.__str__())
