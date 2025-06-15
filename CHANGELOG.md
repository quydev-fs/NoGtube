# 📦 Changelog

All notable changes to **NoGtube** will be documented in this file.  
This project follows **semver pre-release** (`alpha`, `beta`, etc.) while in early development.

---

## [v0.1.0-alpha.1] – 2025-06-15 • [Latest]

### ✨ Added
- JSON configuration via `static/config.json`
- `lang` key for dynamic i18n switching (`vi`, `en`)
- `maxResults` key synced across frontend and backend

### 🗑 Removed
- Dropped `audio only` mode (`bestaudio`) from UI – it might return in another project (SpotiFOSS?)

### 🔧 Internal
- Fully merged `nightly` branch into `main`
- i18n refactored to cover placeholders, buttons, and dropdowns
- Commit [`1ec7486`](https://github.com/quydev-fs/NoGtube/commit/1ec7486): merged config branch

> The first alpha of `v0.1.x` with real config support and improved UX.  
> _(A bit of a stretch — the `v0.0.x-alpha` series technically only lasted a day, but hey, it counts.)_

📄 [Compare changes](https://github.com/quydev-fs/NoGtube/compare/v0.0.1-alpha.1...v0.1.0-alpha.1)

---

## [v0.0.1-alpha.1] – 2025-06-14

### 🚧 Initial draft
- HTML5-based YouTube frontend using yt-dlp
- Minimal layout with search + video playback
- Early Termux/PWA compatibility
