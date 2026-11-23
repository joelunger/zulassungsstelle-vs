import time
from datetime import datetime
import requests

URL = "https://lrasbk.flexappoint.de/api/available-times/disabled-days?departmentId=2&year=2026&month=9&format=Y-m-d&services[0][id]=19&services[0][count]=1"
NTFY_TOPIC = "DEIN TOPIC HIER"  # Replace with your ntfy topic

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:155.0) Gecko/20100101 Firefox/155.0",
    "Accept": "application/json, text/plain, */*",
    "X-Requested-With": "XMLHttpRequest",
    "X-Origin-Url": "https://lrasbk.flexappoint.de/",
    "Referer": "https://lrasbk.flexappoint.de/",
}

COOKIES = {
    "selectedDepartment": "2"
}

# Days before September 14 we want to catch
WORKDAYS_TO_CHECK = [
    "2026-09-03", "2026-09-04", "2026-09-07", "2026-09-08",
    "2026-09-09", "2026-09-10", "2026-09-11"
]

def send_push(title, message, priority="default"):
    try:
        requests.post(
            f"https://ntfy.sh/{NTFY_TOPIC}",
            data=message.encode("utf-8"),
            headers={"Title": title.encode("latin-1", "ignore"), "Priority": priority},
            timeout=10
        )
    except Exception as e:
        print(f"[ntfy] Error: {e}")

def check():
    now = datetime.now().strftime("%H:%M:%S")
    print(f"[{now}] Abfrage laeuft...")

    try:
        res = requests.get(URL, headers=HEADERS, cookies=COOKIES, timeout=10)
        
        if res.status_code != 200:
            print(f"[{now}] HTTP Fehler: {res.status_code}")
            return False

        data = res.json()

        # The API returns blocked days inside the "items" key
        disabled_days = data.get("items", [])

        # Check if any wanted day is NOT in the disabled list
        found_days = [d for d in WORKDAYS_TO_CHECK if d not in disabled_days]

        if found_days:
            found_str = ", ".join(found_days)
            print(f"\n{'='*50}\n[TREFFER] Freier Termin entdeckt: {found_str}!\n{'='*50}\n")
            send_push("TERMIN FREI!", f"Termin frei am: {found_str}! Sofort buchen!", priority="urgent")
            return True

        print(f"[{now}] Alle fruehen Tage weiterhin blockiert (keine Stornierung).")
        return False

    except Exception as e:
        print(f"[{now}] Fehler: {e}")
        return False

if __name__ == "__main__":
    print(f"--- Ueberwachung aktiv fuer topic: {NTFY_TOPIC} ---")
    while True:
        if check():
            break
        print("Warte 45 Sekunden...\n")
        time.sleep(45)
