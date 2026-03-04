
import re, os, datetime, pytz, requests
from bs4 import BeautifulSoup
from icalendar import Calendar, Event, Alarm

SOURCE_URL = "https://vereine.oefb.at/Grazer_Sportclub/Mannschaften/Saison-2025-26/KM/Spiele"
TEAM_NAME = "GRAZER SPORTKLUB Holding Graz"
TZ = pytz.timezone("Europe/Vienna")
HOME_LOCATION = "Gruabn, Kastellfeldgasse 47, 8010 Graz"  # STFV-Profil
OUTPUT_PATH = os.path.join("docs", "gsc_km_2025-26.ics")

# Wettbewerb-Filter: nur Liga & Cup
COMP_WHITELIST = {"Liga", "Cup"}

# Erinnerung 1 Tag vorher
ALARM_TRIGGER = datetime.timedelta(days=-1)


def parse_events():
    resp = requests.get(SOURCE_URL, timeout=30)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "lxml")

    text = " ".join(soup.get_text(" ").split())

    # Split an Wochentagen, um Spielzeilen zu finden
    chunks = re.split(r"(Mo\.|Di\.|Mi\.|Do\.|Fr\.|Sa\.|So\.)\s+", text)
    candidates = []
    for i in range(1, len(chunks), 2):
        weekday = chunks[i]
        rest = chunks[i + 1]
        # Muster: "dd.mm. hh:mm <Comp> <TeamA> ... <TeamB>"
        m = re.match(
            r"(\d{2}\.\d{2}\.)\s+(\d{2}:\d{2})\s+(Testspiel|Liga|Cup)\s+(.*?)\s+(?:- : -|\d+\s*:\s*\d+.*)\s+(.*?)\s",
            rest,
        )
        if m:
            date_s, time_s, comp, left_team, right_team = m.groups()
            if comp not in COMP_WHITELIST:
                continue
            candidates.append((weekday, date_s, time_s, comp, left_team.strip(), right_team.strip()))

    events = []
    for _, date_s, time_s, comp, left, right in candidates:
        day = int(date_s[:2])
        month = int(date_s[3:5])
        year = 2026 if month <= 6 else 2025  # Saison 2025/26
        hour = int(time_s[:2])
        minute = int(time_s[3:5])

        start_dt = TZ.localize(datetime.datetime(year, month, day, hour, minute))
        end_dt = start_dt + datetime.timedelta(hours=2)

        # Heim/Auswärts bestimmen und Titel/Ort setzen
        if left.upper().startswith(TEAM_NAME.upper()):
            title = f"GSC vs {right}"
            location = HOME_LOCATION
        else:
            title = f"{left} vs GSC"
            location = ""

        description = f"{comp} | Quelle: {SOURCE_URL}"
        uid = f"{abs(hash(title + start_dt.isoformat()))}@gsc-calendar"

        events.append({
            "summary": title,
            "dtstart": start_dt,
            "dtend": end_dt,
            "location": location,
            "description": description,
            "uid": uid,
        })

    return events


def build_calendar(events):
    cal = Calendar()
    cal.add("prodid", "-//GSC KM 2025/26 Auto-Feed (Liga+Cup)//oefb.at//")
    cal.add("version", "2.0")
    cal.add("X-WR-CALNAME", "GSC KM 2025/26 (Liga & Cup)")
    cal.add("X-WR-TIMEZONE", "Europe/Vienna")

    for ev in events:
        e = Event()
        e.add("summary", ev["summary"]) 
        e.add("dtstart", ev["dtstart"]) 
        e.add("dtend", ev["dtend"]) 
        if ev["location"]:
            e.add("location", ev["location"]) 
        e.add("description", ev["description"]) 
        e.add("uid", ev["uid"]) 

        # 1 Tag vorher Erinnerung
        alarm = Alarm()
        alarm.add("action", "DISPLAY")
        alarm.add("description", "Erinnerung: Spieltermin")
        alarm.add("trigger", ALARM_TRIGGER)
        e.add_component(alarm)

        cal.add_component(e)

    return cal.to_ical()


def main():
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    events = parse_events()
    ics_bytes = build_calendar(events)
    with open(OUTPUT_PATH, "wb") as f:
        f.write(ics_bytes)
    print(f"Wrote {OUTPUT_PATH} with {len(events)} events")


if __name__ == "__main__":
    main()
