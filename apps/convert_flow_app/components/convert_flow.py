from lightrag.core import Component
from lightrag.components.model_client import OpenAIClient
from lightrag.core.generator import Generator
from data_classes.flow import Flow


class ConvertFlow(Component):
    def __init__(self):
        super().__init__()
        self.generator = Generator(
            model_client=OpenAIClient(),
            model_kwargs={"model": "gpt-3.5-turbo"}
        )

    def call(self, content: str, flow: Flow) -> str:
        prompt = flow.prompt.replace("{{input}}", content)
        response = self.generator({"input_str": prompt})
        return response.data if response.data else "No patterns extracted"
