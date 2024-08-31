# AniBot: Anime Recommendation Chatbot

## Project Overview

AniBot is an AI-powered chatbot designed to recommend anime movies and TV shows based on user preferences such as genre, timeline, mood, and other factors. This project aims to help anime enthusiasts discover new content tailored to their tastes.

## Project Structure

The project is organized into two main directories:

- `backend/`: Contains the FastAPI application, database interactions, and AI/ML models.
- `frontend/`: Will contain the React.js frontend application (to be implemented).

## Features (Planned)

- Personalized anime recommendations
- Genre-based filtering
- Mood-based suggestions
- Timeline-specific recommendations
- User preference learning
- Conversational interface

## Tech Stack

### Backend
- Language: Python 3.9+
- Web Framework: FastAPI
- Database: MongoDB
- AI/ML: TensorFlow
- NLP: spaCy
- ODM: Motor (asynchronous MongoDB driver)

### Frontend (Planned)
- Framework: React.js
- State Management: Redux (tentative)
- UI Library: Material-UI or Chakra UI (to be decided)

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

5. Open your browser and navigate to `http://localhost:8000` to see the API documentation.

## Backend Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── routers/
│   │   ├── __init__.py
│   │   └── anime.py
│   └── services/
│       ├── __init__.py
│       ├── recommendation.py
│       └── nlp.py
├── .env
├── requirements.txt
└── README.md
```

## API Endpoints

- `POST /anime/`: Create a new anime entry
- `GET /anime/{anime_id}`: Retrieve details of a specific anime

More endpoints will be added as the project develops.

## Development Roadmap

1. Implement core recommendation logic
2. Expand NLP capabilities for better understanding of user queries
3. Develop data ingestion scripts for populating the database
4. Implement user authentication and personalization features
5. Begin frontend development with React.js
6. Integrate frontend and backend
7. Implement conversational UI
8. Conduct thorough testing and refinement
9. Deploy MVP (Minimum Viable Product)

## Contributing

This project is currently in its early stages. Contributions, ideas, and feedback are welcome! Please feel free to open an issue or submit a pull request.

## License

[MIT License](https://opensource.org/licenses/MIT)

## Contact

[Fazli Berisha] - [fazliberisha03@gmail.com]

Project Link: https://github.com/FazliBerisha/anibot
