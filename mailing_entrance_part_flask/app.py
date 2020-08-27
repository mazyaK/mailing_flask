import pika
import sys
from flask import Flask, render_template, json, request
from validate_email import validate_email


app = Flask(__name__)

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.queue_declare(queue='mailing')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/check_mail', methods=['GET', 'POST'])
def check_mail():
    mail = request.form['mail']
    mail_status = validate_email(mail)
    if mail_status:
        message = mail
        channel.basic_publish(exchange='',
                              routing_key='mailing',
                              body=message)
        print(f" [x] Sent mail: {message}")

    return json.dumps({'mail_status': validate_email(mail, verify=True)})


if __name__ == '__main__':
    app.run(debug=True)
