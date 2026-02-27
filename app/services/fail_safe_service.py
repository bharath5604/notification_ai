def safe_run(func):
    try:
        return func()
    except Exception as e:
        return {
            "decision": "LATER",
            "reason": f"Fail-safe triggered: {str(e)}"
        }