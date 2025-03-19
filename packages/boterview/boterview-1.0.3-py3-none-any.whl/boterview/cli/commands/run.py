# Imports.
import click
import uvicorn
from fastapi import FastAPI
from boterview.server.sever import create_server
from boterview.services.configuration.configuration import Configuration
from boterview.services.boterview.boterview import Boterview
from boterview.services.ui.ui import UI

# Import the application context.
import boterview.context.app as app


# Command to run a `boterview` study.
@click.command(name = "run")
@click.option("--config", type = str, required = True, help = "The study `.toml` configuration file to use.")
@click.option("--port", type = int, default = 8080, help = "The port for the application (i.e., defaults to `8080`).")
@click.option("--port-frontend", type = int, default = 5173, help = "The port for the development frontend application (i.e., defaults to `5173`).")
@click.option("--database", type = str, default = "boterview.db", help = "The name of the database to use (i.e., defaults to `boterview.db`).")
@click.option("--headless", is_flag = True, help = "Run the application in headless mode.")
def run(config: str, port: int, port_frontend: int, database: str, headless: bool) -> None:
    """Command to start a study based on a configuration file."""

    # Get the current configuration.
    configuration: Configuration = app.get_configuration()

    # Get the current user interface.
    ui: UI = app.get_ui()

    #  Get the current `boterview` instance.
    boterview: Boterview = app.get_boterview()

    # Load the configuration.
    configuration.load_configuration(config)

    # Initialize the user interface.
    ui.initialize_ui(configuration)

    # Initialize the `boterview` study.
    boterview.initialize_study(configuration)

    # Create the server instance.
    server: FastAPI = create_server(port, port_frontend, database, headless)

    # Start the `FastAPI` server.
    uvicorn.run(
        server,
        host = "localhost",
        port = port,
        log_level = "info"
    )
