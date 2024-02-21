 let lastScrollTop = 0;
  window.addEventListener("scroll", function() {
    let currentScroll = window.pageYOffset || document.documentElement.scrollTop;
    if (currentScroll > lastScrollTop) {

      document.querySelector("header").style.top = "-80px";
    } else {

      document.querySelector("header").style.top = "0";
    }
    lastScrollTop = currentScroll <= 0 ? 0 : currentScroll;
  }, false);