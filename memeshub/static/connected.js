// Store the last page visited when online
function storeLastPage() {
  if (navigator.onLine) {
    localStorage.setItem("lastPage", window.location.pathname);
    console.log("Stored last page:", window.location.pathname);
  }
}

// Check internet connection and handle redirection
function checkInternetConnection() {
  if (navigator.onLine) {
    fetch("https://www.google.com/favicon.ico", { mode: "no-cors" })
    .then(() => {
    const lastPage = localStorage.getItem("lastPage") || "/";
    console.log("Internet connection restored. Redirecting to last visited page:",lastPage);
    window.location.href = lastPage;
  })
  .catch(() => {
    console.log("Network connected but no internet access.");
  });
}
}

// Event listener for load event
window.addEventListener("load", () => {
  checkInternetConnection();
});

// Event listener for online event
window.addEventListener("online", () => {
  console.log("Online event detected");
  checkInternetConnection();
});
