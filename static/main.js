    let currentPlaying = null;
    let lang = 'vi';
    let currentQuery = '';
    let offset = 0;
    let maxResults;
    let configLoaded = false;

    const i18n = {
      vi: {
        title: "📺 Trình phát YouTube FOSS NoGtube",
        now_playing: "🎬 Đang phát",
        searching: "⏳ Đang tìm kiếm...",
        placeholder: "Tìm kiếm video...",
        btn_search: "🔍",
        btn_more: "Tải lại...",
        opt_default: "Mặc định",
        opt_720p: "720p",
        opt_480p: "480p",
        theme_status: "Bảng màu: ",
        lang_status: "Ngôn ngữ: "
      },
      en: {
        title: "📺 NoGtube YouTube FOSS Player",
        now_playing: "🎬 Now Playing",
        searching: "⏳ Searching...",
        placeholder: "Search video...",
        btn_search: "🔍",
        btn_more: "Reload...",
        opt_default: "Default",
        opt_720p: "720p",
        opt_480p: "480p",
        theme_status: "Theme palatte: ",
        lang_status: "Language: "
      }
    };

    function setLang(l) {
      lang = l;

      document.querySelectorAll('[data-lang]').forEach(el => {
        const key = el.getAttribute('data-lang');
        if (i18n[lang] && i18n[lang][key]) {
          el.textContent = i18n[lang][key];
        }
      });

      document.getElementById("query").placeholder = i18n[lang].placeholder;

      const options = document.getElementById("quality").options;
      options[0].text = i18n[lang].opt_default;
      options[1].text = i18n[lang].opt_720p;
      options[2].text = i18n[lang].opt_480p;

      document.querySelector("button[onclick='startSearch()']").textContent = i18n[lang].btn_search;
      document.querySelector("#load-more button").textContent = i18n[lang].btn_more;
    }

    fetch("/static/config.json")
      .then(res => res.json())
      .then(data => {
        lang = data.lang || lang;
        maxResults = data.maxResults || 5;
        setLang(lang);
        theme = data.theme || "default-light";
        document.getElementById("theme-link").href = `/static/themes/${theme}.css`;
        document.getElementById("configinfo-theme").textContent = i18n[lang].theme_status + theme;
        document.getElementById("configinfo-lang").textContent = i18n[lang].lang_status + lang;
        configLoaded = true;
        console.log("✅ Config loaded:", data);
      })
      .catch(err => {
        console.warn("⚠️ Không thể load config.json, dùng mặc định.", err);
        maxResults = 5;
        setLang(lang);
        configLoaded = true;
      });

    function startSearch() {
      if (!configLoaded) {
        alert("🔄 Đang tải cấu hình, thử lại sau...");
        return;
      }

      currentQuery = document.getElementById("query").value.trim();
      offset = 0;
      document.getElementById("results").innerHTML = "";
      document.getElementById("player-container").style.display = "none";
      loadMore();
    }

    async function loadMore() {
      if (!currentQuery) return;
      console.log("🔢 maxResults =", maxResults);

      document.getElementById("loading").style.display = "block";
      const res = await fetch(`/search?q=${encodeURIComponent(currentQuery)}`);
      const videos = await res.json();

      const list = document.getElementById("results");
      document.getElementById("loading").style.display = "none";

      videos.slice(offset, offset + maxResults).forEach((video, index) => {
        const li = document.createElement("li");

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

      offset += maxResults;
    }

    function play(videoUrl, li) {
      const player = document.getElementById("player");
      const container = document.getElementById("player-container");
      const quality = document.getElementById("quality").value;

      if (currentPlaying) {
        currentPlaying.classList.remove("playing");
      }
      currentPlaying = li;
      currentPlaying.classList.add("playing");

      player.src = `/play?url=${encodeURIComponent(videoUrl)}&quality=${encodeURIComponent(quality)}`;
      player.load();
      player.play();
      container.style.display = "block";
    }
