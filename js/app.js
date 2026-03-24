let allMovies = [];

// 1. Fetch data from your GitHub-hosted JSON
async function fetchMovies() {
    const grid = document.getElementById('movieGrid');
    grid.innerHTML = '<p style="text-align:center; width:100%;">Loading the latest hits...</p>';

    try {
        // We add a timestamp to the URL to bypass browser cache
        const response = await fetch(`data/movies.json?v=${new Date().getTime()}`);
        allMovies = await response.json();
        renderMovies(allMovies);
    } catch (error) {
        console.error("Failed to load movies:", error);
        grid.innerHTML = '<p style="text-align:center; width:100%;">Syncing data... Please refresh in 60 seconds.</p>';
    }
}

// 2. Build the HTML for the movie cards
function renderMovies(movies) {
    const grid = document.getElementById('movieGrid');
    grid.innerHTML = '';

    if (movies.length === 0) {
        grid.innerHTML = '<p style="text-align:center; width:100%;">No movies found matching that search.</p>';
        return;
    }

    movies.forEach(movie => {
        const poster = movie.image && movie.image !== "N/A" 
            ? movie.image 
            : 'https://via.placeholder.com/300x450?text=No+Poster+Available';

        const card = document.createElement('div');
        card.className = 'movie-card';
        card.innerHTML = `
            <img src="${poster}" alt="${movie.title}" loading="lazy">
            <div class="movie-info">
                <span class="category-tag">${movie.category}</span>
                <h3>${movie.title}</h3>
                <p>${movie.summary}</p>
                <a href="${movie.link}" target="_blank" class="btn-details">Full Story</a>
            </div>
        `;
        grid.appendChild(card);
    });
}

// 3. Search Bar Logic
function filterMovies() {
    const query = document.getElementById('searchInput').value.toLowerCase();
    const filtered = allMovies.filter(m => 
        m.title.toLowerCase().includes(query) || 
        m.category.toLowerCase().includes(query) ||
        m.summary.toLowerCase().includes(query)
    );
    renderMovies(filtered);
}

// 4. Dark/Light Mode Toggle
function toggleTheme() {
    const body = document.body;
    const btn = document.getElementById('themeToggle');
    body.classList.toggle('light-mode');
    
    if (body.classList.contains('light-mode')) {
        btn.innerText = "Switch to Dark Mode";
    } else {
        btn.innerText = "Switch to Light Mode";
    }
}

// Start the app
fetchMovies();
