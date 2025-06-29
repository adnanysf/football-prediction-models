# Football Prediction Models

A FastAPI-based web service for football match predictions using different models, using only Poisson distribution for now. This application fetches real-time football data from the API-Football service and provides statistical predictions for match outcomes. This is meant to be a service that can be used with a front facing client.

## Features

- **Real-time Football Data**: Fetches leagues, teams, and statistics from API-Football
- **Poisson Model Prediction**: Uses statistical modeling to predict match outcomes
- **RESTful API**: Clean REST endpoints for accessing football data and predictions
- **Caching**: Built-in request caching to reduce API calls and improve performance
- **Comprehensive Testing**: Includes both mock and real data testing capabilities

## Project Structure

```
football-prediction-models/
├── server.py              # FastAPI server with API endpoints
├── GAPoissonModel.py      # Poisson distribution model for predictions
├── test.py               # Comprehensive test suite
├── requirements.txt      # Python dependencies
├── startup-instructions.txt # Quick setup commands
├── football_api_cache.sqlite # API response cache database
└── __pycache__/          # Python bytecode cache
```

## Prerequisites

- Python 3.7+
- API-Football subscription (for real data)

## Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd football-prediction-models
   ```

2. **Create and activate virtual environment**:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # macOS/Linux
   # or
   .venv\Scripts\activate     # Windows
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Setup**:
   Create a `.env` file in the project root with your API credentials:
   ```env
   APIFOOTBALL_API_KEY=your_api_key_here
   APIFOOTBALL_API_URL=https://v3.football.api-sports.io
   DEBUG=False
   ```

## Usage

### Starting the Server

1. **Run the FastAPI server**:
   ```bash
   uvicorn server:app --reload --port 8000
   ```

2. **Access the API**:
   - Base URL: `http://localhost:8000`
   - API Documentation: `http://localhost:8000/docs`

### API Endpoints

#### Get Leagues by Country
```http
GET /leagues/{country}
```
Returns available leagues for a specific country.

**Example**: `GET /leagues/England`

#### Get Teams by League
```http
GET /teams/{leagueId}
```
Returns teams participating in a specific league for the 2023 season.

**Example**: `GET /teams/39` (Premier League)

#### Get Team Statistics
```http
GET /stats/{teamId}/{leagueId}
```
Returns detailed statistics for a team in a specific league.

**Example**: `GET /stats/50/39` (Manchester City in Premier League)

### Running Tests

Execute the comprehensive test suite:
```bash
python test.py
```

The test suite includes:
- Server startup verification
- Mock data prediction testing
- Real API data testing
- Poisson model validation

## Poisson Model

The `GAPoissonModel.py` implements a Poisson distribution-based prediction system that:

1. **Calculates Attack/Defense Strengths**: Based on team's goal-scoring and conceding averages
2. **Determines Expected Goals**: Uses league averages and team strengths
3. **Computes Match Probabilities**: Calculates win/draw/loss probabilities
4. **Provides Predictions**: Returns expected goals and outcome probabilities

### Model Input Format

The model expects team data in the following format:
```python
{
    'team_name': 'Team Name',
    'team_id': 123,
    'league_id': 456,
    'goals': {
        'for': {
            'average': {
                'home': 2.1,
                'away': 1.8
            }
        },
        'against': {
            'average': {
                'home': 0.8,
                'away': 1.0
            }
        }
    }
}
```

### Prediction Output

```python
{
    'expected_goals': {
        'Home Team': 1.85,
        'Away Team': 1.23
    },
    'probabilities': {
        'Home Team home_win': 45.2,
        'draw': 28.3,
        'Away Team away_win': 26.5
    }
}
```

## Caching

The application uses `requests_cache` to cache API responses for one week, reducing:
- API call frequency
- Response times
- API quota usage

Cache is stored in `football_api_cache.sqlite`.

## Error Handling

The API includes comprehensive error handling for:
- Missing API credentials
- Invalid API responses
- Network connectivity issues
- Data validation errors

## Development

### Common Issues

1. **Server won't start**:
   - Check if port 8000 is available
   - Verify all dependencies are installed
   - Ensure virtual environment is activated

2. **API errors**:
   - Verify API credentials in `.env` file
   - Check internet connection
   - Confirm API quota hasn't been exceeded

3. **Prediction errors**:
   - Ensure team statistics are available
   - Verify data format matches expected structure
   - Check for division by zero in calculations

### Debug Mode

Enable debug mode by setting `DEBUG=True` in your `.env` file for detailed error logs.

## Contributing
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## License

This project is available for educational and research purposes. Please ensure compliance with API-Football's terms of service when using their data.

## Support

For issues and questions:
1. Check existing documentation
2. Review error logs
3. Verify API credentials and quotas
4. Test with mock data to isolate issues
