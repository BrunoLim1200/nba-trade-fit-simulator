# Frontend README.md

# NBA Trade Fit Simulator - Frontend

This is the frontend application for the NBA Trade Fit Simulator project, built using Angular. The application allows users to simulate how a selected NBA player would fit into a chosen team's rotation based on statistical analysis.

## Project Structure

- `src/`: Contains the main source code for the Angular application.
  - `app/`: The main application module.
    - `core/`: Core services, models, and interceptors.
    - `features/`: Feature modules for different parts of the application.
    - `shared/`: Shared components used across the application.
  - `environments/`: Environment-specific configuration files.
  - `index.html`: The main HTML file for the application.
  - `main.ts`: The entry point for the Angular application.
  - `styles.scss`: Global styles for the application.

## Getting Started

To get started with the frontend application, follow these steps:

1. **Install Dependencies**: Make sure you have Node.js and npm installed. Then, navigate to the `frontend` directory and run:
   ```
   npm install
   ```

2. **Run the Application**: After installing the dependencies, you can run the application using:
   ```
   ng serve
   ```
   This will start the development server, and you can access the application at `http://localhost:4200`.

## Features

- Player Search: Search for NBA players by name.
- Team Selector: Select a target NBA team.
- Simulation Result: View how the selected player fits into the team's rotation.

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue for any suggestions or improvements.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.