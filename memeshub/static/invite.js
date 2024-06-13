 document.addEventListener(`DOMContentLoaded`, function () {
    const inviteFriendBtn = document.getElementById('inviteFriendBtn');
    const popupOverlay = document.getElementById('popupOverlay');
    const closePopupBtn = document.getElementById('closePopupBtn');
    const pageLink = document.getElementById('pageLink');
    const copyLinkBtn = document.getElementById('copyLinkBtn');
    const shareBtn = document.getElementById('shareBtn');

    inviteFriendBtn.addEventListener('click', function () {
        pageLink.value = window.location.href;
        popupOverlay.style.display = 'block';
    });

    closePopupBtn.addEventListener('click', function () {
        popupOverlay.style.display = 'none';
    });

    copyLinkBtn.addEventListener('click', function () {
        pageLink.select();
        document.execCommand('copy');
        alert('Link copied to clipboard');
    });

    shareBtn.addEventListener('click', function () {
        if (navigator.share) {
            navigator.share({
                title: document.title,
                text: 'Check out this page!',
                url: window.location.href
            }).then(() => {
                console.log('Thanks for sharing!');
            }).catch(err => {
                console.error('Error sharing:', err);
            });
        } else {
            alert('Share API not supported in this browser. Copy the link instead.');
        }
    });
});