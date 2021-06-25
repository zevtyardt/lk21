from . import BaseExtractor


class KDramaindo(BaseExtractor):
    tag = "movie"
    host = "https://k.dramaindo.my.id"

    def extract_meta(self, id: str) -> dict:
        """
        Ambil semua metadata dari halaman web

        Args:
              id: type 'str'
        """

        raw = self.session.get(f"{self.host}/{id}")
        soup = self.soup(raw)

        meta = self.MetaSet()
        content = soup.find(class_="post-wrapper single")
        meta.register(None, content.text)

        meta.setItem("title", "judul")
        meta.setItem("original title", "judul alternatif")
        meta.setItem("genre")
        meta.setItem("cast", "karakter")
        meta.setItem("year", "tahun")
        meta.setItem("duration", "durasi")
        meta.setItem("type", "tipe")
        meta.setItem("episode", "total episode")
        meta.setItem("rating")
        meta.setItem("score")

        sinopsis = content.find(class_="sinopsis")
        meta["sinopsis"] = sinopsis.div.text
        meta["image"] = content.img["src"]

        return meta

    def extract_data(self, id: str) -> dict:
        """
        Ambil semua situs unduhan dari halaman web

        Args:
              id: jalur url dimulai setelah host, type 'str'
        """

        raw = self.session.get(f"{self.host}/{id}")
        soup = self.soup(raw)

        result = {}
        if (dl := soup.find(class_="download")):
            if (batch := dl.find(class_="batch_content")):
                r = {}
                for p in batch.findAll("p"):
                    urls = {}
                    for a in p.findAll("a"):
                        urls[a.text] = a["href"]
                        a.decompose()
                    r[" ".join(p.text.split())] = urls
                result["Batch"] = r
            if (content := dl.find(class_="content")):
                for ul in content.findAll("ul"):
                    r = {}
                    for li in ul.findAll("li"):
                        urls = {}
                        for a in li.findAll("a"):
                            urls[a.text] = a["href"]
                        r[li.strong.text] = urls
                    result[ul.findPrevious("h3").text] = r
        return result

    def search(self, query: str, page: int = 1) -> list:
        """
        Cari item berdasarkan 'query' yang diberikan

        Args:
              query: kata kunci pencarian, type 'str'
              page: indeks halaman web, type 'int'
        """

        raw = self.session.get(f"{self.host}/page/{page}",
                               params={"s": query})
        soup = self.soup(raw)

        result = []
        for info in soup.findAll(class_="info-post"):
            if (a := info.a):
                result.append({
                    "id": self.getPath(a["href"]),
                    "title": a.text
                })
        return result
