let allMovies = [];

async function init() {
    const res = await fetch('data/movies.json');
    allMovies = await res.json();
    render(allMovies);
}

function render(movies) {
    const grid = document.getElementById('movieGrid');
    grid.innerHTML = movies.map(m => `
        <div class="movie-card" onclick="window.location.href='movie-details.html?id=${m.imdbID}'">
            <img src="${m.Poster}">
            <h3>${m.Title}</h3>
            <p>${m.Year} • ${m.imdbRating}</p>
        </div>
    `).join('');
}

function filterMovies() {
    const search = document.getElementById('searchInput').value.toLowerCase();
    const filtered = allMovies.filter(m => 
        m.Title.toLowerCase().includes(search) || 
        m.Actors.toLowerCase().includes(search)
    );
    render(filtered);
}

document.addEventListener('DOMContentLoaded', init);
