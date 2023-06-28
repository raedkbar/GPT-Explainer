class SlideProcessingError(Exception):
    def __init__(self, slide_num, message):
        self.slide_num = slide_num
        self.message = message
        super().__init__(f"Error occurred while processing slide {slide_num}: {message}")


class PresentationProcessingError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(f"Failed to process presentation: {message}")


class OpenAIError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(f"OpenAI error occurred: {message}")