# رفيق التحرر - Social Media Awareness Chatbot

A Streamlit-based chatbot that helps users understand social media addiction and the psychological tactics used by social media platforms.

## Setup

1. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

2. **Set up Environment Variables**
   - Copy `.env.example` to `.env`
   - Get your Google Generative AI API key from [Google AI Studio](https://makersuite.google.com/app/apikey)
   - Replace `your_api_key_here` with your actual API key in the `.env` file

3. **Run the Application**

   ```bash
   streamlit run streamlit_app.py
   ```

## Features

- Arabic and English language support
- Educational content about social media psychology
- Based on "The Social Dilemma" documentary insights
- Streaming responses for better user experience
- Error handling and fallback mechanisms

## Troubleshooting

### Common Issues

1. **API Key Errors**
   - Ensure your `.env` file contains a valid `GOOGLE_API_KEY`
   - Check that your Google AI API key is active and has quota available

2. **Streaming Errors**
   - The app includes fallback mechanisms for streaming issues
   - If streaming fails, it will attempt a non-streaming response

3. **Rate Limiting**
   - If you encounter rate limits, wait a moment before trying again
   - Consider upgrading your Google AI API plan if needed

## Model Information

This chatbot uses Google's Gemini 1.5 Flash model for generating responses.
