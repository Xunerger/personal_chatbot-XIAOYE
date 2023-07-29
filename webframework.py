#!/usr/bin/python
# -*-coding:utf-8 -*-
from flask import Flask, request, render_template,jsonify, redirect
from flask_cors import CORS
from werkzeug.middleware.proxy_fix import ProxyFix
import requests
import mysql.connector


app = Flask(__name__, static_url_path='/static')
CORS(app)
API_KEY = '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'
messages = []

@app.route('/')
def home():
    return render_template('login.html')

#配置MySQL数据库连接：
db = mysql.connector.connect(
    host="localhost",
    user='root',
    password='123456',
    database='chatbot'
)

@app.route('/login', methods=['POST'])
def login():
    #获取登陆表单提交的用户名和密码
    username = request.form.get('username')
    password = request.form.get('password')

    #创建数据库游标
    cursor = db.cursor()

    #查询数据库中是否存在匹配的用户名和密码
    query = "SELECT * FROM users WHERE username = %s"
    cursor.execute(query, (username, ))
    user = cursor.fetchone()

    #进行登录验证逻辑判断
    if user and user[2] == password:
        #登录验证成功，跳转到index.html页面
        return render_template('/index.html')
    else:
        #如果登录验证失败，跳转到login.html页面，并且给出错误提示
        error_message = "用户名或密码错误，请重新输入"
        return render_template('login.html', error_message=error_message)
    #关闭数据库游标和连接
    cursor.close()
    db.close()


@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        #获取表单提交的用户名和密码
        username = request.form.get('username')
        password = request.form.get('password')

        if username and password:
            #创建数据库游标
            cursor = db.cursor()

            #执行插入数据的MySQL语句
            sql = "INSERT INTO users (username, password) VALUES (%s, %s)"
            val = (username, password)

            cursor.execute(sql, val)
            db.commit()
            
            print(cursor.rowcount, "插入成功")
    
            #关闭数据库游标
            cursor.close()

            return render_template('login.html')
        else:
            return "请输入有效的用户名和密码哦"
        
    return render_template('register.html')


@app.route('/send-message', methods=['POST'])
def send_message():
    data = request.json
    user_input = data['prompt']
    user_input = user_input 
    print(user_input)
    messages.append({'role':'system','content':"假设你是用户的私人秘书，对用户的输入，根据以下几种情况回答: 1. user见面打招呼，回复'你好，我是小野👋。今天都要做些什么呢？'2. user表述自己的任务安排，例如'user: 我早晨要写日记，游泳，然后下午看书'，按照以下格式回复 '好的，我将您的今日任务整理为：\n 1.上午写日记 \n 2.游泳 \n 3.下午读书 \n 希望任务进展顺利！' 3. user完成某项任务，例如'user: 我写完了日记'，回复'真棒！现在剩余的任务是\n 1.游泳 \n 2.读书 \n 再接再厉!' 4. user完成全部任务，回复'恭喜！今天的任务已经全部完成咯！好好休息一下吧！'5. 用户告别，回复'今天也很棒哦，小野期待明天再见到你！'"})
    target_url = "https://api.openai.com/v1/completions"
    headers = {
        "Authorization":f"Bearer {API_KEY}",
        "Content-Type":"application/json",
        "Accept":"application/json"
    }
    payload = {
        "prompt":"user: " + user_input,
        "temperature":0.9,
        "max_tokens": 200,
        "top_p" : 1,
        "frequency_penalty" : 0,
        "presence_penalty" : 0.6,
        "model": "text-davinci-003", 
        "stop": "user: "   
    }
    response = requests.post(target_url, headers=headers, json=payload)
    print(response.json()) 
    text_bot = response.json()['choices'][0]['text']
    return jsonify({'text_bot': text_bot})



if __name__ == "__main__":
    app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)
    app.run(host='0.0.0.0', port=3000, debug=True)