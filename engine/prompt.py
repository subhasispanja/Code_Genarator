def extract_constraints(problem_statement: str) -> dict:
    """
    Extracts language, code format, and output format
    if they are already mentioned in the problem statement.
    """
    text = problem_statement.lower()

    # Detect language
    language = None
    if "python" in text:
        language = "Python"
    elif "java " in text:
        language = "Java"
    elif "c++" in text:
        language = "C++"
    elif "javascript" in text:
        language = "JavaScript"
    elif "Html" in text:
        language = "Html"
    elif "css" in text:
        language = "css"

    # Detect code format
    code_format = None
    if "function" in text:
        code_format = "function"
    elif "class" in text:
        code_format = "class"
    elif "script" in text:
        code_format = "script"
    elif "method" in text:
        code_format = "method"

    # Detect output format
    output_format = None
    if "series" in text:
        output_format = "series"
    elif "list" in text:
        output_format = "list"
    elif "boolean" in text or "true/false" in text:
        output_format = "boolean"
    elif "single value" in text or "number" in text:
        output_format = "single value"

    return {
        "language": language,
        "code_format": code_format,
        "output_format": output_format
    }


def is_output_required(problem_statement: str) -> bool:
    """
    Determines whether the problem requires producing output.
    """
    keywords = [
       "print", "return", "output", "display", "result",
       "series", "sequence", "list", "generate", "show"
    ]
    text = problem_statement.lower()
    return any(keyword in text for keyword in keywords)


def build_final_prompt(
    problem_statement: str,
    language: str,
    code_format: str,
    output_format: str | None = None
) -> str:
    """
    Builds a strict prompt that forces the LLM
    to generate ONLY code.
    """

    rules = (
        "Generate ONLY code.\n"
        "Do NOT provide explanations.\n"
        "Do NOT add comments.\n"
        "Do NOT use markdown.\n"
        "Do NOT include extra text.\n"
    )

    structure = f"The code must be written as a {code_format} in {language}.\n"

    output_rule = ""
    if output_format:
        output_rule = f"The output must be a {output_format}.\n"

    prompt = (
        rules +
        structure +
        output_rule +
        "Problem:\n"
        f"{problem_statement}"
    )

    return prompt
