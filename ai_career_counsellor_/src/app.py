import streamlit as st
import nltk
import json
import os
import requests
from dotenv import load_dotenv
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import base64
import random
import time

# Load environment variables
load_dotenv()

# Download NLTK resources
try:
    nltk.data.find('tokenizers/punkt')
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('punkt')
    nltk.download('stopwords')

# Function to load local images as base64 strings
def get_image_base64(image_path):
    try:
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except FileNotFoundError:
        # Return a default SVG if file not found
        return "PHN2ZyB3aWR0aD0iMjQiIGhlaWdodD0iMjQiIHZpZXdCb3g9IjAgMCAyNCAyNCIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KPHBhdGggZD0iTTEyIDJMMTMuMDkgOC4yNkwyMCA5TDEzLjA5IDE1Ljc0TDEyIDIyTDEwLjkxIDE1Ljc0TDQgOUwxMC45MSA4LjI2TDEyIDJaIiBmaWxsPSIjNkM1Q0U3Ii8+Cjwvc3ZnPgo="

# Function to load CSS
def load_css(css_file):
    try:
        with open(css_file, "r") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        st.warning("CSS file not found. Using default styling.")

# Function to set background image
def set_background(image_path):
    base64_image = get_image_base64(image_path)
    background_style = f"""
    <style>
    .stApp {{
        background-image: url("data:image/svg+xml;base64,{base64_image}");
        background-size: cover;
    }}
    </style>
    """
    st.markdown(background_style, unsafe_allow_html=True)

# Load career data
def load_career_data():
    with open(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'careers.json'), 'r') as f:
        return json.load(f)

# Preprocess text
def preprocess_text(text):
    tokens = word_tokenize(text.lower())
    stop_words = set(stopwords.words('english'))
    filtered_tokens = [w for w in tokens if w not in stop_words and w.isalpha()]
    return filtered_tokens

# Extract keywords from user input
def extract_keywords(text):
    tokens = preprocess_text(text)
    # Simple keyword extraction - in a real app, you might use more sophisticated methods
    return tokens

# Match keywords to career fields
def match_careers(keywords, career_data):
    matches = {}
    
    for field, data in career_data.items():
        score = 0
        for keyword in keywords:
            if keyword in data["keywords"]:
                score += 1
        
        if score > 0:
            matches[field] = score
    
    # Sort by score
    sorted_matches = sorted(matches.items(), key=lambda x: x[1], reverse=True)
    return sorted_matches

# Get AI response using OpenRouter API
def get_ai_response(prompt, conversation_history):
    # Check if the user is asking about the creator
    creator_patterns = [
        "who created you", "who built you", "who developed you", "who invented you",
        "who made you", "your creator", "who programmed you", "who designed you",
        "who is your creator", "who is your developer", "who is your inventor",
        "who's your creator", "who's your developer", "who's your inventor",
        "who are you made by", "who are you created by", "who are you developed by"
    ]
    
    # Check if the prompt contains any of the creator patterns
    if any(pattern in prompt.lower() for pattern in creator_patterns):
        return "I was created by Susan Chandra from IIIT Kancheepuram to help provide career guidance and assistance."
    
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        return "API key not found. Please add your OpenRouter API key to the .env file."
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    messages = conversation_history + [{"role": "user", "content": prompt}]
    
    data = {
        "model": "openai/gpt-3.5-turbo",  # You can change this to another model
        "messages": messages
    }
    
    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers=headers,
        json=data
    )
    
    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        return f"Error: {response.status_code} - {response.text}"

# Custom HTML components
# Render modern header with enhanced design
def render_header():
    logo_path = os.path.join(os.path.dirname(__file__), 'assets', 'elevate_labs_logo.svg')
    logo_base64 = get_image_base64(logo_path)
    
    header_html = f"""
    <div class="modern-header">
        <div class="header-content">
            <div class="logo-section">
                <div class="logo-wrapper">
                    <img src="data:image/svg+xml;base64,{logo_base64}" alt="Elevate Labs Logo" class="logo-img">
                </div>
                <div class="title-section">
                    <h1 class="main-title">
                        <span class="gradient-text">AI Career</span>
                        <span class="highlight-text">Counsellor</span>
                    </h1>
                    <p class="subtitle-modern">✨ Powered by AI • Created by Susan from IIIT Kancheepuram</p>
                </div>
            </div>
            <div class="header-stats">
                <div class="stat-item">
                    <div class="stat-number">1000+</div>
                    <div class="stat-label">Career Paths</div>
                </div>
                <div class="stat-item">
                    <div class="stat-number">24/7</div>
                    <div class="stat-label">AI Support</div>
                </div>
            </div>
        </div>
        <div class="header-decoration"></div>
    </div>
    """
    st.markdown(header_html, unsafe_allow_html=True)

def render_message(role, content, avatar_path, timestamp=None):
    from datetime import datetime
    
    avatar_base64 = get_image_base64(avatar_path)
    message_class = "user-message" if role == "user" else "ai-message"
    
    # Generate timestamp if not provided
    if timestamp is None:
        timestamp = datetime.now().strftime("%I:%M %p")
    
    # Process content to handle markdown properly for AI messages
    if role == "assistant":
        import re
        import markdown
        
        # First handle code blocks with special styling
        code_block_pattern = r'```(?:\w+)?\n([\s\S]*?)\n```'
        
        def replace_code_block(match):
            code_content = match.group(1)
            return f'<div class="code-block"><code>{code_content}</code></div>'
        
        # Replace code blocks first
        content_with_code_blocks = re.sub(code_block_pattern, replace_code_block, content)
        
        # Then convert remaining markdown to HTML
        # Use markdown library to convert markdown to HTML
        content = markdown.markdown(content_with_code_blocks, extensions=['extra'])
        
        # No need for BeautifulSoup here as we want to keep the HTML as is
    
    if role == "user":
        message_html = f"""
        {content}\n{timestamp}\n
           
        
        """
    else:
        # AI message with proper container structure and avatar
        message_html = f"""
        {content}\n{timestamp}\n
        
        """
    return message_html

def render_career_card(title, description, skills, education, icon_path):
    icon_base64 = get_image_base64(icon_path)
    
    skills_html = "".join([f"<li>{skill}</li>" for skill in skills])
    education_html = "".join([f"<li>{edu}</li>" for edu in education])
    
    # Calculate a match percentage (for demonstration)
    import random
    match_percentage = random.randint(75, 98)
    
    card_html = f"""
    <div class="career-card">
        <div class="career-title">
            <img src="data:image/svg+xml;base64,{icon_base64}" width="32" height="32">
            {title.title()}
        </div>
        <div class="match-indicator" style="margin-bottom: 15px;">
            <div class="match-bar" style="width: {match_percentage}%; background: linear-gradient(90deg, var(--primary-color), var(--accent-color));"></div>
            <span class="match-text">{match_percentage}% Match</span>
        </div>
        <p>{description}</p>
        <h4>Key Skills</h4>
        <ul>{skills_html}</ul>
        <h4>Education Path</h4>
        <ul>{education_html}</ul>
        <div class="career-footer">
            <button class="learn-more-btn">Learn More</button>
        </div>
    </div>
    """
    return card_html

def render_footer():
    footer_html = """
    <div class="footer">
        <p>© 2023 AI Career Counsellor | Powered by Elevate Labs | Created by Susan from IIIT Kancheepuram</p>
    </div>
    """
    st.markdown(footer_html, unsafe_allow_html=True)

# Main app
def main():
    # Set page configuration
    st.set_page_config(
        page_title="AI Career Counsellor | Elevate Labs",
        page_icon=os.path.join(os.path.dirname(__file__), 'assets', 'favicon.svg'),
        layout="wide",
        initial_sidebar_state="collapsed"
    )
    
    # Load CSS
    load_css(os.path.join(os.path.dirname(__file__), 'style.css'))
    
    # Set background pattern
    set_background(os.path.join(os.path.dirname(__file__), 'assets', 'background_pattern.svg'))
    
    # Render header
    render_header()
    
    # Initialize session state for conversation history
    if "conversation_history" not in st.session_state:
        st.session_state.conversation_history = [
            {"role": "system", "content": "You are a helpful career counsellor created by Susan from IIIT Kancheepuram. Your goal is to help users discover suitable career paths based on their interests, skills, and aspirations. Provide detailed information about potential careers, required skills, education paths, and job prospects."}
        ]
    
    # Initialize session state for recommended careers
    if "recommended_careers" not in st.session_state:
        st.session_state.recommended_careers = []
    
    # Load career data
    career_data = load_career_data()
    
    # Create two columns layout
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("<h2 style='color: var(--primary-color);'>Chat with your Career Counsellor</h2>", unsafe_allow_html=True)
        
        # Chat container
        chat_html = ""
        
        # Check if there are messages to display
        if len(st.session_state.conversation_history) > 1:
            # Display chat history
            for message in st.session_state.conversation_history[1:]:
                if message["role"] == "user":
                    avatar_path = os.path.join(os.path.dirname(__file__), 'assets', 'user_avatar.svg')
                    chat_html += render_message("user", message["content"], avatar_path)
                else:
                    avatar_path = os.path.join(os.path.dirname(__file__), 'assets', 'ai_avatar.svg')
                    chat_html += render_message("ai", message["content"], avatar_path)
        else:
            # Display empty chat state
            ai_avatar_path = os.path.join(os.path.dirname(__file__), 'assets', 'ai_avatar.svg')
            ai_avatar_base64 = get_image_base64(ai_avatar_path)
            chat_html += f"""
            <div class="empty-chat">
                <img src="data:image/svg+xml;base64,{ai_avatar_base64}" alt="AI Avatar">
                <h3>Welcome to AI Career Counsellor!</h3>
                <p>Share your interests, skills, or ask questions about specific careers to get personalized guidance.</p>
            </div>
            """
           
        
       # chat_html += "</div>"
        st.markdown(chat_html, unsafe_allow_html=True)
        
        # Input area
        st.markdown("<div class='input-area'>", unsafe_allow_html=True)
        user_input = st.text_area("Tell me about your interests, skills, or ask questions about specific careers:", height=100, key="user_input")
        col1_1, col1_2, col1_3 = st.columns([1, 1, 1])
        with col1_2:
            send_button = st.button("Send", use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
        
        if send_button and user_input:
            # Add user message to history
            st.session_state.conversation_history.append({"role": "user", "content": user_input})
            
            # Extract keywords and match careers
            keywords = extract_keywords(user_input)
            career_matches = match_careers(keywords, career_data)
            
            # Update recommended careers
            st.session_state.recommended_careers = career_matches[:3]  # Top 3 matches
            
            # Get AI response
            with st.spinner("Thinking..."):
                ai_response = get_ai_response(user_input, st.session_state.conversation_history)
            
            # Add AI response to history
            st.session_state.conversation_history.append({"role": "assistant", "content": ai_response})
            
            # Rerun to update the UI
            st.experimental_rerun()
    
    with col2:
        st.markdown("<h2 style='color: var(--secondary-color);'>Recommended Careers</h2>", unsafe_allow_html=True)
        
        if st.session_state.recommended_careers:
            career_cards_html = ""
            for field, score in st.session_state.recommended_careers:
                icon_path = os.path.join(os.path.dirname(__file__), 'assets', 'career_icon.svg')
                career_cards_html += render_career_card(
                    field.replace('_', ' '),
                    career_data[field]['description'],
                    career_data[field]['skills'],
                    career_data[field]['education'],
                    icon_path
                )
            st.markdown(career_cards_html, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style="background-color: var(--card-bg); border-radius: var(--border-radius); padding: 1.5rem; text-align: center;">
                <img src="data:image/svg+xml;base64,{0}" width="60" height="60" style="margin-bottom: 1rem;">
                <p>Share your interests and skills to get personalized career recommendations!</p>
            </div>
            """.format(get_image_base64(os.path.join(os.path.dirname(__file__), 'assets', 'career_icon.svg'))), unsafe_allow_html=True)
        
        # Reset button
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Start New Conversation", use_container_width=True):
            st.session_state.conversation_history = [
                {"role": "system", "content": "You are a helpful career counsellor created by Susan from IIIT Kancheepuram. Your goal is to help users discover suitable career paths based on their interests, skills, and aspirations. Provide detailed information about potential careers, required skills, education paths, and job prospects."}
            ]
            st.session_state.recommended_careers = []
            st.experimental_rerun()
    
    # Render footer
    render_footer()

if __name__ == "__main__":
    main()