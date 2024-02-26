# Nendo Plugin Import Core

<br>
<p align="left">
    <img src="https://okio.ai/docs/assets/nendo_core_logo.png" width="350" alt="nendo core">
</p>
<br>

<p align="left">
<a href="https://okio.ai" target="_blank">
    <img src="https://img.shields.io/website/https/okio.ai" alt="Website">
</a>
<a href="https://twitter.com/okio_ai" target="_blank">
    <img src="https://img.shields.io/twitter/url/https/twitter.com/okio_ai.svg?style=social&label=Follow%20%40okio_ai" alt="Twitter">
</a>
<a href="https://discord.gg/gaZMZKzScj" target="_blank">
    <img src="https://dcbadge.vercel.app/api/server/XpkUsjwXTp?compact=true&style=flat" alt="Discord">
</a>
</p>

---

A plugin for importing NendoTracks and NendoCollections from the web. Works with youtube links and direct downloads currently.

## Features

- Import tracks from youtube and other supported sites. 
- Directly import tracks from file links.

## Installation

```bash
pip install nendo-plugin-import-core
```

## Usage
```pycon
>>> from nendo import Nendo
>>> nd = Nendo(plugins=["nendo_plugin_import_core"])

>>> tracks = nd.plugins.import_core(links=["https://www.youtube.com/watch?v=6JYIGclVQdw"])
>>> tracks[0].play()
```

    