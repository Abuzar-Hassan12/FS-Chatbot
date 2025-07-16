const input = document.getElementById("user-input");
const chatBox = document.getElementById("chat-box");
const welcomeScreen = document.getElementById("welcome");
const convoList = document.getElementById("conversation-list");

let currentChat = [];
let allConversations = [];

function getCurrentTime() {
    const now = new Date();
    return now.getHours().toString().padStart(2, '0') + ':' + 
           now.getMinutes().toString().padStart(2, '0');
}

function createMessageElement(msg) {
    const messageDiv = document.createElement('div');
    messageDiv.classList.add('message');
    messageDiv.classList.add(msg.sender === 'user' ? 'user-message' : 'bot-message');
    
    const time = getCurrentTime();
    
    messageDiv.innerHTML = `
        <div class="message-header">
            <div class="avatar">${msg.sender === 'user' ? 'U' : 'BoT'}</div>
            <div class="username">${msg.sender === 'user' ? 'You' : 'FSPro Assistant'}</div>
        </div>
        <div class="message-content">
            ${msg.text}
        </div>
        <div class="message-time">${time}</div>
    `;
    
    return messageDiv;
}

function renderChat() {
    if (currentChat.length > 0) {
        welcomeScreen.style.display = "none";
    } else {
        welcomeScreen.style.display = "block";
        return;
    }
    
    while (chatBox.children.length > 1) {
        chatBox.removeChild(chatBox.lastChild);
    }
    
    currentChat.forEach(msg => {
        chatBox.appendChild(createMessageElement(msg));
    });
    
    scrollToBottom();
}

function sendMessage() {
    const msg = input.value.trim();
    if (!msg) return;
    
    currentChat.push({ sender: "user", text: `<p>${msg}</p>` });
    renderChat();
    input.value = "";
    input.focus();
    
    // Show animated typing indicator like original
    const typingDiv = document.createElement('div');
    typingDiv.id = "typing";
    typingDiv.className = "message bot-message";
    typingDiv.innerHTML = `
        <div class="message-header">
            <div class="avatar">BoT</div>
            <div class="username">FSPro Assistant</div>
        </div>
        <div class="message-content">
            <div class="typing-indicator">
                <span></span>
                <span></span>
                <span></span>
            </div>
        </div>
        <div class="message-time">${getCurrentTime()}</div>
    `;
    chatBox.appendChild(typingDiv);
    scrollToBottom();

    // Send to backend
    fetch("/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ input: msg })
    })
    .then(res => res.json())
    .then(data => {
        document.getElementById("typing")?.remove();
        currentChat.push({ sender: "bot", text: `<p>${data.response}</p>` });
        renderChat();
    })
    .catch(() => {
        document.getElementById("typing")?.remove();
        currentChat.push({ sender: "bot", text: `<p style="color: var(--error);">❌ Error processing response. Please try again.</p>` });
        renderChat();
    });
}

function startNewChat() {
    if (currentChat.length) {
        allConversations.push([...currentChat]);
        updateSidebar();
    }
    currentChat = [];
    renderChat();
    input.value = "";
}

function updateSidebar() {
    convoList.innerHTML = "";
    allConversations.forEach((convo, index) => {
        const firstMessage = convo[0]?.text.replace(/<[^>]*>/g, '') || "New Chat";
        const shortText = firstMessage.length > 20 ? firstMessage.substring(0, 20) + '...' : firstMessage;
        
        const li = document.createElement('div');
        li.className = "history-item";
        li.innerHTML = `
            <i class="fas fa-comment"></i> ${shortText}
            <span class="delete-btn">&times;</span>
        `;
        
        li.onclick = () => loadChat(index);
        
        const delBtn = li.querySelector('.delete-btn');
        delBtn.onclick = (e) => {
            e.stopPropagation();
            allConversations.splice(index, 1);
            updateSidebar();
            if (currentChat === allConversations[index]) {
                startNewChat();
            }
        };
        
        convoList.appendChild(li);
    });
}

function loadChat(index) {
    currentChat = [...allConversations[index]];
    renderChat();
}

function scrollToBottom() {
    chatBox.scrollTop = chatBox.scrollHeight;
}

input.addEventListener("keydown", (e) => {
    if (e.key === "Enter") sendMessage();
});

updateSidebar();
