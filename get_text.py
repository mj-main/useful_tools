import librosa
import numpy as np
import soundfile as sf
from pydub import AudioSegment
import urllib3
import json
import base64
import ast
import os
import shutil
import argparse

# input
parser = argparse.ArgumentParser()
parser.add_argument('--fname', required=True)
parser.add_argument('--api', required=True)
parser.add_argument('--lan', default="korean")
args = parser.parse_args()

# temp 폴더 생성
os.makedirs("./temp", exist_ok=True)


# raw 파일 생성
def get_raw(filename, duration=30):
    audio1 = librosa.load(filename, sr=16000)[0]

    modified = np.delete(audio1, np.where(audio1 == 0))  # 무음 제거

    num = int(len(modified) / (16000 * duration)) + 1  # 분할할 개수

    rest_list = [0 for i in range(num * 16000 * duration - len(modified))]

    audio_array = np.append(modified, rest_list)
    audio_array = audio_array.reshape(num, -1)

    for i in range(num):
        output_fname = filename[:-4] + "_" + str(i)

        sf.write("./temp/" + output_fname + '.wav', audio_array[i], 16000, 'PCM_16')

        sound = AudioSegment.from_wav("./temp/" + output_fname + '.wav')
        sound = sound.set_channels(1)
        sound.export("./temp/" + output_fname + '.raw', format="raw")

    print(filename, ": 완료")


# Raw to text
def get_text(filename, language):
    openApiURL = "http://aiopen.etri.re.kr:8000/WiseASR/Recognition"
    accessKey = args.api
    try:
        file = open(filename, "rb")
        audioContents = base64.b64encode(file.read()).decode("utf8")
        file.close()

        requestJson = {
            "access_key": accessKey,
            "argument": {
                "language_code": language,
                "audio": audioContents
            }
        }

        http = urllib3.PoolManager()
        response = http.request(
            "POST",
            openApiURL,
            headers={"Content-Type": "application/json; charset=UTF-8"},
            body=json.dumps(requestJson)
        )

        byte_str = response.data
        dict_str = byte_str.decode("UTF-8")
        dict_data = ast.literal_eval(dict_str)
        text = dict_data['return_object']['recognized']
        print(text)
        text_list.append(text) # text_list에 음성인식된 텍스트를 추가한다.
    except:
        print("error")


get_raw(args.fname)

text_list = []
path = "./temp"
file_list = [i for i in os.listdir(path) if i[-3:] == "raw"]
for file in file_list:
    get_text("./temp/" + file, args.lan)

results = "".join(text_list)

# Write txt file
file = open('output.txt', 'w')
file.write(results)
file.close()


shutil.rmtree("./temp")