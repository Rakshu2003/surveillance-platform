import os
from groq import Groq
from dotenv import load_dotenv
import json

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def generate_incident_summary(event: dict) -> dict:
    prompt = f"""You are an expert security intelligence analyst.
Given the following surveillance event, produce a concise incident report.

Event Data:
{json.dumps(event, indent=2)}

Respond in JSON with exactly these fields:
- "incident_summary": 2-3 sentence plain-English description
- "classification_reasoning": why this severity level was assigned
- "recommended_action": specific actionable guidance for security operator
- "confidence_note": any caveats about AI confidence

Return ONLY valid JSON, no extra text."""

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
        )
        content = response.choices[0].message.content
        return json.loads(content)

    except Exception as e:
        return {
            "incident_summary": f"Event detected: {event.get('event_type')} with threat score {event.get('threat_score')}",
            "classification_reasoning": f"Severity {event.get('severity')} assigned based on threat scoring.",
            "recommended_action": "Review the flagged footage and assess manually.",
            "confidence_note": f"GenAI unavailable: {str(e)}"
        }
