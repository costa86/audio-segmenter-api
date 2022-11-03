# Instructions

## Description
The project is an API that receives an audio file as a input, analyses it with a machine learning algorithm, then sends the output back to the user. 


## Documentation (internal)

### Structure
The project was built on top of [inaSpeechSegmenter](https://github.com/ina-foss/inaSpeechSegmenter), where we added [api](/api) as a custom [FastAPI](https://fastapi.tiangolo.com/) project. [Dockerfile](../Dockerfile) was modified to serve the API along with the base project.

### Specs
The audio analysis process might take a while to be handled, therefore the procedure is divided into 2 steps.
1. A `POST` request with the audio file. The user receives a ticket ID that identifies the audio analysis request.
2. A `GET` request with the ticket ID. The user receives the result or the status of the audio analysis, since it might still be in queue to be processed.

There's also a `DELETE` request to delete both the files (audio and CSV) used for the analysis.

### Run the project with docker

Build

    docker build . -t <custom_name>
    
Run

    docker run --rm -p 80:80 <custom_name>

## Documentation (external)

See details of the endpoints. With the app in execution:

|Default|Alternative|
|-|-|
|http://0.0.0.0/docs| http://0.0.0.0/redoc|
    