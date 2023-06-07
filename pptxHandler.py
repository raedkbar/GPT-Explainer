import asyncio
import os
import json
import pptx
import openai

API_KEY = "API_KEY"
PROMPT_INIT = "Explain the content of the following slide. Write a response as if you were writing an article:"


async def process_slide(slide_text):
    print("Slide text:", slide_text)
    prompt = f"{PROMPT_INIT}\n{slide_text}\n"
    print("Generated prompt:", prompt)

    response = await openai.ChatCompletion.acreate(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that explains PowerPoint slides:"},
            {"role": "user", "content": prompt}
        ]
    )

    explanation = response.choices[0].message.content
    print(str(explanation))
    return explanation


async def process_presentation(presentation_path):
    presentation = pptx.Presentation(presentation_path)
    slides = []

    for slide in presentation.slides:
        slide_text = ""

        for shape in slide.shapes:
            if shape.has_text_frame:
                for paragraph in shape.text_frame.paragraphs:
                    for run in paragraph.runs:
                        slide_text += run.text

        slides.append(slide_text.strip())

    print("Extracted slide texts:", slides)

    explanations = []

    for i, slide_text in enumerate(slides, start=1):
        if slide_text:
            try:
                explanation = await process_slide(slide_text)
            except Exception as e:
                explanation = f"Failed to process slide: {str(e)}"
            explanations.append({"slide": i, "explanation": explanation})
        else:
            explanations.append({"slide": i, "explanation": None})

    return explanations


async def main():
    presentation_path = "presentation.pptx"
    output_file = os.path.splitext(presentation_path)[0] + ".json"

    openai.api_key = API_KEY

    explanations = await process_presentation(presentation_path)

    # Save explanations to a JSON file
    with open(output_file, "w") as f:
        json.dump(explanations, f, indent=4)

    print("Explanations saved successfully.")


if __name__ == "__main__":
    asyncio.run(main())
