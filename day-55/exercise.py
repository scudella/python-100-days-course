from flask import Flask

app = Flask(__name__)

def make_bold(function):
    def bold(*args, **kwargs):
        text = function(*args, **kwargs)
        return f'<b>{text}</b>'
    return bold

def make_emphasis(function):
    def emphasis(*args, **kwargs):
        text = function(*args, **kwargs)
        return f'<em>{text}</em>'
    return emphasis

def make_underlined(function):
    def underline(*args, **kwargs):
        text = function(*args, **kwargs)
        return f'<u>{text}</u>'
    return underline

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/bye")
@make_bold
@make_emphasis
@make_underlined
def bye():
    return "Bye!"

if __name__ == "__main__":
    app.run()