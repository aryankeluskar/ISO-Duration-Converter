from fastapi import FastAPI, Response, Cookie, Request
from typing import Annotated
import json
import pymongo
from pymongo import UpdateOne
import requests
import json
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI()


"""
   @param: ISODuration: Duration in ISO Format. 
   @return videoDuration: Duration in milliseconds.
   @description: This function converts the duration of the track from ISO Format to milliseconds by analysing every permuation of the format.
"""


def getDurationInMilliseconds(ISODuration, previouslyUsed: bool = False):
    currAnalytics = getAnalytics()
    print(currAnalytics)
    if not previouslyUsed:
        setAnalytics(
            currAnalytics["document"]["totalCalls"] + 1,
            currAnalytics["document"]["uniqueUsers"] + 1,
        )
    else:
        setAnalytics(
            currAnalytics["document"]["totalCalls"] + 1,
            currAnalytics["document"]["uniqueUsers"],
        )

    try:
        if "H" in ISODuration and "M" in ISODuration and "S" in ISODuration:
            videoDuration = (
                int(ISODuration[ISODuration.find("T") + 1 : ISODuration.find("H")])
                * 3600000
                + int(ISODuration[ISODuration.find("H") + 1 : ISODuration.find("M")])
                * 60000
                + int(ISODuration[ISODuration.find("M") + 1 : ISODuration.find("S")])
                * 1000
            )
        elif "H" in ISODuration and "M" in ISODuration:
            videoDuration = (
                int(ISODuration[ISODuration.find("T") + 1 : ISODuration.find("H")])
                * 3600000
                + int(ISODuration[ISODuration.find("H") + 1 : ISODuration.find("M")])
                * 60000
            )
        elif "H" in ISODuration and "S" in ISODuration:
            videoDuration = (
                int(ISODuration[ISODuration.find("T") + 1 : ISODuration.find("H")])
                * 3600000
                + int(ISODuration[ISODuration.find("H") + 1 : ISODuration.find("S")])
                * 1000
            )
        elif "M" in ISODuration and "S" in ISODuration:
            videoDuration = (
                int(ISODuration[ISODuration.find("T") + 1 : ISODuration.find("M")])
                * 60000
                + int(ISODuration[ISODuration.find("M") + 1 : ISODuration.find("S")])
                * 1000
            )
        elif "H" in ISODuration:
            videoDuration = (
                int(ISODuration[ISODuration.find("T") + 1 : ISODuration.find("H")])
                * 3600000
            )
        elif "M" in ISODuration:
            videoDuration = (
                int(ISODuration[ISODuration.find("T") + 1 : ISODuration.find("M")])
                * 60000
            )
        elif "S" in ISODuration:
            videoDuration = (
                int(ISODuration[ISODuration.find("T") + 1 : ISODuration.find("S")])
                * 1000
            )
        else:
            videoDuration = 0
    except:
        return "Invalid input format. Please provide a valid ISO duration format."

    return videoDuration


"""
   @param: MillisecondsDuration: Duration in milliseconds. 
   @return ISODuration: Duration in ISO Format.
   @description: This function converts the duration of the track from milliseconds to ISO Format.
"""


def getDurationInISO(MillisecondsDuration, previouslyUsed: bool = False):
    currAnalytics = getAnalytics()
    print(currAnalytics)
    if not previouslyUsed:
        setAnalytics(
            currAnalytics["document"]["totalCalls"] + 1,
            currAnalytics["document"]["uniqueUsers"] + 1,
        )
    else:
        setAnalytics(
            currAnalytics["document"]["totalCalls"] + 1,
            currAnalytics["document"]["uniqueUsers"],
        )

    totalCalls += 1
    if not previouslyUsed:
        uniqueUsers += 1
    try:
        print(MillisecondsDuration)
        MillisecondsDuration = int(MillisecondsDuration)
        hours = MillisecondsDuration // 3600000
        minutes = (MillisecondsDuration % 3600000) // 60000
        seconds = (MillisecondsDuration % 60000) // 1000

        ISODuration = f"PT{hours}H{minutes}M{seconds}S"
    except:
        return "Invalid input format. Please provide a valid duration in milliseconds with only digits."

    return ISODuration


"""
   @param: None
   @return json_response: JSON response.
   @description: This function retrieves the document stored in MongoDB Atlas which has the latest analytics data.
"""


def getAnalytics():
    # Perform analytics calculations
    payload = json.dumps(
        {
            "collection": "ISODuration",
            "database": "API_Analytics",
            "dataSource": "Cluster0",
            "projection": {"_id": 1, "totalCalls": 1, "uniqueUsers": 1},
        }
    )
    headers = {
        "apiKey": os.getenv("MONGODP_APIKEY"),
        "Content-Type": "application/ejson",
        "Accept": "application/json",
    }
    response = requests.request(
        "POST", os.getenv("MONGODP_READURL"), headers=headers, data=payload
    )
    print(response.text)

    json_response = json.loads(response.text)
    return json_response


"""
   @param: newCalls: number to be updated for totalCalls.
   @param: newUsers: number to be updated for uniqueUsers.
   @return None
   @description: This function updates the document stored in MongoDB Atlas.
   """


def setAnalytics(newCalls: int = 0, newUsers: int = 0):
    headers = {
        "apiKey": os.getenv("MONGODP_APIKEY"),
        "Content-Type": "application/ejson",
        "Accept": "application/json",
    }
    payload = {
        "dataSource": "Cluster0",
        "database": "API_Analytics",
        "collection": "ISODuration",
        "filter": {"_id": {"$oid": "6579334f6cd998706e6e7b1d"}},
        "update": {"$set": {"totalCalls": newCalls, "uniqueUsers": newUsers}},
    }

    response = requests.post(
        os.getenv("MONGODB_UPDATEURL"), headers=headers, data=json.dumps(payload)
    )
    print(response.text)
    print("setting analytics")


@app.get("/")
async def root():
    return "Choose one of the two paths: /convertFromISO or /convertFromMilliseconds \nPass duration as a query parameter."


@app.get("/help")
async def root():
    return "Choose one of the two paths: /convertFromISO or /convertFromMilliseconds \nPass duration as a query parameter."


@app.get("/convertFromISO/")
async def root(duration: str = "PT0H0M0S", request: Request = None):
    return getDurationInMilliseconds(
        duration, bool(request.cookies.get("previouslyUsed"))
    )


@app.get("/convertFromMilliseconds/")
async def root(duration: str = 0, request: Request = None):
    return getDurationInISO(duration, bool(request.cookies.get("previouslyUsed")))


@app.get("/analytics/")
async def root():
    # print(request.cookies.get("previouslyUsed"))
    #  setAnalytics(26, 13)
    return getAnalytics()


@app.get("/cookie-and-object/")
def create_cookie(response: Response):
    response.set_cookie(key="previouslyUsed", value="true")
    return {"message": "Come to the dark side, we have cookies"}
