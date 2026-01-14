"""
02_evals_framework.py - Simple evaluation system
"""

from openai import OpenAI
import json

client = OpenAI()

class Evaluator:
    def __init__(self):
        self.results = []

    def score_exact_match(self, predicted, expected):
        return 1.0 if predicted.strip().lower() == expected.strip().lower() else 0.0

    def score_llm_judge(self, question, predicted, expected):
        """Use GPT-4o to judge if the answer is semanticly correct"""
        prompt = f"""
        Question: {question}
        Expected Answer: {expected}
        Actual Answer: {predicted}
        
        Is the Actual Answer correct based on the Expected Answer? 
        Respond with ONLY 'YES' or 'NO'.
        """
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}]
        )
        return 1.0 if "YES" in response.choices[0].message.content else 0.0

    def run_eval(self, test_cases, system_func):
        print(f"🧪 Running Eval on {len(test_cases)} cases...")
        
        total_score = 0
        for case in test_cases:
            prediction = system_func(case["question"])
            
            if case["type"] == "exact":
                score = self.score_exact_match(prediction, case["expected"])
            else:
                score = self.score_llm_judge(case["question"], prediction, case["expected"])
                
            print(f"  Q: {case['question'][:30]}... | Score: {score}")
            total_score += score
            
        avg = total_score / len(test_cases)
        print(f"📊 Final Accuracy: {avg:.2%}")

# --- System Under Test ---

def my_chatbot(question):
    # Determine model based on complexity (simulated)
    response = client.chat.completions.create(
        model="gpt-5-mini",
        messages=[{"role": "user", "content": question}]
    )
    return response.choices[0].message.content

# --- Main ---

def main():
    test_set = [
        {"question": "What is 2+2?", "expected": "4", "type": "exact"},
        {"question": "Who is the CEO of OpenAI (in 2024)?", "expected": "Sam Altman", "type": "semantic"},
        {"question": "Capital of France?", "expected": "Paris", "type": "semantic"}
    ]
    
    evaluator = Evaluator()
    evaluator.run_eval(test_set, my_chatbot)

if __name__ == "__main__":
    main()
