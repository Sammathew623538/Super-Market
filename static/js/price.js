
  const quantityField = document.getElementById('quantity');
  const priceDisplay = document.getElementById('total-price');

  // Make sure unitPrice is JS number
  const unitPrice = parseFloat("{{ product.price|floatformat:2 }}");

  quantityField.addEventListener('input', function() {
    let qty = parseInt(this.value) || 1;
    priceDisplay.textContent = (unitPrice * qty).toFixed(2);
  });
