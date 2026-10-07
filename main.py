from flask import Flask, request, redirect, url_for, Response
import random

app = Flask(__name__)

# =========================
# اطلاعات بازیکن
# =========================

player_name = "بازیکن"
character = "🏹 شکارچی جنگل"

coins = 100
health = 100
score = 0

inventory = []
treasures = []
completed_missions = []

# =========================
# شخصیت‌ها
# =========================

characters = {
    "hunter": {
        "name": "🏹 شکارچی جنگل",
        "power": "حمله از فاصله",
        "health": 100
    },
    "warrior": {
        "name": "⚔️ جنگجوی باستانی",
        "power": "قدرت شمشیر",
        "health": 120
    },
    "explorer": {
        "name": "🧭 کاوشگر جزیره",
        "power": "کشف گنج",
        "health": 105
    },
    "guardian": {
        "name": "🛡️ نگهبان باستانی",
        "power": "دفاع قوی",
        "health": 140
    }
}

# =========================
# مناطق جهان
# =========================

regions = {

    "jungle": {
        "name": "🌴 جنگل گمشده",
        "description": "جنگلی مرموز با رودخانه، حیوانات وحشی و گنج‌های پنهان.",
        "enemy": "🐊 نگهبان جنگل",
        "treasure": "💎 الماس سبز",
        "season": "🌧️ فصل بارانی",
        "difficulty": "متوسط",
        "reward": 40
    },

    "island": {
        "name": "🏝️ جزیره باستانی",
        "description": "جزیره‌ای ناشناخته با خرابه‌های قدیمی و آثار تمدن باستانی.",
        "enemy": "⚔️ جنگجوی باستانی",
        "treasure": "👑 تاج گمشده",
        "season": "☀️ تابستان",
        "difficulty": "سخت",
        "reward": 70
    },

    "mountain": {
        "name": "🏔️ کوهستان",
        "description": "کوهستان سرد و خطرناک با مسیرهای مخفی و گنج‌های یخی.",
        "enemy": "🐺 نگهبان کوه",
        "treasure": "💎 سنگ آبی",
        "season": "❄️ زمستان",
        "difficulty": "سخت",
        "reward": 60
    },

    "desert": {
        "name": "🏜️ سرزمین خشک",
        "description": "سرزمینی گرم با معابد قدیمی و گنج‌های دفن‌شده.",
        "enemy": "🐍 نگهبان صحرا",
        "treasure": "🏺 گنج باستانی",
        "season": "🔥 تابستان داغ",
        "difficulty": "متوسط",
        "reward": 50
    }
}

# =========================
# فروشگاه
# =========================

items = {
    "sword": {
        "name": "⚔️ شمشیر باستانی",
        "price": 50
    },

    "bow": {
        "name": "🏹 کمان قدیمی",
        "price": 70
    },

    "shield": {
        "name": "🛡️ سپر جنگی",
        "price": 40
    }
}

# =========================
# قالب صفحه
# =========================

def page(title, content):

    return f"""
<!DOCTYPE html>

<html lang="fa" dir="rtl">

<head>

<meta charset="UTF-8">

<meta name="viewport"
content="width=device-width, initial-scale=1.0">

<meta name="theme-color"
content="#177245">

<link rel="manifest"
href="/manifest.webmanifest">

<title>{title}</title>

<style>

* {{
    box-sizing: border-box;
}}

body {{
    margin: 0;
    font-family: Tahoma, Arial, sans-serif;

    background:
    linear-gradient(
        rgba(0,0,0,.58),
        rgba(0,0,0,.78)
    ),
    radial-gradient(
        circle at top,
        #185c3b,
        #06100b 75%
    );

    color: white;
    min-height: 100vh;
}}

.container {{
    width: 94%;
    max-width: 900px;
    margin: auto;
    padding: 18px 0 50px;
}}

h1 {{
    text-align: center;
    font-size: 30px;
    margin: 10px 0 22px;
}}

h2 {{
    text-align: center;
}}

.card {{
    background: rgba(255,255,255,.09);
    border: 1px solid rgba(255,255,255,.15);

    border-radius: 20px;

    padding: 20px;

    margin: 15px 0;

    box-shadow:
    0 10px 30px rgba(0,0,0,.35);
}}

.grid {{
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 13px;
}}

button,
.btn {{
    display: block;
    width: 100%;

    border: 0;
    border-radius: 14px;

    padding: 15px;

    margin: 10px 0;

    font-size: 17px;
    font-weight: bold;

    text-decoration: none;
    text-align: center;

    color: white;

    background:
    linear-gradient(
        135deg,
        #177245,
        #0b4a2d
    );

    cursor: pointer;
}}

.btn2 {{
    background:
    linear-gradient(
        135deg,
        #76501a,
        #a16b1d
    );
}}

.btn3 {{
    background:
    linear-gradient(
        135deg,
        #344b60,
        #182735
    );
}}

input {{
    width: 100%;

    padding: 15px;

    border-radius: 12px;

    border: 1px solid #777;

    margin: 8px 0;

    font-size: 17px;

    text-align: center;
}}

.stat {{
    display: flex;
    justify-content: space-between;

    background: rgba(0,0,0,.30);

    padding: 12px;

    border-radius: 12px;

    margin: 8px 0;
}}

.big {{
    font-size: 60px;
    text-align: center;
}}

.center {{
    text-align: center;
}}

.small {{
    color: #c8d7cc;
    line-height: 1.9;
}}

.badge {{
    display: inline-block;

    padding: 7px 12px;

    border-radius: 20px;

    background:
    rgba(255,255,255,.12);

    margin: 4px;
}}

.success {{
    background:
    rgba(30,130,70,.25);

    border:
    1px solid rgba(60,220,120,.35);
}}

.warning {{
    background:
    rgba(170,110,20,.25);

    border:
    1px solid rgba(240,180,50,.35);
}}

</style>

</head>

<body>

<div class="container">

{content}

</div>

</body>

</html>
"""


# =========================
# صفحه اصلی
# =========================

@app.route("/")
def home():

    content = f"""

<h1>🌍 NEXORA WORLD</h1>

<div class="card center">

<div class="big">🌎</div>

<h2>دنیای ماجراجویی</h2>

<p class="small">

به دنیای NEXORA خوش آمدی.

در سرزمین‌های مختلف سفر کن،
مأموریت انجام بده،
با دشمنان روبه‌رو شو،
گنج پیدا کن و قدرت بگیر.

</p>

</div>

<div class="card">

<div class="stat">
<span>👤 بازیکن</span>
<span>{player_name}</span>
</div>

<div class="stat">
<span>🧝 شخصیت</span>
<span>{character}</span>
</div>

<div class="stat">
<span>❤️ سلامتی</span>
<span>{health}</span>
</div>

<div class="stat">
<span>🪙 سکه</span>
<span>{coins}</span>
</div>

<div class="stat">
<span>⭐ امتیاز</span>
<span>{score}</span>
</div>

<div class="stat">
<span>💎 گنج‌ها</span>
<span>{len(treasures)}</span>
</div>

</div>

<div class="grid">

<a class="btn" href="/play">
🎮 شروع بازی
</a>

<a class="btn" href="/map">
🗺️ نقشه جهان
</a>

<a class="btn btn2" href="/missions">
🎯 مأموریت‌ها
</a>

<a class="btn btn2" href="/shop">
🏪 فروشگاه
</a>

<a class="btn btn3" href="/characters">
🧝 شخصیت‌ها
</a>

<a class="btn btn3" href="/profile">
👤 پروفایل
</a>

</div>

"""

    return page("NEXORA WORLD", content)


# =========================
# شروع بازی
# =========================

@app.route("/play")
def play():

    content = f"""

<h1>🎮 ماجراجویی</h1>

<div class="card center">

<div class="big">🗺️</div>

<h2>{player_name}</h2>

<p>
شخصیت تو:
<b>{character}</b>
</p>

<p class="small">

جهان NEXORA آماده است.

یک منطقه را انتخاب کن
و مأموریت خودت را شروع کن.

</p>

<a class="btn" href="/map">
🗺️ نقشه جهان
</a>

<a class="btn btn2" href="/missions">
🎯 مأموریت‌ها
</a>

<a class="btn btn3" href="/">
🏠 خانه
</a>

</div>

"""

    return page("بازی", content)


# =========================
# نقشه
# =========================

@app.route("/map")
def world_map():

    cards = ""

    for key, region in regions.items():

        cards += f"""

<div class="card">

<h2>{region["name"]}</h2>

<p class="small">
{region["description"]}
</p>

<span class="badge">
👾 {region["enemy"]}
</span>

<span class="badge">
💎 {region["treasure"]}
</span>

<span class="badge">
{region["season"]}
</span>

<span class="badge">
⚔️ {region["difficulty"]}
</span>

<a class="btn" href="/region/{key}">
🚶 ورود به منطقه
</a>

</div>

"""

    content = f"""

<h1>🗺️ نقشه جهان</h1>

<div class="card center">

<p class="small">

چهار سرزمین بزرگ در انتظار تو هستند.

هر منطقه دشمن، گنج،
آب‌وهوا و مأموریت مخصوص خودش را دارد.

</p>

</div>

{cards}

<a class="btn btn3" href="/">
🏠 بازگشت
</a>

"""

    return page("نقشه جهان", content)


# =========================
# منطقه
# =========================

@app.route("/region/<region_key>")
def region(region_key):

    if region_key not in regions:
        return redirect(url_for("world_map"))

    r = regions[region_key]

    content = f"""

<h1>{r["name"]}</h1>

<div class="card center">

<div class="big">
🗺️
</div>

<h2>منطقه کشف‌شده</h2>

<p class="small">
{r["description"]}
</p>

<div class="stat">
<span>👾 دشمن</span>
<span>{r["enemy"]}</span>
</div>

<div class="stat">
<span>💎 گنج</span>
<span>{r["treasure"]}</span>
</div>

<div class="stat">
<span>🌦️ فصل</span>
<span>{r["season"]}</span>
</div>

<div class="stat">
<span>⚔️ سختی</span>
<span>{r["difficulty"]}</span>
</div>

<div class="stat">
<span>🪙 پاداش</span>
<span>{r["reward"]} سکه</span>
</div>

<a class="btn" href="/mission/{region_key}">
🎯 شروع مأموریت
</a>

<a class="btn btn2" href="/map">
🗺️ نقشه
</a>

</div>

"""

    return page(r["name"], content)


# =========================
# لیست مأموریت‌ها
# =========================

@app.route("/missions")
def missions():

    cards = ""

    for key, r in regions.items():

        completed = key in completed_missions

        if completed:
            status = "✅ انجام شده"
            button = f"""
<a class="btn btn3" href="/region/{key}">
🔎 مشاهده منطقه
</a>
"""
        else:
            status = "🎯 آماده انجام"
            button = f"""
<a class="btn" href="/mission/{key}">
🚀 شروع مأموریت
</a>
"""

        cards += f"""

<div class="card">

<h2>{r["name"]}</h2>

<p>
👾 دشمن:
{r["enemy"]}
</p>

<p>
💎 جایزه:
{r["treasure"]}
</p>

<p>
🪙 پاداش:
{r["reward"]} سکه
</p>

<p>
<b>{status}</b>
</p>

{button}

</div>

"""

    content = f"""

<h1>🎯 مأموریت‌ها</h1>

<div class="card center">

<p class="small">

مأموریت‌های مختلف را انجام بده،
گنج پیدا کن و امتیاز خودت را افزایش بده.

</p>

</div>

{cards}

<a class="btn btn3" href="/">
🏠 خانه
</a>

"""

    return page("مأموریت‌ها", content)


# =========================
# شروع مأموریت
# =========================

@app.route("/mission/<region_key>")
def mission(region_key):

    if region_key not in regions:
        return redirect(url_for("world_map"))

    r = regions[region_key]

    content = f"""

<h1>🎯 مأموریت</h1>

<div class="card center">

<div class="big">⚔️</div>

<h2>{r["name"]}</h2>

<p class="small">

ماموریت تو این است که
از منطقه عبور کنی،
با <b>{r["enemy"]}</b> روبه‌رو شوی
و به گنج <b>{r["treasure"]}</b> برسی.

</p>

<div class="stat">
<span>👾 دشمن</span>
<span>{r["enemy"]}</span>
</div>

<div class="stat">
<span>💎 گنج</span>
<span>{r["treasure"]}</span>
</div>

<div class="stat">
<span>🪙 پاداش</span>
<span>{r["reward"]}</span>
</div>

<a class="btn" href="/mission-result/{region_key}">
⚔️ ورود به مأموریت
</a>

<a class="btn btn3" href="/missions">
↩️ بازگشت
</a>

</div>

"""

    return page("شروع مأموریت", content)


# =========================
# نتیجه مأموریت
# =========================

@app.route("/mission-result/<region_key>")
def mission_result(region_key):

    global coins
    global score

    if region_key not in regions:
        return redirect(url_for("world_map"))

    r = regions[region_key]

    if region_key in completed_missions:

        content = f"""

<h1>🎯 مأموریت</h1>

<div class="card center warning">

<div class="big">ℹ️</div>

<h2>این مأموریت قبلاً انجام شده است.</h2>

<p>
گنج این منطقه را قبلاً پیدا کرده‌ای.
</p>

<a class="btn" href="/missions">
🎯 مأموریت‌ها
</a>

</div>

"""

        return page("مأموریت", content)

    # پاداش
    reward = r["reward"]

    bonus = random.randint(5, 20)

    total_reward = reward + bonus

    coins += total_reward
    score += 100

    inventory.append(r["treasure"])
    treasures.append(r["treasure"])
    completed_missions.append(region_key)

    content = f"""

<h1>🏆 مأموریت موفق</h1>

<div class="card center success">

<div class="big">💎</div>

<h2>مأموریت با موفقیت انجام شد!</h2>

<p class="small">

تو از منطقه عبور کردی
و گنج را پیدا کردی.

</p>

</div>

<div class="card">

<div class="stat">
<span>💎 گنج پیدا شده</span>
<span>{r["treasure"]}</span>
</div>

<div class="stat">
<span>🪙 پاداش منطقه</span>
<span>+{reward}</span>
</div>

<div class="stat">
<span>🎁 پاداش اضافی</span>
<span>+{bonus}</span>
</div>

<div class="stat">
<span>🪙 مجموع سکه</span>
<span>{total_reward}</span>
</div>

<div class="stat">
<span>⭐ امتیاز</span>
<span>+100</span>
</div>

</div>

<a class="btn" href="/missions">
🎯 مأموریت بعدی
</a>

<a class="btn btn2" href="/profile">
👤 پروفایل
</a>

<a class="btn btn3" href="/">
🏠 خانه
</a>

"""

    return page("مأموریت موفق", content)


# =========================
# شخصیت‌ها
# =========================

@app.route("/characters")
def characters_page():

    cards = ""

    for key, c in characters.items():

        cards += f"""

<div class="card center">

<div class="big">
{c["name"].split()[0]}
</div>

<h2>{c["name"]}</h2>

<p>
✨ قدرت:
{c["power"]}
</p>

<p>
❤️ سلامتی:
{c["health"]}
</p>

<a class="btn" href="/select-character/{key}">
انتخاب شخصیت
</a>

</div>

"""

    content = f"""

<h1>🧝 انتخاب شخصیت</h1>

{cards}

<a class="btn btn3" href="/">
🏠 خانه
</a>

"""

    return page("شخصیت‌ها", content)


# =========================
# انتخاب شخصیت
# =========================

@app.route("/select-character/<key>")
def select_character(key):

    global character
    global health

    if key in characters:

        character = characters[key]["name"]
        health = characters[key]["health"]

    return redirect(url_for("profile"))


# =========================
# پروفایل
# =========================

@app.route("/profile")
def profile():

    if inventory:
        inv = "، ".join(inventory)
    else:
        inv = "هنوز چیزی نداری"

    content = f"""

<h1>👤 پروفایل</h1>

<div class="card">

<div class="stat">
<span>👤 نام</span>
<span>{player_name}</span>
</div>

<div class="stat">
<span>🧝 شخصیت</span>
<span>{character}</span>
</div>

<div class="stat">
<span>❤️ سلامتی</span>
<span>{health}</span>
</div>

<div class="stat">
<span>🪙 سکه</span>
<span>{coins}</span>
</div>

<div class="stat">
<span>⭐ امتیاز</span>
<span>{score}</span>
</div>

<div class="stat">
<span>💎 تعداد گنج</span>
<span>{len(treasures)}</span>
</div>

</div>

<div class="card">

<h2>🎒 تجهیزات و گنج‌ها</h2>

<p class="small">
{inv}
</p>

</div>

<div class="card">

<h2>✏️ تغییر نام</h2>

<form method="POST" action="/setname">

<input
type="text"
name="name"
placeholder="نام جدید"
maxlength="20"
required
>

<button type="submit">
💾 ذخیره نام
</button>

</form>

</div>

<a class="btn btn2" href="/characters">
🧝 تغییر شخصیت
</a>

<a class="btn btn3" href="/">
🏠 خانه
</a>

"""

    return page("پروفایل", content)


# =========================
# تغییر نام
# =========================

@app.route("/setname", methods=["POST"])
def setname():

    global player_name

    name = request.form.get("name", "").strip()

    if name:
        player_name = name[:20]

    return redirect(url_for("profile"))


# =========================
# نبرد
# =========================

@app.route("/attack")
def attack():

    content = f"""

<h1>⚔️ میدان نبرد</h1>

<div class="card center">

<div class="big">⚔️</div>

<h2>دشمن در مقابل توست!</h2>

<p>
بازیکن:
<b>{player_name}</b>
</p>

<p>
شخصیت:
<b>{character}</b>
</p>

<div class="stat">
<span>❤️ سلامتی</span>
<span>{health}</span>
</div>

</div>

<div class="card">

<h2>انتخاب حرکت</h2>

<a class="btn" href="/attack-result?move=1">
🏹 حمله سریع
</a>

<a class="btn btn2" href="/attack-result?move=2">
⚔️ حمله قدرتمند
</a>

<a class="btn btn3" href="/play">
🏃 فرار
</a>

</div>

"""

    return page("نبرد", content)


# =========================
# نتیجه نبرد
# =========================

@app.route("/attack-result")
def attack_result():

    global coins
    global score

    move = request.args.get("move", "1")

    if move == "1":

        result = "🏹 حمله سریع انجام شد!"
        reward = 15

    else:

        result = "⚔️ حمله قدرتمند انجام شد!"
        reward = 25

    coins += reward
    score += 30

    content = f"""

<h1>⚔️ نتیجه نبرد</h1>

<div class="card center success">

<div class="big">🏆</div>

<h2>{result}</h2>

<p>
تو از دشمن عبور کردی.
</p>

</div>

<div class="card">

<div class="stat">
<span>🪙 پاداش</span>
<span>+{reward}</span>
</div>

<div class="stat">
<span>⭐ امتیاز</span>
<span>+30</span>
</div>

<div class="stat">
<span>🪙 سکه فعلی</span>
<span>{coins}</span>
</div>

</div>

<a class="btn" href="/map">
🗺️ ادامه ماجراجویی
</a>

<a class="btn btn2" href="/attack">
⚔️ نبرد دوباره
</a>

<a class="btn btn3" href="/">
🏠 خانه
</a>

"""

    return page("نتیجه نبرد", content)


# =========================
# فروشگاه
# =========================

@app.route("/shop")
def shop():

    cards = ""

    for key, item in items.items():

        cards += f"""

<div class="card center">

<div class="big">
{item["name"].split()[0]}
</div>

<h2>{item["name"]}</h2>

<p>
🪙 قیمت:
{item["price"]}
</p>

<a class="btn" href="/buy/{key}">
🛒 خرید
</a>

</div>

"""

    content = f"""

<h1>🏪 فروشگاه NEXORA</h1>

<div class="card center">

<h2>
🪙 سکه‌های تو:
{coins}
</h2>

</div>

{cards}

<a class="btn btn3" href="/">
🏠 خانه
</a>

"""

    return page("فروشگاه", content)


# =========================
# خرید
# =========================

@app.route("/buy/<item>")
def buy(item):

    global coins

    if item not in items:
        return redirect(url_for("shop"))

    product = items[item]

    if coins >= product["price"]:

        coins -= product["price"]

        inventory.append(product["name"])

        message = f"""
<h2>✅ خرید موفق بود!</h2>

<p>
{product["name"]}
به تجهیزات تو اضافه شد.
</p>
"""

    else:

        message = f"""
<h2>❌ سکه کافی نیست.</h2>

<p>
برای خرید {product["name"]}
به {product["price"]} سکه نیاز داری.
</p>
"""

    content = f"""

<h1>🏪 فروشگاه</h1>

<div class="card center">

<div class="big">🛒</div>

{message}

<div class="stat">
<span>🪙 سکه باقی‌مانده</span>
<span>{coins}</span>
</div>

<a class="btn" href="/shop">
🏪 فروشگاه
</a>

<a class="btn btn2" href="/profile">
🎒 تجهیزات
</a>

</div>

"""

    return page("خرید", content)


# =========================
# Manifest
# =========================

@app.route("/manifest.webmanifest")
def manifest():

    data = """
{
    "name": "NEXORA WORLD",
    "short_name": "NEXORA",
    "start_url": "/",
    "display": "standalone",
    "background_color": "#07120d",
    "theme_color": "#177245",
    "orientation": "portrait"
}
"""

    return Response(
        data,
        mimetype="application/manifest+json"
    )


# =========================
# آیکون
# =========================

@app.route("/icon.svg")
def icon():

    svg = """
<svg xmlns="http://www.w3.org/2000/svg"
width="512"
height="512"
viewBox="0 0 512 512">

<rect
width="512"
height="512"
rx="100"
fill="#07120d"/>

<circle
cx="256"
cy="220"
r="130"
fill="#177245"/>

<text
x="256"
y="250"
font-size="110"
text-anchor="middle"
fill="white">
N
</text>

<text
x="256"
y="390"
font-size="55"
text-anchor="middle"
fill="white">
NEXORA
</text>

</svg>
"""

    return Response(
        svg,
        mimetype="image/svg+xml"
    )


# =========================
# Service Worker
# =========================

@app.route("/sw.js")
def service_worker():

    js = """
const CACHE = "nexora-world-v2";

self.addEventListener("install", event => {

    event.waitUntil(

        caches.open(CACHE).then(cache => {

            return cache.addAll([
                "/",
                "/map",
                "/play",
                "/missions",
                "/characters",
                "/profile",
                "/shop"
            ]);

        })

    );

});

self.addEventListener("fetch", event => {

    event.respondWith(

        fetch(event.request).catch(() => {

            return caches.match(event.request);

        })

    );

});
"""

    return Response(
        js,
        mimetype="application/javascript"
    )


# =========================
# اجرای برنامه
# =========================

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False
    )