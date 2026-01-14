"""
02_text_generation_tasks.py - Common text generation use cases
"""

import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI()


def summarization(text):
    """Summarize long text"""
    print("\n" + "="*60)
    print("SUMMARIZATION")
    print("="*60)

    response = client.chat.completions.create(
        model="gpt-5-mini",
        messages=[{
            "role": "user",
            "content": f"Summarize this text in 2-3 sentences:\n\n{text}"
        }]
    )

    return response.choices[0].message.content


def translation(text, target_language):
    """Translate text to another language"""
    print("\n" + "="*60)
    print(f"TRANSLATION TO {target_language.upper()}")
    print("="*60)

    response = client.chat.completions.create(
        model="gpt-5-mini",
        messages=[{
            "role": "user",
            "content": f"Translate this text to {target_language}: '{text}'"
        }]
    )

    return response.choices[0].message.content


def content_generation(topic, content_type):
    """Generate various types of content"""
    print("\n" + "="*60)
    print(f"CONTENT GENERATION: {content_type.upper()}")
    print("="*60)

    prompts = {
        "blog_post": f"Write a 200-word blog post about {topic}",
        "email": f"Write a professional email about {topic}",
        "story": f"Write a short creative story about {topic}",
        "tweet": f"Write an engaging tweet about {topic} (under 280 characters)"
    }

    response = client.chat.completions.create(
        model="gpt-5-mini",
        messages=[{
            "role": "user",
            "content": prompts.get(content_type, f"Write about {topic}")
        }]
    )

    return response.choices[0].message.content


def question_answering(context, question):
    """Answer questions based on context"""
    print("\n" + "="*60)
    print("QUESTION ANSWERING")
    print("="*60)

    prompt = f"""Based on the following context, answer the question.

Context: {context}

Question: {question}

Answer:"""

    response = client.chat.completions.create(
        model="gpt-5-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0  # More deterministic for Q&A
    )

    return response.choices[0].message.content


def main():
    print("Common Text Generation Tasks")

    # Example 1: Summarization
    long_text = """
    Artificial intelligence (AI) is intelligence demonstrated by machines, as opposed to
    natural intelligence displayed by animals including humans. AI research has been
    defined as the field of study of intelligent agents, which refers to any system that
    perceives its environment and takes actions that maximize its chance of achieving its
    goals. The term "artificial intelligence" had previously been used to describe machines
    that mimic and display "human" cognitive skills that are associated with the human
    mind, such as "learning" and "problem-solving". This definition has since been
    rejected by major AI researchers who now describe AI in terms of rationality and
    acting rationally, which does not limit how intelligence can be articulated.
    """
    summary = summarization(long_text.strip())
    print(f"\nSummary: {summary}")

    # Example 2: Translation
    translation_result = translation("Hello, how are you today?", "Spanish")
    print(f"\nTranslation: {translation_result}")

    # Example 3: Content Generation
    blog_post = content_generation("the benefits of morning exercise", "blog_post")
    print(f"\nBlog Post:\n{blog_post}")

    # Example 4: Question Answering
    context = "Python was created by Guido van Rossum and first released in 1991. Python emphasizes code readability with its use of significant indentation."
    question = "Who created Python?"
    answer = question_answering(context, question)
    print(f"\nAnswer: {answer}")


if __name__ == "__main__":
    main()
