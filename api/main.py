from fastapi import FastAPI, UploadFile, HTTPException
from .helpers.helpers import AudioAnalysisStatus, delete_files, get_analysis_status, \
    get_response, start_audio_analysis, create_analysis_file
from threading import Thread


app = FastAPI()


@app.post('/analysis/')
async def request_audio_analysis(file: UploadFile):
    '''
    Sends audio file for analysis.\n
    Body parameters:\n
        \tfile (audio file): The audio file to be processed
    '''
    if file.content_type != 'audio/mpeg':
        raise HTTPException(
            status_code=400,
            detail=f"file must be in audio format, got {file.content_type}"
        )

    analysis_file = create_analysis_file(file)
    Thread(target=start_audio_analysis, args=(analysis_file,)).start()
    return {'ticketId': analysis_file}


@app.get('/analysis/{id}/')
async def get_audio_analysis_result(id: str):
    '''
    Receives audio analysis.\n
        Path parameters:\n
            \tid(str): The ticker ID received when the audio request was first initiated\n
        Returns:\n
            \t(json). The audio analysis result, or its current status, in case it is still in queue.

    '''
    return get_analysis_status(id)


@app.delete('/analysis/{id}/')
async def delete_audio_analysis_result(id: str):
    '''
    Deletes all audio analysis-related files for a given ticket ID.\n
        Path parameters:\n
            \tid(str): The ticker ID received when the audio request was first initiated\n
        Returns:\n
            \t(json). The confirmation of the deletion process
    '''
    result = get_analysis_status(id)

    if result['status'] == AudioAnalysisStatus.DONE:
        delete_files([id, id + '.csv'])
        return get_response(AudioAnalysisStatus.DONE, f'audio analysis for {id} has been deleted')

    return result
