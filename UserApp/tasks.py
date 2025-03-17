from celery import shared_task
from groq import Groq
from django.conf import settings

client = Groq(api_key=settings.GROQ_API_KEY)

@shared_task
def generate_resume(user_data):
    # Step 1: Generate Professional Summary
    summary_response = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": f"Analyze the following user data and generate a detailed professional summary:\n\n{user_data}"
            }
        ],
        model="llama-3.3-70b-versatile"
    )
    professional_summary = summary_response.choices[0].message.content

    # Step 2: Format Resume
    resume_prompt = f"""
    Create a professionally formatted resume using the following data:
    
    {professional_summary}
    
    The resume should be in the following format:
    
    === RESUME FORMAT ===
    Name:
    Contact Information:
    Summary:
    Education:
    Professional Experience:
    Skills:
    =====================
    """
    resume_response = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": resume_prompt
            }
        ],
        model="llama-3.3-70b-versatile"
    )
    
    # Final Resume Content
    final_resume = resume_response.choices[0].message.content
    return final_resume
