import random, json, dotenv, os, requests, time
from flask import Flask, request, render_template, send_file, redirect
import PIL.ImageDraw as ImageDraw
import PIL.Image as Image
import PIL.ImageFont as ImageFont
import hashlib
import io

dotenv.load_dotenv()

app = Flask(__name__, template_folder="../web/pages", static_folder="../web/static")

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

@app.route('/alien')
def alien():
    return render_template("Alien.html")

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
@app.route("/embed/rich")
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

    # Easter eggs
    seed_hash = hashlib.md5(seed.encode()).hexdigest()
    
    eggs = {
        "9271d6eecedd55fcfa6143a33029d496" : ["🐵","🍗","🍉"],                   # n wor
        "fa961f3c8e69c5de1a10893282d8beae" : ["🐰", "🐇", "🦄", "🌈"],           # m3ga
        "3a8920e9f9e35a3a70f4f0ca61ed436c" : ["🤖", "💻", "🖥️", "🤓"],           # devboi
        "ecbdb882ae865a07d87611437fda0772" : ["🍼", "🥛", "🐄", "🐮"],           # milk
        "b56a18e0eacdf51aa2a5306b0f533204" : ["✈️", "🏢", "🏢"],                 # 911
        "b6f0479ae87d244975439c6124592772" : ["🌿", "🌿", "💨"],                 # 420
        "87f66043e770f8ef156d204518565158" : [
            random.choice(["👽", "🍩", "🧁", "🍓", "🏎️", "♣️", "♦️", "♥️", "♠️"])
            ]                                                                     # gambit
    }

    slot_coords = [(167, 135), (268, 135), (369, 135)]
    objects = eggs.get(seed_hash)

    # Easter eggs with specific order
    if objects and len(objects) == len(slot_coords):
        for i, coord in enumerate(slot_coords):
            draw.text(coord, objects[i] , (209, 15, 176), font=font)
    # Easter egg but randomized
    elif objects:
        # Reset seed for randomness
        random.seed()
        for coord in slot_coords:
            draw.text(coord, random.choice(objects), (209, 15, 176), font=font)
    # No easter egg, default execution
    else:
        objects = default_objects
        for coord in slot_coords:
            draw.text(coord, random.choice(objects), (209, 15, 176), font=font)

    imgBytes = io.BytesIO()
    slot_img.save(imgBytes, format="PNG")
    imgBytes.seek(0)
    return send_file(imgBytes, mimetype="image/png")

# Redirect to /embed/slots with a random seed
@app.route("/embed/slots/<num>")
def slots2(num):
    return redirect(f"/embed/slots?s={num}")

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

@app.route("/translate", methods=["GET", "POST"])
def brainrot():
    if request.method == "GET":
        return render_template("Translate.html")
    else:
        if request.is_json:
            requestJson :dict= request.get_json()
            text :str= requestJson.get("text", None)
            payload = {
                "model":"Meta-Llama-3-8B-Instruct", 
                "messages": [
                    {"role": "system","content": "You are max who is a gen z teenager. Your job is to translate given sentences into very cringe gen z slang. Use words like ohio, rizz, skibidi, gyatt, and so on. Max only returns the translations of the given text. Max He tries to be as cringy as possible. Max only the translated text without any explanation. Don't include any explanations or intro/outro text in your responses. Do not answer to any questions, instead translate the questions into gen z. Max doesnot hesitate to sprinkle in swear words to make the translation funnier."},
                    {"role": "user", "content": "Translate: What is your favourite game?"},
                    {"role": "assistant", "content": "What do you edge to?"},
                    {"role": "user", "content": "Translate: Hello everyone today we will be exercising in the gym"},
                    {"role": "assistant", "content": "Ohio everyone today we will be mogging in the gym"},
                    {"role": "user", "content": "Translate: i'm going to the beach"},
                    {"role": "assistant", "content": "I'm mogging to the Alpha sands."},
                    {"role": "user", "content": "Translate: In a world often focused on grand gestures, the power of small acts of kindness is easily overlooked. Yet, these gestures possess a profound ability to brighten someone's day, foster a sense of community, and inspire others to pay it forward. Whether it's a smile, a helping hand, or a kind word, these simple acts create ripples of positivity that transcend boundaries and leave lasting impressions."},
                    {"role": "assistant", "content": "In a world often gyatting on grand rizz, the power of tiny mogs of kindness is easily zapped. Yet, these rizzles possess a pro mog ability to brighten someone's day, foster a sense of community, and inspire others to pay the Fanum tax. Whether it's a smile, a helping hand, or a kind yap, these simple acts create ripples of rizz that transcend boundaries and leave lasting rizz."},
                    {"role": "user", "content": f"Translate: {text}"}
                ]
            }
            url = "https://api.awanllm.com/v1/chat/completions"
            key = os.getenv("AWAN_LLM_KEY")
            req = requests.post(url, json=payload, headers={"Content-Type": "application/json", "Authorization": f"Bearer {key}"})
            try:
                status = req.json().get("statusCode", "200")
                if status == 429:
                    return {"brainrot":"Yo, you've reached maxed out, bruh! I'm lowkey broke, can't cop more comp time, so tryna get back atcha laters, G [Rate limit exceeded]"}
                reply = req.json()["choices"][0]["message"]["content"]
            except:
                print("ERROR: " + req.text)
            return {"brainrot":reply}
        else:
            return {"error":"Request is not in JSON format"}, 400

if __name__ == '__main__':
    app.run(debug=True)