// Function to open the share modal
function openShareModal(fileUrl) {
  const shareOptions = document.getElementById("shareOptions");
  shareOptions.innerHTML = "";

  const fullFileUrl = `${window.location.origin}${window.location.pathname}`;
  console.log('path', window.location.pathname)
  console.log("origin", window.location.origin);

  if (navigator.share) {
    const shareButton = document.createElement("button");
    shareButton.className = "list-group-item list-group-item-action";
    shareButton.innerText = "Share";
    shareButton.onclick = () => {
      navigator
        .share({
          title: document.title,
          text: "Here is the file I want to share with you.",
          url: fullFileUrl,
        })
        .then(() => {
          console.log("Successfully shared");
        })
        .catch((error) => {
          console.log("Error sharing:", error);
        });
    };
    shareOptions.appendChild(shareButton);
  }
  const copyButton = document.createElement("button");
  copyButton.className = "list-group-item list-group-item-action";
  copyButton.innerText = "Copy Link";
  copyButton.onclick = () => {
    copyLink(fullFileUrl);
  };
  shareOptions.appendChild(copyButton);

  document.getElementById("fileLink").value = fullFileUrl;
  document.getElementById("shareModal").style.display = "flex";
}

// Function to close the share modal
function closeShareModal() {
  document.getElementById("shareModal").style.display = "none";
}

// Function to copy the file link
function copyLink(fileUrl) {
  const copyText = document.getElementById("fileLink");
  copyText.select();
  copyText.setSelectionRange(0, 99999); // For mobile devices

  navigator.clipboard
    .writeText(copyText.value)
    .then(() => {
      alert("Copied the link: " + copyText.value);
    })
    .catch((err) => {
      console.error("Could not copy text: ", err);
    });
}

function handleKeyPress(event) {
  if (event.key === "Enter" || event.key === " ") {
    closeShareModal();
  }
}

