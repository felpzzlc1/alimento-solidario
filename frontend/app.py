from flask import Flask, render_template

app = Flask(__name__, static_folder="static", template_folder="templates")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login.html")
def login():
    return render_template("login.html")

@app.route("/home.html")
def home():
    return render_template("home.html")

@app.route("/realizar-doacao.html")
def realizar_doacao():
    return render_template("realizar-doacao.html")

@app.route("/realizar-doacao-produto.html")
def realizar_doacao_produto():
    return render_template("realizar-doacao-produto.html")

@app.route("/realizar-doacao-produto-tipo.html")
def realizar_doacao_produto_tipo():
    return render_template("realizar-doacao-produto-tipo.html")

@app.route("/solicitar-doacao.html")
def solicitar_doacao():
    return render_template("solicitar-doacao.html")

@app.route("/visualizar-doacao.html")
def visualizar_doacao():
    return render_template("visualizar-doacao.html")

@app.route("/logout")
def logout():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)