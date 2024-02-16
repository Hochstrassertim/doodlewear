function selectProcuctToEdit(input) {
    window.location.href = "/admin/edit_product?productId=" + input;
}

function saveProduct(productid) {
    description = document.getElementById("description")
    window.location.href = "/admin/edit_product/save?productId="+productid+"&name="+name+"&description="+description+"&price="+price+"&available="+available+"&story="+story+"&picture="+picture+"&discount="+discount
}