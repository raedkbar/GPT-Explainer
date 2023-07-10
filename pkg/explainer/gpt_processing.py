import openai

from pkg.explainer.exceptions import SlideProcessingError

API_KEY = "API_KEY"     # TODO: Type you openai API key here.
PROMPT_INIT = "Explain the content of the following slide. " \
              "Write a response as if you were writing an article, and don't break the fourth wall! " \
              "Meaning, don't mention the words slide or presentation:"
SYSTEM_PROMPT = "You are a helpful assistant that explains PowerPoint slides:"
MODEL_VERSION = "gpt-3.5-turbo"
MAX_RETRIES = 3  # Maximum number of retries for slide processing

# Define the path to the database file
UPLOADS_DIR = "uploads"
OUTPUTS_DIR = "outputs"


async def process_slide(slide_num, slide_text, retry_count=1):
    """
    Processes a slide by generating an explanation using OpenAI's ChatCompletion model.

    Args:
        slide_num (int): The slide number.
        slide_text (str): The text content of the slide.
        retry_count (int): The number of times the slide processing has been retried (default: 1).

    Returns:
        str: The generated explanation for the slide.

    Raises:
        SlideProcessingError: If the slide processing fails after the maximum number of retries.
    """
    try:
        openai.api_key = API_KEY
        print(f"Processing slide {slide_num}...\n")
        prompt = f"{PROMPT_INIT}\n{slide_text}\n"
        response = await openai.ChatCompletion.acreate(
            model=MODEL_VERSION,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt}
            ]
        )
        explanation = response.choices[0].message.content
        return explanation
    except Exception as e:
        if retry_count < MAX_RETRIES:
            print(f"Error occurred while processing slide {slide_num}: {str(e)}\n")
            print(f"Retrying to process slide {slide_num}. Retry count: {retry_count + 1}\n")
            return await process_slide(slide_num, slide_text, retry_count=retry_count + 1)
        else:
            raise SlideProcessingError(slide_num, str(e)) from e
