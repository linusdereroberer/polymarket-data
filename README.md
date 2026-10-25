# Private prediction-market data snapshot

Status: **complete**. Capture started 2026-10-24T23:39:28Z; completed 2026-10-25T01:23:15Z.

15,908 files, 51,604,621,728 original bytes, 75 ZIP archives, 42,096,779,271 uploaded bytes. All data is in GitHub Release assets, never Git LFS. This repository is private.

## Contents and snapshot semantics

- `lake/`: Polymarket datasets except Hugging Face trades, scratch, and secret-pattern filenames.
- `lake-kalshi/`, `lake-opinion/`, `lake-limitless/`, `lake-hyperliquid/`, `lake-predictit/`, `lake-metaculus/`: venue datasets.
- `data/`: recorder/dashboard data and stream journals. SQLite databases are independent consistent SQLite backup-API snapshots, each checked with `PRAGMA quick_check`; WAL/SHM files are represented by the backup and excluded. This is not a single atomic snapshot across all files or both databases.
- The file list is frozen at task start; immutable files are checked for changes when read. Append-only logs/journals are captured as bounded byte prefixes at individual read times. A live Zstandard journal can end with an unfinished frame, matching the recorder's existing streaming format; recover complete lines with a streaming Zstandard reader.

## Restore

Requires Python 3.11+, authenticated GitHub CLI (`gh auth login`) with access to this private repository, and enough disk for restored data plus one archive and a 12 GiB reserve. Download the repository's metadata (or `gh repo clone linusdereroberer/polymarket-data`), then:

```powershell
./restore.ps1 -Destination C:/Data/polymarket-restored
```

```bash
bash restore.sh /path/to/polymarket-restored
```

Choose an empty destination. Both scripts call the included standard-library `restore.py`; it downloads one release asset at a time with `gh`, checks archive SHA-256 and size, extracts only manifest-listed members, writes split members at their original byte offsets, verifies member and final whole-file hashes, then removes the downloaded archive. Files return to their original relative folder layout. No separate manual concatenation is needed. A failed restore leaves its output for inspection; retry into a fresh empty directory.

Optional subset test: `python restore.py --destination test-output --archives data-0001.zip data-0002.zip`. A partial selection verifies each included part and any whole files fully represented; it is not a complete restore.

## Exclusions and secret scan

`MANIFEST.json` records every included file's path, byte count, SHA-256, scan mode, and archive/member/offset mapping, plus exact excluded paths and reasons. Exclusions: `lake/trades/`, `lake/tmp*/`, `lake/jobs/`, `*.claim`, `*.tmp`, `duckdb_temp_storage_*`, `.env*`, `*.pem`, and any path component containing `key` or `token`. The last rule intentionally excludes public-data paths such as `lake/chain/token_moves/`. No files under the home `.kalshi` directory are traversed. Links are excluded.

Before upload, selected bytes are scanned for private-key headers, GitHub/OpenAI/AWS credential formats, Authorization Bearer values, and long API-key/access-token/client-secret assignments. Parquet text/binary fields (including nested values) and Zstandard contents are also decoded and scanned. SQLite snapshots are byte-scanned; binary DuckDB contents receive a raw-byte scan, not full logical decoding. This is an obvious-secret pattern check, not a proof that no arbitrary unknown secret exists. Matching or undecodable files are withheld and recorded without publishing matched values.

## Archives

| Archive | Dataset root | Uploaded bytes | Members |
|---|---|---:|---:|
| data-0001.zip | `lake-metaculus/` | 6,544,769 | 1 |
| data-0002.zip | `lake-predictit/` | 2,526,820 | 94 |
| data-0003.zip | `lake-limitless/` | 239,098,002 | 1214 |
| data-0004.zip | `lake-hyperliquid/` | 122,335,008 | 558 |
| data-0005.zip | `lake-opinion/` | 795,593,730 | 283 |
| data-0006.zip | `lake-opinion/` | 191,755,562 | 1469 |
| data-0007.zip | `data/` | 780,508,760 | 341 |
| data-0008.zip | `data/` | 647,191,296 | 31 |
| data-0009.zip | `data/` | 316,087,112 | 123 |
| data-0010.zip | `lake-kalshi/` | 795,313,422 | 1724 |
| data-0011.zip | `lake-kalshi/` | 787,248,688 | 134 |
| data-0012.zip | `lake-kalshi/` | 799,226,640 | 46 |
| data-0013.zip | `lake-kalshi/` | 797,103,169 | 39 |
| data-0014.zip | `lake-kalshi/` | 784,346,083 | 30 |
| data-0015.zip | `lake-kalshi/` | 767,978,912 | 26 |
| data-0016.zip | `lake-limitless/` | 9,433,322 | 19 |
| data-0017.zip | `lake-opinion/` | 18,562,683 | 8 |
| data-0018.zip | `lake-kalshi/` | 753,217,321 | 13 |
| data-0019.zip | `lake-kalshi/` | 745,581,122 | 11 |
| data-0020.zip | `lake-kalshi/` | 795,918,323 | 13 |
| data-0021.zip | `lake-kalshi/` | 759,321,916 | 13 |
| data-0022.zip | `lake-kalshi/` | 760,377,890 | 13 |
| data-0023.zip | `lake-kalshi/` | 776,114,916 | 14 |
| data-0024.zip | `lake-kalshi/` | 791,215,039 | 14 |
| data-0025.zip | `lake-kalshi/` | 802,981,011 | 11 |
| data-0026.zip | `data/` | 269,981,242 | 1 |
| data-0027.zip | `data/` | 46,084,380 | 1 |
| data-0028.zip | `data/` | 98,132,353 | 1 |
| data-0029.zip | `data/` | 84,473,375 | 1 |
| data-0030.zip | `data/` | 87,251,264 | 1 |
| data-0031.zip | `data/` | 367,368,145 | 1 |
| data-0032.zip | `data/` | 126,375,268 | 1 |
| data-0033.zip | `data/` | 120,283,526 | 1 |
| data-0034.zip | `data/` | 146,799,134 | 1 |
| data-0035.zip | `data/` | 51,953,620 | 1 |
| data-0036.zip | `data/` | 151,254,049 | 1 |
| data-0037.zip | `data/` | 291,710,214 | 1 |
| data-0038.zip | `data/` | 23,693,143 | 1 |
| data-0039.zip | `lake-kalshi/` | 747,963,793 | 10 |
| data-0040.zip | `lake-kalshi/` | 761,982,071 | 9 |
| data-0041.zip | `lake-kalshi/` | 782,593,322 | 8 |
| data-0042.zip | `lake-kalshi/` | 799,336,297 | 15 |
| data-0043.zip | `lake-kalshi/` | 794,122,619 | 4052 |
| data-0044.zip | `lake/` | 697,375,331 | 829 |
| data-0045.zip | `lake/` | 791,609,268 | 60 |
| data-0046.zip | `lake/` | 794,463,256 | 28 |
| data-0047.zip | `lake/` | 804,593,605 | 57 |
| data-0048.zip | `lake/` | 297,218,964 | 40 |
| data-0049.zip | `lake/` | 805,306,732 | 2 |
| data-0050.zip | `lake/` | 805,306,580 | 1 |
| data-0051.zip | `lake/` | 805,306,580 | 1 |
| data-0052.zip | `lake/` | 805,306,580 | 1 |
| data-0053.zip | `lake/` | 726,289,220 | 2 |
| data-0054.zip | `lake/` | 176,211,246 | 1 |
| data-0055.zip | `lake/` | 795,085,375 | 42 |
| data-0056.zip | `lake/` | 804,397,070 | 358 |
| data-0057.zip | `lake/` | 801,608,172 | 1859 |
| data-0058.zip | `lake/` | 576,602,247 | 1329 |
| data-0059.zip | `lake/` | 371,723,336 | 25 |
| data-0060.zip | `lake/` | 735,912,933 | 277 |
| data-0061.zip | `lake/` | 608,825,054 | 2 |
| data-0062.zip | `lake/` | 797,353,324 | 4 |
| data-0063.zip | `lake/` | 763,802,435 | 8 |
| data-0064.zip | `lake/` | 768,491,291 | 8 |
| data-0065.zip | `lake/` | 734,048,657 | 8 |
| data-0066.zip | `lake/` | 797,848,239 | 9 |
| data-0067.zip | `lake/` | 737,837,561 | 8 |
| data-0068.zip | `lake/` | 721,555,957 | 8 |
| data-0069.zip | `lake/` | 748,070,471 | 8 |
| data-0070.zip | `lake/` | 736,640,582 | 10 |
| data-0071.zip | `lake/` | 717,914,267 | 282 |
| data-0072.zip | `lake/` | 372,391,896 | 303 |
| data-0073.zip | `lake/` | 805,303,119 | 4 |
| data-0074.zip | `lake/` | 805,306,580 | 1 |
| data-0075.zip | `lake/` | 590,134,012 | 2 |

Each archive is below 1.9 GiB. Large files are split into manifest-addressed byte parts; archives never need to be concatenated. GitHub asset sizes and SHA-256 digests were verified after upload.
