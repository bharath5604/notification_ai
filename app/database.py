from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

client = MongoClient(os.getenv("MONGO_URI"))
db = client["notification_engine"]

# 📌 Incoming events storage
events_collection = db["events"]

# 📌 User fatigue tracking
history_collection = db["user_history"]

# 📌 Audit logs (decisions, failures, etc.)
audit_collection = db["audit_logs"]

# ⭐ NEW — Notification logs (for duplicate detection)
notification_log_collection = db["notification_logs"]

# ⭐ NEW — Queue for LATER notifications
queue_collection = db["notification_queue"]