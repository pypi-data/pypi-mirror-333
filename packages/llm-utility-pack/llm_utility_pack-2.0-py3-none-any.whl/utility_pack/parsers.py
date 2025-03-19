import json, re

def find_and_parse_json_from_string(response: str) -> dict:
    """
    Finds and parses JSON from a string. It can be encapsulated in triple backticks or not.
    """
    try:
        pattern_json_encapsulated = r"```json\n([\s\S]*?)\n```"
        pattern_json_non_encapsulated = r"\{[\s\S]*?\}"
        json_encapsulated = re.search(pattern_json_encapsulated, response)
        json_non_encapsulated = re.search(pattern_json_non_encapsulated, response)
        if json_encapsulated:
            return json.loads(json_encapsulated.group(1))
        elif json_non_encapsulated:
            return json.loads(json_non_encapsulated.group(0))
        return json.loads(response)

    except Exception:
        pass

    return None
