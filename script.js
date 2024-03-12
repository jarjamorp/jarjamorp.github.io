// function openModal(imageElement) {
//     const modal = document.getElementById("imageModal");
//     const modalImg = document.getElementById("modalImage");
//     const captionText = document.getElementById("caption");
    
//     modal.style.display = "block";
//     modalImg.src = imageElement.src;
//     captionText.innerHTML = imageElement.alt;  // Use the alt text as caption
// }

function openModal(imageElement) {
    const modal = document.getElementById("imageModal");
    const modalImg = document.getElementById("modalImage");
    const captionText = document.getElementById("caption");
    
    modal.style.display = "block";

    // Remove "-tn" from the thumbnail src to get the large image src
    const largeImageSrc = imageElement.src.replace("-tn", "");

    modalImg.src = largeImageSrc;
    captionText.innerHTML = imageElement.alt; 
}


function closeModal() {
    document.getElementById("imageModal").style.display = "none";
}