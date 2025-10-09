document.querySelectorAll(".add-to-cart").forEach(btn => {
  btn.addEventListener("click", function() {
    const productId = this.getAttribute("data-id");

    fetch(`/one/cart/add/${productId}/`, {
      method: "POST",   // 🔴 important: POST aakum
      headers: {
        "X-CSRFToken": getCookie("csrftoken"),  // CSRF token add cheyyuka
        "Content-Type": "application/json"
      },
      body: JSON.stringify({})  // body empty aayalum ok
    })
    .then(res => res.json())
    .then(data => {
      if (data.success) {
        alert(data.message);
      }
    });
  });
});

// csrf helper
function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}
