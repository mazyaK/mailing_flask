import pika
import smtplib
from logpas_from_mail import login, password

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.queue_declare(queue='mailing')

smtpObj = smtplib.SMTP('smtp.gmail.com', 587)
smtpObj.starttls()
smtpObj.login(login, password)


def callback(ch, method, properties, body):
    mail_to = str(body)[2:-1]
    smtpObj.sendmail(login, str(mail_to), "Sending a message via a website using RabbitMQ")


channel.basic_consume(queue='mailing',
                      auto_ack=True,
                      on_message_callback=callback)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
