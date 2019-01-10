from flask import Flask, redirect, render_template, request
from URL import URLFunctions
import json
from hash_store import HashURLStore

app = Flask(__name__)


@app.route("/")
def main():
    return redirect("/new")


@app.route("/new", methods=["GET", "POST"])
def hello():
    if request.method == "POST":
        print("POSTED!")
        try:
            print(request.json["data"])
            url_store = HashURLStore(request.json["data"])
            url_code = url_store.hash_url_store()
            return url_code
        except Exception as err:
            print("ERR", err)
            return json.dumps({"result": str(err)})
    return render_template("index.html")


@app.route("/<string:url_code>")
def url_render(url_code):
    base_url = URLFunctions(url_code).get_url()
    return redirect(base_url)


if __name__ == '__main__':
    app.run(debug=True)
