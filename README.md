# Dans Alarmı music catalog

This repository serves music content only. The iOS source is in a separate private repository.

The app refreshes https://raw.githubusercontent.com/Enesurkan/dans-alarmi-music/main/catalog.json when its music picker opens or the user refreshes it. Changes to this repository's `main` branch do not require an App Store release once the remote-catalog-capable app is installed. GitHub/CDN caching can delay visibility by a few minutes.

## Add music

Use audio you have the rights to distribute. The included tracks are original instrumental compositions synthesized for Dans Alarmı, with no third-party recordings or samples. No general redistribution license is granted by this repository.

```sh
python3 Scripts/music_catalog.py add /path/to/song.wav --id unique-song-id --title 'Song name' --title-tr 'Parça adı' --genre Funk --bpm 104
python3 Scripts/music_catalog.py validate
git add catalog.json tracks
git commit -m 'Add new dance music'
git push origin main
```

Use `--pro` for a Pro track. MP3/M4A input requires `--duration` in seconds. Existing IDs must stay stable. Files are stored with a hash in the name; never replace the contents of a published filename. The script updates the catalog hash, byte count and revision. Keep old files for compatibility.

`catalog.json` schema version 1 includes localized titles, genre, BPM, duration, Pro access, relative file path, byte count and SHA-256. Maximum track size is 25 MB and maximum duration is 5 minutes. The iOS app verifies downloads, keeps them on the device for offline use, and retains a previous good catalog when refresh fails. Its six built-in fallback tracks remain available without a connection.

Catalog and audio changes are content updates. Changing the Swift client or adding new app capabilities still requires an app release. The catalog and audio are public; this repository must not contain tokens, app source or private user data.
