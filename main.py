from fastapi import FastAPI, Response, Cookie, Request
from typing import Annotated
import json


app = FastAPI()


"""
   @param: ISODuration: Duration in ISO Format. 
   @return videoDuration: Duration in milliseconds.
   @description: This function converts the duration of the track from ISO Format to milliseconds by analysing every permuation of the format.
"""


def getDurationInMilliseconds(ISODuration, previouslyUsed: bool = False):
    try:
        totalCalls += 1
        if not previouslyUsed:
            uniqueUsers += 1

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


def getAnalytics():
    # Perform analytics calculations


    # Create JSON object
    analytics = {
        "totalCalls": totalCalls,
        "uniqueUsers": uniqueUsers,
    }

    return analytics


@app.get("/")
async def root():
    return "Choose one of the two paths: /convertFromISO or /convertFromMilliseconds \nPass duration as a query parameter."


@app.get("/help")
async def root():
    return "Choose one of the two paths: /convertFromISO or /convertFromMilliseconds \nPass duration as a query parameter."


@app.get("/convertFromISO/")
async def root(duration: str = "PT0H0M0S", request: Request=None):
    return getDurationInMilliseconds(duration, bool(request.cookies.get("previouslyUsed")))


@app.get("/convertFromMilliseconds/")
async def root(duration: str = 0, request: Request=None):
    return getDurationInISO(duration, bool(request.cookies.get("previouslyUsed")))


@app.get("/analytics/")
async def root():
    # print(request.cookies.get("previouslyUsed"))
    return getAnalytics()


@app.get("/cookie-and-object/")
def create_cookie(response: Response):
    response.set_cookie(key="previouslyUsed", value="true")
    return {"message": "Come to the dark side, we have cookies"}
