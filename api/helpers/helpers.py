import csv
from datetime import datetime
import string
import random
import os
from enum import Enum
from typing import List, Union
from fastapi import UploadFile
from shutil import copyfileobj


class AudioAnalysisStatus(Enum):
    DONE = 'done'
    PENDING = 'pending'
    INVALID = 'invalid'


ANALYSIS_FILE_PATH = 'samples'
API_FOLDER = 'api'


def get_audio_analysis_result(file_name: str) -> List[dict]:
    file_name = os.path.join(os.getcwd(), API_FOLDER,
                             ANALYSIS_FILE_PATH, file_name)

    with open(file_name) as file:
        csv_file = csv.reader(file)
        result_list = []
        for i in csv_file:
            line = i[0].split()
            record = {
                "labels": line[0],
                "start": line[1],
                "stop": line[2],
            }
            result_list.append(record)
        return result_list[1:]


def get_random_string(size: int = 10) -> str:
    return ''.join(random.choices(string.digits + string.ascii_letters, k=size))


def create_id() -> str:
    datetime_format = '%Y%m%d%H%M%S-'
    return datetime.now().strftime(datetime_format) + get_random_string()


def get_response(status: AudioAnalysisStatus, result: Union[str, dict, list]) -> dict:
    return {'status': status, 'result': result}


def get_analysis_status(ticket_id: str) -> dict:
    path = os.path.join(os.getcwd(), API_FOLDER, ANALYSIS_FILE_PATH)
    dir_list = os.listdir(path)

    csv_file = list(filter(lambda x: x == ticket_id + '.csv', dir_list))
    audio_file = list(filter(lambda x: x == ticket_id, dir_list))

    if csv_file:
        return get_response(AudioAnalysisStatus.DONE, get_audio_analysis_result(csv_file[0]))

    if audio_file:
        return get_response(AudioAnalysisStatus.PENDING, f'ticketId {ticket_id} was found but it is still pending. please come back later')

    return get_response(AudioAnalysisStatus.INVALID, f'ticketId {ticket_id} was not found')


def delete_files(files: List[str]):
    for i in files:
        os.remove(os.path.join(os.getcwd(), API_FOLDER, ANALYSIS_FILE_PATH, i))


def start_audio_analysis(file_name: str):
    '''
    Starts audio analysis in a container. This might take a while
    '''
    script = './scripts/ina_speech_segmenter.py'
    command = f'{script} -i ./{API_FOLDER}/{ANALYSIS_FILE_PATH}/{file_name} -o ./{API_FOLDER}/{ANALYSIS_FILE_PATH}/'
    os.system(command)


def create_analysis_file(file: UploadFile) -> str:
    analysis_file = create_id()
    file_path = os.path.join(
        os.getcwd(), API_FOLDER, ANALYSIS_FILE_PATH, analysis_file)

    with open(file_path, 'wb') as buffer:
        copyfileobj(file.file, buffer)
        return analysis_file
