CONVERT_FLOW_PROMPT = """
You are an expert article summarizer. Your task is to convert a {{ input_format }} into a {{ output_format }} that follows the following style:
{{ summaryPatterns }}
Please create a {{ output_format }} that follows the style above.
{{ input_str }}
Think step-by-step about the main points of the {{ input_format }} and write a {{ output_format }} that follows the style and structure above. Pay attention to the examples given above and try to match the writing style of them as closely as possible. Do not include any pre-ambles or post-ambles. Return text answer only, do not wrap answer in any XML tags.
"""