import difflib

def generate_full_diff(old_code, new_code):
    """Generate a full diff between the original and refactored code."""
    diff = difflib.unified_diff(
        old_code.splitlines(),
        new_code.splitlines(),
        lineterm='',
        fromfile='Original',
        tofile='Refactored'
    )
    return "\n".join(diff)