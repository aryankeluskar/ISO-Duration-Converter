# Simplest API Ever! Convert duration from ISO Form to Millisecond
Built using Python, FastAPI, hosted on Render.com <br>
Multiple APIs (like YouTube's) return media's duration in ISO Format but most data is processed with Milliseconds. I created this simple-to-use **Web API** to convert either form to the other. 
#### You get: _Skip coding logic, Directly process Milliseconds, Peace of Mind_ <br> I get _(hopefully): Star, Heart, Follow :)_

[<img src="https://run.pstmn.io/button.svg" alt="Try In Postman" style="width: 140px; height: 35px;">](https://www.postman.com/altimetry-explorer-27820642/workspace/all-my-apis/collection/31514208-08c0b3ff-f7ca-4389-b9f9-e1608a928670?action=share&creator=31514208)

## Install (Only if local instance needed)
    Requirements: gh, pip, python 3.12+
    Run the following commands:
    gh repo clone aryankeluskar/ISO-Duration-Converter
    pip install fastapi
    pip install "uvicorn[standard]"


## Run the app (Only if local instance needed)
    uvicorn main:app --reload
Open your broswer at [http://127.0.0.1:8000](http://127.0.0.1:8000)

## Usage
Visit [iso-duration-converter.onrender.com](https://iso-duration-converter.onrender.com/) to access this API <br>
Visit [detailed API documentation here](https://iso-duration-converter.onrender.com/docs) generated with OpenAPI.json <br>
Example: https://iso-duration-converter.onrender.com/convertFromISO?duration=PT5H21M49S responds with [19309000]() which can be processed with HttpRequest in Java, or requests.get in Python.

### GET /
    Parameters: None 
    Response: (string) Displays the valid paths available
    
<hr>

### GET /convertFromISO
    Parameters: duration (string) Duration in ISO Format
    Response: (int) Duration in Milliseconds
    
<hr>

### GET /convertFromMilliseconds
    Parameters: duration (int) Duration in Milliseconds
    Response: (string) Duration in ISO Format
    
## Support this project!
### This is my first ever API! Please consider leaving a 🌟 if this added value to your wonderful project
### Made with pure love and [freshman fascination](## "it's a real term i swear"). Visit my website at [aryankeluskar.github.io](https://aryankeluskar.github.io) <3
