#!/usr/bin/env python
# coding: utf-8

# # Database Setup
# 

# In[1]:


import sqlite3

def create_database():
    # Connect to SQLite database (creates the database file if it doesn't exist)
    conn = sqlite3.connect('rule_engine.db') 
    cursor = conn.cursor()

   
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS rules (
            rule_id INTEGER PRIMARY KEY AUTOINCREMENT,
            rule_string TEXT NOT NULL,
            ast TEXT
        )
    ''')

    conn.commit()  
    conn.close()   

# Run the function to create the database and table
create_database()
print("Database and table created successfully!")


# # AST Structure
# 

# In[2]:


class Node:
    def __init__(self, node_type, left=None, right=None, value=None):
        self.type = node_type 
        self.left = left
        self.right = right
        self.value = value  # Operand-specific value (e.g., {"field": "age", "operator": ">", "value": 30})

    def __repr__(self):
        return f"Node(type={self.type}, left={self.left}, right={self.right}, value={self.value})"


# In[3]:


# Example node for testing
example_node = Node("operand", value={"field": "age", "operator": ">", "value": 30})
print(example_node)


# # Rule Parsing
# 

# In[4]:


def create_rule(rule_string):
   
    tokens = rule_string.split()  
    if "AND" in tokens:
        # Create nodes manually for demonstration
        left_operand = Node("operand", value={"field": tokens[0], "operator": tokens[1], "value": tokens[2]})
        right_operand = Node("operand", value={"field": tokens[4], "operator": tokens[5], "value": tokens[6]})
        root = Node("operator", left=left_operand, right=right_operand, value="AND")
        return root
    return None

# Test the rule creation
rule = "age > 30 AND department = 'Sales'"
ast = create_rule(rule)
print(ast)


# # Rule Evaluation
# 

# In[5]:


def evaluate_rule(ast, data):
    if ast.type == "operand":
        field = ast.value["field"]
        operator = ast.value["operator"]
        value = ast.value["value"]

        if operator == ">":
            return data[field] > int(value)
        elif operator == "<":
            return data[field] < int(value)
        elif operator == "=":
            return data[field] == value.strip("'")  # Removing quotes from value

    elif ast.type == "operator":
        if ast.value == "AND":
            return evaluate_rule(ast.left, data) and evaluate_rule(ast.right, data)
        elif ast.value == "OR":
            return evaluate_rule(ast.left, data) or evaluate_rule(ast.right, data)

    return False

# Test the rule evaluation
sample_data = {"age": 35, "department": "Sales"}
result = evaluate_rule(ast, sample_data)
print("Evaluation Result:", result)


# # Combine Rules
# 

# In[6]:


def combine_rules(rules, operator="AND"):
    combined_root = None

    for rule in rules:
        rule_ast = create_rule(rule)

        if combined_root is None:
            combined_root = rule_ast
        else:
            combined_root = Node("operator", left=combined_root, right=rule_ast, value=operator)

    return combined_root

# Test combining rules
combined_rule = combine_rules(["age > 30 AND department = 'Sales'", "salary > 50000 OR experience > 5"])
print(combined_rule)


# In[1]:




# In[ ]:




