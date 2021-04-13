![title](https://drive.google.com/uc?export=view&id=1kNTbXCojFechk1MKt1BPwVwoOWqE3kUW)

<br/>
<div align="center">
<strong> cari anime dan film subtitle Indonesia </strong>
</div>

-------

Pernah terpikir untuk menonton film atau anime di website secara gratis tapi selalu direpotkan dengan iklan. atau jika ingin mendownload harus melalui shortlink ini itu, tenang melalui tool ini anda dapat dengan mudah mencari link download anime atau film yang anda inginkan tanpa harus terganggu oleh iklan dan shortlink.

# instalasi
Menggunakan python package manager
```bash
python -m pip install lk21
```

bagaimana jika terdapat versi baru? tidak perlu khawatir `lk21` sudah dilengkapi dengan pemberitahuan yang akan muncul setelah program selesai dijalankan. Kamu bisa langsung memperbaharui menggunakan perintah berikut
```bash
python -m pip install --upgrade lk21
```

# Cara Penggunaan
Melalui terminal secara langsung, sebagai contoh saya akan mencari film `insurgent`.

```bash
$ lk21 insurgent
Mencari 'insurgent' -> 149.56.24.226 halaman 1
Total item terkumpul: 1 item dari total 1 halaman
Mengekstrak link unduhan: insurgent-2015
? Pilih: (Use arrow keys)
» 1. Fembed
  2. 1fichier
  3. Cloudvideo
  4. Uptobox
  5. Mirrorace
  6. Go4up
  7. Embedupload
```

Sangat mudah bukan, untuk membuat user input yang <i>user friendly</i> saya menggunakan library [questionary](https://pypi.org/project/questionary).

# Bypass situs unduhan
| no | funcname | pattern |
|:---:|:---:|:---:|
| 1 | bypass_anonfiles | `anonfiles.com/[id]` |
| 2 | bypass_fembed | `layarkacaxxi.icu/f/[id]` |
|  |  | `www.naniplay.nanime.in/file/[id]` |
|  |  | `www.naniplay.nanime.biz/file/[id]` |
|  |  | `www.naniplay.com/file/[id]` |
|  |  | `naniplay.nanime.in/file/[id]` |
|  |  | `naniplay.nanime.biz/file/[id]` |
|  |  | `naniplay.com/file/[id]` |
| 3 | bypass_filesIm | `files.im/[id]` |
|  |  | `racaty.net/[id]` |
|  |  | `hxfile.co/[id]` |
| 4 | bypass_letsupload | `letsupload.[id]/[id]` |
|  |  | `letsupload.[id]?pt=[id]` |
| 5 | bypass_linkpoi | `uservideo.xyz/file/[id]` |
|  |  | `www.uservideo.xyz/file/[id]` |
|  |  | `linkpoi.me/[id]` |
| 6 | bypass_mediafire | `mediafire.com/file/[id]` |
|  |  | `mediafire.com/file/[id]/file` |
|  |  | `www.mediafire.com/file/[id]` |
|  |  | `www.mediafire.com/file/[id]/file` |
| 7 | bypass_ouo | `ouo.press/[id]` |
|  |  | `ouo.io/[id]` |
| 8 | bypass_redirect | `link.zonawibu.cc/redirect.php?go=[id]` |
|  |  | `player.zafkiel.net/blogger.php?yuzu=[id]` |
|  |  | `bit.ly/[id]` |

# Daftar Website
| no | name | site | tag |
|:---:|:---:|:---:|:---:|
| 1 | Anikyojin | `https://anikyojin.net` | anime |
| 2 | Animeindo | `https://animeindo.asia` | anime |
| 3 | Anitoki | `https://www.anitoki.com` | anime |
| 4 | Anibatch | `https://o.anibatch.me/` | anime |
| 5 | Asuka_Zonawibu | `https://asuka.zonawibu.net` | anime |
| 6 | Drivenime | `https://drivenime.com` | anime |
| 7 | Dramaindo | `https://k.dramaindo.my.id` | movie |
| 8 | Kuramanime | `https://kuramanime.com` | None |
| 9 | Layarkaca21 | `http://149.56.24.226/` | movie |
| 10 | Kusonime | `https://kusonime.com` | anime |
| 11 | Melongmovie | `https://melongmovie.net` | movie |
| 12 | Meownime | `https://meownime.moe` | anime |
| 13 | Nekonime | `https://nekonime.stream` | anime |
| 14 | Nekopoi | `https://nekopoi.care` | anime |
| 15 | Oploverz | `https://www.oploverz.in` | anime |
| 16 | Otakudesu | `https://otakudesu.moe` | anime |
| 17 | Samehadaku | `https://samehadaku.vip` | anime |
| 18 | Riie | `https://riie.jp` | anime |
| 19 | Wibudesu | `https://wibudesu.com` | anime |
| 20 | Bbcsjav | `https://bbcsjav.com` | JAV |

# Library
lk21 juga dapat digunakan sebagai library. Artinya, Anda dapat mengimpornya ke aplikasi Anda sendiri.

```python
from lk21.extractors.anibatch import Anibatch

scraper = Anibatch()
result = scraper.search("non non biyori")
# [{'title': 'Non Non Biyori Season 2', 'id': 'non-non-biyori-season-2'}, {'title': 'Non Non Biyori Movie: Vacation BD', 'id': 'non-non-biyori-movie-vacation-bd'}, {'title': 'Non Non Biyori Season 1', 'id': 'non-non-biyori-season-1'}]

scraper.extract(result[0])
# {'extractor': 'Anibatch', 'url': 'https://o.anibatch.me//non-non-biyori-season-2', 'host': 'https://o.anibatch.me/', 'id': 'non-non-biyori-season-2', 'metadata': {'image': 'https://o.anibatch.me/wp-content/uploads/2020/09/Non-Non-Biyori-S2-min-750x410.jpg', 'judul': 'Non Non Biyori Season 2', 'judul_alternatif': 'Non Non Biyori Repeat', 'tipe': 'TV', 'status': 'Finished Airing', 'musim': 'Summer 2015', 'studio': 'Silver Link.', 'genre': ['Comedy', 'School', 'Seinen', 'Slice of Life'], 'durasi': '23 min. per ep.', 'score': '8.19', 'sinopsis': 'Jauh dari hiruk pikuk kehidupan perkotaan, dan hanya dengan satu toko permen dan rute bus untuk namanya, pedesaan Asahigaoka jelas bukan tempat untuk semua orang. Meski demikian, anak-anak desa masih bisa dengan ceria menghabiskan hari-harinya menjelajahi dan bersenang-senang di alam liar di sekitar mereka. Salah satu anak tersebut, Renge Miyauchi, yang termuda dari grup, menantikan upacara masuk tahun ajaran mendatang, menandakan dia masuk ke kelas satu dan awal kehidupan sekolah dasarnya. Menghadiri satu-satunya sekolah di kota, Renge dan teman-temannya, siswa kelas tujuh Natsumi Koshigaya dan saudara perempuan kelas delapannya Komari, memanfaatkan gaya hidup pedesaan mereka, bermain dan belajar setiap hari.'}, 'download': [{'key': 'Season 2 — Non Non Biyori BD Batch AniBatch', 'value': [{'key': '720p', 'value': [{'key': 'Google Drive', 'value': 'https://drive.google.com/file/d/1HAxvReTEhUw7lbFNmXxzvzsR-O2zdplW/view?usp=sharing'}, {'key': 'Google Sharer', 'value': 'https://acefile.co/f/25305243/meownime-moe_nn_byori_s2_-_720p-rar'}, {'key': 'Files.im', 'value': 'https://files.im/dle2y6gptyqf'}, {'key': 'Uptobox', 'value': 'https://uptobox.com/ag4cr12mon1u'}]}]}]}
```

atau digunakan untuk melewati situs unduhan

```python
import lk21

bypasser = lk21.Bypass()
bypasser.bypass_url("https://letsupload.io/49FA1/Otakudesu_ShoShuuRyo--09_360p.mp4")
# 'https://fs4.cdnrobot.xyz/49FA1/Shahid4U.Com.Riverdale.US.S02E17.720p.BluRay.mp4?download_token=191b7c96508b510fbfb7ac8ddb6a33d906fd473d0c00274a3f861407f4171130'
```

# Changelog
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


<i> Bantu saya memperbaiki dokumentasi module </i>

-------

lk21 is licemsed under MIT License
