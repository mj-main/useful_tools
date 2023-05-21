import openai
from time import time
openai.api_key = 'https://platform.openai.com/account/api-keys에서 발급 필요'

# 이전 메시지를 저장해서 입력으로 사용
messages = []
i = 0
while True:
    i+=1
    print("="*20)
    print(f'{i}번째 메시지')
    print("="*20)
    print('user:')

    # 메시지 입력
    inputMessage = ''
    while True:
        line = input()
        inputMessage += (line + '\n')
        if not line:
            print('ChatGPT:')
            inputMessage = inputMessage[:-1]
            break

    # 메시지 응답
    s = time() # 응답 시작 시간
    messages.append({'role': 'user',
                    'content': inputMessage})

    completion = openai.ChatCompletion.create(
        model = 'gpt-3.5-turbo',
        messages = messages
    )

    chat_response = completion.choices[0].message.content

    e = time() # 응답 완료 시간

    print(chat_response)
    print("="*20)
    print(f"응답 시간: {round(e-s,1)}s")
    print("="*20)
    print()

    messages.append({'role': 'assistant', 'content': chat_response})
