document.addEventListener("DOMContentLoaded", function() {
    const qnaContainer = document.getElementById('qna-container');
    const promptInput = document.getElementById('prompt');
    const submitBtn = document.getElementById('submitBtn');

    // Function to add a message to the Q&A container
    function addMessage(message, isUser) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `mb-2 ${isUser ? 'text-right' : 'text-left'}`;
        messageDiv.innerText = message;
        qnaContainer.appendChild(messageDiv);
    }

    // Function to handle user submission
    function handleSubmit() {
        const prompt = promptInput.value.trim();
        if (prompt !== '') {
            // Add user's prompt to the Q&A container
            addMessage(prompt, true);
            // Simulate chatbot response (you can replace this with your actual chatbot logic)
            setTimeout(() => {
                const response = "This is a response from the chatbot. You can replace it with actual logic.";
                addMessage(response, false);
            }, 500);
            // Clear the input field
            promptInput.value = '';
        }
    }

    // Event listener for submit button
    submitBtn.addEventListener('click', handleSubmit);

    // Optional: Allow pressing Enter to submit
    promptInput.addEventListener('keydown', function(event) {
        if (event.key === 'Enter') {
            handleSubmit();
        }
    });
});