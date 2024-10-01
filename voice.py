import speech_recognition as sr
from difflib import SequenceMatcher
import pyttsx3
import streamlit as st
import time

class PronunciationAssessmentSystem:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', 150)  # Adjust speech rate for clear feedback
        self.similarity_threshold = 0.8  # Fixed threshold for pronunciation matching

    def listen_to_speech(self):
        st.info("Listening... Please speak now.")
        with sr.Microphone() as source:
            self.recognizer.adjust_for_ambient_noise(source)  # Adjust for ambient noise
            try:
                audio = self.recognizer.listen(source, timeout=10, phrase_time_limit=10)
                return audio
            except sr.WaitTimeoutError:
                st.warning("Timeout! No speech detected. Please try again.")
                return None

    def convert_speech_to_text(self, audio):
        try:
            text = self.recognizer.recognize_google(audio)
            st.write(f"Recognized Text: {text}")
            return text.lower()
        except sr.UnknownValueError:
            st.error("Sorry, I couldn't understand the speech. Please try again.")
            return None
        except sr.RequestError as e:
            st.error(f"Could not request results from the speech recognition service: {e}")
            return None

    def compare_words(self, spoken_word, correct_word):
        similarity = SequenceMatcher(None, spoken_word, correct_word).ratio()
        return similarity > self.similarity_threshold

    def provide_feedback(self, spoken_words, correct_words):
        feedback = []
        all_correct = True

        for i, correct_word in enumerate(correct_words):
            if i < len(spoken_words):
                spoken_word = spoken_words[i]
                if not self.compare_words(spoken_word, correct_word):
                    feedback.append(f"'{spoken_word}' should be '{correct_word}'")
                    all_correct = False
            else:
                feedback.append(f"missing '{correct_word}'")
                all_correct = False

        if len(spoken_words) > len(correct_words):
            extra_words = spoken_words[len(correct_words):]
            feedback.append(f"extra words: {' '.join(extra_words)}")
            all_correct = False

        if all_correct:
            feedback_message = "All words pronounced correctly."
        else:
            feedback_message = "Feedback: " + ", ".join(feedback)

        st.write(feedback_message)
        self.engine.say(feedback_message)
        self.engine.runAndWait()

    def run_assessment(self, correct_text):
        st.subheader("Pronunciation Assessment System")
        st.write(f"Target Text: '{correct_text}'")

        # Listen for user input
        audio = self.listen_to_speech()
        if not audio:
            return

        # Convert speech to text
        spoken_text = self.convert_speech_to_text(audio)
        if not spoken_text:
            return

        # Split spoken and correct text into words
        spoken_words = spoken_text.split()
        correct_words = correct_text.split()

        # Provide detailed feedback
        self.provide_feedback(spoken_words, correct_words)


# Streamlit App Logic
def main():
    st.title("Pronunciation Assessment System")

    system = PronunciationAssessmentSystem()

    # Get the target sentence from the user
    correct_text = st.text_input("Enter the sentence or word you want to assess:", "This is India")

    if st.button("Start Pronunciation Assessment"):
        with st.spinner("Listening..."):
            system.run_assessment(correct_text)


if __name__ == "__main__":
    main()
