// Store the last page visited when online
function storeLastPage() {
  if (navigator.onLine) {
    localStorage.setItem("lastPage", window.location.pathname);
    console.log("Stored last page:", window.location.pathname);
  }
}

// Check internet connection and handle redirection
function checkInternetConnection() {
  console.log("Checking internet connection...");

  if (!navigator.onLine) {
    console.log("No internet connection. Redirecting to /offline");
    window.location.href = "/offline";
  } else {
    const currentPath = window.location.pathname;
    const lastPage = localStorage.getItem("lastPage") || "/";

    console.log("Internet connection restored.");
    console.log("Current Path:", currentPath);
    console.log("Last Page:", lastPage);

  }
}

// Event listener for load event
window.addEventListener("load", () => {
  storeLastPage();
  checkInternetConnection();
});

// Event listener for online event
window.addEventListener("online", () => {
  console.log("Online event detected");
  storeLastPage();
  checkInternetConnection();
});

// Event listener for offline event
window.addEventListener("offline", () => {
  console.log("Offline event detected");
  storeLastPage();
  checkInternetConnection();
});
