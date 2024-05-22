from objects.ProductInfo import ProductInfo
from objects.MessageBody import MessageBody
from objects.Email import Email
import win32com.client
import params
import datetime
import re
import imaplib
import email
from email.header import decode_header
from datetime import datetime,timezone
from email.message import Message


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
    messages = inbox.Items #Get the items
    unread_messages = messages.Restrict("[Unread]=True")  # getting only unread messages

    messages_count= len(unread_messages)
    list = []

    if messages_count>0:
        for message in unread_messages:
            if message.SenderEmailAddress == params.SENDER:
                #if message.Subject == params.TOPIC:    # Only when the subject is the one we need
                    print("Asunto:", message.Subject)
                    print("De:", message.SenderName)
                    print("Hora de recepción:", message.ReceivedTime)
                    print("-----------------------------------")
                    list.append(str(message.body))
    else:
        print("no hay mensajes pendientes ")
    
    return list

def get_email_list_from_Outlook()->list[Email]:
#Get the conection
    outlook = win32com.client.Dispatch("Outlook.Application").GetNamespace("MAPI")
    inbox = outlook.GetDefaultFolder(6)  # 6 for inbox
    messages = inbox.Items #Get the items
    unread_messages = messages.Restrict("[Unread]=True")  # getting only unread messages

    messages_count= len(unread_messages)
    list = []

    if messages_count>0:
        for message in unread_messages:
            if message.SenderEmailAddress == params.SENDER:
                #if message.Subject == params.TOPIC:    # Only when the subject is the one we need
                    print("Asunto:", message.Subject)
                    print("De:", message.SenderName)
                    print("Hora de recepción:", message.ReceivedTime)
                    print("-----------------------------------")
                    auxuliar_email = Email(message.SenderEmailAddress, message.Subject, message.ReceivedTime, message.body)
                    list.append(auxuliar_email)
    else:
        print("no hay mensajes pendientes ")
    
    return list

def clean_emprty_lines_from_text(text: str) -> str:
    return '\n'.join([line for line in text.splitlines() if line.strip()])


def create_file_from_MessageBody(messageBody: MessageBody, destination_folder: str):
    #get the date and pass it to text
    now = datetime.datetime.now()
    date_text = now.strftime("%Y-%m-%d_%H%M%S")
    filename = f"mail_{date_text}.csv"

    #create the file content
    with open(f"{destination_folder}/{filename}", "w") as file:
        file.write(messageBody.__str__())


def leer_correos_hotmail(usuario, contraseña):
    # Configuración de conexión IMAP para Hotmail
    imap_servidor = 'outlook.office365.com'
    puerto = 993
    
    # Conexión al servidor IMAP
    conexion = imaplib.IMAP4_SSL(imap_servidor, puerto)
    
    try:
        # Iniciar sesión y seleccionar la bandeja de entrada, despues seleccionar los correos no leidos
        conexion.login(usuario, contraseña)
        conexion.select('inbox')
        resultado, data = conexion.search(None, 'UNSEEN')
        
        # Recorrer los identificadores de los correos electrónicos
        for num in data[0].split():
            # Obtener el correo electrónico
            resultado, mensaje = conexion.fetch(num, '(RFC822)')
            raw_email = mensaje[0][1]
            email_message = email.message_from_bytes(raw_email)
            
            # Obtener los encabezados del correo electrónico
            remitente = email_message['From']
            asunto = email_message['Subject']
            fecha = email_message['Date']
            
            # Decodificar el asunto si es necesario
            if isinstance(asunto, bytes):
                asunto = decode_header(asunto)[0][0].decode()
            
            print('De:', remitente)
            print('Asunto:', asunto)
            print('Fecha:', fecha)
            # Si quieres ver el cuerpo del correo, puedes descomentar las siguientes líneas
            cuerpo = obtener_cuerpo_correo(email_message)
            print('Cuerpo:', cuerpo)
            
    finally:
        # Cerrar la conexión IMAP, no inverte el orden. ya que si cerramos la sesion primero, el servidor podria no recivir la info de cerrar la sesion
        # es una practica comun al trabajar con IMAP
        conexion.close()
        conexion.logout()

def leer_correos_no_leidos_outlook(usuario, contraseña):
    # Configuración de conexión IMAP para Outlook
    imap_servidor = 'outlook.office365.com'
    puerto = 993
    
    try:
        # Conexión al servidor IMAP
        conexion = imaplib.IMAP4_SSL(imap_servidor, puerto)
    
        # Iniciar sesión
        conexion.login(usuario, contraseña)
        
        # Seleccionar la bandeja de entrada
        conexion.select('inbox')
        
        # Buscar todos los correos electrónicos no leídos
        resultado, data = conexion.search(None, 'UNSEEN')
        
        # Recorrer los identificadores de los correos electrónicos no leídos
        for num in data[0].split():
            # Obtener el correo electrónico
            resultado, mensaje = conexion.fetch(num, '(RFC822)')
            raw_email = mensaje[0][1]
            email_message = email.message_from_bytes(raw_email)
            
            # Obtener los encabezados del correo electrónico
            remitente = email_message['From']
            asunto = email_message['Subject']
            fecha = email_message['Date']
            
            # Decodificar el asunto si es necesario
            if isinstance(asunto, bytes):
                asunto = decode_header(asunto)[0][0].decode()
            
            print('De:', remitente)
            print('Asunto:', asunto)
            
            # Si quieres ver el cuerpo del correo, puedes descomentar las siguientes líneas
            cuerpo = obtener_cuerpo_correo(email_message)
            print('Cuerpo:', cuerpo)
            # Cerrar la conexión
        conexion.close()
        conexion.logout()

    except Exception as e:
        print(e)

def obtener_correos_no_leidos(usuario: str, contraseña: str) -> list[str]:
    """
    Función que conecta a un servidor IMAP para leer correos de hotmail, busca correos electrónicos no leídos,
    obtiene el cuerpo de cada correo y los devuelve en una lista.

    Args:
        usuario (str): Nombre de usuario para el login.
        contraseña (str): Contraseña para el login.

    Returns:
        List[str]: Lista de cuerpos de los correos electrónicos no leídos.
    """
    # Configuración de conexión IMAP para Hotmail
    imap_servidor = 'imap-mail.outlook.com'
    puerto = 993
    
    # Conexión al servidor IMAP
    conexion = imaplib.IMAP4_SSL(imap_servidor, puerto)
    
    try:
        # Iniciar sesión
        conexion.login(usuario, contraseña)
        
        # Seleccionar la bandeja de entrada
        conexion.select('inbox')
        
        # Buscar todos los correos electrónicos no leídos
        resultado, data = conexion.search(None, 'UNSEEN')
        
        correos_no_leidos = []
        
        # Recorrer los identificadores de los correos electrónicos no leídos
        for num in data[0].split():
            # Obtener el correo electrónico
            resultado, mensaje = conexion.fetch(num, '(RFC822)')
            raw_email = mensaje[0][1]
            email_message = email.message_from_bytes(raw_email)

            #obtenemos datos
            asunto = email_message['Subject']
            remitente = email_message['From']
            
            # Obtener el cuerpo del correo electrónico
            cuerpo_correo = obtener_cuerpo_correo(email_message)
            print("Asunto:", asunto)
            print("Remitente:", remitente)
            print("-------------------------------")
            #testMail = Email(remitente, asunto, cuerpo_correo)
            #print(testMail)
            #print("-----------------------------------")
            correos_no_leidos.append(cuerpo_correo)
            
            # Marcar el correo como no leído nuevamente
            #conexion.store(num, '-FLAGS', '\\Seen')
            
    finally:
        # Cerrar la conexión
        conexion.close()
        conexion.logout()
        
    return correos_no_leidos

# Función auxiliar para obtener el cuerpo del correo electrónico




def obtener_cuerpo_correo(email_message: Message) -> str:
    """
    Obtiene el cuer de un correo electrónico.

    Args:
        email_message (Message): El mensaje del correo electrónico.

    Returns:
        str: El cuer del correo electrónico.
    """
    cuer = ''
    if email_message.is_multipart():
        for part in email_message.walk():
            content_type = part.get_content_type()
            if content_type == "text/plain":
                cuer += part.get_payload(decode=True).decode(part.get_content_charset(), 'ignore')
    else:
        cuer = email_message.get_payload(decode=True).decode(email_message.get_content_charset(), 'ignore')
    return cuer

def obtener_lista_mails(usuario: str, contraseña: str) -> list[Email]:
    """
    Función que conecta a un servidor IMAP, busca correos electrónicos no leídos,
    obtiene el cuerpo de cada correo y los devuelve en una lista.

    Args:
        usuario (str): Nombre de usuario para el login.
        contraseña (str): Contraseña para el login.

    Returns:
        List[str]: Lista de cuerpos de los correos electrónicos no leídos.
    """
    # Configuración de conexión IMAP para Hotmail
    imap_servidor = 'imap-mail.outlook.com'
    puerto = 993
    
    # Conexión al servidor IMAP
    conexion = imaplib.IMAP4_SSL(imap_servidor, puerto)
    
    try:
        # Iniciar sesión
        conexion.login(usuario, contraseña)
        
        # Seleccionar la bandeja de entrada
        conexion.select('inbox')
        
        # Buscar todos los correos electrónicos no leídos
        resultado, data = conexion.search(None, 'UNSEEN')
        
        correos_no_leidos = []
        
        # Recorrer los identificadores de los correos electrónicos no leídos
        for num in data[0].split():
            # Obtener el correo electrónico
            resultado, mensaje = conexion.fetch(num, '(RFC822)')
            raw_email = mensaje[0][1]
            email_message = email.message_from_bytes(raw_email)

            #obtenemos datos
            asunto = email_message['Subject']
            remitente = email_message['From']
            fecha = email_message['Date']

            #cadena = remitente
            remitente = re.search(r'[\w\.-]+@[\w\.-]+', remitente).group()
                        
            # Obtener el cuerpo del correo electrónico
            cuerpo_correo = obtener_cuerpo_correo(email_message)
            testMail = Email(remitente, asunto, fecha, cuerpo_correo)
            correos_no_leidos.append(testMail)
            
            # Marcar el correo como no leído nuevamente
            conexion.store(num, '-FLAGS', '\\Seen')
            
    finally:
        # Cerrar la conexión
        conexion.close()
        conexion.logout()
        
    return correos_no_leidos




def get_last_proceced_date_from_file() -> str:
    last_date_text = ''
    try:
        with open(params.LAST_DATE_ARCHIVE_ROUTE, "r") as file:
            last_date_text = file.read()
            print(last_date_text)
    except Exception as e:
        print(e)
    return last_date_text

def write_last_proceced_date(date: str) -> None:
    try:
        with open(params.LAST_DATE_ARCHIVE_ROUTE, "w") as file:
            file.write(date)
    except Exception as e:
        print(e)

def compare_dates(date1: str, date2: str) -> str:
    format = "%Y-%m-%d %H:%M:%S.%f%z"

    date1_to_datetime = datetime.strptime(date1, format).astimezone(timezone.utc)
    date2_to_datetime = datetime.strptime(date2, format).astimezone(timezone.utc)

    if date1_to_datetime > date2_to_datetime:
        return date1
    else:
        return date2
