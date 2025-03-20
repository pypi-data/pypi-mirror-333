let sessionId = null;
let sentinelCalled = false;
const apiUrl = 'http://localhost:8001/api/v1';
const apiSession = 'http://localhost:8002/api/v1';

const chatContainer = document.getElementById('chat-container');
const messageInput = document.getElementById('message-input');
const sendButton = document.getElementById('send-button');

async function callSentinel() {
    sentinelCalled = true;
    try {
        const response = await fetch(`${apiUrl}/sentinel`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-Session-Id': sessionId
            },
        });
        const data = await response.text();
        console.log('Sentinel Response:', data);

    } catch (error) {
        console.error('Error calling sentinel:', error);
        sentinelCalled = false;
    }
}

async function createSession() {
    try {
        const response = await fetch(`${apiSession}/create-session`, {
            method: 'POST',
            headers: {
                'accept': 'application/json',
            }
        });
        const data = await response.json();
        sessionId = data.sessionId;
        console.log('Session ID:', sessionId);
        // startEventSource();
    } catch (error) {
        console.error('Errore nella creazione della sessione:', error);
    }
    askUsername();
}

async function closeSession(sessionId) {
    try {
        const response = await fetch(`${apiSession}/close-session`, {
            method: 'POST',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json' // Specify that we're sending JSON
            },
            body: JSON.stringify({
                'sessionId': sessionId
            }),
        });

        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }

        const data = await response.json();
        console.log('Status:', data.status);
    } catch (error) {
        console.error('Error closing session:', error);
    }
}

function showWaitingMessage(show) {
    const waitingMessage = document.getElementById('waiting-message');
    waitingMessage.style.display = show ? 'block' : 'none';
}

async function sendMessage(message) {
    try {
        addMessageToChat(message, 'sent');
        showWaitingMessage(true);

        console.log("Question: ", message)

        const url = `${apiUrl}/stream?sessionId=${encodeURIComponent(sessionId)}&content=${encodeURIComponent(message)}`;
        const eventSource = new EventSource(url);

        eventSource.onmessage = function (event) {
            const data = JSON.parse(event.data);

            if (data.messages) {
                data.messages.forEach(message => {
                    if (message.message_type === 'assistant_message') {
                        addMessageToChat(message.content, 'received');
                    } else if (message.message_type === 'reasoning_message') {
                        console.log("Reasoning:", message.reasoning);
                    } else {
                        console.log("Message:", message);
                    }
                });
            }

            if (data.usage) {
                console.log("Usage data:", data.usage);
            }

            showWaitingMessage(false);
            eventSource.close();
        };

        // eventSource.onerror = function (event) {
        //     console.error("EventSource failed:", event);
        //     eventSource.close();
        // };

        // const eventSource = new EventSource(`${apiUrl}/stream?sessionId=${encodeURIComponent(sessionId)}&content=${encodeURIComponent(message)}`);

        // eventSource.onmessage = function (event) {
        //     const data = JSON.parse(event);
        //     console.log("New message:", data);
        //     // const data = JSON.parse(event.data);
        //     // console.log('Received:', data);
        //     // addMessageToChat(data.messages, 'received');
        //     // showWaitingMessage(false);
        //     // eventSource.close();
        // };

        // eventSource.onerror = function (event) {
        //     console.error("EventSource failed:", event);
        //     eventSource.close();
        // };

    } catch (error) {
        console.error('Error sending message:', error);
    }
}

function addMessageToChat(message, type) {
    const messageElement = document.createElement('div');
    messageElement.classList.add('message', type);

    // Recupera il contenuto di chatbox, se presente
    const chatbox = document.getElementById('chat-box');
    if (chatbox && chatbox.children.length > 0) {
        const chatboxContent = chatbox.innerHTML; // Prende tutto il contenuto HTML
        messageElement.innerHTML = chatboxContent + `<p>${message}</p>`; // Appende il messaggio
        chatbox.innerHTML = ''; // Svuota chatbox
    } else {
        messageElement.textContent = message;
    }

    chatContainer.appendChild(messageElement);
    chatContainer.scrollTop = chatContainer.scrollHeight;

    setTimeout(() => {
        messageElement.classList.add('visible');
    }, 10);
}

function startEventSource() {
    const eventSource = new EventSource(`${apiUrl}/stream?sessionId=${encodeURIComponent(sessionId)}`);

    eventSource.onmessage = function (event) {
        console.log('Received:', event.data);
        addMessageToChat(event.data, 'received');
    };

    window.addEventListener('beforeunload', () => {
        eventSource.close();
    });
}

async function askUsername() {
    // const username = prompt("Please enter your name:", "Emmanuele");
    // if (username) {
    //     // document.getElementById('username').textContent = username;
    //     try {
    //         const response = await fetch(`${apiUrl}/set-username`, {
    //             method: 'POST',
    //             headers: {
    //                 'Content-Type': 'application/json',
    //             },
    //             body: JSON.stringify({
    //                 'X-Session-Id': sessionId,
    //                 'username': username,
    //             }),
    //         });
    //         if (!response.ok) {
    //             throw new Error('Failed to set username');
    //         }
    //     } catch (error) {
    //         console.error('Error setting username:', error);
    //     }
    // }
}


sendButton.addEventListener('click', () => {
    let message = messageInput.value.trim();
    
    if (message) {
        chatbox = document.getElementById("chat-box"); // Assicurati che l'ID sia corretto
        preElement = chatbox.querySelector('pre');

        if (preElement) {
            message += ': ' + preElement.textContent.trim();
        }

        sendMessage(message);
        messageInput.value = '';
    }
});

messageInput.addEventListener('keydown', (event) => {
    if (!sentinelCalled) {
        callSentinel();
    }
    if (event.key === 'Enter' && !event.altKey) {
        event.preventDefault();
        const message = messageInput.value.trim();
        if (message) {
            sendMessage(message);
            messageInput.value = '';
        }
    }
});

window.addEventListener('beforeunload', () => {
    if (sessionId) {
        closeSession(sessionId);
    }
});

document.addEventListener('DOMContentLoaded', (event) => {
    createSession();
    
});


