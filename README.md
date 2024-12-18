# Gemini-Speaker: AI-Powered English Speaking Assistant 🎤

## Overview  
**Gemini-Speaker** is a Python-based English-speaking training assistant powered by Google's Gemini API. It provides real-time feedback on pronunciation, grammar, and sentence structure while guiding users step-by-step to improve their spoken English.

## Features  
1. **Real-Time Voice Input**:  
   - Captures your voice using the microphone and processes it seamlessly.  

2. **AI Feedback**:  
   - Corrects pronunciation mistakes.  
   - Highlights grammar errors.  
   - Provides suggestions for improvement.  

3. **Interactive Training Loop**:  
   - Suggests contextual sentences for continuous practice.  
   - Listens, evaluates, and progresses the training dynamically.  

4. **Seamless User Experience**:  
   - Runs in your terminal with interactive outputs.  

---

## Installation  

### Prerequisites  
1. **Python 3.11 or higher**  
2. **Pip**  
3. **Google API Key**  
4. **Required Libraries**: See `requirements.txt`.  

### Steps  
1. Clone the repository:  
   ```bash
   git clone https://github.com/Xudong-Mao/Gemini-Speaker.git  
   cd Gemini-Speaker
   ```

2. Install dependencies:  
   ```bash
   pip install -r requirements.txt  
   ```

3. Set up the environment variables:  
   - Create a `.env` file in the root directory.  
   - Add your Google API key:  
     ```
     GOOGLE_API_KEY=your_google_api_key_here
     ```

---

## Usage  

1. Run the program:  
   ```bash
   python main.py  
   ```

2. Follow the on-screen instructions:  
   - Speak an English sentence (e.g., *"What is blockchain?"*).  
   - Receive AI feedback and suggestions.  

3. Say "OK, 我要退出" to exit the program.  

---

## Example Interaction  

```
🎤 说一句英语吧！比如: What is blockchain?  
User: What is block chain?  

🤖 =============================================  
你说的句子是: "What is block chain?"  
发音错误: "block chain" 应发 /ˈblɒkˌtʃeɪn/。  
语法提示: 词汇拼写正确，注意连读发音。  
请再试一次！  
```

---

## Dependencies  
- Python >= 3.11  
- pyaudio  
- websockets  
- python-dotenv  
- rich  

---


## License  
This project is licensed under the MIT License.  

