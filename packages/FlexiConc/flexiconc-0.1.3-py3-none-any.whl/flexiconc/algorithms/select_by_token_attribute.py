import re
from flexiconc.utils.line_operations import *


def select_by_token_attribute(conc, **args):
    """
    Selects lines based on a positional attribute at a specific offset.

    Args are dynamically validated and extracted from the schema.

    Parameters:
    - conc (Union[Concordance, ConcordanceSubset]): The full concordance or a subset of it.
    - **kwargs: Arguments defined dynamically in the schema.

    Returns:
    - dict: A dictionary containing:
        - "selected_lines": A list of line IDs where the condition is met.
        - "line_count": The number of selected lines.
    """

    # Metadata for the algorithm
    select_by_token_attribute._algorithm_metadata = {
        "name": "Select by a Token-Level Attribute",
        "description": "Selects lines based on the specified token-level attribute at a given offset, with optional case-sensitivity, regex, or negation.",
        "algorithm_type": "selection",
        "args_schema": {
            "type": "object",
            "properties": {
                "value": {
                    "type": "string",
                    "description": "The value to match against.",
                    "default": ""
                },
                "tokens_attribute": {
                    "type": "string",
                    "description": "The positional attribute to check (e.g., 'word').",
                    "default": "word",
                    "x-eval": "dict(enum=list(set(conc.tokens.columns) - {'id_in_line', 'line_id', 'offset'})"
                },
                "offset": {
                    "type": "integer",
                    "description": "The offset from the concordance node to apply the check.",
                    "default": 0,
                    "x-eval": "dict(minimum=min(conc.tokens['offset']), maximum=max(conc.tokens['offset']))"
                },
                "case_sensitive": {
                    "type": "boolean",
                    "description": "If True, performs a case-sensitive match.",
                    "default": False
                },
                "regex": {
                    "type": "boolean",
                    "description": "If True, use regex matching instead of exact matching.",
                    "default": False
                },
                "negative": {
                    "type": "boolean",
                    "description": "If True, invert the selection (i.e., select lines where the match fails).",
                    "default": False
                }
            },
            "required": ["value"]
        }
    }

    # Extract arguments
    tokens_attribute = args.get("tokens_attribute", "word")
    offset = args.get("offset", 0)
    value = args.get("value", "")
    case_sensitive = args.get("case_sensitive", False)
    regex = args.get("regex", False)
    negative = args.get("negative", False)

    # Extract words or tokens based on the positional attribute and offset
    items = list(extract_words_at_offset(conc.tokens, p=tokens_attribute, offset=offset))

    # Retrieve the line IDs for this concordance
    line_ids = conc.metadata.index.tolist()

    # Apply selection based on whether regex matching is enabled
    if regex:
        # Set the appropriate regex flags based on case sensitivity
        flags = 0 if case_sensitive else re.IGNORECASE
        selection = [1 if re.match(value, item, flags=flags) else 0 for item in items]
    else:
        # If not regex, preprocess case sensitivity
        if not case_sensitive:
            value = value.lower()
            items = [item.lower() for item in items]

        selection = [1 if item == value else 0 for item in items]

    # If negative flag is enabled, invert the selection
    if negative:
        selection = [1 - x for x in selection]

    # Create a dictionary mapping line_id to the corresponding selection result (0 or 1)
    selected_lines = [line_id for i, line_id in enumerate(line_ids) if selection[i] == 1]

    # Return the selected lines and their count
    return {
        "selected_lines": selected_lines
    }
