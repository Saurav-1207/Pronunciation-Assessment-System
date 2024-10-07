import streamlit as st
import torchaudio
from transformers import Wav2Vec2ForCTC, Wav2Vec2Processor
from pydub import AudioSegment
import sounddevice as sd
import wavio
import torch
import difflib
import eng_to_ipa as ipa  # Library for IPA transcription
import syllapy  # Library for syllable breakdown
from gtts import gTTS
import tempfile

# 1. Record audio from the user with better volume normalization
def record_audio(duration=5, filename='user_audio.wav', fs=16000):
    st.write("Recording... Please speak the sentence you provided.")
    recording = sd.rec(int(duration * fs), samplerate=fs, channels=1)
    sd.wait()
    wavio.write(filename, recording, fs, sampwidth=2)
    st.write("Recording complete.")
    # Increase volume using pydub
    sound = AudioSegment.from_wav(filename)
    louder_sound = sound + 10  # Increase volume by 10dB
    louder_sound.export(filename, format='wav')

# 2. Transcribe audio using wav2vec
def transcribe_audio(audio_path):
    processor = Wav2Vec2Processor.from_pretrained("facebook/wav2vec2-base-960h")
    model = Wav2Vec2ForCTC.from_pretrained("facebook/wav2vec2-base-960h")
    model.eval()

    waveform, sample_rate = torchaudio.load(audio_path)

    # Resample to 16000Hz if needed
    if sample_rate != 16000:
        resampler = torchaudio.transforms.Resample(orig_freq=sample_rate, new_freq=16000)
        waveform = resampler(waveform)

    input_values = processor(waveform.squeeze(), sampling_rate=16000, return_tensors="pt").input_values

    # Perform transcription
    with torch.no_grad():
        logits = model(input_values).logits

    predicted_ids = torch.argmax(logits, dim=-1)
    transcription = processor.decode(predicted_ids[0])

    return transcription.lower()

# 3. Extract phonemes and syllables using eng_to_ipa and syllapy
def extract_ipa_and_syllables(word):
    ipa_transcription = ipa.convert(word)  # Get IPA transcription
    syllables = syllapy.count(word)  # Get syllable count
    return ipa_transcription, syllables

# 4. Compare words using difflib and provide simplified feedback for laymen
def provide_simplified_feedback(transcription, correct_text):
    feedback = []
    user_words = transcription.split()
    correct_words = correct_text.split()

    st.write("Repeating your pronunciation...")
    st.write(f"You said: {transcription}")

    for i, correct_word in enumerate(correct_words):
        if i < len(user_words):
            user_word = user_words[i]
            correct_ipa, _ = extract_ipa_and_syllables(correct_word)
            user_ipa, _ = extract_ipa_and_syllables(user_word)

            # Compare phonemes using SequenceMatcher
            similarity = difflib.SequenceMatcher(None, user_ipa, correct_ipa).ratio()

            if similarity < 0.8:  # You can adjust the threshold if needed
                # Provide feedback in layman’s terms
                feedback.append(f"Try saying '{correct_word}' again. You said '{user_word}', but it should sound more like '{correct_word}'.")

                # Offer simple pronunciation tips for common mistakes
                if correct_word == "this" and user_word.lower() != "this":
                    feedback.append("Tip: For 'this', try placing your tongue between your teeth and blow out softly to make the 'th' sound.")
                elif correct_word == "is" and user_word.lower() != "is":
                    feedback.append("Tip: 'Is' should sound short and quick, like in 'this is'.")
                elif correct_word == "india" and user_word.lower() != "india":
                    feedback.append("Tip: Say 'india' with emphasis on the 'in', and let the 'di-a' flow smoothly.")

        else:
            feedback.append(f"You missed saying the word '{correct_word}'.")

    if feedback:
        st.write("Feedback: ", " ".join(feedback))
    else:
        st.write("Great! You pronounced everything correctly.")

    # Use Google Text-to-Speech to generate audio feedback
    feedback_text = " ".join(feedback) if feedback else "All words are pronounced correctly."
    tts = gTTS(feedback_text)
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp_file:
        tts.save(tmp_file.name)
        st.audio(tmp_file.name, format='audio/mp3')

# Streamlit app
def pronunciation_assessment():
    st.title("Pronunciation Assessment Tool")
    st.write("Enter a sentence and record your audio to assess pronunciation.")

    # Input box for correct sentence
    correct_text = st.text_input("Enter the sentence you want to assess:", "this is india")

    # Audio recording section
    if st.button("Record Audio"):
        audio_filename = 'user_audio.wav'
        record_audio(filename=audio_filename)

        # Transcribe the audio
        transcription = transcribe_audio(audio_filename)
        st.write("Recognized Text:", transcription)

        # Provide simplified feedback based on transcription
        provide_simplified_feedback(transcription, correct_text)

if __name__ == "__main__":
    pronunciation_assessment()
