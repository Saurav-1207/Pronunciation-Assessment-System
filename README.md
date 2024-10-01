![alt text](https://github.com/Saurav-1207/Pronunciation-Assessment-System/blob/25c04377f7818438f240a49131603a9f2afb8396/Capture.PNG)
# Pronunciation Assessment System

This project is a real-time pronunciation assessment tool that evaluates spoken words or sentences and provides feedback on their correctness. By leveraging **Speech Recognition**, **Natural Language Processing**, and **Text-to-Speech** technologies, this system offers real-time feedback on pronunciation, helping users improve their speaking skills.

## Table of Contents
- Overview
- Features
- How It Works
- Setup and Installation
- Usage
- Example Output
- Contributing

## Overview

The **Pronunciation Assessment System** allows users to assess their pronunciation of words and sentences. By providing immediate, detailed feedback on mispronounced words, it assists users in refining their pronunciation accuracy. Key components of the system include:

- **Real-time Speech Recognition**: Continuous listening and speech-to-text conversion using the Google Speech Recognition API.
- **Pronunciation Comparison**: Checks for pronunciation accuracy using **phonetic similarity** and word-by-word analysis.
- **Text-to-Speech Feedback**: The system uses **pyttsx3** for delivering spoken feedback.

## Features

- **Speech Recognition**: Users can speak into their microphone and receive instant feedback.
- **Pronunciation Feedback**: Provides a word-by-word analysis comparing spoken text to the correct text.
- **Real-time Processing**: Continuously listens to speech, allowing users to practice pronunciation in real-time.
- **Customizable Sentences**: Users can input their own sentences for assessment.
- **Interactive Feedback**: Clear visual and spoken feedback using **pyttsx3**.

## How It Works

1. **Speech Input**: The system listens to the user’s speech via the microphone.
2. **Speech Recognition**: Converts the spoken words into text using the **Google Speech Recognition API**.
3. **Pronunciation Assessment**: Compares the recognized text with the correct text, identifying mispronunciations.
4. **Feedback Delivery**: Provides feedback both visually and via text-to-speech, highlighting any mispronounced words.

## Setup and Installation

### Prerequisites

- Python 3.7 or newer
- Required Python packages:
  - `SpeechRecognition`
  - `pyttsx3`
  - `pyaudio` (for microphone input)
  - `difflib`

### Installation

1. **Create a Virtual Environment**:
   ```bash
   python -m venv myenv
   ```

2. **Activate the Virtual Environment**:
   - For Windows:
     ```bash
     myenv\Scripts\activate
     ```
   - For macOS/Linux:
     ```bash
     source myenv/bin/activate
     ```

3. **Clone the Repository**:
   ```bash
   git clone https://github.com/Saurav-1207/pronunciation-assessment-system.git
   ```

4. **Install Required Packages**:
   ```bash
   pip install -r requirements.txt
   ```

5. **Run the Application**:
   ```bash
   python pronunciation_assessment.py
   ```

## Usage

1. **Launch the System**: Run the program, and the system will prompt for a sentence or word you want to assess.
2. **Speak into the Microphone**: The system will listen to your pronunciation.
3. **Get Feedback**: The system will display feedback and provide spoken feedback through the speaker.

## Example Output

```
Target Text: "This is an example."
Recognized Text: "This is an exmple."
Feedback: Incorrect pronunciation of 'exmple', should be 'example'.
```

## Contributing

Contributions are welcome! If you'd like to add features or improve the system, feel free to fork the repository and submit a pull request. For major changes, please open an issue first to discuss what you'd like to change.
