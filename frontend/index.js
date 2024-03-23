document.addEventListener("DOMContentLoaded", function() {
  const fileUploadInput = document.getElementById("fileUpload");
  const submitButton = document.querySelector("button[type='submit']");
  const messageContainer = document.getElementById("messageContainer");

  submitButton.addEventListener("click", function(event) {
      event.preventDefault(); // Prevent form submission
      
      // Check if a file is selected
      if (fileUploadInput.files.length === 0) {
          showMessage("Please select a file to upload.");
          return;
      }

      // Simulating file upload process
      setTimeout(function() {
          showMessage("File uploaded successfully!");
          // Optionally, you can reset the form after successful upload
          // document.getElementById("uploadForm").reset();
      }, 2000); // Change delay time as needed
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
