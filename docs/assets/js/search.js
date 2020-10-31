function searchResultCard(bit) {
    return `<div class="card">
    <div class="card-content">
      <p class="subtitle">
        <b>${bit.name}</b>
      </p>
    </div>
    <footer class="card-footer">
        <p class="card-footer-item">
        </p>
    </footer>
  </div>`
}

function emptySearchResults() {
    return "no bits found";
}


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
            method: 'GET'
        })
        .then(response => response.json())
        .then(data => {
            const searchResults = document.querySelector('#search_results');
            if (data.length == 0) {
                contents = emptySearchResults();
            } else {
                var contents = '';
                for (var bit of data) {
                    contents = contents.concat(searchResultCard(bit));
                }
            }
            searchResults.innerHTML = contents;
        });
    }
});
