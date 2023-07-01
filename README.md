## The GPT-Explainer Project

This repository contains the GPT-Explainer project, which consists of Python scripts that work together to provide functionality for processing PowerPoint presentations and generating explanations for each slide.

### Script Descriptions

The program is designed to process PowerPoint presentations and generate explanations for each slide. It uses OpenAI's ChatCompletion model to generate the explanations. The program consists of several scripts:

- `exceptions.py`: Defines custom exceptions used in the program.
- `gpt_processing.py`: Contains functions for processing individual slides using OpenAI's ChatCompletion model.
- `presentation_processing.py`: Processes a PowerPoint presentation by extracting slide texts and generating explanations for each slide.
- `db_session.py`: Handles the database session for storing upload records.
- `flask_web_API.py`: Provides a Flask web API for uploading files and checking the status of uploads.
- `gpt_explainer.py`: Scans the database for pending uploads and processes them.
- `model.py`: Defines the database models for users and uploads.
- `user_client.py`: Provides a client for interacting with the web application.


### Requirements

To run the program, you need to have the following installed:

- Python 3.7 or later
- OpenAI Python package (`openai`)
- Flask Python package (`flask`)
- pptx Python package (`python-pptx`)
- aiohttp Python package (`aiohttp`)

You also need to have an OpenAI API key to use the ChatCompletion model.


### Usage

- Set up the database by running the following command:
- db_session.py: This will create an empty SQLite database file.
- flask_web_API.py: Start the Flask web API
- gpt_explainer.py: Start the GPT explainer. The explainer will start scanning the database for pending uploads and process them. When available ot will upload a PowerPoint presentation file using the web API.
- Check the status of an upload using the web API:
- You can specify the uid parameter to retrieve the status of a specific upload. Alternatively, you can specify filename and email parameters to retrieve the status of the most recent upload with the given filename and email.
- Use the userClient.py script to interact with the web application from the command line:
  `python user_client.py --file <file_path> [--email <email>]`
  This script uploads a PowerPoint presentation file to the web application and displays the status of the upload.
- Upload a PowerPoint presentation file using the web API:


### Configuration

The program uses the following configuration options:

    API_KEY: The API key for OpenAI.
    PROMPT_INIT: The initial prompt to be used when generating explanations for slides.
    MODEL_VERSION: The version of the ChatCompletion model to use.
    MAX_RETRIES: The maximum number of retries for processing a slide.
    UPLOADS_DIR: The directory where uploaded files are stored.
    OUTPUTS_DIR: The directory where output files are stored.

You can modify these options in the respective scripts to customize the program behavior.

### File Structure

As shown before, the program consists of the following files and directories:

- exceptions.py: Contains custom exception classes for error handling.
- gpt_processing.py: Implements slide processing using OpenAI's ChatCompletion model. 
- presentation_processing.py: Processes PowerPoint presentations by extracting slide texts and generating explanations. 
- db_session.py: Sets up the database session and creates tables if they don't exist. 
- flask_web_API.py: Provides a web API for uploading files and checking upload status. 
- gpt_explainer.py: Runs indefinitely to process pending uploads and generate explanations. 
- model.py: Defines the database models for users and uploads. 
- user_client.py: Provides a client for interacting with the web application API.

### Database

The program uses a SQLite database to store upload records and user information.
The database file is located at db/explainer.db.

### Notes

- Make sure to replace API_KEY in gpt_processing.py with your actual OpenAI API key. 
- The uploads directory is used to store PowerPoint presentation files. 
- The outputs directory is used to store the generated explanations.