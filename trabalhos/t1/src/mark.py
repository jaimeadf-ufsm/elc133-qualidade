from typing import Any

def format_mark_for_display(mark: Any) -> str:
    if isinstance(mark, int):
        return f'#{int(mark)}'
    elif isinstance(mark, str):
        return str(mark)
    else:
        raise ValueError(f'Unsupported mark type: {type(mark)}')

def format_mark_for_code(mark: Any) -> str:
    if isinstance(mark, int):
        return f'{mark}'
    elif isinstance(mark, str):
        return f"'{mark.replace('\'', '\\\'')}'"
    else:
        raise ValueError(f'Unsupported mark type: {type(mark)}')
