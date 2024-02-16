function selectProcuctToEdit(input) {
    window.location.href = "/admin/edit_product?productId=" + input;
}

function saveProduct() {
    const productId = document.getElementById('productId').value;
    const name = document.getElementById('name').value;
    const description = document.getElementById('description').value;
    const price = parseFloat(document.getElementById('price').value);
    const available = parseInt(document.getElementById('available').value);
    const story = document.getElementById('story').value;
    const picture = document.getElementById('picture').value;
    const discount = document.getElementById('discount').value;

    const data = {
        productId: productId,
        name: name,
        description: description,
        price: price,
        available: available,
        story: story,
        picture: picture,
        discount: discount,
    };

    fetch('/admin/edit_product/save', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
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
