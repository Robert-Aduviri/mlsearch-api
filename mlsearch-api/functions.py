from flask import Flask

app = Flask(__name__)

@app.route('/')
def ping():
    return 'ML Search: It Works!'

if __name__ == '__main__':
    app.run()