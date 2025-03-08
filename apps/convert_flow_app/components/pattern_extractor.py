from lightrag.core import Component
from lightrag.components.model_client import OpenAIClient
from lightrag.core.generator import Generator
from lightrag.core.prompt_builder import Prompt
from typing import List
from data_classes.flow import Example, Pattern
from prompts.extract_patterns_prompt import EXTRACT_PATTERNS_PROMPT


class PatternExtractor(Component):
    def __init__(self):
        super().__init__()
        self.generator = Generator(
            model_client=OpenAIClient(),
            model_kwargs={"model": "gpt-3.5-turbo"},
            template=EXTRACT_PATTERNS_PROMPT
        )

    def call(self, examples: List[Example]) -> List[Pattern]:
        examples_str = "\n\n".join([ex.output for ex in examples])
        response = self.generator({"examples": examples_str})
        return response.data if response.data else "No patterns extracted"
