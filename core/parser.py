import json
import re
from core.groq_helper import chat_with_groq

def parse_query(user_input: str, history: list) -> dict:
    try:
        m = re.search(r"\b(.*) jobs in ([A-Za-z ]+)", user_input, re.IGNORECASE)
        if m:
            role = m.group(1).strip()
            loc = m.group(2).strip()
            return {"keywords": [role], "location": loc}
        
        m2 = re.search(r"\bin ([A-Za-z ]+)", user_input, re.IGNORECASE)
        if m2:
            return {"location": m2.group(1).strip()}

        serializable = [{"user": h[0], "slots": h[1]} for h in history]
        system = (
            "You are JobGPT. Given last 5 interactions history and new user message, "
            "extract slots like keywords, location, remote, days."
        )
        user = f"History: {json.dumps(serializable)}\nUser: \"{user_input}\""
        raw = chat_with_groq(system, user)
        return json.loads(raw)
    
    except Exception as e:
        print(f"[Warning] parse_query failed: {e}")
        return {}
