from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import json
import os

app = FastAPI(
    title="AgriTrace AI API",
    description="Intelligent Livestock Video & Digital Record System",
    version="1.0.0"
)

# ======================================
# CORS
# ======================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ======================================
# DATA PATH
# ======================================

ANIMAL_RECORDS_PATH = "ai/animal_records.json"


# ======================================
# LOAD ANIMAL RECORDS
# ======================================

def load_animal_records():

    if not os.path.exists(ANIMAL_RECORDS_PATH):
        return {}

    with open(
        ANIMAL_RECORDS_PATH,
        "r"
    ) as file:

        return json.load(file)


# ======================================
# ROOT
# ======================================

@app.get("/")
def root():

    return {
        "project": "AgriTrace AI",
        "status": "running",
        "message": "Livestock AI backend is running."
    }


# ======================================
# HEALTH
# ======================================

@app.get("/health")
def health():

    return {
        "status": "healthy"
    }


# ======================================
# ALL ANIMALS
# ======================================

@app.get("/animals")
def get_animals():

    records = load_animal_records()

    return {
        "count": len(records),
        "animals": records
    }


# ======================================
# SINGLE ANIMAL
# ======================================

@app.get("/animals/{animal_id}")
def get_animal(animal_id: str):

    records = load_animal_records()

    if animal_id not in records:

        return {
            "error": "Animal not found"
        }

    return records[animal_id]


# ======================================
# ALERTS
# ======================================

@app.get("/alerts")
def get_alerts():

    records = load_animal_records()

    alerts = []

    for animal_id, record in records.items():

        for alert in record.get(
            "alerts",
            []
        ):

            alerts.append({
                "animal_id": animal_id,
                **alert
            })

    return {
        "count": len(alerts),
        "alerts": alerts
    }


# ======================================
# EVENTS
# ======================================

@app.get("/events")
def get_events():

    records = load_animal_records()

    events = []

    for animal_id, record in records.items():

        for event in record.get(
            "events",
            []
        ):

            events.append({
                "animal_id": animal_id,
                **event
            })

    return {
        "count": len(events),
        "events": events
    }