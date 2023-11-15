from flask import Flask
from threading import Thread


app = Flask('')

@app.route('/')
def home():
    return 'keep me alive'


def run():  # spin a web server up, keep pinging it with uptimerobot to keep bot alive
    app.run(host='0.0.0.0', port=8080)


def persist():
    t = Thread(target=run)
    t.start()
