class Chatbox {
  constructor() {
      this.args = {
          
          chatBox: document.querySelector('.chatbox__support'),
          sendButton: document.querySelector('.send__button')
      }
      this.messages = [];
    }
    display() {
      const {chatBox, sendButton} = this.args;

      

      sendButton.addEventListener('click', () => this.onSendButton(chatBox))

      const node = chatBox.querySelector('input');
      node.addEventListener("keyup", ({key}) => {
          if (key === "Enter") {
              this.onSendButton(chatBox)
          }
      })
  }
  onSendButton(chatbox) {
    let textField = chatbox.querySelector('input');
    let text1 = textField.value
    if (text1 === "") {
        return;
    }

    let msg1 = { name: "User", message: text1 }
    this.messages.push(msg1);

    fetch($SCRIPT_ROOT+'/predict', {
        method: 'POST',
        body: JSON.stringify({ message: text1 }),
        
        headers: {
          'Content-Type': 'application/json'
        },
      })
      .then(r => r.json())
      .then(r => {
        let msg2 = { name: "Sam", message: r.answer };
        this.messages.push(msg2);
        this.updateChatText(chatbox)
        textField.value = ''

    }).catch((error) => {
        console.error('Error:', error);
        this.updateChatText(chatbox)
        textField.value = ''
      });
}

updateChatText(chatbox) {
    var html = '';
    this.messages.slice().reverse().forEach(function(item, index) {
        if (item.name === "Sam")
        {
            html += '<div class="messages__item messages__item--visitor">' + item.message + '</div>'
        }
        else
        {
            html += '<div class="messages__item messages__item--operator">' + item.message + '</div>'
        }
      });

    const chatmessage = chatbox.querySelector('.chatbox__messages');
    chatmessage.innerHTML = html;
}
}


const chatbox = new Chatbox();
chatbox.display();