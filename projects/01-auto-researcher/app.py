"""
Project 1: Auto Researcher Agent
--------------------------------
This script demonstrates an agentic workflow using:
1. GPT-4o for planning (breaking down a topic).
2. o1-mini for deep reasoning/research on specific sub-questions.
3. GPT-4o for final synthesis.
"""

import os
import time
from typing import List
from openai import OpenAI
from pydantic import BaseModel, Field

# Initialize client
client = OpenAI()

# --- Data Structures ---

class ResearchPlan(BaseModel):
    """Structure for the initial research plan"""
    topic: str
    sub_questions: List[str] = Field(description="List of 3-5 distinct sub-questions to research")
    summary_goal: str = Field(description="The goal of the final summary")

class SearchResult(BaseModel):
    """Structure for a single research finding"""
    question: str
    answer: str
    key_points: List[str]

# --- Agent Functions ---

def create_plan(topic: str) -> ResearchPlan:
    """Step 1: Create a research plan using GPT-4o"""
    print(f"\n📋 Planning research for: '{topic}'...")
    
    completion = client.beta.chat.completions.parse(
        model="gpt-4o-2024-08-06",  # Use a structured-output capable model
        messages=[
            {"role": "system", "content": "You are a senior research lead. Break down the user's topic into 3 distinct, investigatable sub-questions."},
            {"role": "user", "content": f"Research topic: {topic}"}
        ],
        response_format=ResearchPlan
    )
    
    plan = completion.choices[0].message.parsed
    print(f"✅ Plan created with {len(plan.sub_questions)} sub-questions.")
    return plan

def conduct_research(question: str) -> str:
    """Step 2: Deep research using o1-mini (Reasoning Model)"""
    print(f"  🔍 Researching: {question}...")
    
    # NOTE: o1 models do not support 'system' role, use 'user' for instructions
    # They effectively 'think' before answering.
    response = client.chat.completions.create(
        model="o1-mini", 
        messages=[
            {
                "role": "user", 
                "content": f"Research this question in depth. Provide a comprehensive answer with facts and technical details.\n\nQuestion: {question}"
            }
        ]
    )
    
    return response.choices[0].message.content

def synthesize_report(plan: ResearchPlan, findings: List[dict]) -> str:
    """Step 3: Synthesize findings into a final report using GPT-4o"""
    print("\n📝 Synthesizing final report...")
    
    # Prepare context
    context = f"Topic: {plan.topic}\n\nFindings:\n"
    for item in findings:
        context += f"Question: {item['question']}\nFindings: {item['answer']}\n\n"
        
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a technical writer. Compile the provided research findings into a polished Markdown report. Use headers, bullet points, and a professional tone."},
            {"role": "user", "content": context}
        ]
    )
    
    return response.choices[0].message.content

# --- Main Application ---

def main():
    print("🤖 AUTO RESEARCHER AGENT INITIALIZED")
    print("="*60)
    
    topic = input("Enter a topic to research (e.g., 'Quantum Computing usage in Finance'): ")
    if not topic:
        topic = "The future of solid-state batteries in Electric Vehicles"
        print(f"Using default topic: {topic}")
        
    # 1. Plan
    try:
        plan = create_plan(topic)
    except Exception as e:
        print(f"Error creating plan: {e}")
        return

    # 2. Execute Research
    findings = []
    print("\n🚀 Starting execution phase...")
    
    for i, question in enumerate(plan.sub_questions):
        print(f"\n[Task {i+1}/{len(plan.sub_questions)}]")
        answer = conduct_research(question)
        findings.append({"question": question, "answer": answer})
        time.sleep(1) # Be nice to the rate limits

    # 3. Synthesize
    final_report = synthesize_report(plan, findings)
    
    # 4. Save and Output
    filename = f"report_{str(int(time.time()))}.md"
    with open(filename, "w", encoding='utf-8') as f:
        f.write(final_report)
        
    print(f"\n✅ Report saved to {filename}")
    print("\n" + "="*60)
    print(final_report[:500] + "...\n[Content truncated]")
    print("="*60)

if __name__ == "__main__":
    main()
