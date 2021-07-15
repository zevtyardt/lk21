# Changelog
- versi 1.6
  - Menambahkan opsi mencari disemua ekstraktor
    - `-a`, `--all`
  - Menambahkan bypass baru
    - `antfiles.com`
  - Memperbaiki bypass `streamtape`

- versi 1.5.61
  - Menambahkan ekstraktor baru
    - `lk21.extractors.dramaindo.Dramaindo`
  - Mengganti nama ekstraktor
    - `lk21.extractors.dramaindo.Dramaindo` menjadi `lk21.extractors.kdramaindo.KDramaindo`
  - menambahkan bypass baru
    - `uservideo.xyz`

- versi 1.5.41
  - Mengembalikan algoritma lama bypass zippyshare

- versi 1.5.34
  - Menambahkan bypass baru
    - `sbembed.com`
    - `streamtape.com`
    - `fembed.com`
    - `femax20.com`

- versi 1.5.31
  - Nonaktifkan sementara fungsi bypass `zippyshare`. alasan terdapat perubahan algoritma
  - Perbaikan bug
  - Menambahkan extractor baru
    - `lk21.extractors.bbcsjav.Bbcsjav`

- versi 1.5.23
  - Menambahkan 2 bypass baru
    - `bit.ly`
    - `ouo.io`

- versi 1.5.20
  - Mengganti algoritma bypass zippyshare
  - Perbaikan bug

- versi 1.5.17
  - Menambahkan bypass baru
    - `letsupload.co`
    - `anonfiles.com`
  - Refactoring code

- versi 1.5.13
  - Menambahkan 3 bypass baru
    - `racaty.net`, `files.im`, `hxfile.co`
  - Menambahkan 2 ekstraktor baru
    - `lk21.extractors.dramaindo`
    - `lk21.extractors.meownime`
  - Fix error: <i>name 'os' is not defined</i>

- versi 1.5.8
  - Memperbaiki masalah pada argument `--json` dan `--json-dump` sekarang anda dapat mengekstrak seluruh link unduhan tanpa terkecuali
  - Menambahkan ekstraktor baru `lk21.extractors.Anitoki`

- versi 1.5.1
  - Menambahkan Changelog ke dalam README.md
  - Mengubah fungsi `extract` menjadi 2 bagian
    - `extract_meta` mengambil metadata dari halaman web
    - `extract_data` mengambil link unduhan dari halaman web
    Sedangkan fungsi `extract` akan mengambil metadata dan link unduhan dari halaman web
  - Menambahkan proxy \
    Beberapa website tidak dapat diakses tanpa menggunakan proxy/VPN. Anda dapat menambahkan proxy manual melalui argument `--proxy` dengan format `IP:PORT` atau `--skip-proxy` jika sudah menggunakan layanan proxy pihak ketiga
  - Mengganti beberapa host
    - melongmovie menjadi `melongmovie.net`
    - otakudesu menjadi `otakudesu.moe`
