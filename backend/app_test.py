from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello_world():
    return '¡Hola! La configuración básica de Flask está funcionando correctamente.'

if __name__ == '__main__':
    app.run(debug=True)
