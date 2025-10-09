
function scrollCategories(direction) {
  const container = document.getElementById("categoryList");
  const card = container.querySelector(".category-card");
  if (!card) return;

  const cardWidth = card.offsetWidth + 20; // width + gap
  const scrollAmount = cardWidth * 5;      // scroll 5 at a time

  container.scrollBy({
    left: direction * scrollAmount,
    behavior: "smooth"
  });
}

