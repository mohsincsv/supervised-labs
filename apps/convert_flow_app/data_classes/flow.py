from lightrag.core import DataClass
from dataclasses import dataclass, field
from typing import List


@dataclass
class Example(DataClass):
    output: str = field(metadata={"desc": "The output text example"})


@dataclass
class Pattern(DataClass):
    description: str = field(metadata={"desc": "Description of the pattern"})
    category: str = field(metadata={"desc": "Category of the pattern"}, default="")

@dataclass
class Flow(DataClass):
    name: str = field(metadata={"desc": "Name of the flow"})
    input_format: str = field(metadata={"desc": "The input format description"})
    output_format: str = field(metadata={"desc": "The output format description"})
    examples: List[Example] = field(metadata={"desc": "List of output examples"})
    patterns: List[Pattern] = field(metadata={"desc": "List of extracted patterns"})
    prompt: str = field(metadata={"desc": "The constructed prompt for the flow"})