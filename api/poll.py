import os
import json
import requests

BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")

PRAYERS = {
    "fazr": "ফজর (Fazr)",
    "johor": "যোহর (Johor)",
    "asr": "আসর (Asr)",
    "magrib": "মাগরিব (Magrib)",
    "esha": "এশা (Esha)"
}

POLL_OPTIONS = [
    "তাকবীরে উলা",
    "১ম রাকাত",
    "মাসবুক",
    "জামাত মিস",
    "কাযা"
]


def handler(request):

    prayer = request.get("query", {}).get("prayer")

    if prayer not in PRAYERS:
        return {
            "statusCode": 400,
            "body": json.dumps({
                "error": "Invalid prayer"
            })
        }

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPoll"

    payload = {
        "chat_id": CHAT_ID,
        "question": f"সালাত ট্র্যাকার: {PRAYERS[prayer]}",
        "options": json.dumps(POLL_OPTIONS),
        "is_anonymous": False,
        "allows_multiple_answers": False
    }

    response = requests.post(url, data=payload)

    return {
        "statusCode": response.status_code,
        "body": response.text
    }