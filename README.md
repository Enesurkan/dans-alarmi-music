# Dans Alarmı music catalog

This repository serves music content only. The iOS source is in a separate private repository.

The app refreshes https://raw.githubusercontent.com/Enesurkan/dans-alarmi-music/main/catalog.json when its music picker opens or the user refreshes it. Changes to this repository's `main` branch do not require an App Store release once the remote-catalog-capable app is installed. GitHub/CDN caching can delay visibility by a few minutes.

## Publishing workflow

This is the public distribution mirror. The canonical content is the `MusicCatalog/` directory of the private `Enesurkan/dans-alarmi` repository. Add or update audio there with `Scripts/music_catalog.py`, then push the app repository's `main` branch. Its GitHub Actions workflow validates the files and synchronizes this repository's `main` branch automatically. The app fetches the resulting catalog without an App Store update.

The original eight tracks are instrumental compositions synthesized for Dans Alarmı, with no third-party recordings or samples; no general redistribution license is granted for those original tracks. The Kevin MacLeod and Sascha Ende recordings added in October 2026 are separately licensed under CC BY 4.0. See [ATTRIBUTIONS.md](ATTRIBUTIONS.md) for their credits, source links, license and redistribution permissions. The original-track restriction does not apply to these CC BY recordings. New contributions must have the necessary distribution rights.

Do not edit this mirror independently; later synchronization uses the private app repository as its source. Old versioned audio files are retained for compatibility.

`catalog.json` schema version 1 includes localized titles, genre, BPM, duration, Pro access, relative file path, byte count and SHA-256. Maximum track size is 25 MB and maximum duration is 5 minutes. The iOS app verifies downloads, keeps them on the device for offline use, and retains a previous good catalog when refresh fails. Its six built-in fallback tracks remain available without a connection.

Catalog and audio changes are content updates. Changing the Swift client or adding new app capabilities still requires an app release. The catalog and audio are public; this repository must not contain tokens, app source or private user data.
