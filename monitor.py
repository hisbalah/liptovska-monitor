import requests
from bs4 import BeautifulSoup
import hashlib
from datetime import datetime
import os


URL = "https://www.liptovskaosada.com/index.php/samosprava/uznesenia-a-zapisnice-oz/678-uznesenia-a-zapisnice-rok-2026"

BOT_TOKEN = "8811690834:AAE5eiiiVXrwG1oIQF-2pCNP_Gx0MmqctY4"
CHAT_ID = "5691403626"

HASH_FILE = "page_hash.txt"


def send_telegram(message):

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    r = requests.post(
        url,
        data={
            "chat_id": CHAT_ID,
            "text": message
        },
        timeout=20
    )

    print("Telegram odpoveď:", r.text)


def get_page_hash():

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    r = requests.get(
        URL,
        headers=headers,
        timeout=30
    )

    r.raise_for_status()

    soup = BeautifulSoup(
        r.text,
        "html.parser"
    )

    for tag in soup(["script", "style"]):
        tag.decompose()

    text = soup.get_text(
        " ",
        strip=True
    )

    return hashlib.sha256(
        text.encode("utf-8")
    ).hexdigest()


# ===== TEST TELEGRAMU =====
# Ak chceš test, zmeň False na True,
# spusti Actions a potom vráť späť na False

TEST_MESSAGE = True


if TEST_MESSAGE:

    send_telegram(
        "✅ TEST\n\n"
        "Telegram bot pre Liptovskú Osadu funguje."
    )

    exit()


# ===== KONTROLA STRÁNKY =====

new_hash = get_page_hash()


if os.path.exists(HASH_FILE):

    with open(HASH_FILE, "r") as f:
        old_hash = f.read()

else:

    old_hash = None



if old_hash is None:

    with open(HASH_FILE, "w") as f:
        f.write(new_hash)

    print("Prvý stav uložený.")


elif old_hash != new_hash:

    cas = datetime.now().strftime("%d.%m.%Y %H:%M")

    send_telegram(
        "🔔 LIPTOVSKÁ OSADA - NOVÁ ZMENA\n\n"
        "Na stránke pribudla zmena.\n"
        "Môže ísť o nové uznesenia alebo zápisnicu.\n\n"
        f"Čas: {cas}\n\n"
        f"{URL}"
    )

    with open(HASH_FILE, "w") as f:
        f.write(new_hash)

    print("Zmena nájdená.")


else:

    print("Bez zmeny.")
