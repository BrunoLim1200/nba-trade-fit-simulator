# NBA Trade Fit Simulator

## Overview
The NBA Trade Fit Simulator is a web application designed to help users evaluate how a selected NBA player would fit into a target team's rotation. By analyzing player statistics and team composition, the application provides insights into whether the player would be a starter, a sixth man, part of the rotation, or on the bench.

## Features
- Search for NBA players by name.
- Select a target NBA team by name or ID.
- Analyze player statistics using the NBA API.
- Determine player fit based on Player Efficiency Rating (PER) compared to the team's current players.

## Technology Stack
- **Backend:**
  - Python 3.11+
  - FastAPI for building the REST API
  - Pandas for data manipulation
  - SQLAlchemy as the ORM
  - `nba_api` for fetching NBA statistics

- **Frontend:**
  - Angular 17+ for building the user interface
  - Angular Material for UI components
  - Ngx-Charts for data visualization

- **Database:**
  - SQLite for the MVP (with plans to migrate to PostgreSQL)

## Getting Started

### Prerequisites
- Python 3.11+
- Node.js and npm (for Angular)

### Backend Setup
1. Navigate to the `backend` directory.
2. Install the required Python packages:
   ```
   pip install -r requirements.txt
   ```
3. Run the FastAPI application:
   ```
   uvicorn src.main:app --reload
   ```

### Frontend Setup
1. Navigate to the `frontend` directory.
2. Install the required Node packages:
   ```
   npm install
   ```
3. Run the Angular application:
   ```
   ng serve
   ```

## API Endpoints
- `GET /simulate-fit`: Simulates the fit of a player into a team based on `player_id` and `team_id`.

## Contributing
Contributions are welcome! Please feel free to submit a pull request or open an issue for any suggestions or improvements.

## License
This project is licensed under the MIT License. See the LICENSE file for more details.