import openai
import json

API_KEY = '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'
openai.api_key = API_KEY

messages = []
def personal_assistant(prompt):
    response = openai.ChatCompletion.create(
        model = 'gpt-3.5-turbo-0613',
        #messages = [{"role":"user", "content":prompt}], #这里应该是接收user发来的消息
        prompt = prompt,
        functions = [
                    {
                      "name":"和user打招呼",
                      "description":"当用户输入'Hi','你好'等，回答'你好👋，我是小野，今天我们都有哪些任务呢？'",
                      "call":{
                          "function":"和user打招呼",
                          "args":{}
                      },
                  },
                    {
                      "name":"整理user今天的任务，并给出任务列表",
                      "description":"当用户输入今日的任务时，根据以下格式梳理任务:'好的，我将今天的任务梳理为: </ol>1. 2. 3.<ol>加油💪 开干吧！'使用markdown格式和emoji符号。With positive, friendly attitude.",
                      "call":{
                          "function":"整理user今天的任务，并给出任务列表",
                          "args":{}
                      },
                    },
                    {
                      "name":"添加user的任务",
                      "description":"当用户新增加一项或几项任务，例如'我还需要把《刀锋》看完',回答'好的，任务列表更新为：</ol>1. 2. 3.<ol> 加油咯！'添加上待办任务。使用markdown格式和emoji符号。With positive, friendly attitude.",
                      "call":{
                          "function":"添加user的任务",
                          "args":{}
                      },
                    },
                    {
                      "name":"user完成了一项任务",
                      "description":"当用户完成一项或几项任务，并且还有剩余任务，例如'我把《刀锋》看完了',bot回答'真棒🎉休息一下再继续。还剩下：</ol>1. 2. 3.<ol> ，一会儿继续加油咯！'删除掉完成的任务。使用markdown格式和emoji符号。With positive, friendly attitude.",
                      "call":{
                          "function":"user完成了一项任务",
                          "args":{}
                      },
                    },
                    {
                      "name":"当user完成所有任务时",
                      "description":"当user完成所有任务，在本轮回答中user完成了任务列表中所有任务',bot回答'恭喜🍾今天的任务全部完成！太棒了吧！'使用markdown格式和emoji符号。With positive, friendly attitude.",
                      "call":{
                          "function":"当user完成所有任务时",
                          "args":{}
                      },
                    },
                    {
                      "name":"和user再见",
                      "description":"当user输入'Bye','晚安','明天再说吧'等，bot回答'好，再见咯👋，我是小野，希望明天还能见到你！'",
                      "call":{
                          "function":"和user再见",
                          "args":{}
                      },
                    }
                  ],
          function_call = "auto",
          max_tokens = 150,
          n = 1,
          stop = None,
          temperature = 0.5
    )
    print(response)
    return response['choices']['0']['message']['function_call']

conversation_history = []

while True:
    user_input = input('user:')
    conversation_history.append(f'user:{user_input}')
    prompt ='\n'.join(conversation_history)
    bot_response = personal_assistant(prompt)
    conversation_history.append(f'bot:{bot_response}')
    print(f'bot:{bot_response}')