# Changelog
- versi 1.5.17
  - Menambahkan bypass baru
    - `letsupload.co`

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
