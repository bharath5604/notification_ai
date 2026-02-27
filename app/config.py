import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RULES_PATH = os.path.join(BASE_DIR, "config", "rules.json")

with open(RULES_PATH) as f:
    RULES = json.load(f)