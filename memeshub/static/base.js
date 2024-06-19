var a;
let searchForm = document.querySelector("#myform");
let body_content = document.querySelector("#contentId");
let navbarId = document.querySelector("#navId");
let following_content = document.querySelector("#following");
function showForm() {
  if (a == 1) {
    searchForm.style.visibility = "visible";
    body_content.style.visibility = "hidden";
    navbarId.style.visibility = "visible";
    return (a = 0);
  } else {
    searchForm.style.visibility = "hidden";
    body_content.style.visibility = "visible";
    return (a = 1);
  }
}
var b;
let searchAgain = document.querySelector("#myOtherForm");
function searchHere() {
  if (b == 1) {
    searchAgain.style.visibility = "visible";
    return (b = 0);
  } else {
    searchAgain.style.visibility = "hidden";
    return (b = 1);
  }
}
document.addEventListener("DOMContentLoaded", function () {
  const lightButton = document.getElementById("lightButton");
  const darkButton = document.getElementById("darkButton");
  const body = document.body;

  // Function to apply the theme
  function applyTheme(theme) {
    if (theme === "dark") {
      body.classList.add("dark-theme");
      body.classList.remove("light-theme");
    } else {
      body.classList.add("light-theme");
      body.classList.remove("dark-theme");
    }
  }

  // Load theme from localStorage
  const savedTheme = localStorage.getItem("theme") || "light";
  applyTheme(savedTheme);

  lightButton.addEventListener("click", function () {
    applyTheme("light");
    localStorage.setItem("theme", "light");
  });

  darkButton.addEventListener("click", function () {
    applyTheme("dark");
    localStorage.setItem("theme", "dark");
  });
});
const body = document.body;
