# Changelog
- Versi 1.6.2
  - Menambahkan bypass baru
    - `kotakanimeid.com`
    - `mirrored.to`
    - `reupload.org`
    - `racaty.com`

- Versi 1.6.0
  - Menambahkan opsi mencari disemua ekstraktor
    - `-a`, `--all`
  - Menambahkan bypass baru
    - `antfiles.com`
  - Memperbaiki bypass `streamtape`

- Versi 1.5.61
  - Menambahkan ekstraktor baru
    - `lk21.extractors.dramaindo.Dramaindo`
  - Mengganti nama ekstraktor
    - `lk21.extractors.dramaindo.Dramaindo` menjadi `lk21.extractors.kdramaindo.KDramaindo`
  - menambahkan bypass baru
    - `uservideo.xyz`

- Versi 1.5.41
  - Mengembalikan algoritma lama bypass zippyshare

- Versi 1.5.34
  - Menambahkan bypass baru
    - `sbembed.com`
    - `streamtape.com`
    - `fembed.com`
    - `femax20.com`

- Versi 1.5.31
  - Nonaktifkan sementara fungsi bypass `zippyshare`. alasan terdapat perubahan algoritma
  - Perbaikan bug
  - Menambahkan extractor baru
    - `lk21.extractors.bbcsjav.Bbcsjav`

- Versi 1.5.23
  - Menambahkan 2 bypass baru
    - `bit.ly`
    - `ouo.io`

- Versi 1.5.20
  - Mengganti algoritma bypass zippyshare
  - Perbaikan bug

- Versi 1.5.17
  - Menambahkan bypass baru
    - `letsupload.co`
    - `anonfiles.com`
  - Refactoring code

- Versi 1.5.13
  - Menambahkan 3 bypass baru
    - `racaty.net`, `files.im`, `hxfile.co`
  - Menambahkan 2 ekstraktor baru
    - `lk21.extractors.dramaindo`
    - `lk21.extractors.meownime`
  - Fix error: <i>name 'os' is not defined</i>

- Versi 1.5.8
  - Memperbaiki masalah pada argument `--json` dan `--json-dump` sekarang anda dapat mengekstrak seluruh link unduhan tanpa terkecuali
  - Menambahkan ekstraktor baru `lk21.extractors.Anitoki`

- Versi 1.5.1
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
