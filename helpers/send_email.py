import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from decouple import config


def create_and_send_email(file, type_counts, total_lines):
    send_email_list = config("SEND_EMAIL_LIST")
    if "," in send_email_list:
        send_email_list = send_email_list.split(",")
    msg = config_email(send_email_list, file, type_counts, total_lines)
    send_email(msg, send_email_list)


def config_email(send_email_list, file, type_counts, total_lines):
    msg = MIMEMultipart()
    msg["From"] = config("USER")
    msg["To"] = ", ".join(send_email_list)
    msg["Subject"] = "Relação de Valores T2 Group"
    email_content = f"Prezado, Segue relação de valores da T2 Group:\nQuantidade de Linhas: {total_lines}\n"
    for type_value, count in type_counts.items():
        email_content += f"{type_value} - Quantidade: {count}\n"

    msg.attach(MIMEText(email_content, "plain"))
    with open(file, "rb") as attachment:
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())

    encoders.encode_base64(part)
    part.add_header(
        "Content-Disposition",
        f"attachment; filename= {file.split('/')[-1]}",
    )
    msg.attach(part)

    return msg


def send_email(msg, send_email_list):
    try:
        server = smtplib.SMTP(config("EMAIL_SERVER"), config("EMAIL_PORT"))
        server.starttls()
        server.login(config("USER"), config("EMAIL_PWD"))
        server.sendmail(config("USER"), send_email_list, msg=msg.as_string())
        server.quit()
    except Exception as e:
        print(f"erro - {e}")
