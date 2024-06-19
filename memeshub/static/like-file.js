var tooltipTriggerList = [].slice.call(
  document.querySelectorAll('[data-bs-toggle="tooltip"]')
);
var tooltipList = tooltipTriggerList.map(function (tooltipTriggerE1) {
  return new bootstrap.Tooltip(tooltipTriggerE1);
});

document.addEventListener("DOMContentLoaded", function () {
  document.querySelectorAll(".like-button").forEach(function (element) {
    let fileId = element.getAttribute("data-file-id");
    let icon = element.querySelector("i.material-icons");
    let likeCountSpan = element.querySelector("span.ms-1");

    // Check local storage for like status
    if (localStorage.getItem(`liked_${fileId}`) === "true") {
      icon.classList.add("liked");
      icon.classList.remove("not-liked");
    } else {
      icon.classList.add("not-liked");
      icon.classList.remove("liked");
    }

    element.addEventListener("click", function (event) {
      event.preventDefault(); // Prevent the default action

      // Make AJAX request to like the image
      fetch(
        `/like-image?x_id=${fileId}&next=${encodeURIComponent(
          window.location.pathname
        )}`,
        {
          method: "GET",
          headers: {
            "X-Requested-With": "XMLHttpRequest",
          },
        }
      )
        .then((response) => response.json())
        .then((data) => {
          if (data.authenticated === false) {
            window.location.href = data.login_url;
          } else {
            if (data.liked) {
              icon.classList.add("liked");
              icon.classList.remove("not-liked");
              localStorage.setItem(`liked_${fileId}`, "true");
            } else {
              icon.classList.add("not-liked");
              icon.classList.remove("liked");
              localStorage.setItem(`liked_${fileId}`, "false");
            }
            likeCountSpan.textContent = data.likes;
          }
        })
        .catch((error) => console.error("Error:", error));
    });
  });
});
