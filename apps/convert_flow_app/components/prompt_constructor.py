from lightrag.core import Component
from lightrag.core.prompt_builder import Prompt
from typing import List
from data_classes.flow import Pattern, Example
from prompts.convert_flow_prompt import CONVERT_FLOW_PROMPT


class PromptConstructor(Component):
    def __init__(self):
        super().__init__()
        self.prompt_template = Prompt(
                template=CONVERT_FLOW_PROMPT,
                prompt_kwargs={}
        )

    def call(self, input_format: str, output_format: str, patterns: List[Pattern], examples: List[Example]) -> str:
        patterns_str = "\n".join([pattern.description for pattern in patterns])
        examples_str = "\n\n".join([example.output for example in examples])

        self.prompt_template.prompt_kwargs.update({
            "input_format":    input_format,
            "output_format":   output_format,
            "summaryPatterns": patterns_str,
            "examples":        examples_str
        })

        return self.prompt_template()