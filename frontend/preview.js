function loadDocument(documentUrl) {
    // Load the document based on the URL
    // Example code to load a PDF document
    // Replace this with your actual code to load the document
    const documentPreview = document.querySelector('.document-preview');
    documentPreview.innerHTML = `<iframe src="${documentUrl}" style="width: 100%; height: 100%; border: none;"></iframe>`;
}