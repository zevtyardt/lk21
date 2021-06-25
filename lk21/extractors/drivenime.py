from . import BaseExtractor


class Drivenime(BaseExtractor):
    tag = "anime"
    host = "https://drivenime.com"

    def extract_meta(self, id: str) -> dict:
        """
        Ambil semua metadata dari halaman web

        Args:
              id: type 'str'
        """

        raw = self.session.get(f"{self.host}/{id}")
        soup = self.soup(raw)

        meta = self.MetaSet()
        content = soup.find(class_="post-single-content")
        meta.register(None, content.text)
        meta["image"] = soup.find("img", class_="alignnone")["src"]
        meta["judul"] = soup.title.text.split("Subtitle")[0]
        meta.setItem("romaji", "judul alternatif")
        meta.setItem("japanese", "judul alternatif")
        meta.setItem("type", "tipe")
        meta.setItem("episodes", "total episode")
        meta.setItem("status")
        meta.setItem("start", split=False)
        meta.setItem("end", split=False)
        meta.setItem("season", "musim")
        meta.setItem("producers", "produser")
        meta.setItem("main studio", "studio")
        meta.setItem("duration", "durasi")
        meta.setItem("genres", "genre")

        meta["tayang"] = meta.pop(
            "start", "?", force=True) + " - " + meta.pop("end", "?", force=True)

        if (sinop := content.find("h2", text="Sinopsis")):
            s = []
            for p in sinop.findAllNext(["p", "h2"]):
                if p.name != "p":
                    break
                s.append(p.text)
            meta["sinopsis"] = " ".join(s)
        return meta

    def extract_data(self, id: str) -> dict:
        """
        Ambil semua situs unduhan dari halaman web

        Args:
              id: jalur url dimulai setelah host, type 'str'

        """

        raw = self.session.get(f"{self.host}/{id}")
        soup = self.soup(raw)

        dl = soup.find(class_="post-single-content")
        for p in dl.findAll("p"):
            if (p.find("a")) and "download" in p.text.lower():
                break
        title = self.re.findall(r"(?s)a>\s*(\[[^>]+?\])\s*<", str(p))
        return {
            ttl: a["href"] for ttl, a in zip(title, p.findAll("a"))
        }

    def search(self, query: str, page: int = 1) -> list:
        """
        Cari item berdasarkan 'query' yang diberikan

        Args:
              query: kata kunci pencarian, type 'str'
              page: indeks halaman web, type 'int'

        Returns:
              list: daftar item dalam bentuk 'dict'
        """

        raw = self.session.get(f"{self.host}/page/{page}", params={
            "s": query})
        soup = self.soup(raw)

        result = []
        for post in soup.findAll(class_="post"):
            a = post.find("a")
            r = {
                "title": a["title"],
                "id": self.getPath(a["href"])
            }

            if (genre := post.find(class_="theauthor")):
                r["genre"] = [a.text for a in genre.findAll("a")]

            result.append(r)
        return result
