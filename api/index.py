from flask import Flask, request, render_template, send_file
import random, json, functions
from functools import cache

app = Flask(__name__, template_folder="../web/templates", static_folder="../web/static")

# Initialise
with open("assets/bbcQuotes.json","r", encoding="utf8") as quoteFile:
    quotes = json.load(quoteFile)


@app.route('/')
def index():
    return render_template("index.html", title = "DebBoiAgru - Silly Willy")

@app.route('/house')
def house():
    return render_template("EndlessHouse.html")

@app.route('/laser')
def laser():
    return render_template("Laser.html")

@app.route('/calculator')
def calculator():
    return render_template("Calculator.html")

# Quote from the baby blue club
@app.route('/bbcquote')
def quote():
    raw = request.args.get('raw', "0")          # Either 1 or 0. Also 0 if not specified
    quote = random.choice(quotes)
    if raw == "1":
        return random.choice(quotes)
    else:
        return render_template("SimpleGUI.html", data = {"heading":quote["quote"], "content":quote["author"]})

# Discord rich embed
@app.route("/embed")
def dcembed():
    title = request.args.get("title")
    description = request.args.get("desc")
    name = request.args.get("name") # Top heading
    image = request.args.get("img")
    color = request.args.get("color")
    title_tag = f'<meta property="og:title" content="{title}">'
    desc_tag = f'<meta property="og:description" content="{description}">'
    name_tag = f'<meta property="og:site_name" content="{name}">'
    img_tag = f'<meta property="og:image" content="{image}">'
    clr_tag = f'<meta name="theme-color" content="#{color}">'
    out = f"""
{title_tag if title else "<!--no title-->"}
{img_tag if image else "<!--no image-->"}
{desc_tag if description else "<!--no description-->"}
{name_tag if name else "<!--no name-->"}
{clr_tag if color else "<!--no color-->"}
"""
    return render_template('Embed.html', data = out)

# Fizzbuzz as a service
@app.route("/fizzbuzz")
def fizzbuzz():
    try:
        n = int(request.args.get("n", 200))
    except ValueError:
        return {"error":"Requested number is not a number"}, 400
    if n > 5000:
        return {"error":"Requested number is too large"}, 400
    if n <= 0:
        return []
    # Simple fizzbuzz logic
    print(n)
    fb = []
    for i in range(1, n): fb.append ("FizzBuzz" if i%3==0 and i%5==0 else "Fizz" if i%3==0 else "Buzz" if i%5==0 else i)
    return fb

# Return ip address as an image
@app.route("/ip")
def ip():
    ip = request.headers.get("X-Real-IP", request.remote_addr)
    image = functions.CreateImage(ip)
    return send_file(f"../{image}", mimetype="image/png", download_name="ip.png")

if __name__ == '__main__':
    app.run(debug=True)