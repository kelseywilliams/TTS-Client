from google.cloud import texttospeech
import pygame
import requests
import time
import os
# This file is just my post password and is included in the .gitignore
import password

# Instantiates a client
client = texttospeech.TextToSpeechClient()
while True:
    print("Fetching posts")
    req = requests.post("https://kelseywilliams.net/TTS-Server/api.php", data = {"password":password.PASSWORD,"filter":"unread"})

    # It's important to note that if the json response holds no keys, it cannot be converted to a dictionary as python won't create
    # dict's without keys.  Therefore the response is of type str.  This took a minute to figure out and it's why the len of the
    # response is unreliable for checking whether or not data is present in the response -- That requires a quick isinstance() call.
    posts = req.json()
    
    if isinstance(posts, dict):
        for i in range(len(posts.keys())):
            print(posts[str(i)]["data"])

            # Set the text input to be synthesized
            synthesis_input = texttospeech.types.SynthesisInput(text=posts[str(i)]["data"])

            # Build the voice request, select the language code ("en-US") 
            # ****** the NAME
            # and the ssml voice gender ("neutral")
            voice = texttospeech.types.VoiceSelectionParams(
                language_code='en-US',
                #name='en-US-Wavenet-C',
                ssml_gender=texttospeech.enums.SsmlVoiceGender.FEMALE)

            # Select the type of audio file you want returned
            audio_config = texttospeech.types.AudioConfig(
                audio_encoding=texttospeech.enums.AudioEncoding.MP3)

            # Perform the text-to-speech request on the text input with the selected
            # voice parameters and audio file type
            response = client.synthesize_speech(synthesis_input, voice, audio_config)

            filename = "file" + str(i) + ".mp3"
            
            # The response's audio_content is binary.
            with open(filename, 'wb') as out:
                # Write the response to the output file.
                out.write(response.audio_content)

            pygame.mixer.init()
            pygame.mixer.music.load(filename)
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy() == True:
                continue
            os.remove(filename)
            time.sleep(1)
