let allMovies = [];

async function fetchMovies() {
    const grid = document.getElementById('movieGrid');
    
    try {
        // We use ./data/ to be extra specific for GitHub Pages
        const response = await fetch('./data/movies.json');
        if (!response.ok) throw new Error('File not found');
        
        allMovies = await response.json();
        console.log("Data loaded successfully:", allMovies); // This helps us debug
        renderMovies(allMovies);
    } catch (error) {
        console.error("Failed to load movies:", error);
        grid.innerHTML = `<p style="color:white; text-align:center;">Error: ${error.message}. Make sure data/movies.json exists!</p>`;
    }
}

function renderMovies(movies) {
    const grid = document.getElementById('movieGrid');
    grid.innerHTML = '';

    if (!movies || movies.length === 0) {
        grid.innerHTML = '<p style="color:white; text-align:center;">The movie list is currently empty.</p>';
        return;
    }

    movies.forEach(movie => {
        const poster = movie.image && movie.image !== "N/A" ? movie.image : 'https://via.placeholder.com/300x450?text=No+Poster';
        const card = document.createElement('div');
        card.className = 'movie-card';
        card.innerHTML = `
            <img src="${poster}" alt="${movie.title}">
            <div class="movie-info">
                <span class="category-tag">${movie.category || 'Movie'}</span>
                <h3>${movie.title}</h3>
                <p>${movie.summary}</p>
                <a href="${movie.link}" target="_blank" class="btn-details">Full Story</a>
            </div>
        `;
        grid.appendChild(card);
    });
}

function filterMovies() {
    const query = document.getElementById('searchInput').value.toLowerCase();
    const filtered = allMovies.filter(m => 
        m.title.toLowerCase().includes(query) || 
        (m.category && m.category.toLowerCase().includes(query))
    );
    renderMovies(filtered);
}

function toggleTheme() {
    document.body.classList.toggle('light-mode');
    const btn = document.getElementById('themeToggle');
    btn.innerText = document.body.classList.contains('light-mode') ? "Dark Mode" : "Light Mode";
}

// Ensure the script waits for the page to be ready
window.onload = fetchMovies;
