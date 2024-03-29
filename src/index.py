from fastapi import FastAPI, Response, Cookie, Request
from dotenv import load_dotenv
import os
from pymongo import MongoClient


load_dotenv()

app = FastAPI()


"""
   @param: ISODuration: Duration in ISO Format. 
   @return videoDuration: Duration in milliseconds.
   @description: This function converts the duration of the track from ISO Format to milliseconds by analysing every permuation of the format.
"""


def getDurationInMilliseconds(
    ISODuration, previouslyUsed: bool = False, response: Response = None
):
    

    client = MongoClient(os.getenv("MONGO_URI"))
    # Select the database and collection
    db = client[os.getenv("MONGO_DB")]
    collection = db[os.getenv("MONGO_COLLECTION")]

    collection.update_many({}, {'$inc': 
                                {'ISOtotalCalls': 1}})


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
        response.set_cookie(key="previouslyUsed", value="true")
    except:
        return "Invalid input format. Please provide a valid ISO duration format."

    return videoDuration


"""
   @param: MillisecondsDuration: Duration in milliseconds. 
   @return ISODuration: Duration in ISO Format.
   @description: This function converts the duration of the track from milliseconds to ISO Format.
"""


def getDurationInISO(
    MillisecondsDuration, previouslyUsed: bool = False, response: Response = None
):
    

    client = MongoClient(os.getenv("MONGO_URI"))
    
    # Select the database and collection
    db = client[os.getenv("MONGO_DB")]
    collection = db[os.getenv("MONGO_COLLECTION")]

    collection.update_many({}, {'$inc': 
                                {'ISOtotalCalls': 1}})

    client.close()
    try:
        print(MillisecondsDuration)
        MillisecondsDuration = int(MillisecondsDuration)
        hours = MillisecondsDuration // 3600000
        minutes = (MillisecondsDuration % 3600000) // 60000
        seconds = (MillisecondsDuration % 60000) // 1000

        ISODuration = f"PT{hours}H{minutes}M{seconds}S"
        response.set_cookie(key="previouslyUsed", value="true")
    except:
        return "Invalid input format. Please provide a valid duration in milliseconds with only digits."

    return ISODuration

@app.get("/")
async def root():
    return "Choose one of the two paths: /convertFromISO or /convertFromMilliseconds. Pass duration as a query parameter."


@app.get("/help")
async def root():
    return "Choose one of the two paths: /convertFromISO or /convertFromMilliseconds. Pass duration as a query parameter."


@app.get("/convertFromISO/")
async def root(
    duration: str = "PT0H0M0S", request: Request = None, response: Response = None
):
    return getDurationInMilliseconds(
        duration, bool(request.cookies.get("previouslyUsed")), response
    )


@app.get("/convertFromMilliseconds/")
async def root(duration: str = 0, request: Request = None, response: Response = None):
    return getDurationInISO(
        duration, bool(request.cookies.get("previouslyUsed")), response
    )
