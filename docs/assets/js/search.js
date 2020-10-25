document.addEventListener("DOMContentLoaded", function() { 
    const searchButton = document.querySelector('#search_button');
    const searchQuery = document.querySelector('#search_query');
    
    searchButton.addEventListener('click', () => {
        window.location = `/search.html?q=${searchQuery.value}`;
    })
    
    var windowLoc = window.location.pathname;
    if (windowLoc == "/search.html") {
        const urlParams = new URLSearchParams(window.location.search);
        const bit_name = urlParams.get('q');
        fetch(`https://repo.cpmbits.com:8000/bits?name=${bit_name}`, {
            method: 'GET',
            mode: 'cors',
            headers: {
                'Content-Type': 'application/json',
            }
        })
        .then(response => {
            console.log(response.status)
            console.log(response.ok)
            if (response.status == 200) {
                const searchResults = document.querySelector('#search_results');
                searchResults.value = response.body
            }
        })
        .then(data => {});
    }
});
