function openModal(imageElement) {
    const modal = document.getElementById("imageModal");
    const modalImg = document.getElementById("modalImage");
    const captionText = document.getElementById("caption");
    
    modal.style.display = "block";
    modalImg.src = imageElement.src;
    captionText.innerHTML = imageElement.alt;  // Use the alt text as caption
}

function closeModal() {
    document.getElementById("imageModal").style.display = "none";
}
