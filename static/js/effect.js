
  const text = "Freshness delivered fast";
  let i = 0;

  function typeEffect() {
    if (i < text.length) {
      document.getElementById("typing-text").innerHTML += text.charAt(i);
      i++;
      setTimeout(typeEffect, 100); // typing speed
    } else {
      // wait 2 sec, clear and restart
      setTimeout(() => {
        document.getElementById("typing-text").innerHTML = "";
        i = 0;
        typeEffect();
      }, 2000);
    }
  }

  window.onload = typeEffect;
