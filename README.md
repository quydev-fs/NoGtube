# 📺 NoGtube - FOSS YouTube Player

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
![Status](https://img.shields.io/badge/status-stable-green)
![Python](https://img.shields.io/badge/python-3.7%2B-blue)
![yt-dlp](https://img.shields.io/badge/powered%20by-yt--dlp-yellow)
[![nightly](https://img.shields.io/badge/branch-nightly-blueviolet)](https://github.com/quydev-fs/NoGtube/tree/nightly)

**NoGtube** is a simple, lightweight and privacy-friendly YouTube player powered by Flask + yt-dlp.

No ads, no tracking, no bloat. Just search → click → play.

> 💡 Designed for devs, tinkerers, minimalist users and offline-friendly environments.

---

## 🚀 Features

- 🔍 YouTube search via `yt-dlp`
- 🎬 Video streaming in browser
- 🖼️ Thumbnail previews
- 🌐 Pure HTML UI (no frontend framework)
- 🛠 Configurable via `config.json`
- 🌍 Language support: English (`en`), Vietnamese (`vi`)

---

## ⚙️ Configuration

Edit `static/config.json`:

```json
{
  "lang": "en", // or "vi" for Vietnamese
  "maxResults": 7
}
```

## Setup
```bash
git clone https://github.com/quydev-fs/NoGtube
cd NoGtube
pip install -r requirements.txt
```
## Run
- after configuring NoGtube, run this to start the server:
```bash
python app.py 
```
## Another Branch?
- that `nightly` branch is my development branch. if you want to try, just running this command after clone and cd:
```bash
git checkout nightly
```

# Contributor guidelines

Contributions are welcome — whether it's a bug fix, a new feature, or just improving the documentation.

### 🧩 What you can help with

- Fixing bugs or edge cases
- Improving UI or internationalization (`i18n`)
- Adding new search sources / streaming backends
- Refactoring or simplifying code
- Expanding `config.json` support

## Remember
- Keep PRs focused & minimal

- Mention what you changed and why

- Use English or Vietnamese in commits

- Screenshots/GIFs welcome for UI changes

- Don't worry if it's not perfect — we’ll work it out together 😎
