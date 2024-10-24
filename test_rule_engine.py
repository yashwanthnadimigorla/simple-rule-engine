import unittest
from rule_engine import create_rule, combine_rules, evaluate_rule, Node  # Ensure this matches your actual file name

class TestRuleEngine(unittest.TestCase):

    def test_create_rule(self):
        rule = "age > 30 AND department = 'Sales'"
        ast = create_rule(rule)
        self.assertIsInstance(ast, Node)  # Check if the result is a Node instance

    def test_combine_rules(self):
        rules = [
            "age > 30 AND department = 'Sales'",
            "age < 25 AND department = 'Marketing'"
        ]
        combined_ast = combine_rules(rules)
        self.assertIsInstance(combined_ast, Node)  # Check if the combined result is a Node

    def test_evaluate_rule(self):
        ast = create_rule("age > 30 AND department = 'Sales'")
        data = {"age": 35, "department": "Sales", "salary": 60000}
        result = evaluate_rule(ast, data)
        self.assertTrue(result)  # Check if evaluation returns True

        data = {"age": 25, "department": "Sales"}
        result = evaluate_rule(ast, data)
        self.assertFalse(result)  # Check if evaluation returns False

if __name__ == '__main__':
    unittest.main()
