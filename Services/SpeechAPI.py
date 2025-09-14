import azure.cognitiveservices.speech as speechsdk
import base64
import io
import tempfile



def text_to_speech(text, speechClient):
    speechClient.speech_synthesis_voice_name = "en-US-JennyNeural"


    # Use None for audio_config so it doesn’t try to play sound
    synthesizer = speechsdk.SpeechSynthesizer(
        speech_config=speechClient,
        audio_config=None
    )

    result = synthesizer.speak_text_async(text).get()

    if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        audio_base64 = base64.b64encode(result.audio_data).decode("utf-8")
        return audio_base64
    else:
        print("Error synthesizing speech:", result.reason)
        return None
    







def speech_to_text(audio_base64, speechClient):
    try:
        audio_bytes = base64.b64decode(audio_base64)

        # Create a temp WAV file, don't delete immediately
        tmp_file = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
        tmp_file.write(audio_bytes)
        tmp_file.flush()
        tmp_file.close()  # important

        # Pass the filename to Azure
        audio_config = speechsdk.audio.AudioConfig(filename=tmp_file.name)
        recognizer = speechsdk.SpeechRecognizer(speech_config=speechClient, audio_config=audio_config)
        result = recognizer.recognize_once()

        if result.reason == speechsdk.ResultReason.RecognizedSpeech:
            print("Speech recognized:", result.text)
            return result.text
        else:
            print("Speech recognition failed:", result.reason)
            return None
    except Exception as e:
        print("Error ",e)
