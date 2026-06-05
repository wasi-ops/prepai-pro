import json
def parse_json_response(ai_output):
    try:
        parsed_result = json.loads(ai_output)
        return parsed_result

    except json.JSONDecodeError as error:
        print("JSON parsing failed.")
        print("Reason:", error)
        print("Raw AI output:")
        print(ai_output)
        return None