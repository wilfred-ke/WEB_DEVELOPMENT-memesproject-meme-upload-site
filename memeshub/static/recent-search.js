document.getElementById('inputBox').addEventListener('focus', function() {
    fetchRecentSearches();
    fetchUserSuggestions();
});

document.getElementById('inputBox').addEventListener('input', function() {
    fetchUserSuggestions();
});

function fetchRecentSearches() {
    fetch("{% url 'recent_searches' %}")  // You'll need to create this view
        .then(response => response.json())
        .then(data => {
            const recentSearches = document.getElementById('recentSearches');
            recentSearches.innerHTML = '';
            data.recent_searches.forEach(search => {
                const item = document.createElement('div');
                item.className = 'dropdown-item';
                item.textContent = search.search_term;
                item.onclick = () => {
                    document.getElementById('inputBox').value = search.search_term;
                    document.querySelector('form').submit();
                };
                recentSearches.appendChild(item);
            });
            recentSearches.style.display = data.recent_searches.length ? 'block' : 'none';
        });
}

function fetchUserSuggestions() {
    const query = document.getElementById('inputBox').value;
    fetch("{% url 'user_suggestions' %}?q=" + query)  // You'll need to create this view
        .then(response => response.json())
        .then(data => {
            const userSuggestions = document.getElementById('userSuggestions');
            userSuggestions.innerHTML = '';
            data.user_suggestions.forEach(user => {
                const item = document.createElement('div');
                item.className = 'dropdown-item';
                item.textContent = user.username;
                item.onclick = () => {
                    document.getElementById('inputBox').value = user.username;
                    document.querySelector('form').submit();
                };
                userSuggestions.appendChild(item);
            });
            userSuggestions.style.display = data.user_suggestions.length ? 'block' : 'none';
        });
}