#!/usr/bin/python3

import base64
import requests
from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument('text', help='text to convert to speech')
parser.add_argument('file', help='output file')
parser.add_argument('-k', '--key', help='API key for Google Cloud Services', required=True)
parser.add_argument('-l', '--lang', help='speech language', default='en-AU')
parser.add_argument('-g', '--gender', help='speech gender', choices=['MALE', 'FEMALE', 'NEUTRAL'], default='NEUTRAL')
parser.add_argument('-f', '--format', help='output format', choices=['wav', 'mp3', 'ogg'], default='mp3')
args = parser.parse_args()

url = 'https://texttospeech.googleapis.com/v1/text:synthesize?key=' + args.key

if args.format == 'wav':
    encoding = 'LINEAR16'
elif args.format == 'ogg':
    encoding = 'OGG_OPUS'
elif args.format == 'mp3':
    encoding = 'MP3'

lang = args.lang
gender = args.gender
text = args.text

data = {"input":{"text": text},"voice":{"languageCode": lang,"ssmlGender": gender},"audioConfig":{"audioEncoding": encoding,"speakingRate": 1.0,"pitch": 0,"volumeGainDb": 0.0,"sampleRateHertz": 0}}

response = requests.post(url, json=data)

if response.status_code != 200:
    print('Request failed')
    exit(1)

decoded_audio = base64.b64decode(response.json()['audioContent'])

with open(args.file, 'wb') as f:
    f.write(decoded_audio)
