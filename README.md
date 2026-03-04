
# Spieltermine Grazer Sportklub Straßenbahn — Automatischer Kalender (Liga & Cup)

Dieser Kalender erzeugt sich automatisch aus der offiziellen ÖFB-Seite der Kampfmannschaft des **GRAZER SPORTKLUB Holding Graz** für die **Saison 2025/26** und stellt die Termine als **.ics** zum Abonnieren bereit (Outlook, Apple Kalender, Google Kalender etc.).

**Quelle (ÖFB):** https://vereine.oefb.at/Grazer_Sportclub/Mannschaften/Saison-2025-26/KM/Spiele

## Was ist enthalten?
- **Liga**- und **Cup**-Spiele (Heim & Auswärts)
- Titel: **„GSC vs Gegner“** (bei Heimspielen)
- Ort bei Heimspielen: **Gruabn, Kastellfeldgasse 47, 8010 Graz**
- Erinnerung: **1 Tag vorher** (VALARM, Display)

## Öffentlicher Kalender-Link
Nach dem ersten erfolgreichen Lauf von GitHub Actions liegt der abonnierbare Kalender hier:

```
https://<GITHUB_USERNAME>.github.io/<REPO_NAME>/gsc_km_2025-26.ics
```

> **Hinweis:** Outlook & Google Kalender aktualisieren abonnierte ICS-Feeds **nicht in Echtzeit**. Änderungen können bis zu ~24 Stunden benötigen, bis sie in allen Clients ankommen.

## Deployment (einmalig, 3–5 Minuten)
1. **GitHub-Account anlegen** (z. B. `gsc-spieltermine`). GitHub erlaubt in Benutzernamen nur Buchstaben/Ziffern/Bindestrich, keine Leerzeichen/Ä/Ö/Ü/ß.
2. Neues **öffentliches Repository** anlegen, Name z. B. `gsc-calendar`.
3. Diese Dateien in das Repo hochladen (oder via `git push`).
4. **GitHub Pages** aktivieren: *Settings → Pages → Build and deployment* → Source: **Deploy from a branch**, Branch: **main**, Folder: **/docs**.
5. **Actions** erlauben (falls gefragt) und den Workflow laufen lassen (oder manuell unter *Actions → Run workflow* starten).
6. Den oben genannten **ICS-Link** abonnieren (Outlook/Apple/Google).

## Lokaler Test (optional)
```bash
pip install -r requirements.txt
python generate_gsc_ics.py
```
Die Datei wird unter `docs/gsc_km_2025-26.ics` erzeugt.

## Lizenz
MIT
