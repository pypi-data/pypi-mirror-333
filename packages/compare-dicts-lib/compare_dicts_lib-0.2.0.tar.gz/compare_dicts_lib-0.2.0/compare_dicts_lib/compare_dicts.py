from typing import Any, Dict, Optional, List

def compare_dicts(content: Dict[str, Any],
                  previous_content: Optional[Dict[str, Any]],
                  detailed: bool = False,
                  ignore_keys: Optional[list] = None,
                  strict_type_checking: bool = True,
                  detect_order_changes: bool = True) -> Dict[str, Any]:
    """
    Compare two dictionaries and returns only the differences.
    If a key is removed, it is assigned None.
    Can also return a detailed mode that indicates the type of modification.
    Supports ignoring specific keys and handling type conversions.

    Args:
        content (dict): The new dictionary.
        previous_content (dict, optional): The previous dictionary. Can be None.
        detailed (bool): If True, return a dict with indications of changes.
        ignore_keys (list, optional): A list of keys to ignore.
        strict_type_checking (bool): If False, compares values as strings (e.g., 1 == "1").
        compare_lists (bool): If True, compares lists item by item.
        detect_order_changes (bool): If True, detects order changes in lists.

    Returns:
        dict: The differences between the two dictionaries.
    """
    if ignore_keys is None:
        ignore_keys = []
    
    differences = {}

    if previous_content is None: # Everything is new if there is no previous content.
        return {key: {"type": "added", "new_value": value} for key, value in content.items()
                if key not in ignore_keys} if detailed else {key: value for key, value in content.items() if key not in ignore_keys}

    match_key = "id" if detailed else None

    def compare_lists(new_list: List[Any], old_list: List[Any], detect_order_changes: bool = True) -> Dict[str, Any]:
        """Compare two lists and return the differences."""
        added, removed, modified = [], [], []
        # For lists of int, str, etc.
        if not all(isinstance(item, dict) for item in new_list + old_list):
            added = [item for item in new_list if item not in old_list]
            removed = [item for item in old_list if item not in new_list]
            if detect_order_changes and new_list != old_list:
                modified.append({"type": "reordered", "old_value": old_list, "new_value": new_list})
    
        # For lists of dicts
        elif match_key:
        # Convert lists into dicts keyed by `id`
            old_dict = {item[match_key]: item for item in old_list if match_key in item}
            new_dict = {item[match_key]: item for item in new_list if match_key in item}

            added = [new_dict[key] for key in new_dict if key not in old_dict]
            removed = [old_dict[key] for key in old_dict if key not in new_dict]
            modified = []

            for key in new_dict:
                if key in old_dict:
                    nested_diff = compare_dicts(new_dict[key], old_dict[key], detailed, ignore_keys, strict_type_checking)
                    if nested_diff:
                        modified.append({"id": key, "type": "modified", "old_value": old_dict[key], "new_value": new_dict[key]})

        else:
            # Default comparison (without id-based matching)
            added = [item for item in new_list if item not in old_list]
            removed = [item for item in old_list if item not in new_list]
            modified = []

            for i, (old_item, new_item) in enumerate(zip(old_list, new_list)):
                if isinstance(old_item, dict) and isinstance(new_item, dict):
                    nested_diff = compare_dicts(new_item, old_item, detailed, ignore_keys, strict_type_checking)
                    if nested_diff:
                        modified.append({"index": i, "type": "modified", "old_value": old_item, "new_value": new_item})

        result = {}
        if added:
            result["added"] = added
        if removed:
            result["removed"] = removed
        if modified:
            result["modified"] = modified

        return result

    for key in content:
        if key in ignore_keys:
            continue  # Ignore the specified keys

        if isinstance(content[key], dict) and isinstance(previous_content.get(key), dict):
            nested_differences = compare_dicts(content[key], previous_content[key], detailed, ignore_keys, strict_type_checking)
            if nested_differences:
                differences[key] = nested_differences

        elif isinstance(content[key], list) and isinstance(previous_content.get(key), list):
            list_diff = compare_lists(content[key], previous_content[key], detect_order_changes) if detailed else content[key] if content[key] != previous_content[key] else None
            if list_diff:
                differences[key] = list_diff

        elif key not in previous_content:
            differences[key] = {"type": "added", "new_value": content[key]} if detailed else content[key]

        else:
            old_value, new_value = previous_content[key], content[key]
            # Compare values based on strict_type_checking
            values_differ = (old_value != new_value) if strict_type_checking else (str(old_value) != str(new_value))
            if values_differ:
                differences[key] = {
                    "type": "modified",
                    "old_value": old_value,
                    "new_value": new_value
                } if detailed else new_value

    for key in previous_content.keys():
        if key in ignore_keys:
            continue  # Ignore the specified keys
        if key not in content: # Indicate that the key was removed.
            differences[key] = {"type": "deleted", "old_value": previous_content[key]} if detailed else None

    return differences

def apply_diff(original: Dict[str, Any], diff: Dict[str, Any], detailed: bool = False) -> Dict[str, Any]:
    """
    Apply a difference dictionary to an original dictionary.

    Args:
        original (dict): The original dictionary.
        diff (dict): The differences to apply.
        detailed (bool): If True, handles detailed diffs (with "type" keys).

    Returns:
        dict: The updated dictionary.
    """
    updated = original.copy()

    for key, change in diff.items():
        if detailed:
            # Case 1 : detailed diff
            if isinstance(change, dict) and "type" in change:
                if change["type"] == "added":
                    updated[key] = change["new_value"]
                elif change["type"] == "deleted":
                    updated.pop(key, None)
                elif change["type"] == "modified":
                    updated[key] = change["new_value"]
            elif isinstance(change, dict):
                updated[key] = apply_diff(updated.get(key, {}), change, detailed=True)
        else:
            # Case 2 : not detailed diff
            if change is None:
                updated.pop(key, None)
            elif isinstance(change, dict) and key in updated:
                updated[key] = apply_diff(updated[key], change, detailed=False)
            else:
                updated[key] = change

    return updated
