# AI Career Counsellor Project Report

## Introduction

The AI Career Counsellor is an innovative application designed to provide personalized career guidance to users through an interactive chat interface. Developed by Susan Chandra from IIIT Kancheepuram for Elevate Labs, this project leverages artificial intelligence and natural language processing to analyze user interests and recommend suitable career paths. The application aims to bridge the gap between career aspirations and informed decision-making by providing accessible, AI-powered career counseling.

## Abstract

This project implements a modern web-based career counseling application that combines natural language processing techniques with a comprehensive career database to deliver personalized guidance. The system processes user inputs through keyword extraction and matching algorithms to identify relevant career paths. Additionally, it utilizes the OpenRouter API (GPT-3.5 Turbo) to generate conversational responses, creating a dynamic and engaging user experience. The application features a responsive user interface with real-time career recommendations displayed alongside the chat conversation, making career exploration intuitive and informative.

## Tools Used

- **Python**: Core programming language for backend development
- **Streamlit**: Web application framework for creating the interactive interface
- **NLTK (Natural Language Toolkit)**: For text processing and keyword extraction
- **OpenRouter API (GPT-3.5 Turbo)**: For generating conversational AI responses
- **JSON**: For storing structured career data
- **Markdown & HTML**: For formatting chat messages and UI elements
- **CSS**: For custom styling and responsive design
- **SVG Graphics**: For vector-based icons and visual elements

## Steps Involved in Building the Project

1. **Project Planning and Design**:
   - Defined project requirements and user experience goals
   - Designed the application architecture and data flow
   - Created wireframes for the user interface

2. **Data Collection and Structuring**:
   - Compiled comprehensive career information including descriptions, required skills, and education paths
   - Organized data in a structured JSON format with relevant keywords for matching
   - Designed a scoring system for career recommendations based on keyword matching

3. **Backend Development**:
   - Implemented natural language processing functions using NLTK for text preprocessing and keyword extraction
   - Developed the career matching algorithm to score and rank career recommendations
   - Integrated the OpenRouter API for AI-powered conversational responses
   - Created custom response handling for specific queries (e.g., creator information)

4. **Frontend Development**:
   - Built the user interface using Streamlit with custom HTML/CSS components
   - Designed a modern header with Elevate Labs branding
   - Implemented the chat interface with user and AI message styling
   - Created responsive career recommendation cards in the sidebar
   - Added custom SVG icons and visual elements for enhanced user experience

5. **Testing and Refinement**:
   - Conducted user testing to identify usability issues
   - Refined the keyword matching algorithm for more accurate recommendations
   - Optimized the UI for different screen sizes and devices
   - Enhanced error handling and edge cases

## Conclusion

The AI Career Counsellor project successfully demonstrates the potential of AI-powered applications in providing personalized career guidance. By combining natural language processing techniques with a comprehensive career database and conversational AI, the application offers an accessible and informative platform for career exploration. The modern, responsive interface enhances user engagement, while the real-time recommendations provide valuable insights into various career paths.

This project serves as a foundation for future enhancements, such as incorporating more sophisticated matching algorithms, expanding the career database, and implementing user profiles for personalized tracking. The AI Career Counsellor represents a significant step toward democratizing career guidance and making professional advice more accessible to individuals at various stages of their career journey.