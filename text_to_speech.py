# import os
# from elevenlabs.client import ElevenLabs
# from elevenlabs.core import ApiError
# from dotenv import load_dotenv
# load_dotenv()
# client = ElevenLabs(api_key=os.environ["ELEVENLABS_API_KEY"])

# try:
#     audio = client.text_to_speech.convert(
#         text="Hello! I am learning text to speech.",
#         voice_id="JBFqnCBsd6RMkjVDRZzb",
#         model_id="eleven_multilingual_v2",
#     )

#     with open("eleven.mp3", "wb") as f:      # yahin request actually chalti hai
#         for chunk in audio:
#             f.write(chunk)
#     print("Saved eleven.mp3")

# except ApiError as e:
#     print("Status:", e.status_code)
#     print("Detail:", e.body)

import os
from io import BytesIO
from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs

load_dotenv()
client = ElevenLabs(api_key=os.getenv("ELEVENLABS_API_KEY"))

voice = client.voices.ivc.create(
    name="My Voice Clone",
    files=[BytesIO(open("agneepath-dialogue.mp3", "rb").read())],
)
print("Clone ban gaya. Voice ID:", voice.voice_id)