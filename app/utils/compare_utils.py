from deepdiff import DeepDiff

def compare_json(data1, data2):
    diff = DeepDiff(data1, data2, ignore_order=True)
    return diff.to_dict() if hasattr(diff, "to_dict") else dict(diff)
