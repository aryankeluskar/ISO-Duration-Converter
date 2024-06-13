import json
import os

import requests
from dotenv import load_dotenv
from fastapi import FastAPI, Request, Response

load_dotenv()

app = FastAPI()


def getDurationInMilliseconds(
    ISODuration, previouslyUsed: bool = False, response: Response = None
):
    r"""
    Convert duration from ISO format to milliseconds

    Parameters
    ---
    ISODuration : str
        Duration in ISO Format.

    Returns
    ---
    videoDuration : int
        Duration in milliseconds.

    Detailed Description
    ---
    This function converts the duration of the track from ISO Format to
    milliseconds by analysing every permuation of the format.
    """

    setAnalytics(1)
    try:
        if "H" in ISODuration and "M" in ISODuration and "S" in ISODuration:
            videoDuration = (
                int(
                    ISODuration[
                        ISODuration.find("T") + 1 : ISODuration.find("H")
                    ]
                )
                * 3600000
                + int(
                    ISODuration[
                        ISODuration.find("H") + 1 : ISODuration.find("M")
                    ]
                )
                * 60000
                + int(
                    ISODuration[
                        ISODuration.find("M") + 1 : ISODuration.find("S")
                    ]
                )
                * 1000
            )
        elif "H" in ISODuration and "M" in ISODuration:
            videoDuration = (
                int(
                    ISODuration[
                        ISODuration.find("T") + 1 : ISODuration.find("H")
                    ]
                )
                * 3600000
                + int(
                    ISODuration[
                        ISODuration.find("H") + 1 : ISODuration.find("M")
                    ]
                )
                * 60000
            )
        elif "H" in ISODuration and "S" in ISODuration:
            videoDuration = (
                int(
                    ISODuration[
                        ISODuration.find("T") + 1 : ISODuration.find("H")
                    ]
                )
                * 3600000
                + int(
                    ISODuration[
                        ISODuration.find("H") + 1 : ISODuration.find("S")
                    ]
                )
                * 1000
            )
        elif "M" in ISODuration and "S" in ISODuration:
            videoDuration = (
                int(
                    ISODuration[
                        ISODuration.find("T") + 1 : ISODuration.find("M")
                    ]
                )
                * 60000
                + int(
                    ISODuration[
                        ISODuration.find("M") + 1 : ISODuration.find("S")
                    ]
                )
                * 1000
            )
        elif "H" in ISODuration:
            videoDuration = (
                int(
                    ISODuration[
                        ISODuration.find("T") + 1 : ISODuration.find("H")
                    ]
                )
                * 3600000
            )
        elif "M" in ISODuration:
            videoDuration = (
                int(
                    ISODuration[
                        ISODuration.find("T") + 1 : ISODuration.find("M")
                    ]
                )
                * 60000
            )
        elif "S" in ISODuration:
            videoDuration = (
                int(
                    ISODuration[
                        ISODuration.find("T") + 1 : ISODuration.find("S")
                    ]
                )
                * 1000
            )
        else:
            videoDuration = 0
        response.set_cookie(key="previouslyUsed", value="true")
    except Exception:
        return (
            "Invalid input format. Please provide a valid ISO duration format."
        )

    return videoDuration


def getDurationInISO(
    MillisecondsDuration,
    previouslyUsed: bool = False,
    response: Response = None,
):
    r"""
    Convert duration from milliseconds to ISO format

    Parameters
    ---
    MillisecondsDuration : int
        Duration in milliseconds.

    Returns
    ---
    ISODuration : str
        Duration in ISO Format.

    Detailed Description
    ---
    This function converts the duration of the track from milliseconds to
    ISO Format.
    """
    setAnalytics(requests.Session(), 1)
    try:
        print(MillisecondsDuration)
        MillisecondsDuration = int(MillisecondsDuration)
        hours = MillisecondsDuration // 3600000
        minutes = (MillisecondsDuration % 3600000) // 60000
        seconds = (MillisecondsDuration % 60000) // 1000

        ISODuration = f"PT{hours}H{minutes}M{seconds}S"
        response.set_cookie(key="previouslyUsed", value="true")
    except Exception:
        return """Invalid input format. Please provide a valid duration
        in milliseconds with only digits."""

    return ISODuration


def make_request(url=None, method="GET", headers=None, data=None):
    r"""
    Makes a request to the url and returns the response

    Parameters
    ---
    url : str
        The url to make the request to
    method : str
        The method of the request (GET or POST)
    headers : dict
        The headers of the request
    data : dict
        The data to send in the request

    Returns
    ---
    The response of the request if successful, None otherwise
    """
    #  print("making request", method, url, headers, data)
    try:
        if method == "GET":
            with requests.session.get(url) as response:
                if response.status == 200:
                    return response.json()
                else:
                    print(f"Error: {response.status}")
                    return None
        elif method == "POST":
            with requests.session.post(
                url, headers=headers, data=data
            ) as response:
                if response.status == 200:
                    return response.json()
                else:
                    print(f"Error: {response.status}")
                    return None
    except Exception as e:
        print("error occured: " + str(e))
        return "ERROR"


def setAnalytics(newCalls: int = 0) -> str:
    r"""
    Updates the analytics database (hosted on MongoDB)

    Parameters
    ---
    newCalls : int
        The number of new calls to add


    Returns
    ---
    The response of the request if successful, None otherwise
    """

    headers = {
        "apiKey": os.getenv("MONGODP_APIKEY"),
        "Content-Type": "application/ejson",
        "Accept": "application/json",
    }
    payload = {
        "dataSource": "Cluster0",
        "database": "API_Analytics",
        "collection": "SpotifyToYoutube",
        "filter": {"_id": {"$oid": os.getenv("MONGO_OID")}},
        "update": {
            "$inc": {
                "ISOtotalCalls": newCalls,
            }
        },
    }

    response = make_request(
        requests.session,
        os.getenv("MONGODB_UPDATEURL"),
        "POST",
        headers=headers,
        data=json.dumps(payload),
    )
    if response:
        print("was database modification successful? " + str(response))
        # print("setting analytics\n")
        #  print(response.text)
        #  return response.text
    return response


@app.get("/")
async def root():
    r"""
    Returns home page with instructions on how to use the API
    """
    return """Choose one of the two paths: /convertFromISO or
    /convertFromMilliseconds \nPass duration as a query parameter."""


@app.get("/help")
async def help():
    r"""
    Returns help page with instructions on how to use the API
    """
    return """Choose one of the two paths: /convertFromISO or
/convertFromMilliseconds \nPass duration as a query parameter."""


@app.get("/convertFromISO/")
async def convertISO(
    duration: str = "PT0H0M0S",
    request: Request = None,
    response: Response = None,
):
    r"""
    Convert duration from ISO format to milliseconds

    Parameters
    ---
    duration : str
        Duration in ISO Format.

    Returns
    ---
    MillisecondsDuration : int
        Duration in milliseconds.

    Detailed Description
    ---
    This route converts the duration of the track from ISO format to
    milliseconds .
    """
    return getDurationInMilliseconds(
        duration, bool(request.cookies.get("previouslyUsed")), response
    )


@app.get("/convertFromMilliseconds/")
async def convertMilliseconds(
    duration: str = 0, request: Request = None, response: Response = None
):
    r"""
    Convert duration from milliseconds to ISO format

    Parameters
    ---
    duration : int
        Duration in milliseconds.

    Returns
    ---
    ISODuration : str
        Duration in ISO Format.

    Detailed Description
    ---
    This route converts the duration of the track from milliseconds
    to ISO format.
    """
    return getDurationInISO(
        duration, bool(request.cookies.get("previouslyUsed")), response
    )
