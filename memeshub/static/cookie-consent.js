function getCookie(name) {
    let cookieArr = document.cookie.split(";");
    for (let i = 0; i < cookieArr.length; i++) {
        let cookiePair = cookieArr[i].split("=");
        if (name == cookiePair[0].trim()) {
            return decodeURIComponent(cookiePair[1]);
        }
    }
    return null;
}

function setCookie(name, value, days) {
    let date = new Date();
    date.setTime(date.getTime() + (days * 24 * 60 * 60 * 1000));
    let expires = "expires=" + date.toUTCString();
    document.cookie = name + "=" + encodeURIComponent(value) + ";" + expires + ";path=/, path=/explore, path=/discover, path=/about";
}

// Check if sessionStorage has a flag indicating page refresh
  var pageRefreshed = sessionStorage.getItem("pageRefreshed");

function checkCookieConsent() {
  let cookieConsent = getCookie("cookie_consent");
  if ( cookieConsent === "accepted" || (cookieConsent === "rejected" && !pageRefreshed)) {
    document.getElementById("cookieConsentBanner").style.display = "none";
  } else {
    document.getElementById("cookieConsentBanner").style.display = "block";
    sessionStorage.setItem("pageRefreshed", true);
  }
}
 document.addEventListener("DOMContentLoaded", function () {
    document.getElementById("acceptCookies").addEventListener("click", function () {
        setCookie("cookie_consent", "accepted", 30);
        document.getElementById("cookieConsentBanner").style.display = "none";
    });

    document.getElementById("rejectCookies").addEventListener("click", function () {
        setCookie("cookie_consent", "rejected", 30);
        document.getElementById("cookieConsentBanner").style.display = "none";
    });

    document.getElementById("customizeCookies").addEventListener("click", function () {
        const cookieSettingsModal = new bootstrap.Modal(document.getElementById("cookieSettingsModal"));
        cookieSettingsModal.show();
        document.getElementById("cookieConsentBanner").style.visibility = 'hidden';
    });
});
document.getElementById("savePreferences").addEventListener("click", function () {
    // Save preferences logic
    const analyticsCookies = document.getElementById("analyticsCookies").checked;
    const marketingCookies = document.getElementById("marketingCookies").checked;
    const socialMediaCookies = document.getElementById("socialMediaCookies").checked;

    setCookie("analyticsCookies", analyticsCookies, 30);
    setCookie("marketingCookies", marketingCookies, 30);
    setCookie("socialMediaCookies", socialMediaCookies, 30);

    setCookie("cookie_consent", "accepted", 30); // Mark as accepted
    document.getElementById("cookieConsentBanner").style.display = "none";
    const cookieSettingsModal = bootstrap.Modal.getInstance(document.getElementById("cookieSettingsModal"));
    cookieSettingsModal.hide();
});

// Check cookie consent on page load
window.onload = function () {
    checkCookieConsent();
};

// Function to open the share modal
function openShareModal(fileUrl) {
    const shareOptions = document.getElementById("shareOptions");
    shareOptions.innerHTML = '';

    const fullFileUrl = `${window.location.origin}${fileUrl}`;

    if (navigator.share) {
        const shareButton = document.createElement('button');
        shareButton.className = 'list-group-item list-group-item-action';
        shareButton.innerText = 'Share';
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
        const copyButton = document.createElement('button');
        copyButton.className = 'list-group-item list-group-item-action';
        copyButton.innerText = 'Copy Link';
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

    navigator.clipboard.writeText(copyText.value).then(() => {
        alert("Copied the link: " + copyText.value);
    }).catch(err => {
        console.error('Could not copy text: ', err);
    });
}

function handleKeyPress(event) {
  if (event.key === "Enter" || event.key === " ") {
    closeShareModal();
  }
}