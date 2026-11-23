# Zulassungsstelle-VS

Dieses Python-Skript überwacht die verfügbaren Termine der Zulassungsstelle
Villingen-Schwenningen. Es prüft die gewünschten Werktage regelmäßig und
sendet über [ntfy](https://ntfy.sh/) eine Push-Benachrichtigung, sobald ein
Termin frei wird.

## Voraussetzungen

- Python 3.11 oder neuer
- Internetverbindung
- Ein installiertes ntfy-Konto bzw. ein ntfy-Topic

## Installation

Repository klonen und in das Projektverzeichnis wechseln:

```bash
git clone https://github.com/joelunger/zulassungsstelle-vs.git
cd zulassungsstelle-vs
```

Abhängigkeiten installieren:

```bash
python3 -m pip install -r requirements.txt
```

## Konfiguration

Vor dem Start [index.py](index.py) öffnen und mindestens `NTFY_TOPIC`
anpassen:

```python
NTFY_TOPIC = "DEIN_TOPIC"
```

Die überwachten Termine stehen in `WORKDAYS_TO_CHECK`. Bei einem anderen
Zeitraum müssen außerdem die Angaben in `URL` (`year` und `month`) angepasst
werden. Die Werte für `departmentId` und den Service gehören zur jeweiligen
Terminbuchung und müssen bei Bedarf ebenfalls geändert werden.

## Start

```bash
python3 index.py
```

Das Skript prüft alle 45 Sekunden. Sobald ein gewünschter Tag verfügbar ist,
wird eine dringende ntfy-Benachrichtigung gesendet und das Skript beendet sich.
Mit `Ctrl+C` kann die Überwachung jederzeit beendet werden.

## Hinweise

- Das Skript bucht keinen Termin automatisch.
- Bitte die Verfügbarkeit und die Nutzungsbedingungen des Terminportals
  beachten.
- Ein ntfy-Topic kann je nach Konfiguration öffentlich erreichbar sein. Daher
  sollte kein vertraulicher Topic-Name veröffentlicht oder wiederverwendet
  werden.
