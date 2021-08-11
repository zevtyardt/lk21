![title](https://drive.google.com/uc?export=view&id=1kNTbXCojFechk1MKt1BPwVwoOWqE3kUW)

<br/>
<div align="center">
<strong> unduh anime dan film subtitle Indonesia </strong>
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
| 2 | bypass_antfiles | `antfiles.com/?dl=[id]` |
| 3 | bypass_fembed | `layarkacaxxi.icu/[id]` |
|  |  | `fembed.com/[id]` |
|  |  | `femax20.com/[id]` |
|  |  | `www.naniplay.nanime.in/file/[id]` |
|  |  | `www.naniplay.nanime.biz/file/[id]` |
|  |  | `www.naniplay.com/file/[id]` |
|  |  | `naniplay.nanime.in/file/[id]` |
|  |  | `naniplay.nanime.biz/file/[id]` |
|  |  | `naniplay.com/file/[id]` |
| 4 | bypass_filesIm | `files.im/[id]` |
|  |  | `racaty.net/[id]` |
|  |  | `racaty.com/[id]` |
|  |  | `hxfile.co/[id]` |
| 5 | bypass_kotakanimeid | `kotakanimeid.com/videoku/dl/?link=[id]` |
|  |  | `kotakanimeid.com/url/[id]` |
| 6 | bypass_letsupload | `letsupload.io/[id]/[id]` |
|  |  | `letsupload.io/[id]?pt=[id]` |
|  |  | `letsupload.co/[id]/[id]` |
|  |  | `letsupload.co/[id]?pt=[id]` |
| 7 | bypass_linkpoi | `linkpoi.me/[id]` |
| 8 | bypass_mediafire | `mediafire.com/file/[id]` |
|  |  | `mediafire.com/file/[id]/file` |
|  |  | `www.mediafire.com/file/[id]` |
|  |  | `www.mediafire.com/file/[id]/file` |
| 9 | bypass_mirrored | `mirrored.to/files/[id]` |
|  |  | `mirrored.to/mirstats.php[id]` |
|  |  | `www.mirrored.to/files/[id]` |
|  |  | `www.mirrored.to/mirstats.php[id]` |
| 10 | bypass_ouo | `ouo.press/[id]` |
|  |  | `ouo.io/[id]` |
| 11 | bypass_redirect | `link.zonawibu.cc/redirect.php?go=[id]` |
|  |  | `player.zafkiel.net/blogger.php?yuzu=[id]` |
|  |  | `bit.ly/[id]` |
| 12 | bypass_reupload | `reupload.org/[id]` |
| 13 | bypass_sbembed | `sbembed.com/[id].html` |
|  |  | `streamsb.net/[id].html` |
| 14 | bypass_streamtape | `streamtape.com/v/[id]/[id]` |
| 15 | bypass_uservideo | `uservideo.xyz/file/[id]` |
|  |  | `www.uservideo.xyz/file/[id]` |
| 16 | bypass_zippyshare | `www[id].zippyshare.com/v/[id]/file.html` |

# Daftar Website
| no | name | site | tag | import |
|:---:|:---:|:---:|:---:|:---:|
| 1 | Anibatch | `https://o.anibatch.me/` | anime | `lk21.extractors.anibatch.Anibatch` |
| 2 | Anikyojin | `https://anikyojin.net` | anime | `lk21.extractors.anikyojin.Anikyojin` |
| 3 | Animeindo | `https://animeindo.asia` | anime | `lk21.extractors.animeindo.Animeindo` |
| 4 | Anitoki | `https://www.anitoki.com` | anime | `lk21.extractors.anitoki.Anitoki` |
| 5 | Bbcsjav | `https://bbcsjav.com` | JAV | `lk21.extractors.bbcsjav.Bbcsjav` |
| 6 | Dramaindo | `https://dramaindo.cn` | anime, movie | `lk21.extractors.dramaindo.Dramaindo` |
| 7 | Drivenime | `https://drivenime.com` | anime | `lk21.extractors.drivenime.Drivenime` |
| 8 | KDramaindo | `https://k.dramaindo.my.id` | movie | `lk21.extractors.kdramaindo.KDramaindo` |
| 9 | Kusonime | `https://kusonime.com` | anime | `lk21.extractors.kusonime.Kusonime` |
| 10 | Layarkaca21 | `http://149.56.24.226/` | movie | `lk21.extractors.layarkaca21.Layarkaca21` |
| 11 | Melongmovie | `https://melongmovie.net` | movie | `lk21.extractors.melongmovie.Melongmovie` |
| 12 | Meownime | `https://meownime.moe` | anime | `lk21.extractors.meownime.Meownime` |
| 13 | Nekopoi | `http://nekopoi.care` | hentai, JAV | `lk21.extractors.nekopoi.Nekopoi` |
| 14 | Nontonanimeid | `https://nontonanimeid.com` | None | `lk21.extractors.nontonanimeid.Nontonanimeid` |
| 15 | Oploverz | `https://www.oploverz.in` | anime | `lk21.extractors.oploverz.Oploverz` |
| 16 | Otakudesu | `https://otakudesu.moe` | anime | `lk21.extractors.otakudesu.Otakudesu` |
| 17 | Riie | `https://riie.jp` | anime | `lk21.extractors.riie.Riie` |
| 18 | Samehadaku | `https://samehadaku.vip` | anime | `lk21.extractors.samehadaku.Samehadaku` |
| 19 | Wibudesu | `https://wibudesu.com` | anime | `lk21.extractors.wibudesu.Wibudesu` |
| 20 | Zonawibu | `https://asuka.zonawibu.net` | anime | `lk21.extractors.zonawibu.Zonawibu` |

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
- Versi 1.6.2
  - Menambahkan bypass baru
    - `kotakanimeid.com`
    - `mirrored.to`
    - `reupload.org`
    - `racaty.com`

<a href="/CHANGELOG.md">baca lebih lengkap</a>

<i> Bantu saya memperbaiki dokumentasi module </i>

-------

lk21 is licensed under MIT License
