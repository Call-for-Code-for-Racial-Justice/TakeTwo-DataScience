import os

import json

from typing import Optional

from fastapi import FastAPI

from pydantic import BaseModel

from fastapi.responses import HTMLResponse

# from fastapi.middleware.cors import CORSMiddleware

from cloudant.client import Cloudant

app = FastAPI()


db_name = os.getenv("DBNAME")
client = None
db = None
creds = None

if "VCAP_SERVICES" in os.environ:
    creds = json.loads(os.getenv("VCAP_SERVICES"))
    print("Found VCAP_SERVICES")
elif os.path.isfile("vcap-local.json"):
    with open("vcap-local.json") as f:
        creds = json.load(f)
        print("Found local VCAP_SERVICES")

if creds:
    username = creds["username"]
    apikey = creds["apikey"]
    url = creds["url"]
    client = Cloudant.iam(username, apikey, url=url, connect=True)
    db = client.create_database(db_name, throw_on_exists=False)


class BiasedTerm(BaseModel):
    _id: Optional[str]
    biased_string: str
    category: str
    definition: str


class Text(BaseModel):
    content: str


@app.get("/", response_class=HTMLResponse)
def read_root():
    return open("template.html").read()

if os.path.isfile("vcap-local.json"):
    @app.put("/clear_all")
    def clear_all(confirm: str):
        if confirm == "yes":
            for doc in db:
                doc.delete()
            return {"status": "success"}
        return {"status": "failed"}


@app.get("/categories")
def read_categories():
    # fmt: off
    return [
        #IBM colour-blindness palette used below https://davidmathlogic.com/colorblind/ 
        {
            "name": "appropriation", 
            "colour": "#648FFF", 
            "description": "description for appropriation"
        },
        {
            "name": "stereotyping",
            "colour": "#785EF0",
            "description": "description for stereotyping",
        },
        {
            "name": "deflection",
            "colour": "#DC267F",
            "description": "description for deflection",
        },
        {
            "name": "racist", 
            "colour": "#FE6100", 
            "description": "description for gaslighting"
        },
        {
            "name": "othering", 
            "colour": "#FFB000", 
            "description": "description for othering"
        },
        {
            "name": "racial slur", 
            "colour": "#18C857", 
            "description": "description for racial slur"
        },
    ]
    # fmt: on


@app.put("/analyse")
def analyse_text(text: Text):
    res = []
    for doc in db:
        if doc["biased_string"] in text.content:
            res.append({"flag" : doc["biased_string"], "category" : doc["category"], "definition" : doc["definition"], "alternative": doc["alternative"]})
    return {"biased": res}

@app.get("/biasedbase")
def biased_terms():
    return list(map(lambda doc: doc, db))

@app.post("/load")
def populate_db(item: BiasedTerm):
    data = item.dict()
    if client:
        my_document = db.create_document(data)
        data["_id"] = my_document["_id"]
        return data
    else:
        print("No database")
        return data
