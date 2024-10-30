import configparser
import requests
import time as mytime
from skyfield.api import Topos, load, EarthSatellite
from datetime import datetime, timedelta
import pytz
import os
import sys

sys.path.append('..')
from DAPNET import News

# Konstanten
KEPLER_DATA_FILE = "kepler_data.txt"
UPDATE_INTERVAL = 14400  # 4 Stunden in Sekunden
CONFIG_FILE = 'config_dapnet_iss.ini'

slot = 1


def fetch_kepler_data():
    url = "https://www.celestrak.com/NORAD/elements/stations.txt"
    response = requests.get(url)

    if response.status_code == 200:
        with open(KEPLER_DATA_FILE, "w") as file:
            file.write(response.text)
        print("Kepler-Daten erfolgreich abgerufen und gespeichert.")
    else:
        print(f"Fehler beim Abrufen der Kepler-Daten: {response.status_code}")


def get_kepler_data():
    if not os.path.exists(KEPLER_DATA_FILE) or \
       (mytime.time() - os.path.getmtime(KEPLER_DATA_FILE) > UPDATE_INTERVAL):
        fetch_kepler_data()
    else:
        print("Verwende die gespeicherten Kepler-Daten.")

def load_config(filename="config_dapnet_iss.ini"):
    current_dir = os.getcwd()
    config = configparser.ConfigParser()
    config_file = current_dir + '/' + filename
    config.read(config_file)
    
    latitude = float(config["Location"]["latitude"])
    longitude = float(config["Location"]["longitude"])
    elevation = float(config["Location"]["elevation"])
    news = News(config['DAPNET']['dapnetuser'], config['DAPNET']['dapnetpasswd'])
    rubrik = config['DAPNET']['rubrik']
    
    return latitude, longitude, elevation, news, rubrik


def fetch_iss_tle():
    # Lade Kepler-Daten
    with open(KEPLER_DATA_FILE, "r") as file:
        lines = file.readlines()
        for i, line in enumerate(lines):
            if line.strip() == "ISS (ZARYA)":
                return lines[i + 1], lines[i + 2]


def get_iss_passes(latitude, longitude, elevation):
    # Standort und Zeitkonfiguration
    location = Topos(latitude_degrees=latitude, longitude_degrees=longitude, elevation_m=elevation)
    ts = load.timescale()
    tle_line1, tle_line2 = fetch_iss_tle()
    satellite = EarthSatellite(tle_line1, tle_line2, "ISS (ZARYA)", ts)
    now = ts.now()
    end_time = now + timedelta(hours=24)
    
    # Ereignisse (Aufgang, maximale Höhe, Untergang) finden
    t0, events = satellite.find_events(location, now, end_time, altitude_degrees=10.0)
    berlin_tz = pytz.timezone("Europe/Berlin")
    
    passes = []
    for ti, event in zip(t0, events):
        local_time = ti.utc_datetime().replace(tzinfo=pytz.utc).astimezone(berlin_tz)
        if event == 0:
            passes.append(("Rise", local_time))
        elif event == 1:
            passes.append(("Maximum", local_time))
        elif event == 2:
            passes.append(("Set", local_time))
    return passes


def announce_event(event, event_time, news, rubrik):
    global slot
    # Text für Rurbik
    announcement = f"{event} of ISS at {event_time.strftime('%H:%M')} UTC."
    news.send(announcement, rubrik, slot)
    slot += 1
    if slot == 11:
        slot = 1


# Prüfe, ob eine Ansage nötig ist
def check_for_announcement(passes, news, rubrik):
    now = datetime.now(pytz.timezone("UTC"))
    for event, time in passes:
        delta = (time - now).total_seconds() / 60  # Differenz in Minuten
        if 239.5 <= delta <= 240.5 or 59.5 <= delta <= 60.5 or 0.5 <= delta <= 1.5 or delta <= 0.5:
            announce_event(event, time, news, rubrik)


# Test der Berechnungen und Ansagen
latitude, longitude, elevation, news, rubrik = load_config(CONFIG_FILE)
get_kepler_data()
iss_passes = get_iss_passes(latitude, longitude, elevation)
check_for_announcement(iss_passes, news, rubrik)

