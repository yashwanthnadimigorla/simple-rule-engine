Objective
Develop a simple 3-tier rule engine application with:

UI to allow users to input rules.
API for rule processing and management.
Backend for storing rules and application data.
Key Features
Abstract Syntax Tree (AST): Used to represent conditional rules dynamically for eligibility determination.
Dynamic Rule Changes: Allows creating, modifying, and combining rules efficiently.
Data Structure
Node:
Type: "operator" (like AND/OR) or "operand" (like conditions).
Left/Right: References to child nodes.
Value: Optional, for operand nodes (e.g., comparison values like age, salary).
Data Storage
Database: Use SQLite for its simplicity.
Schema Example:
Rules Table: id, rule_string, created_at, updated_at.
API Functions
create_rule(rule_string): Converts a string rule into an AST (Node-based structure).
combine_rules(rules): Combines multiple rules efficiently into a single AST.
evaluate_rule(ast, data): Evaluates the rule against provided data attributes (returns True/False).
Example Rules
Rule 1: ((age > 30 AND department = 'Sales') OR (age < 25 AND department = 'Marketing')) AND (salary > 50000 OR experience > 5)
Rule 2: ((age > 30 AND department = 'Marketing')) AND (salary > 20000 OR experience > 5)
Dependencies for Jupyter Notebook
Python Libraries:
sqlite3 for database interactions.
ast for parsing expressions into an Abstract Syntax Tree.
json for handling JSON-based rule evaluations.
datetime for storing timestamps.
Sample Jupyter Notebook Workflow:
Setup database and schema using sqlite3.
Define Node data structure and utility functions to create, combine, and evaluate rules using Python classes.
Write helper functions to handle rule creation from strings, combining rules, and evaluating them.
Test each function with sample rules and JSON data.

1. Setup and Database Schema
First, let's import the necessary libraries and create the SQLite database schema:
import sqlite3
import json
from datetime import datetime
import ast

# Connect to SQLite database (or create it if not exists)
conn = sqlite3.connect('rules_database.db')
cursor = conn.cursor()

# Create rules table to store rule strings and metadata
cursor.execute('''
    CREATE TABLE IF NOT EXISTS rules (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        rule_string TEXT NOT NULL,
        created_at TEXT,
        updated_at TEXT
    )
''')
conn.commit()
2. Define Node Data Structure for AST
Define a class to represent each node in the Abstract Syntax Tree (AST):
class Node:
    def __init__(self, node_type, left=None, right=None, value=None):
        self.node_type = node_type  # e.g., 'operator' (AND/OR) or 'operand' (conditions)
        self.left = left
        self.right = right
        self.value = value  # e.g., "age > 30" for operand nodes

    def __repr__(self):
        if self.node_type == "operator":
            return f"({self.left} {self.value} {self.right})"
        else:
            return f"{self.value}"
3. Create Utility Functions for Rules
Implement utility functions to create rules from strings, combine rules, and evaluate rules against user data:
def create_rule(rule_string):
    try:
        # Use Python's ast module to parse the rule_string into an AST
        parsed_ast = ast.parse(rule_string, mode='eval')
        
        # Convert parsed AST into our custom Node structure (recursive function)
        def parse_ast(node):
            if isinstance(node, ast.BoolOp):
                operator = "AND" if isinstance(node.op, ast.And) else "OR"
                left = parse_ast(node.values[0])
                right = parse_ast(node.values[1])
                return Node("operator", left, right, operator)
            elif isinstance(node, ast.Compare):
                left = node.left.id
                op = node.ops[0]
                right = node.comparators[0].n if isinstance(node.comparators[0], ast.Num) else node.comparators[0].s
                return Node("operand", value=f"{left} {ast.dump(op)} {right}")
            else:
                raise ValueError("Unsupported node type")
        
        # Convert parsed AST to custom Node
        return parse_ast(parsed_ast.body)

    except Exception as e:
        print("Error in parsing rule:", e)
        return None
3.2. Combine Multiple Rules
   def combine_rules(rule_nodes, operator="AND"):
    if not rule_nodes:
        return None
    
    # Start with the first rule in the list
    combined = rule_nodes[0]
    
    for node in rule_nodes[1:]:
        combined = Node("operator", left=combined, right=node, value=operator)
    
    return combined
3.3. Evaluate Rule Against User Data
   def evaluate_rule(node, data):
    if node.node_type == "operator":
        left_result = evaluate_rule(node.left, data)
        right_result = evaluate_rule(node.right, data)
        return (left_result and right_result) if node.value == "AND" else (left_result or right_result)
    elif node.node_type == "operand":
        # Extract attribute, comparison operator, and value from operand
        attribute, operator, value = node.value.split()
        if operator == "==":
            return data.get(attribute) == int(value) if value.isdigit() else data.get(attribute) == value
        elif operator == ">":
            return data.get(attribute, 0) > int(value)
        elif operator == "<":
            return data.get(attribute, 0) < int(value)
        # Add more comparisons as needed
    return False
4. Test Cases and Rule Creation
4.1. Create and Store Rules
   # Create and store a sample rule
rule1_string = "age > 30 and department == 'Sales' or (age < 25 and department == 'Marketing')"
rule1 = create_rule(rule1_string)

# Store rule in database
cursor.execute("INSERT INTO rules (rule_string, created_at, updated_at) VALUES (?, ?, ?)",
               (rule1_string, datetime.now(), datetime.now()))
conn.commit()
4.2. Combine and Evaluate Rules
# Create multiple rules and combine them
rule2_string = "salary > 50000 or experience > 5"
rule2 = create_rule(rule2_string)

combined_rule = combine_rules([rule1, rule2], operator="AND")

# Test evaluation with sample data
sample_data = {"age": 35, "department": "Sales", "salary": 60000, "experience": 3}
print("Is eligible?", evaluate_rule(combined_rule, sample_data))
5. Optional: Visualize Rules and Debug
You can use IPython's display capabilities to visualize your rule structures if needed.

6. Bonus: Error Handling and Validation
Add exception handling for invalid rules or attribute validation to ensure correctness.
