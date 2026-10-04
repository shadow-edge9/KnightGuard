async function sendMessage() {
    const input = document.getElementById("message-input");
    const chatBox = document.getElementById("chat-box");
    const sender = document.getElementById("sender").value;

    const message = input.value.trim();

    if (message === "") {
        return;
    }

    try {
        const response = await fetch("http://127.0.0.1:8000/chat", {
            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                sender: sender,
                message: message
            })
        });

        const data = await response.json();

        // Show the message in the chat
        const messageElement = document.createElement("div");

        if (sender === "A") {
            messageElement.className = "user-message";
            messageElement.textContent = `Person A: ${message}`;
        } 
        else if (sender === "B") {
            messageElement.className = "bot-message";
            messageElement.textContent = `Person B: ${message}`;
        } 
        else {
            messageElement.className = "user-message";
            messageElement.textContent = `You: ${message}`;
        }

        chatBox.appendChild(messageElement);


        // If AI is selected, show its response
        if (sender === "AI" && data.response) {

            const aiResponse = document.createElement("div");

            aiResponse.className = "bot-message";

            aiResponse.textContent = `AI: ${data.response}`;

            chatBox.appendChild(aiResponse);
        }


        // Show safety popup
        if (data.alert) {

            const popup = document.getElementById("safety-popup");

            const popupMessage =
                document.getElementById("safety-message");

            popupMessage.textContent = data.alert;

            popup.classList.add("show");
        }


        // Clear input
        input.value = "";

        // Keep chat scrolled to the bottom
        chatBox.scrollTop = chatBox.scrollHeight;

    } catch (error) {

        console.error("Error:", error);

        const popup = document.getElementById("safety-popup");

        const popupMessage =
            document.getElementById("safety-message");

        popupMessage.textContent =
            "Could not connect to the chat system.";

        popup.classList.add("show");
    }
}


// Close safety popup
function closeSafetyPopup() {

    const popup = document.getElementById("safety-popup");

    popup.classList.remove("show");
}