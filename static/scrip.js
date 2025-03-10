document.addEventListener("DOMContentLoaded", function () {
  let productInput = document.getElementById("name");
  let productList = JSON.parse(document.getElementById("product-data").textContent);
  
  productInput.addEventListener("blur", function () {
      let enteredValue = productInput.value.trim().toLowerCase();
      let matchFound = productList.some(product => product.toLowerCase() === enteredValue);
      
      if (!matchFound) {
          alert("Please select a product from the dropdown.");
          productInput.value = "";
      }
  });
});
