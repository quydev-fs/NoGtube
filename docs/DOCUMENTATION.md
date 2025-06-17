# Documentation for configuring / creating theme

## 1. Basics
- with users, I'm prepared a example config file (`example.config.json`). inside it contain:
    + `lang` key: for configuring language, it has 2 possible value - `"en"` (English) and `"vi"` (Vuetnamese).
    + `maxResults` key: for config the number of results will be displayed (careful, it is dangerous for setting this value high. youtube may block your IP)
    + `theme` key: I'm prepared 3 theme sets (default, nord, catppuccin) with 2 variants (dark, light). setting the theme by type the theme name + variant. here is the list:
        + default-dark
        + default-light
        + catppuccin-mocha (catppuccin dark)
        + catppuccin-latte (catppuccin light)
        + nord-dark (nord dark)
        + nord-snow (Nord's light varriant)
    + `port` key: for setting the web interface's listening port. with Non-rooted Amdroids, I'm recommend this value to be larger than 1024, for familiar, set it to 8080
    + `listeningIP` key: setting the server's interface. there's the possible value:
        + "127.0.0.1": only host can access
        + "0.0.0.0": all interface (include your device's IP (LAN access), 127.0.0.1 and all others)
        + your device's IP: LAN access only
- after setting all that follow your preferences, delete all comments (start with "//") copy it to `static/config.json` with overwrite mode.

- running by executing `python app.py`
## 2. For theme creators
- for theme creators, I'm prepared a template file (`theme-template.css`), customize it to your favorite pallete by modify any `color` and `background-color` attributes.
- after replace all the color inside that file, save it under your theme name (eg. `gruvbox-dark.css`) and move that file into `static/themes/`.
- for testing the new theme that you just created, modify the `static/config.json`'s theme key into your theme's filename without that `.css` file extension
- after testing completed, upload it to a github repo or creating a pull request with description is `"[theme submitting] + your theme's name"`
