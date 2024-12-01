import openai

# Replace 'your-api-key' with your actual OpenAI API key
openai.api_key = 'your-api-key'

openai.base_url = 'http://127.0.0.1:18188/v1/'


# Define the prompt
prompt = '画一个美女吧'

# Generate a response
response = openai.chat.completions.create(
    model='draw',
    messages=[
        {"role": "user", "content": prompt}
    ]
)

# Print the generated image URL
print(response.choices[0].message.content["image_urls"])