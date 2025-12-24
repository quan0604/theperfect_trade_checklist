import openai

def get_ai_opinion(prompt, model="gpt-3.5-turbo", api_key=None):
    """
    Query OpenAI GPT for trading signal confirmation or pattern opinion.
    """
    openai.api_key = api_key
    response = openai.ChatCompletion.create(
        model=model,
        messages=[{"role": "user", "content": prompt}]
    )
    return response['choices'][0]['message']['content']


