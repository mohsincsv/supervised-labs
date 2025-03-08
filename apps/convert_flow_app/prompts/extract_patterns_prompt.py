EXTRACT_PATTERNS_PROMPT = """
You are an expert writing analyst. Your task is to analyze the provided examples and extract the key patterns in terms of tone, voice, personality, style, structure, and additional elements. Please provide a detailed breakdown following this structure:

Tone:
- List 3-5 key characteristics of the tone

Voice:
- List 3-5 key characteristics of the voice

Personality:
- List 3-5 key traits of the personality conveyed

Style:
- List 5-7 key stylistic elements

Structure:
1. Introduction:
   - List 2-3 key elements of the introduction
2. Main body:
   - List 3-5 key characteristics of the main body
3. Practical application (if applicable):
   - List 1-2 key elements related to practical application
4. Conclusion:
   - List 2-3 key elements of the conclusion

Additional elements:
- List 3-5 additional elements or techniques used throughout the writing

Analyze the following examples and provide a detailed breakdown of the writing patterns:

{{examples}}

Your analysis should be thorough and specific, capturing the essence of the writing style in the examples.
"""