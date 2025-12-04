# NBA Trade Fit Simulator

## Backend

This project utilizes FastAPI for the backend, providing a RESTful API to simulate the fit of an NBA player within a selected team. The backend is structured to follow Clean Architecture principles, ensuring separation of concerns and maintainability.

### Directory Structure

- **src/**: Contains the main application code.
  - **api/**: Defines the API routes and dependencies.
  - **core/**: Contains configuration and constants.
  - **domain/**: Holds the business logic, including entities and services.
  - **infrastructure/**: Manages database connections and external API interactions.
  - **schemas/**: Defines Pydantic models for data validation and serialization.

### Requirements

To install the necessary dependencies for the backend, run:

```bash
pip install -r requirements.txt
```

### Running the Application

To start the FastAPI application, use the following command:

```bash
uvicorn src.main:app --reload
```

The API will be available at `http://127.0.0.1:8000`.

## Frontend

The frontend is built using Angular, providing a user-friendly interface for interacting with the backend API. It leverages Angular Material for UI components and Ngx-Charts for data visualization.

### Directory Structure

- **src/**: Contains the main application code.
  - **app/**: Holds the core application logic, including services, models, and components.
  - **shared/**: Contains shared components used across the application.
  - **environments/**: Defines environment-specific configurations.

### Running the Application

To run the Angular application, navigate to the `frontend` directory and execute:

```bash
ng serve
```

The application will be available at `http://localhost:4200`.

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue for any suggestions or improvements.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.