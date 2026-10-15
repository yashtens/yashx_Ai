# CampusX AI

A Streamlit chat interface for the Gemini 2.5 Flash model using LangChain.

## Run locally

1. Install the project dependencies with `uv sync`.
2. Add your Gemini API key to a `.env` file in the project root:

   ```dotenv
   GEMINI_API_KEY=your_api_key_here
   ```

   `GOOGLE_API_KEY` can be used instead.
3. Start the app:

   ```powershell
   uv run streamlit run app.py
   ```

The app keeps conversation history for the current Streamlit session. The `.env`
file is ignored by Git so API keys are not committed.