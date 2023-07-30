import openai
import json

API_KEY = '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'
openai.api_key = API_KEY

messages = []
def personal_assistant(prompt):
    response = openai.ChatCompletion.create(
        model = 'gpt-3.5-turbo-0613',
        messages = [{"role":"user", "content":prompt}], #这里应该是接收user发来的消息
        #prompt = prompt,
        functions = [
                    {
                      "name":"greet_user",
                      "description":"当用户输入今日的任务时，根据以下格式梳理任务:'好的，我将今天的任务梳理为: </ol>1. 2. 3.<ol>加油💪 开干吧！'",
                      "parameters":{
                          "type":"object",
                          "properties":{
                              "greeting":{
                                  "type":"string",
                                  "description":"常见的打招呼用语。Common greeting phrases."
                              }
                          },
                          "required":["greeting"],
                      }
                    },
                    {
                      "name":"orgnanize_user_tasks_and_provide_task_list",
                      "description":"当用户输入今日的任务时，根据以下格式梳理任务:'好的，我将今天的任务梳理为: </ol>1. 2. 3.<ol>加油💪 开干吧！'使用markdown格式和emoji符号。With positive, friendly attitude.",
                      "parameters":{
                        "type":"object",
                        "properties":{
                              "organize_user_tasks":{
                                  "type":"string",
                                  "description":"待办任务。to-do list"
                              }
                          },
                        "required":["organize_user_tasks"],
                      },
                    },
                    {
                      "name":"add_user_task",
                      "description":"当用户新增加一项或几项任务，例如'我还需要把《刀锋》看完',回答'好的，任务列表更新为：</ol>1. 2. 3.<ol> 加油咯！'添加上待办任务。使用markdown格式和emoji符号。When the user adds one or more tasks, such as 'I still need to finish reading The Razor's Edge', reply with 'Okay, the task list has been updated to:</ol>1. 2. 3.<ol> Let's go!' Add the to-do task. Use markdown format and emoji symbols. With positive, friendly attitude.",
                      "parameters":{
                        "type":"object",
                        "properties":{
                              "add_user_tasks":{
                                  "type":"string",
                                  "description":"添加任务到待办任务列表中。Add user tasks to to-do list"
                              }
                          },
                        "required":["add_user_tasks"],
                      },
                    },
                    {
                      "name":"user_completes_a_task",
                      "description":"当user完成一项或几项任务，并且还有剩余任务，例如'我把《刀锋》看完了',bot回答'真棒🎉休息一下再继续。还剩下：</ol>1. 2. 3.<ol> ，一会儿继续加油咯！'删除掉完成的任务。使用markdown格式和emoji符号。When the user completes one or more tasks and there are still remaining tasks, such as 'I finished reading The Razor's Edge', bot replies with 'Great🎉 Take a break and continue. There are still:</ol>1. 2. 3.<ol>, let's continue later!' Delete the completed task. Use markdown format and emoji symbols. With positive, friendly attitude.",
                      "parameters":{
                        "type":"object",
                        "properties":{
                              "user_completes_a_task":{
                                  "type":"string",
                                  "description":"完成一项任务。complete a task."
                              }
                          },
                        "required":["user_completes_a_task"],
                      },
                    },
                    {
                      "name":"when_user_completes_all_tasks",
                      "description":"当user完成所有任务，在本轮回答中user完成了任务列表中所有任务',bot回答'恭喜🍾今天的任务全部完成！太棒了吧！'使用markdown格式和emoji符号。When the user completes all tasks, in this round of replies the user completes all tasks in the task list, bot replies with 'Congratulations🍾 All tasks for today are completed! Great!' Use markdown format and emoji symbols. With positive, friendly attitude.",
                      "parameters":{
                        "type":"object",
                        "properties":{
                              "completes_all_tasks":{
                                  "type":"string",
                                  "description":"完成所有任务。Complete all task."
                              }
                          },
                        "required":["completes_all_tasks"],
                      },
                    },
                    {
                      "name":"say_goodbye_to_user",
                      "description":"当user输入'Bye','晚安','明天再说吧'等，bot回答'好，再见咯👋，我是小野，希望明天还能见到你！'When the user inputs 'Bye', 'Good night', 'Let's talk tomorrow', etc., bot replies with 'Okay, goodbye👋, I am Xiao Ye, hope to see you tomorrow!'",
                      "parameters":{
                        "type":"object",
                        "properties":{
                              "say_goodbye":{
                                  "type":"string",
                                  "description":"再见。Say goodbye."
                              }
                        },
                        "required":["say_goodbye"],
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
    return response['choices'][0]['message']['content']

conversation_history = []

while True:
    user_input = input('user:')
    conversation_history.append(f'user:{user_input}')
    prompt ='\n'.join(conversation_history)
    bot_response = personal_assistant(prompt)
    conversation_history.append(f'bot:{bot_response}')
    print(f'bot:{bot_response}')