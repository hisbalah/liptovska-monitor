import requests
from bs4 import BeautifulSoup
import hashlib
import os
from datetime import datetime


URL = "https://www.liptovskaosada.com/index.php/samosprava/uznesenia-a-zapisnice-oz/678-uznesenia-a-zapisnice-rok-2026"

BOT_TOKEN = os.environ["8811690834:AAE5eiiiVXrwG1oIQF-2pCNP_Gx0MmqctY4"]
CHAT_ID = "5691403626"

HASH_FILE = "page_hash.txt"


def send_telegram(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    requests.post(
        url,
        data={
            "chat_id": CHAT_ID,
            "text": message
        },
        timeout=20
    )


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


new_hash = get_page_hash()


if os.path.exists(HASH_FILE):

    with open(HASH_FILE, "r") as f:
        old_hash = f.read()

else:

    old_hash = None


if old_hash is None:

    with open(HASH_FILE, "w") as f:
        f.write(new_hash)

    print("Prvé spustenie - uložený stav stránky.")


elif old_hash != new_hash:

    cas = datetime.now().strftime("%d.%m.%Y %H:%M")

    send_telegram(
        "🔔 LIPTOVSKÁ OSADA - ZMENA\n\n"
        "Na stránke uznesení a zápisníc bola zistená zmena.\n"
        "Skontroluj nové zasadnutie alebo zápisnicu.\n\n"
        f"Čas: {cas}\n\n"
        f"{URL}"
    )

    with open(HASH_FILE, "w") as f:
        f.write(new_hash)

    print("Zmena odoslaná na Telegram.")


else:

    print("Žiadna zmena.")
