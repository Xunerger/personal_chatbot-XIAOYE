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
    user_input = user_input +"The end"
    print(user_input)
    messages.append({'role':'user','content':user_input})
    target_url = "https://api.openai.com/v1/completions"
    headers = {
        "Authorization":f"Bearer {API_KEY}",
        "Content-Type":"application/json",
        "Accept":"application/json"
    }
    stop_sequences = ["\n\n","The end"]
    payload = {
        "prompt":user_input,
        "max_tokens": 1024,
        "model": "davinci:ft-personal-2023-07-24-15-56-32", 
        "stop": stop_sequences    
    }
    response = requests.post(target_url, headers=headers, json=payload)
    print(response.json()) 
    text_bot = response.json()['choices'][0]['text']
    return jsonify({'text_bot': text_bot})



if __name__ == "__main__":
    app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)
    app.run(host='0.0.0.0', port=3000, debug=True)