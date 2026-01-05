import ollama

response = ollama.chat(
    model="llama3.1",
    messages=[
        {'role':'user', 'content':'Recommend 3 romantic movies'}
    ]
)
print(response['message']['content'])