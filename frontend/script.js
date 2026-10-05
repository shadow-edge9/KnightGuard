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

        // -----------------------------
        // Show original message
        // -----------------------------
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


        // -----------------------------
        // Show AI response
        // -----------------------------
        if (sender === "AI" && data.response) {
            const aiResponse = document.createElement("div");

            aiResponse.className = "bot-message";
            aiResponse.textContent = `AI: ${data.response}`;

            chatBox.appendChild(aiResponse);
        }


        // -----------------------------
        // Safety status
        // -----------------------------
        if (data.safety) {
            const safetyInfo = document.createElement("div");

            safetyInfo.className = "safety-info";

            const confidencePercent =
                Math.round(data.safety.confidence * 100);

            safetyInfo.innerHTML = `
                <strong>Safety Decision:</strong>
                ${data.safety.decision}
                <br>

                <strong>Risk:</strong>
                ${data.safety.risk.toUpperCase()}
                <br>

                <strong>Confidence:</strong>
                ${confidencePercent}%
                <br>

                <strong>Reason:</strong>
                ${data.safety.reason}
            `;

            chatBox.appendChild(safetyInfo);
        }


        // -----------------------------
        // Privacy status
        // -----------------------------
        if (
            data.privacy &&
            data.privacy.external_ai_used
        ) {
            const privacyInfo = document.createElement("div");

            privacyInfo.className = "privacy-info";

            if (data.privacy.redaction_applied) {
                privacyInfo.innerHTML = `
                    <strong>🔒 Privacy Protection Applied</strong>
                    <br>
                    Removed before external AI:
                    ${data.privacy.redacted_types.join(", ")}
                `;
            }

            else {
                privacyInfo.innerHTML = `
                    <strong>🔒 Privacy Check</strong>
                    <br>
                    No configured personal identifiers detected.
                `;
            }

            chatBox.appendChild(privacyInfo);
        }
// -----------------------------
// Sarvam language normalization
// -----------------------------

if (
    data.language &&
    data.language.normalization_used
) {
    const languageInfo =
        document.createElement("div");

    languageInfo.className = "privacy-info";

    const sourceLanguage =
        data.language.source_language || "auto-detected";

    languageInfo.innerHTML = `
        <strong>🌐 Sarvam Language Normalization</strong>
        <br>

        Source:
        ${sourceLanguage}

        <br>

        Safety analysis performed on:
        "${data.language.normalized_for_safety}"
    `;

    chatBox.appendChild(languageInfo);
}

        // -----------------------------
        // REVIEW / BLOCK popup
        // -----------------------------
        if (data.alert) {
            const popup =
                document.getElementById("safety-popup");

            const popupMessage =
                document.getElementById("safety-message");

            const confidencePercent =
                Math.round(data.safety.confidence * 100);

            popupMessage.innerHTML = `
                ${data.alert}
                <br><br>

                <strong>Decision:</strong>
                ${data.safety.decision}
                <br>

                <strong>Confidence:</strong>
                ${confidencePercent}%
                <br>

                <strong>Reason:</strong>
                ${data.safety.reason}
            `;

            popup.classList.add("show");
        }


        // -----------------------------
        // Special message if blocked
        // -----------------------------
        if (
            sender === "AI" &&
            data.safety &&
            data.safety.decision === "BLOCK"
        ) {
            const blockedMessage =
                document.createElement("div");

            blockedMessage.className = "safety-info";

            blockedMessage.textContent =
                "⛔ Message blocked before being sent to the external AI.";

            chatBox.appendChild(blockedMessage);
        }


        // Clear input
        input.value = "";

        // Scroll down
        chatBox.scrollTop =
            chatBox.scrollHeight;

    }

    catch (error) {
        console.error("Error:", error);

        const popup =
            document.getElementById("safety-popup");

        const popupMessage =
            document.getElementById("safety-message");

        popupMessage.textContent =
            "Could not connect to the chat system.";

        popup.classList.add("show");
    }
}


// -----------------------------
// Close safety popup
// -----------------------------
function closeSafetyPopup() {
    const popup =
        document.getElementById("safety-popup");

    popup.classList.remove("show");
}
