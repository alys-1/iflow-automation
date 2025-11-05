import json
from deepdiff import DeepDiff

def compare_json(obj1, obj2):
    diff = DeepDiff(obj1, obj2, ignore_order=True)
    return json.loads(diff.to_json())

def compare_text(t1, t2):
    set1 = set(t1.splitlines())
    set2 = set(t2.splitlines())
    return {
        "only_in_first": list(set1 - set2),
        "only_in_second": list(set2 - set1)
    }

def compare_responses(body1, body2, headers1, headers2, prefix):
    if isinstance(body1, (dict, list)) and isinstance(body2, (dict, list)):
        body_diff = compare_json(body1, body2)
    else:
        body_diff = compare_text(str(body1), str(body2))

    header_diff = compare_json(headers1, headers2)

    return body_diff, header_diff
