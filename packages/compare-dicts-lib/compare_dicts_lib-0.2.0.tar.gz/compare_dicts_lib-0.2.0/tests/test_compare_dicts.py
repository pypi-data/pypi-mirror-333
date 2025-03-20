import unittest
from compare_dicts_lib import compare_dicts, apply_diff

class TestCompareDicts(unittest.TestCase):

    def test_basic_comparison(self):
        old_data = {"name": "Alice", "age": 30}
        new_data = {"name": "Alice", "age": 31, "email": "alice@example.com"}
        
        expected = {"age": 31, "email": "alice@example.com"}
        self.assertEqual(compare_dicts(new_data, old_data), expected)

    def test_detailed_comparison(self):
        old_data = {
            "name": "Alice",
            "age": 30,
            "address": {"zip": "75000", "city": "Paris"}
        }
        new_data = {
            "name": "Alice",
            "age": 31,
            "email": "alice@example.com",
            "address": {"city": "Paris"}
        }
        
        expected = {
            "age": {"type": "modified", "old_value": 30, "new_value": 31},
            "email": {"type": "added", "new_value": "alice@example.com"},
            "address": {
                "zip": {"type": "deleted", "old_value": "75000"}
            }
        }
        self.assertEqual(compare_dicts(new_data, old_data, detailed=True), expected)

    def test_ignore_keys(self):
        old_data = {"name": "Alice", "age": 30, "timestamp": "2024-03-13T10:00:00Z"}
        new_data = {"name": "Alice", "age": 31, "email": "alice@example.com", "timestamp": "2024-03-13T11:00:00Z"}

        expected = {"age": 31, "email": "alice@example.com"}
        self.assertEqual(compare_dicts(new_data, old_data, ignore_keys=["timestamp"]), expected)

    def test_strict_type_checking(self):
        old_data = {"value": 1, "name": "Alice"}
        new_data = {"value": "1", "name": "Alice"}

        self.assertEqual(compare_dicts(new_data, old_data, strict_type_checking=False), {})

    def test_list_comparison_with_id(self):
        old_data = {"users": [{"id": 1, "name": "Alice"}, {"id": 2, "name": "Bob"}]}
        new_data = {"users": [{"id": 1, "name": "Alice"}, {"id": 2, "name": "Robert"}]}

        expected = {
            "users": {
                "modified": [
                    {
                        "id": 2,
                        "type": "modified",
                        "old_value": {"id": 2, "name": "Bob"},
                        "new_value": {"id": 2, "name": "Robert"}
                    }
                ]
            }
        }
        self.assertEqual(compare_dicts(new_data, old_data, detailed=True), expected)

    def test_apply_diff_basic(self):
        original = {"name": "Bob", "age": 30, "job": "developer"}
        diff = {"name": "Robert", "age": None}

        expected = {"name": "Robert", "job": "developer"}
        self.assertEqual(apply_diff(original, diff, detailed=False), expected)

    def test_apply_diff_detailed(self):
        original = {"users": [{"id": 1, "name": "Alice"}, {"id": 2, "name": "Bob"}]}
        diff = {
            "users": {
                "modified": [
                    {
                        "id": 2,
                        "type": "modified",
                        "old_value": {"id": 2, "name": "Bob"},
                        "new_value": {"id": 2, "name": "Robert"}
                    }
                ]
            }
        }

        expected = {
            "users": [
                {"id": 1, "name": "Alice"},
                {"id": 2, "name": "Robert"}
            ]
        }
        self.assertEqual(apply_diff(original, diff, detailed=True), expected)

if __name__ == "__main__":
    unittest.main()
