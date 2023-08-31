import smtplib, ssl

def create_mail(name,email,number,message):
    port = 465  # For SSL
    smtp_server = "smtp.gmail.com"
    #sender_email = "l20211959@tectijuana.edu.mx"  # Enter your address
    sender_email = "no.replyentryflow@gmail.com"
    receiver_email = "dev.entryflow@gmail.com"  # Enter receiver address
    password = "EntryFlow5000"
    #password = "xtwjhzidrgmqcrof"
    
    message = f"""
    Nombre: {name}
    Email: {email}
    Numero: {str(number)}
    Mensaje: {message}
    """
    context = ssl.create_default_context()

    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message)