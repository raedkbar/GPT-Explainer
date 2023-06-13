<!DOCTYPE html>
<html>
<body>
  <h1>The GPT-Explainer Project</h1>
  <p>This program consists of four Python scripts that work together to provide functionality for processing PowerPoint presentations and generating explanations for each slide. The scripts include:</p>
  <ol>
    <li><code>gptExplainer.py</code>: This script contains functions for processing individual slides, processing the entire presentation, and handling file uploads. It uses OpenAI's ChatCompletion model to generate explanations for the slides. The explanations are then saved to a JSON file.</li>
    <li><code>userClient.py</code>: This script serves as a client for interacting with a web application. It provides a command-line interface for uploading a PowerPoint presentation file to the web application and retrieving the status and explanation of the uploaded file.</li>
    <li><code>flaskWebAPI.py</code>: This script implements a Flask-based web API that handles file uploads, generates unique identifiers (UIDs) for uploaded files, and provides status and explanation information for uploaded files. It uses the Flask framework to handle HTTP requests and responses.</li>
    <li><code>systemTests.py</code>: This script performs a system test by starting the web API, uploading a sample presentation, and starting the explainer. It provides a way to test the functionality of the entire system.</li>
  </ol>

  <h2>Script Descriptions</h2>
  <h3><code>gptExplainer.py</code></h3>
  <p>This script provides functions for processing individual slides, processing entire presentations, and handling file uploads. The main functionalities of the script include:</p>
  <ul>
    <li><code>process_slide(slide_num, slide_text)</code>: Processes a single slide by generating an explanation using OpenAI's ChatCompletion model. The generated explanation is returned as a string.</li>
    <li><code>extract_slide_text(slide)</code>: Extracts the text content from a slide object and returns it as a string.</li>
    <li><code>process_presentation(presentation_path)</code>: Processes a PowerPoint presentation by extracting slide texts and generating explanations for each slide. The result is returned as a list of dictionaries, where each dictionary contains the slide number and its corresponding explanation.</li>
    <li><code>process_file(file_path)</code>: Processes a file by generating explanations for each slide in the PowerPoint presentation. The explanations are saved to a JSON file.</li>
  </ul>

  <h3><code>userClient.py</code></h3>
  <p>This script provides a command-line interface for interacting with the web application. The main functionalities of the script include:</p>
  <ul>
    <li><code>upload_file(file_path)</code>: Uploads a PowerPoint presentation file to the web application.</li>
    <li><code>get_status(uid)</code>: Retrieves the status of an uploaded file based on its unique identifier.</li>
    <li><code>get_explanation(uid)</code>: Retrieves the explanation of an uploaded file based on its unique identifier.</li>
  </ul>

  <h3><code>flaskWebAPI.py</code></h3>
  <p>This script implements a Flask-based web API that handles file uploads, generates unique identifiers for uploaded files, and provides status and explanation information for uploaded files.</p>

  <h3><code>systemTests.py</code></h3>
  <p>This script performs a system test by starting the web API, uploading a sample presentation, and starting the explainer. It provides a way to test the functionality of the entire system.</p>
</body>
</html>
