from http.server import BaseHTTPRequestHandler
import os
import json
import requests
from urllib.parse import urlparse, parse_qs

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


class handler(BaseHTTPRequestHandler):

    def do_GET(self):

        query = parse_qs(urlparse(self.path).query)

        prayer = query.get("prayer", [None])[0]

        if prayer not in PRAYERS:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(b"Invalid prayer")
            return

        response = requests.post(
            f"https://api.telegram.org/bot{BOT_TOKEN}/sendPoll",
            data={
                "chat_id": CHAT_ID,
                "question": f"সালাত ট্র্যাকার: {PRAYERS[prayer]}",
                "options": json.dumps(POLL_OPTIONS),
                "is_anonymous": False,
                "allows_multiple_answers": False
            }
        )

        self.send_response(response.status_code)
        self.end_headers()
        self.wfile.write(response.text.encode())