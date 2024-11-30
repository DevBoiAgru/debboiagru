import random
import dotenv
import io
import sqlite3
import PIL.ImageDraw as ImageDraw
import PIL.Image as Image
import PIL.ImageFont as ImageFont
from flask import Flask, request, render_template, send_file, redirect, url_for
from datetime import datetime
dotenv.load_dotenv()

app = Flask(__name__, template_folder="../web/pages", static_folder="../web/static")

def get_quote(quote_id: int = None):
    """
    Retrieves a quote from the database.

    If quote_id is provided, the quote with that ID is retrieved. Otherwise, a random quote is chosen.

    :param quote_id: The ID of the quote to retrieve, or None to get a random quote
    :return: A tuple containing the ID, content, author username, and the timestamp
    """
    conn = sqlite3.connect('assets/quotes.db')
    cursor = conn.cursor()
    if quote_id:
        cursor.execute("SELECT * FROM quotes WHERE id = ?", (quote_id,))
    else:
        cursor.execute("SELECT * FROM quotes ORDER BY RANDOM() LIMIT 1")
    quote = cursor.fetchone()
    conn.close()
    return quote

@app.route('/')
def index():
    return render_template("index.html", title = "DebBoiAgru - Silly Willy")

# Quote from the baby blue club
@app.route('/bbcquote')
def fetchquote():
    quote_id = request.args.get('id')
    quote = get_quote(quote_id) if quote_id else get_quote()
    
    if quote is None:
        return render_template("quote.html", 
                               title = "Quote not found", 
                               heading = "Quote not found", 
                               content = f"No quote found with the given ID. <a href='{url_for('fetchquote')}'>Get a random quote instead</a>",
                               quote_id = ""
                               ), 404

    json_required = request.args.get('json')
    if json_required == "true":
        return {"id": quote[0], "quote": quote[1], "author": quote[2], "timestamp": quote[3]}
    else:
        return render_template("quote.html", 
                               title = "Quote from the baby blue club", 
                               heading = quote[1], 
                               content = "- " + quote[2],
                               quote_id = quote[0],
                               timestamp = datetime.fromisoformat(quote[3]).strftime('%d/%m/%Y (Source)')
                               )


# Discord rich embed
@app.route("/embed/rich")
def dcembed():
    title = request.args.get("title", "").replace('<', '')
    description = request.args.get("desc", "").replace('<', '')
    name = request.args.get("name", "").replace('<', '')
    image = request.args.get("img", "").replace('<', '')
    color = request.args.get("color", "").replace('<', '')

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
    return render_template('dcembed.html', data = out)

# Discord GIF gambling game
@app.route("/embed/slots")
def slots():
    # Get seed number from query
    seed = request.args.get("s")
    if not seed:
        return redirect(f"/embed/slots?s={random.randint(0, 10_000_000)}")

    random.seed(seed)
    # Draw the slots
    slot_img = Image.open("assets/slots.png")
    draw = ImageDraw.Draw(slot_img)
    font = ImageFont.truetype("assets/NotoEmoji-Regular.ttf", 50)
    default_objects = ["🧁","🍓","🍩", "👽", "🤖", "🏎️"]

    slot_coords = [(167, 135), (268, 135), (369, 135)]

    objects = default_objects
    for coord in slot_coords:
        draw.text(coord, random.choice(objects), (209, 15, 176), font=font)

    imgBytes = io.BytesIO()
    slot_img.save(imgBytes, format="PNG")
    imgBytes.seek(0)
    return send_file(imgBytes, mimetype="image/png")

# Redirect to /embed/slots with the random seed
@app.route("/embed/slots/<num>")
def slots2(num):
    return redirect(f"/embed/slots?s={num}")

# Fizzbuzz as a service
@app.route("/fizzbuzz")
def fizzbuzz():
    try:
        n = int(request.args.get("n", 50))
    except ValueError:
        return {"error":"Requested number is not a number"}, 400
    if n > 5000:
        return {"error":"Requested number is too large. Maximum is 5000"}, 400
    if n <= 0:
        return []
    # Simple fizzbuzz logic
    print(n)
    fb = []
    for i in range(1, n): fb.append ("FizzBuzz" if i%3==0 and i%5==0 else "Fizz" if i%3==0 else "Buzz" if i%5==0 else i)
    return fb


# Single page apps. Mostly for fun
@app.route('/house')
def house():
    return render_template("house.html")
@app.route('/laser')
def laser():
    return render_template("laser.html")
@app.route('/alien')
def alien():
    return render_template("alien.html")

if __name__ == '__main__':
    app.run(debug=True)