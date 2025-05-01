def format_state_for_code(state: str) -> str:
    return f"'{state.replace('\'', '\\\'')}'"