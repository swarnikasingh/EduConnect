document.addEventListener("DOMContentLoaded", function() {
  const fileInput = document.getElementById("fileInput");
  const uploadButton = document.querySelector("button[type='submit']");
  const messageContainer = document.getElementById("messageContainer");

  uploadButton.addEventListener("click", function(event) {
      event.preventDefault(); // Prevent form submission
      
      // Check if a file is selected
      if (!fileInput.files || fileInput.files.length === 0) {
        setTimeout(function() {
          showMessage("Please Upload a File!");
          // Optionally, you can reset the file input after successful upload
          // fileInput.value = null;
      }, 200);
          return;
      }

      // Simulating file upload process
      setTimeout(function() {
          showMessage("File uploaded successfully!");
          // Optionally, you can reset the file input after successful upload
          // fileInput.value = null;
      }, 200); // Change delay time as needed
  });

  function showMessage(message) {
      // Create a new message element
      const messageElement = document.createElement("div");
      messageElement.textContent = message;
      messageElement.classList.add("message");

      // Clear previous messages
      messageContainer.innerHTML = "";

      // Append the new message element to the message container
      messageContainer.appendChild(messageElement);
  }
});
