function showAbout() {
    var x = document.getElementById("about");
    if (x.style.display === "none") {
      x.style.display = "block";
      $('.about')
      .transition('slide down')
    ;
    } else {
      x.style.display = "none";
    }
  } 