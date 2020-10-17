from flask import request, render_template, json
from validate_email import validate_email
from flask_login import current_user

from app import app, channel

from accounts.models import User


@app.route('/')
def index():
    request_username = current_user
    return render_template('core/index.html', username=request_username)


channel.queue_declare(queue='mailing')


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
