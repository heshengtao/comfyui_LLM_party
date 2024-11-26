import openai

# Replace 'your-api-key' with your actual OpenAI API key
openai.api_key = 'your-api-key'

openai.base_url = 'http://127.0.0.1:8187/v1/'


# Define the prompt
prompt = '你叫什么名字？'

# Generate a response
response = openai.chat.completions.create(
    model='fastapi',
    messages=[
        {"role": "user", "content": prompt}
    ],
    stream=True
)

# 流式
for chunk in response:
    print(chunk.choices[0].delta.content)