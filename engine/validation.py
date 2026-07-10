def validate_inputs(
    problem_statement: str,
    language: str | None,
    code_format: str | None,
    output_needed: bool = False,
    output_format: str | None = None
):
    
    # 1️⃣ Problem statement must exist
    if not problem_statement or not problem_statement.strip():
        return "Problem statement cannot be empty."

    # 2️⃣ Language must be resolved (from prompt or UI)
    if not language:
        return "Programming language is required (select it or mention it in the problem statement)."

    # 3️⃣ Code format must be resolved
    if not code_format:
        return "Code format is required (function, class, script, etc.)."

    # 4️⃣ Output format required only if output is needed
    if output_needed and not output_format:
        return (
            "This problem requires output.\n"
            "Please specify the output format (series, list, boolean, etc.) "
            "or mention it in the problem statement."
        )

    # ✅ All validations passed
    return None
