var typingTimer;
var isTyping = false;

//声明一个全局变量,用于存储从API接口返回的文本
var text_bot = '';

//开始计时器
function startTypingTimer() {
  clearTimeout(typingTimer);
  typingTimer = setTimeout(function() {
    isTyping = false;
    resetTypingTimer();
  }, 3000);
}

//重置计时器
function resetTypingTimer() {
  clearTimeout(typingTimer);
  isTyping = true;
  startTypingTimer();
}

//发送消息
function sendMessage() {
  var input = document.getElementById("input-message");
  var message = input.value.trim();
  if (message !== "") {
    addMessage("You", message, "user-message");
    input.value = ""; // 清空输入框
    resetTypingTimer();
    scrollToBottom();
    //Call the ChatGPT API to send a request and retrieve test
    fetch('/send-message',{
      method: 'POST',
      body: JSON.stringify({ 
        model: 'gpt-3.5-turbo-0301',
        temperature:0,
        max_tokens: 1024,
        prompt: message
      }),
      headers: {
        'Content-Type': 'application/json'
      }
    })
      .then(response => response.json())
      .then(data => {
        //将从API接口返回的文本赋值给text_bot变量
        var text_bot = data.text_bot;
        //将文本添加到聊天对话框
        addMessage("Bot", text_bot, "bot-message");
        console.log("Bot", text_bot, "bot-message");
        scrollToBottom();
      })
      .catch(error => {
        console.log(error);
      });
  }
}

//处理按键事件
function handleKeyPress(event) {
  if (event.keyCode === 13) {
    event.preventDefault();
    sendMessage();
  } else {
    resetTypingTimer();
  }
}

//添加消息到聊天对话框
function addMessage(sender, content, className) {
  var messageContainer = document.createElement("div");
  messageContainer.classList.add("message", className);

  var senderSpan = document.createElement("span");
  senderSpan.classList.add("sender");
  senderSpan.textContent = sender + ":";

  var messageContent = document.createElement("div");
  messageContent.classList.add("message-content");
  messageContent.textContent = content;

  messageContainer.appendChild(senderSpan);
  messageContainer.appendChild(messageContent);

  var chatContainer = document.querySelector("#chat-container");
  chatContainer.appendChild(messageContainer);

  scrollToBottom();
}

//滚动到底部
function scrollToBottom() {
  var chatContainer = document.querySelector("#chat-container");
  chatContainer.scrollTop = chatContainer.scrollHeight - chatContainer.clientHeight;
}

var inputMessage = document.getElementById("input-message");
inputMessage.addEventListener("input", resetTypingTimer);
