# DestinE_SPDT
Github for the ESA Scenario-planning Digital Twin

## Quick start
1. Ensure that `docker` and `docker compose` (or the [older](https://stackoverflow.com/questions/66514436/difference-between-docker-compose-and-docker-compose) `docker-compose`) are both installed
Ensure Node.js is installed
2. Create a new docker volume named `RedisDB'. This can be done in docker desktop or using the command:
```bash 
docker volume create RedisDB
```
3. Build the app image from the dockerfile
```bash
docker build -t spdt -f Dockerfile  .
```
4. Run the `compose.yaml` file
```bash
docker compose up 
```
5. To access the Mimick MVP App, in a web browser, go to [localhost](localhost)
## House keeping

This file structure is temporary and is likely to change as the project evolves. For now:
1. Anything concerning modelling should go into /modelling
2. Functionality for the digital twin should go into /other
3. Any static data (e.g. images, datasets, maps etc. that will be the same every time) should go into static. Keep like with like in subfolders, creating new folders as needed
4. Anything without a home should go into /other. We should try and kee this folder as empty as possible, if it gets too full we should reorganise
5. Anything that shouldn't be uploaded to Github should be added to the .gitignore. Any passwords/ user credentials etc. should be filed under /other/private

## Debug version

1. Virtual environment 

```python3 -m venv .env ```


```.env\Scripts\activate ```

2. Install dependencies

```python.exe -m pip install --upgrade pip```
 
```pip install -r requirements.txt```


3. Run flask

```set FLASK_APP=digitalTwin.py```

```set FLASK_DEBUG=1```

```flask run```