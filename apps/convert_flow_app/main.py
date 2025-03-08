import gradio as gr
from lightrag.utils import setup_env
from components.pattern_extractor import PatternExtractor
from components.prompt_constructor import PromptConstructor
from components.convert_flow import ConvertFlow
from data_classes.flow import Flow, Example, Pattern
from utils.file_operations import save_flows, load_flows
from typing import List, Dict
from lightrag.core.prompt_builder import Prompt

setup_env()

pattern_extractor = PatternExtractor()
prompt_constructor = PromptConstructor()
convert_flow = ConvertFlow()

flows: List[Flow] = load_flows()


def extract_patterns(examples_text: str) -> str:
    examples = [Example(output=examples_text.strip())]
    return pattern_extractor(examples)


def construct_prompt(input_format: str, output_format: str, patterns_text: str,
                     examples_text: str) -> str:
    patterns = [Pattern(description=patterns_text)]
    examples = [Example(output=examples_text)]
    return prompt_constructor(input_format, output_format, patterns, examples)


def save_flow(input_format: str, output_format: str, examples_text: str,
              patterns_text: str, prompt: str) -> str:
    examples = [Example(output=example.strip()) for example in
                examples_text.split("\n\n") if example.strip()]
    patterns = [Pattern(description=section.strip(), category="") for section
                in patterns_text.split("\n\n") if section.strip()]
    flow = Flow(input_format=input_format, output_format=output_format,
                examples=examples, patterns=patterns, prompt=prompt)
    flows.append(flow)
    save_flows(flows)
    return f"Flow '{flow.name}' saved successfully. Total flows: {len(flows)}"


def convert_content(flow_name: str, content: str) -> str:
    selected_flow = next((flow for flow in flows if flow.name == flow_name),
                         None)
    if not selected_flow:
        return "Invalid flow selected"

    prompt = Prompt(template=selected_flow.prompt)
    full_prompt = prompt(prompt_kwargs={
        "input_format":    selected_flow.input_format,
        "output_format":   selected_flow.output_format,
        "summaryPatterns": "\n".join(
                [f"{pattern.category}:\n{pattern.description}" for pattern in
                 selected_flow.patterns]),
        "input_str":       content
    })

    return convert_flow(full_prompt, selected_flow)


css = """
body {max-width: 800px; margin: auto; padding: 20px 20px;}
.container {width: 100%; margin: auto;}
.center {display: flex; justify-content: center; align-items: center; text-align: center;}
"""

with gr.Blocks(css=css) as app:
    # State variables
    input_format_state = gr.State("")
    output_format_state = gr.State("")
    examples_state = gr.State("")
    patterns_state = gr.State("")
    prompt_state = gr.State("")

    # Front Page
    with gr.Group(visible=True) as front_page:
        with gr.Column(elem_classes=["container"]):
            gr.Markdown("# Content Conversion Flow Creator",
                        elem_classes=["center"])
            with gr.Row():
                create_flow_btn = gr.Button("Create New Flow")
                use_existing_flow_btn = gr.Button("Use Existing Flow")

    # Create Flow - Step 1
    with gr.Group(visible=False) as create_flow_step1:
        with gr.Column(elem_classes=["container"]):
            gr.Markdown("## Step 1: Define Input and Output Formats",
                        elem_classes=["center"])
            input_format = gr.Textbox(
                label="Input Format (e.g., podcast transcript)")
            output_format = gr.Textbox(
                label="Output Format (e.g., blog article)")
            next_step1_btn = gr.Button("Next")

    # Create Flow - Step 2
    with gr.Group(visible=False) as create_flow_step2:
        with gr.Column(elem_classes=["container"]):
            gr.Markdown("## Step 2: Provide Examples", elem_classes=["center"])
            gr.Markdown(
                "We'll train your flow on the voice, tone, style, and structure of your examples. If you want to convert an interview transcript into an article, provide historical examples of interview transcripts and their resulting articles. You can edit these examples at any point to tweak the output of your flow. The more examples you can provide, the better, and if you only have examples of outputs, it'll work just fine.")
            examples = gr.Textbox(
                label="Provide examples of the output format (separate examples with blank lines)",
                lines=10)
            extract_btn = gr.Button("Extract Patterns")

    # Extract Patterns Result
    with gr.Group(visible=False) as extract_patterns_result:
        with gr.Column(elem_classes=["container"]):
            gr.Markdown("## Extracted Patterns", elem_classes=["center"])
            patterns = gr.Textbox(label="Extracted Patterns (editable)",
                                  lines=20)
            create_flow_btn_final = gr.Button("Create Flow")

    # Flow Created
    with gr.Group(visible=False) as flow_created:
        with gr.Column(elem_classes=["container"]):
            gr.Markdown("## Flow Created Successfully",
                        elem_classes=["center"])
            use_flow_btn = gr.Button("Use Flow")

    # Use Flow
    with gr.Group(visible=False) as use_flow_group:
        with gr.Column(elem_classes=["container"]):
            gr.Markdown("## Use Flow", elem_classes=["center"])
            flow_dropdown = gr.Dropdown(choices=[flow.name for flow in flows],
                                        label="Select Flow")
            input_content = gr.Textbox(label="Input Content", lines=10)
            run_btn = gr.Button("Run")
            output_content = gr.Textbox(label="Converted Content", lines=10)


    # Navigation logic
    def show_create_flow_step1():
        return {
            front_page:        gr.update(visible=False),
            create_flow_step1: gr.update(visible=True)
        }


    def show_use_flow():
        return {
            front_page:     gr.update(visible=False),
            use_flow_group: gr.update(visible=True),
            flow_dropdown:  gr.update(choices=[flow.name for flow in flows])
        }


    def show_create_flow_step2(input_fmt, output_fmt):
        return {
            create_flow_step1:   gr.update(visible=False),
            create_flow_step2:   gr.update(visible=True),
            input_format_state:  input_fmt,
            output_format_state: output_fmt
        }


    def show_extract_patterns_result(examples_text):
        patterns_text = extract_patterns(examples_text)
        return {
            create_flow_step2:       gr.update(visible=False),
            extract_patterns_result: gr.update(visible=True),
            patterns:                patterns_text,
            examples_state:          examples_text
        }


    def show_flow_created(input_fmt, output_fmt, examples_text, patterns_text):
        prompt = construct_prompt(input_fmt, output_fmt, patterns_text,
                                  examples_text)
        save_result = save_flow(input_fmt, output_fmt, examples_text,
                                patterns_text, prompt)
        return {
            extract_patterns_result: gr.update(visible=False),
            flow_created:            gr.update(visible=True),
            prompt_state:            prompt
        }


    # Button click events
    create_flow_btn.click(show_create_flow_step1,
                          outputs=[front_page, create_flow_step1])
    use_existing_flow_btn.click(show_use_flow,
                                outputs=[front_page, use_flow_group,
                                         flow_dropdown])
    next_step1_btn.click(show_create_flow_step2,
                         inputs=[input_format, output_format],
                         outputs=[create_flow_step1, create_flow_step2,
                                  input_format_state, output_format_state])
    extract_btn.click(show_extract_patterns_result, inputs=[examples],
                      outputs=[create_flow_step2, extract_patterns_result,
                               patterns, examples_state])
    create_flow_btn_final.click(show_flow_created, inputs=[input_format_state,
                                                           output_format_state,
                                                           examples_state,
                                                           patterns],
                                outputs=[extract_patterns_result, flow_created,
                                         prompt_state])
    use_flow_btn.click(show_use_flow,
                       outputs=[flow_created, use_flow_group, flow_dropdown])
    run_btn.click(convert_content, inputs=[flow_dropdown, input_content],
                  outputs=[output_content])

app.launch(share=True)