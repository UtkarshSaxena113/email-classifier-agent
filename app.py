import os
from typing import TypedDict, Optional
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, START, END
load_dotenv()

class EmailClassification(BaseModel):
    category: str = Field(
        description="Category of the email: 'urgent', 'work', or 'spam'"
    )
    confidence: float = Field(
        description="Confidence score between 0.0 and 1.0"
    )
    reasoning: Optional[str] = Field(
        default=None, 
        description="Brief explanation for the classification"
    )

class EmailState(TypedDict):
    email: str
    category: Optional[str]
    confidence: Optional[float]
    reasoning: Optional[str]
    summary: Optional[str]
    action_log: Optional[str]

llm = ChatOpenAI(
    model="openai/gpt-4o-mini",
    openai_api_key=os.getenv("OPENROUTER_API_KEY"),
    openai_api_base="https://openrouter.ai/api/v1",
    temperature=0,
)

structured_llm = llm.with_structured_output(EmailClassification)

def classifier_node(state: EmailState) -> EmailState:
    """Email content ko analyze karke classify karta hai."""
    email_text = state.get("email", "")
    
    prompt = f"""
    You are an expert AI Email Classifier. Analyze the following email text carefully and classify it into one of these exact categories: 'urgent', 'work', or 'spam'.
    
    Email Content:
    "{email_text}"
    """
    
    response = structured_llm.invoke(prompt)
    
    return {
        "category": response.category.lower(),
        "confidence": response.confidence,
        "reasoning": response.reasoning,
        "action_log": f"Classified as {response.category} with {response.confidence * 100:.1f}% confidence."
    }

def handle_urgent(state: EmailState) -> EmailState:
    """Urgent emails ko process karta hai (Slack Notification Alert)."""
    print("\n🚨 [URGENT ALERT] Sending high-priority notification to Slack!")
    
    summary = "Urgent attention required: Critical client or system issue detected."
    current_log = state.get("action_log", "")
    
    return {
        "summary": summary,
        "action_log": f"{current_log} -> Handled as Urgent: Alert sent."
    }

def handle_work(state: EmailState) -> EmailState:
    """Work emails ko process karta hai (Google Sheets Logging)."""
    print("\n💼 [WORK LOG] Logging task/email to Google Sheets...")
    
    summary = "Work email processed and logged for team review."
    current_log = state.get("action_log", "")
    
    return {
        "summary": summary,
        "action_log": f"{current_log} -> Handled as Work: Logged to Sheets."
    }

def handle_spam(state: EmailState) -> EmailState:
    """Spam emails ko process karta hai (Gmail Auto-Archive)."""
    print("\n🗑️ [SPAM ACTION] Auto-archiving promotional/junk email.")
    
    summary = "Spam email detected. Marked for auto-archive."
    current_log = state.get("action_log", "")
    
    return {
        "summary": summary,
        "action_log": f"{current_log} -> Handled as Spam: Archived."
    }

def route_email(state: EmailState) -> str:
    """Category ke basis par router node decide karta hai."""
    category = state.get("category", "work")
    
    if category == "urgent":
        return "handle_urgent"
    elif category == "spam":
        return "handle_spam"
    else:
        return "handle_work"

builder = StateGraph(EmailState)

# Add Nodes
builder.add_node("classifier_node", classifier_node)
builder.add_node("handle_urgent", handle_urgent)
builder.add_node("handle_work", handle_work)
builder.add_node("handle_spam", handle_spam)

builder.add_edge(START, "classifier_node")

builder.add_conditional_edges(
    "classifier_node",
    route_email,
    {
        "handle_urgent": "handle_urgent",
        "handle_work": "handle_work",
        "handle_spam": "handle_spam"
    }
)

builder.add_edge("handle_urgent", END)
builder.add_edge("handle_work", END)
builder.add_edge("handle_spam", END)
app_graph = builder.compile()
if __name__ == "__main__":
    test_input = {
        "email": "URGENT: Our production database server is down! Clients are facing 500 errors. Please fix immediately."
    }
    
    print("🚀 Running Email Classifier Agent...\n")
    
    result = app_graph.invoke(test_input)
    
    print("\n--- Final Execution Result ---")
    print(f"📌 Category: {result.get('category')}")
    print(f"📊 Confidence: {result.get('confidence')}")
    print(f"📝 Reasoning: {result.get('reasoning')}")
    print(f"📑 Summary: {result.get('summary')}")
    print(f"📜 Action Log: {result.get('action_log')}")
