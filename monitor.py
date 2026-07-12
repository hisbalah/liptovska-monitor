import requests
from bs4 import BeautifulSoup
import os
import json
from datetime import datetime


URL = "https://www.liptovskaosada.com/index.php/samosprava/uznesenia-a-zapisnice-oz/678-uznesenia-a-zapisnice-rok-2026"

BOT_TOKEN = "8811690834:AAE5eiiiVXrwG1oIQF-2pCNP_Gx0MmqctY4"
CHAT_ID = "5691403626"

FILE = "documents.json"


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


def get_documents():

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

    documents = []

    for a in soup.find_all("a", href=True):

        href = a["href"]

        text = a.get_text(
            " ",
            strip=True
        )

        if (
            ".pdf" in href.lower()
            or "zapis" in text.lower()
            or "uznes" in text.lower()
        ):

            if href.startswith("/"):
                href = "https://www.liptovskaosada.com" + href

            documents.append(
                {
                    "name": text,
                    "url": href
                }
            )


    return documents



new_documents = get_documents()


if os.path.exists(FILE):

    with open(FILE, "r", encoding="utf-8") as f:
        old_documents = json.load(f)

else:

    old_documents = []



old_urls = {
    d["url"]
    for d in old_documents
}


new_items = [
    d
    for d in new_documents
    if d["url"] not in old_urls
]



if not old_documents:

    with open(FILE, "w", encoding="utf-8") as f:
        json.dump(
            new_documents,
            f,
            ensure_ascii=False,
            indent=2
        )

    print("Prvý stav uložený.")



elif new_items:

    cas = datetime.now().strftime(
        "%d.%m.%Y %H:%M"
    )

    message = (
        "🔔 LIPTOVSKÁ OSADA\n\n"
        "Pribudol nový dokument:\n\n"
    )

    for item in new_items:

        message += (
            "📄 "
            + item["name"]
            + "\n"
            + item["url"]
            + "\n\n"
        )


    message += "Čas: " + cas

    send_telegram(message)


    with open(FILE, "w", encoding="utf-8") as f:
        json.dump(
            new_documents,
            f,
            ensure_ascii=False,
            indent=2
        )


    print("Nový dokument odoslaný.")



else:

    print("Žiadny nový dokument.")



