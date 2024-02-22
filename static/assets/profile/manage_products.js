function reload() {
    window.location.href = window.location.href;
}

function cancelEditing() {
    window.location.href = "view_products";
}

function selectProcuctToEdit(input) {
    if (input == null) {
        window.location.href = "/admin/view_products"
    } else {
        window.location.href = "/admin/edit_product?productId=" + input;
    }
}

function saveProduct() {
    const productId = document.getElementById('productId').value;
    const name = document.getElementById('name').value;
    const description = document.getElementById('description').value;
    const price = parseFloat(document.getElementById('price').value);
    const available = parseInt(document.getElementById('available').value);
    const story = document.getElementById('story').value;
    const pictureInput = document.getElementById('picture');
    const discount = document.getElementById('discount').value;

    console.log(productId)

    const formData = new FormData();
    formData.append('productId', productId);
    formData.append('name', name);
    formData.append('description', description);
    formData.append('price', price);
    formData.append('available', available);
    formData.append('story', story);
    formData.append('picture', pictureInput.files[0]);
    formData.append('discount', discount);

    fetch('/admin/edit_product/save', {
        method: 'POST',
        body: formData,
    })
    .then(response => response.json())
    .then(result => {
        console.log(result);
        // Optionally handle success or show a message to the user
    })
    .catch(error => {
        console.error('Error:', error);
        // Optionally handle error or show a message to the user
    });
}


function updatePreview() {
        document.getElementById("previewDescription").textContent = document.getElementById("description").value;
        document.getElementById("previewStory").textContent = document.getElementById("story").value;
        document.getElementById("previewName").textContent = document.getElementById("name").value;
        document.getElementById("previewPrice").textContent = document.getElementById("price").value;
        document.getElementById("previewDescription").textContent = document.getElementById("description").value;
        document.getElementById("previewDescription").textContent = document.getElementById("description").value;
        document.getElementById("previewDescription").textContent = document.getElementById("description").value;

    }

document.getElementById("name").addEventListener("input", updatePreview);
document.getElementById("description").addEventListener("input", updatePreview);
document.getElementById("price").addEventListener("input", updatePreview);
document.getElementById("availability").addEventListener("input", updatePreview);
document.getElementById("story").addEventListener("input", updatePreview);
document.getElementById("picture").addEventListener("input", updatePreview);
document.getElementById("discount").addEventListener("input", updatePreview);