let currentPlaying = null; let lang = 'vi'; let currentQuery = ''; let offset = 0; let maxResults = 5;

const i18n = { vi: { title: "📺 Trình phát YouTube FOSS", now_playing: "🎬 Đang phát", searching: "⏳ Đang tìm kiếm..." }, en: { title: "📺 YouTube FOSS Player", now_playing: "🎬 Now Playing", searching: "⏳ Searching..." } };

function setLang(l) { lang = l; document.querySelectorAll('[data-lang]').forEach(el => { const key = el.getAttribute('data-lang'); if (i18n[lang] && i18n[lang][key]) { el.textContent = i18n[lang][key]; } }); }

function startSearch() { currentQuery = document.getElementById("query").value.trim(); offset = 0; document.getElementById("results").innerHTML = ""; document.getElementById("player-container").style.display = "none"; loadMore(); }

async function loadMore() { if (!currentQuery) return; document.getElementById("loading").style.display = "block";

const res = await fetch(/search?q=${encodeURIComponent(currentQuery)}); const videos = await res.json();

const list = document.getElementById("results"); document.getElementById("loading").style.display = "none";

videos.slice(offset, offset + maxResults).forEach((video, index) => { const li = document.createElement("li");

const thumb = document.createElement("img");
thumb.src = `https://i.ytimg.com/vi/${video.url.split('v=')[1]}/hqdefault.jpg`;
thumb.className = "thumbnail";

const title = document.createElement("div");
title.textContent = video.title;
title.className = "title";
title.onclick = () => play(video.url, li);

li.appendChild(thumb);
li.appendChild(title);
list.appendChild(li);

});

offset += maxResults; }

function play(videoUrl, li) { const player = document.getElementById("player"); const container = document.getElementById("player-container"); const quality = document.getElementById("quality").value;

if (currentPlaying) { currentPlaying.classList.remove("playing"); } currentPlaying = li; currentPlaying.classList.add("playing");

player.src = /play?url=${encodeURIComponent(videoUrl)}&quality=${encodeURIComponent(quality)}; player.load(); player.play(); container.style.display = "block"; }

setLang(lang);

