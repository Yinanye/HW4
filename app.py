from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return "hello world"

@app.route('yinan')
def yinan():
    return "hello yinan!"

if __name__ == '__main__':
    app.run(debug=True)
