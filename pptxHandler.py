import asyncio
import os
import json
import pptx
import openai


async def process_slide(slide_text):
    prompt = f"Explain the content of the slide:\n{slide_text}\n"
    response = await openai.Completion.create(
        model="gpt-3.5-turbo",
        prompt=prompt,
    )
    explanation = response.choices[0].text.strip()
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

    openai.api_key = "API_KEY"

    explanations = await process_presentation(presentation_path)

    # Save explanations to a JSON file
    with open(output_file, "w") as f:
        json.dump(explanations, f, indent=4)

    print("Explanations saved successfully.")


if __name__ == "__main__":
    asyncio.run(main())
