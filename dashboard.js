const csvFiles = {
  moviesWatched: 'data/movies/movies_watched.csv',
  moviesToWatch: 'data/movies/movies_to_watch.csv',
  booksRead: 'data/books/books_read.csv',
  booksToRead: 'data/books/to_read.csv',
  documentaries: 'data/documentaries/documentaries_watched.csv',
  series: 'data/tv-series/series_watched.csv',
  gamesBeaten: 'data/games/games_beaten.csv',
  gamesAbandoned: 'data/games/games_abandoned.csv',
  wineExperiences: 'data/wine/wine_experiences.csv'
};

const palette = {
  purple: '#a855f7',
  cyan: '#22d3ee',
  amber: '#f59e0b',
  teal: '#14b8a6',
  lime: '#a3e635',
  pink: '#f472b6',
  slate: '#94a3b8'
};

// Ajustes globais de fonte e cor para legibilidade
Chart.defaults.color = '#f8fafc';
Chart.defaults.font.family = 'Space Grotesk, system-ui, -apple-system, sans-serif';
Chart.defaults.font.size = 16;
Chart.defaults.font.weight = '700';

const setCardValue = (metric, value) => {
  const card = document.querySelector(`[data-metric="${metric}"]`);
  if (card) card.textContent = value;
};

const toNumber = (value) => {
  const n = parseInt(value, 10);
  return Number.isFinite(n) ? n : null;
};

const countBy = (rows, key) => {
  const map = new Map();
  rows.forEach(row => {
    const val = row[key];
    if (val && val.trim() !== '') {
      map.set(val, (map.get(val) || 0) + 1);
    }
  });
  return Array.from(map.entries()).sort((a, b) => {
    const an = Number(a[0]);
    const bn = Number(b[0]);
    const anIsNum = Number.isFinite(an);
    const bnIsNum = Number.isFinite(bn);
    if (anIsNum && bnIsNum) return an - bn;
    return String(a[0]).localeCompare(String(b[0]));
  });
};

const normalizeLabel = (str, max = 22) => {
  if (!str) return '';
  return str.length > max ? str.slice(0, max) + '...' : str;
};

const pickCount = (entries, key) => {
  const found = entries.find(([k]) => k === key);
  return found ? found[1] : 0;
};

const loadCsv = async (path) => {
  const res = await fetch(path);
  const text = await res.text();
  return Papa.parse(text, { header: true, skipEmptyLines: true }).data;
};

const createBar = (ctx, labels, data, label, color, stacked = false, indexAxis = 'x', showAllTicks = false) => {
  // Skip some ticks automatically when there are many labels to avoid overlap (e.g., years on mobile)
  const tickStep = labels.length > 8 ? Math.ceil(labels.length / 6) : 1;
  const isHorizontal = indexAxis === 'y';

  return new Chart(ctx, {
    type: 'bar',
    indexAxis,
    data: {
      labels,
      datasets: Array.isArray(data[0])
        ? data.map((dataset, i) => ({
            label: label[i],
            data: dataset,
            backgroundColor: i === 0 ? color[0] : color[1],
            borderColor: '#0f172a',
            borderWidth: 1.5,
            borderRadius: 6,
            maxBarThickness: 36,
          }))
        : [{
            label,
            data,
            backgroundColor: color,
            borderColor: '#0f172a',
            borderWidth: 1.5,
            borderRadius: 6,
            maxBarThickness: 36,
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      layout: { padding: { top: 10, left: isHorizontal ? 32 : 10, right: 16, bottom: isHorizontal ? 12 : 26 } },
      plugins: {
        legend: { labels: { color: '#f8fafc', font: { size: 14, weight: '700' } } },
        tooltip: {
          backgroundColor: '#111827',
          titleColor: '#f8fafc',
          bodyColor: '#e2e8f0',
          borderColor: '#1f2937',
          borderWidth: 1,
          callbacks: {
            label: (ctx) => `${ctx.dataset.label}: ${ctx.raw}`
          },
          titleFont: { size: 14, weight: '800' },
          bodyFont: { size: 14, weight: '700' }
        },
      },
      scales: {
        x: isHorizontal
          ? { stacked, ticks: { color: '#ffffff', precision:0, font: { size: 13, weight: '700' } }, grid: { color: '#1f2937' } }
          : {
              stacked,
              ticks: {
                color: '#e2e8f0',
                font: { size: 16, weight: '800' },
                autoSkip: false,
                padding: 12,
                callback: (_, idx) => (showAllTicks || idx % tickStep === 0 ? labels[idx] : '')
              },
              grid: { display: false }
            },
        y: isHorizontal
          ? {
              stacked,
              ticks: {
                color: '#e2e8f0',
                font: { size: 16, weight: '800' },
                autoSkip: false,
                padding: 6,
                callback: (_, idx) => labels[idx]
              },
              grid: { display: false }
            }
          : { stacked, ticks: { color: '#ffffff', precision:0, font: { size: 13, weight: '700' } }, grid: { color: '#1f2937' } }
      }
    }
  });
};

const createDoughnut = (ctx, labels, data, colors) => {
  return new Chart(ctx, {
    type: 'doughnut',
    data: { labels, datasets: [{ data, backgroundColor: colors, borderColor: '#0f172a', borderWidth: 2 }] },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { position: 'bottom', labels: { color: '#f8fafc', font: { size: 14, weight: '700' } } },
        tooltip: { 
          backgroundColor: '#111827',
          titleColor: '#f8fafc',
          bodyColor: '#e2e8f0',
          borderColor: '#1f2937',
          borderWidth: 1,
          callbacks: { label: (ctx) => `${ctx.label}: ${ctx.raw}` },
          titleFont: { size: 14, weight: '800' },
          bodyFont: { size: 14, weight: '700' }
        }
      },
      cutout: '55%'
    }
  });
};

const fillHighlights = (data) => {
  const box = document.getElementById('highlights');
  const topMovieYear = topEntry(countBy(data.moviesWatched, 'watched_year'));
  const topBookYear = topEntry(countBy(data.booksRead.filter(b => toNumber(b.read_year)), 'read_year'));
  const platform = topEntry(countBy(data.moviesToWatch, 'where_to_watch'));
  const grapeTypes = data.wineExperiences
    .flatMap(w => (w.wine_type || '').split(';').map(t => t.trim()).filter(Boolean))
    .map(type => ({ type }));
  const grape = topEntry(countBy(grapeTypes, 'type'));

  box.innerHTML = '';
  const lines = [
    topMovieYear ? `Ano mais cinéfilo: ${topMovieYear.key} (${topMovieYear.count} filmes)` : null,
    topBookYear ? `Ano mais leitor: ${topBookYear.key} (${topBookYear.count} livros)` : null,
    platform ? `Plataforma favorita para filmes a ver: ${platform.key}` : null,
    grape ? `Tipo de vinho mais degustado: ${grape.key}` : null,
    `Backlog: ${data.booksToRead.length} livros, ${data.moviesToWatch.length} filmes`,
  ].filter(Boolean);

  lines.forEach(line => {
    const span = document.createElement('span');
    span.innerHTML = '<strong>•</strong> ' + line;
    box.appendChild(span);
  });
};

const topEntry = (entries) => {
  if (!entries || !entries.length) return null;
  const sorted = entries.slice().sort((a,b) => b[1] - a[1]);
  return { key: sorted[0][0], count: sorted[0][1] };
};

const main = async () => {
  try {
    const data = await Promise.all(Object.values(csvFiles).map(loadCsv));
    const [
      moviesWatched,
      moviesToWatch,
      booksRead,
      booksToRead,
      documentaries,
      series,
      gamesBeaten,
      gamesAbandoned,
      wineExperiences
    ] = data;

    setCardValue('movies-watched', moviesWatched.length);
    setCardValue('movies-to-watch', moviesToWatch.length);
    setCardValue('books-read', booksRead.length);
    setCardValue('books-to-read', booksToRead.length);
    setCardValue('docs-watched', documentaries.length);
    setCardValue('series-watched', series.length);
    setCardValue('games-beaten', gamesBeaten.length);
    setCardValue('games-abandoned', gamesAbandoned.length);
    setCardValue('wine-experiences', wineExperiences.length);
    document.getElementById('last-updated').textContent = 'Atualizado agora';

    // Filmes por ano
    const moviesByYear = countBy(moviesWatched, 'watched_year');
    createBar(
      document.getElementById('moviesByYear'),
      moviesByYear.map(([y]) => y),
      moviesByYear.map(([,c]) => c),
      'Filmes',
      palette.purple,
      false,
      'y',
      true
    );

    // Diretores mais assistidos (top 8) + lista de filmes
    const directors = countBy(moviesWatched, 'director').sort((a,b) => b[1] - a[1]).slice(0,8);
    createBar(
      document.getElementById('directorsTop'),
      directors.map(([d]) => normalizeLabel(d, 18)),
      directors.map(([,c]) => c),
      'Filmes',
      palette.teal,
      false,
      'y',
      true
    );
    const directorsListBox = document.getElementById('directorsList');
    if (directorsListBox) {
      directorsListBox.innerHTML = '';
      const dirToMovies = moviesWatched.reduce((map, movie) => {
        const dir = (movie.director || '').trim();
        const title = (movie.title || '').trim();
        if (!dir || !title) return map;
        if (!map.has(dir)) map.set(dir, []);
        map.get(dir).push(title);
        return map;
      }, new Map());
      directors.forEach(([dir, count]) => {
        const item = document.createElement('span');
        const movies = dirToMovies.get(dir) || [];
        const limited = movies.slice(0, 6).map(t => normalizeLabel(t, 28)).join(', ');
        const more = movies.length > 6 ? '...' : '';
        item.innerHTML = `<strong>${dir}</strong> — ${count} filmes: ${limited}${more}`;
        directorsListBox.appendChild(item);
      });
    }

    // Livros por ano (ignora anos vazios)
    const booksWithYear = booksRead.filter(b => toNumber(b.read_year));
    const booksYearCount = countBy(booksWithYear, 'read_year');
    createBar(
      document.getElementById('booksByYear'),
      booksYearCount.map(([y]) => y),
      booksYearCount.map(([,c]) => c),
      'Livros',
      palette.cyan,
      false,
      'y',
      true
    );

    // Jogos zerados vs abandonados
    const allYears = new Set([
      ...gamesBeaten.map(g => g.year_played).filter(Boolean),
      ...gamesAbandoned.map(g => g.year_played).filter(Boolean),
    ]);
    const yearsSorted = Array.from(allYears).sort();
    const beatenCount = yearsSorted.map(y => gamesBeaten.filter(g => g.year_played === y).length);
    const abandonedCount = yearsSorted.map(y => gamesAbandoned.filter(g => g.year_played === y).length);
    createBar(
      document.getElementById('gamesByYear'),
      yearsSorted,
      [beatenCount, abandonedCount],
      ['Zerados', 'Abandonados'],
      [palette.teal, palette.amber],
      true,
      'y'
    );

    // Documentários e séries por ano
    const docs = countBy(documentaries, 'watched_year');
    const ser = countBy(series, 'watched_year');
    const dsYears = Array.from(new Set([...docs.map(([y]) => y), ...ser.map(([y]) => y)])).sort();
    const docData = dsYears.map(y => pickCount(docs, y));
    const seriesData = dsYears.map(y => pickCount(ser, y));
    createBar(
      document.getElementById('docsSeries'),
      dsYears,
      [docData, seriesData],
      ['Documentários', 'Séries'],
      [palette.pink, palette.lime],
      true,
      'y'
    );

    // Lista de filmes: onde assistir
    const platforms = countBy(moviesToWatch, 'where_to_watch');
    createBar(
      document.getElementById('watchlistPlatforms'),
      platforms.map(([p]) => normalizeLabel(p)),
      platforms.map(([,c]) => c),
      'Qtd',
      palette.amber,
      false,
      'y'
    );

    // Vinhos por tipo
    const wineTypes = [];
    wineExperiences.forEach(w => {
      const types = (w.wine_type || '').split(';').map(t => t.trim()).filter(Boolean);
      if (!types.length) types.push('Não informado');
      types.forEach(t => wineTypes.push({ type: t }));
    });
    const wineCounts = countBy(wineTypes, 'type');
    createDoughnut(
      document.getElementById('wineTypes'),
      wineCounts.map(([t]) => t),
      wineCounts.map(([,c]) => c),
      [palette.purple, palette.cyan, palette.amber, palette.teal, palette.pink, palette.lime]
    );

    // Livros futuros por gênero
    const genresRaw = [];
    booksToRead.forEach(b => {
      const genres = (b.genre || '').split('/').map(g => g.trim()).filter(Boolean);
      if (!genres.length) genresRaw.push({ genre: 'Sem gênero' });
      genres.forEach(g => genresRaw.push({ genre: g }));
    });
    const genreCounts = countBy(genresRaw, 'genre');
    createBar(
      document.getElementById('booksGenres'),
      genreCounts.map(([g]) => normalizeLabel(g)),
      genreCounts.map(([,c]) => c),
      'Livros',
      palette.slate,
      false,
      'y'
    );

    fillHighlights({
      moviesWatched,
      moviesToWatch,
      booksRead,
      booksToRead,
      documentaries,
      series,
      gamesBeaten,
      gamesAbandoned,
      wineExperiences
    });
  } catch (err) {
    console.error(err);
    alert('Erro ao carregar dados. Confira se abriu via servidor local.');
  }
};

main();
