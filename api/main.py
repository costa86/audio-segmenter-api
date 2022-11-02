from fastapi import FastAPI, UploadFile, HTTPException
from .helpers.helpers import AudioAnalysisStatus, delete_files, get_analysis_status, \
    get_response, start_audio_analysis, create_analysis_file
from threading import Thread


app = FastAPI()


@app.post('/analysis/')
async def request_audio_analysis(file: UploadFile):
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
    return get_analysis_status(id)


@app.delete('/analysis/{id}/')
async def delete_audio_analysis_result(id: str):
    result = get_analysis_status(id)

    if result['status'] == AudioAnalysisStatus.DONE:
        delete_files([id, id + '.csv'])
        return get_response(AudioAnalysisStatus.DONE, f'audio analysis for {id} has been deleted')

    return result
