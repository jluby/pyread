"""
AWS Sample Reader
from https://docs.aws.amazon.com/polly/latest/dg/get-started-what-next.html
"""

import os
import sys
from contextlib import closing

from boto3 import Session
from botocore.exceptions import BotoCoreError, ClientError
from google.cloud import texttospeech
from gtts import gTTS


def gtts(paragraph, speed, temp_file):
    gTTS(text=paragraph, lang="en-UK", slow=False).save(temp_file)


def polly(text, speed, temp_file):
    # Create a client using the credentials and region defined in the [adminuser]
    # section of the AWS credentials file (~/.aws/credentials).
    session = Session(profile_name="default")
    polly = session.client("polly")

    try:
        # Request speech synthesis
        response = polly.synthesize_speech(
            Text=f"<speak><prosody rate='{100*speed}%'>{text}</prosody></speak>", OutputFormat="mp3", VoiceId="Matthew"
        )
    except (BotoCoreError, ClientError) as error:
        # The service returned an error, exit gracefully
        print(error)
        sys.exit(-1)

    # Access the audio stream from the response
    if "AudioStream" in response:
        # Note: Closing the stream is important because the service throttles on the
        # number of parallel connections. Here we are using contextlib.closing to
        # ensure the close method of the stream object will be called automatically
        # at the end of the with statement's scope.
        with closing(response["AudioStream"]) as stream:

            try:
                # Open a file for writing the output as a binary stream
                with open(temp_file, "wb") as file:
                    file.write(stream.read())
            except IOError as error:
                # Could not write to file, exit gracefully
                print(error)
                sys.exit(-1)

    else:
        # The response didn't contain audio data, exit gracefully
        print("Could not stream audio")
        sys.exit(-1)


def cloud_tts(text, speed, temp_file):

    client = texttospeech.TextToSpeechClient()

    input_text = texttospeech.SynthesisInput(
        ssml=f"<speak><prosody rate='{100*speed}%'>{text}</prosody></speak>",
    )

    # Note: the voice can also be specified by name.
    # Names of voices can be retrieved with client.list_voices().
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US",
        name="en-US-Standard-I",
        ssml_gender=texttospeech.SsmlVoiceGender.MALE,
    )

    audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.MP3)

    response = client.synthesize_speech(input=input_text, voice=voice, audio_config=audio_config)

    # The response's audio_content is binary.
    with open(temp_file, "wb") as out:
        out.write(response.audio_content)
        print('Audio content written to file "output.mp3"')
