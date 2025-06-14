# AI Virtual Career Counsellor

An AI-powered career counselling application that recommends career paths based on user interests, skills, and aspirations. The application uses natural language processing and a knowledge base of career information to provide personalized career guidance. Developed by Susan from IIIT Kancheepuram for Elevate Labs.

## Features

- Modern, responsive UI with Elevate Labs branding
- Interactive chat interface with avatar icons
- Real-time career recommendations with detailed cards
- Detailed career information including:
  - Required skills
  - Education paths
  - Job descriptions
- Conversation history tracking
- Easy-to-use web interface built with Streamlit
- Custom CSS styling for a professional look and feel

## Screenshots

![AI Career Counsellor UI](docs/screenshot.png)

## Setup and Installation

1. Clone this repository:
   ```bash
   git clone <repository-url>
   cd ai_career_counsellor_
   ```

2. Create and activate a virtual environment (recommended):
   ```bash
   # Windows
   python -m venv venv
   .\venv\Scripts\activate

   # Linux/MacOS
   python -m venv venv
   source venv/bin/activate
   ```

3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   - Create a `.env` file in the `src` directory
   - Add your OpenRouter API key:
     ```
     OPENROUTER_API_KEY=your-api-key-here
     ```

## Running the Application

1. Navigate to the project directory:
   ```bash
   cd ai_career_counsellor_
   ```

2. Start the Streamlit application:
   ```bash
   streamlit run src/app.py
   ```

3. Open your web browser and go to `http://localhost:8501`

## Usage

1. Enter your interests, skills, or career-related questions in the text area
2. Click "Send" to get AI-powered career guidance
3. View recommended career paths in the sidebar
4. Explore detailed information about each recommended career
5. Use the "Start New Conversation" button to reset the chat

## Project Structure

- `src/app.py`: Main application file containing the Streamlit interface and AI logic
- `src/style.css`: Custom CSS styling for the application
- `src/assets/`: Directory containing SVG images and icons
- `data/careers.json`: Career information database
- `requirements.txt`: Python package dependencies
- `.env`: Environment variables configuration

## Technologies Used

- Python
- Streamlit
- NLTK (Natural Language Toolkit)
- OpenRouter API (GPT-3.5 Turbo)
- SVG for vector graphics
- Custom CSS for styling
- JSON for data storage

## Credits

- Developed by Susan from IIIT Kancheepuram
- Created for Elevate Labs