import random
import dotenv
import io
import PIL.ImageDraw as ImageDraw
import PIL.Image as Image
import PIL.ImageFont as ImageFont
import time

from flask import (
    Flask,
    Response,
    request,
    render_template,
    send_file,
    redirect,
    url_for,
)
from datetime import datetime

from utils.clock import ascii_num
from utils.quotes import get_quote

dotenv.load_dotenv()

app = Flask(__name__, template_folder="../web/pages", static_folder="../web/static")


@app.route("/")
def index():
    return render_template("index.html", title="DebBoiAgru - Silly Willy")


# Quote from the baby blue club
@app.route("/bbcquote")
def fetchquote():
    quote_id = request.args.get("id")
    quote = get_quote(quote_id) if quote_id else get_quote()

    if quote is None:
        return render_template(
            "quote.html",
            title="Quote not found",
            heading="Quote not found",
            content=f"No quote found with the given ID. <a href='{url_for('fetchquote')}'>Get a random quote instead</a>",
            quote_id="",
        ), 404

    json_required = request.args.get("json")
    if json_required == "true":
        return {
            "id": quote[0],
            "quote": quote[1],
            "author": quote[2],
            "timestamp": quote[3],
        }
    else:
        return render_template(
            "quote.html",
            title="Quote from the baby blue club",
            heading=quote[1],
            content="- " + quote[2],
            quote_id=quote[0],
            timestamp=datetime.fromisoformat(quote[3]).strftime("%d/%m/%Y (Source)"),
        )


# Discord rich embed
@app.route("/embed/rich")
def dcembed():
    title = request.args.get("title", "").replace("<", "")
    description = request.args.get("desc", "").replace("<", "")
    name = request.args.get("name", "").replace("<", "")
    image = request.args.get("img", "").replace("<", "")
    color = request.args.get("color", "").replace("<", "")

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
    return render_template("dcembed.html", data=out)


# Discord embed gambling game
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
    default_objects = ["🧁", "🍓", "🍩", "👽", "🤖", "🏎️"]

    slot_coords = [(167, 135), (268, 135), (369, 135)]

    objects = default_objects
    for coord in slot_coords:
        draw.text(coord, random.choice(objects), (209, 15, 176), font=font)

    imgBytes = io.BytesIO()
    slot_img.save(imgBytes, format="PNG")
    imgBytes.seek(0)
    return send_file(imgBytes, mimetype="image/png")


# Fizzbuzz as a service
@app.route("/fizzbuzz")
def fizzbuzz():
    try:
        n = int(request.args.get("n", 50))
    except ValueError:
        return {"error": "Requested number is not a number"}, 400
    if n > 5000:
        return {"error": "Requested number is too large. Maximum is 5000"}, 400
    if n <= 0:
        return []
    # Simple fizzbuzz logic
    fb = [
        f"Fizz"
        if i % 3 == 0 and i % 5 != 0
        else f"Buzz"
        if i % 5 == 0 and i % 3 != 0
        else f"FizzBuzz"
        if i % 3 == 0 and i % 5 == 0
        else i
        for i in range(1, n)
    ]
    return fb


# Terminal clock
@app.route("/clock")
def clock():
    # Check if the request is made with curl
    if not request.headers.get("User-Agent", "").lower().startswith("curl"):
        return "Curl it in the terminal!", 400

    def stream():
        clearScreen = "\033[H\033[J"
        while True:
            cur_time = f"{time.strftime('%H:%M:%S', time.gmtime())}"
            yield f"{clearScreen}{ascii_num(cur_time)}\nUTC\n"
            time.sleep(1)

    return Response(
        stream(), mimetype="text/event-stream", headers={"Cache-Control": "no-cache"}
    )


@app.route("/house")
def house():
    return render_template("house.html")


@app.route("/laser")
def laser():
    return render_template("laser.html")


@app.route("/embed/slots/<num>")
def slots2(num):
    return redirect(f"/embed/slots?s={num}")


if __name__ == "__main__":
    app.run(debug=True)
