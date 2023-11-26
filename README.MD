## Install

    pip install fastapi
    pip install "uvicorn[standard]"


## Run the app

    uvicorn main:app --reload
Open your broswer at [http://127.0.0.1:8000](http://127.0.0.1:8000)

## Usage
Visit [http://127.0.0.1:8000](http://127.0.0.1:8000)

### GET '/'
    Parameters: None <br>
    Return: 
| Name | Type | Description |    
|------|------|-------------|
|helper|string|Displays the valid paths available|
    
### GET '/convertFromISO'
    Parameters: 
| Name | Type | Description |    
|------|------|-------------|
|duration|string|Duration in ISO Format|
    Return: 
| Name | Type | Description |    
|------|------|-------------|
|videoDuration|int|Duration in Milliseconds|
    
### GET '/convertFromMilliseconds'
    Parameters: 
| Name | Type | Description |    
|------|------|-------------|
|duration|string|Duration in Milliseconds|
    Return: 
| Name | Type | Description |    
|------|------|-------------|
|videoDuration|string|Duration in ISO Format|