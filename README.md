# AniBot: Anime Recommendation Chatbot

## Project Overview

AniBot is an AI-powered chatbot designed to recommend anime movies and TV shows based on user preferences such as genre, timeline, mood, and other factors. This project aims to help anime enthusiasts discover new content tailored to their tastes.

## Project Structure

The project is organized into two main directories:

- `backend/`: Contains the FastAPI application, database interactions, and AI/ML models.
- `frontend/`: Contains the React.js frontend application.

## Features

### Implemented
- Basic chatbot functionality
- Genre-based anime recommendations
- Integration with Jikan API for anime data

### Planned
- Personalized anime recommendations
- Mood-based suggestions
- Timeline-specific recommendations
- User preference learning
- Enhanced conversational interface

## Tech Stack

### Backend
- Language: Python 3.9+
- Web Framework: FastAPI
- Database: MongoDB
- AI/ML: TensorFlow (planned)
- NLP: spaCy
- ODM: Motor (asynchronous MongoDB driver)

### Frontend
- Framework: React.js
- State Management: React Hooks
- UI Library: Material-UI

## Setup

1. Clone the repository:
   ```
   git clone https://github.com/FazliBerisha/anibot.git
   cd anibot
   ```

2. Set up the backend:
   ```
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   pip install -r requirements.txt
   python -m spacy download en_core_web_sm
   ```

3. Set up environment variables:
   Create a `.env` file in the `backend/` directory with the following content:
   ```
   MONGODB_URL=mongodb://localhost:27017
   DATABASE_NAME=anibot
   ```

4. Run the backend application:
   ```
   uvicorn app.main:app --reload
   ```

5. Set up the frontend:
   ```
   cd ../frontend/anibot-react
   npm install
   ```

6. Run the frontend application:
   ```
   npm start
   ```

7. Open your browser and navigate to `http://localhost:3000` to use the application.

## API Endpoints

- `POST /api/v1/chat/`: Send a message to the chatbot
- `POST /api/v1/anime/`: Create a new anime entry
- `GET /api/v1/anime/{anime_id}`: Retrieve details of a specific anime

More endpoints will be added as the project develops.

## Development Roadmap

1. Enhance recommendation logic
2. Expand NLP capabilities for better understanding of user queries
3. Develop data ingestion scripts for populating the database
4. Implement user authentication and personalization features
5. Improve frontend UI/UX
6. Implement advanced conversational UI features
7. Conduct thorough testing and refinement
8. Deploy MVP (Minimum Viable Product)

## Contributing

This project is currently in its alpha stage. Contributions, ideas, and feedback are welcome! Please feel free to open an issue or submit a pull request.

## License

[MIT License](https://opensource.org/licenses/MIT)

## Contact

[Fazli Berisha] - [fazliberisha03@gmail.com]

Project Link: https://github.com/FazliBerisha/anibot
