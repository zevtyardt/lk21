from . import BaseExtractor


class Anikyojin(BaseExtractor):
    host = "https://anikyojin.net"
    tag = "anime"
    required = ["proxy"]

    def prepare(self):
        if self.args:
            self.setProxies(self.args.proxy)

    def extract_meta(self, id: str) -> dict:
        """
        Ambil semua metadata dari halaman web

        Args:
              id: type 'str'
        """

        raw = self.session.get(f"{self.host}/{id}")
        soup = self.soup(raw)

        meta = self.MetaSet()
        meta["image"] = soup.find(class_="wp-post-image")["src"]
        if (infox := soup.find(class_="infox")):
            meta.register(r"(?i){id}\s*:\s*([^>]+?) *?\n", infox.text)

            meta.setItem("judul")
            meta.setItem("judul lain", "judul alternatif")
            meta.setItem("type", "tipe")
            meta.setItem("episode", "total episode")
            meta.setItem("duration", "durasi")
            meta.setItem("category", "genre")
            meta.setItem("aried", "tayang")
            meta.setItem("studio")
            meta.setItem("rating")
            meta.setItem("score", split=False)

        if (sinop := soup.find(class_="sinop")):
            meta["sinopsis"] = sinop.p.text

        return meta

    def extract_data(self, id: str) -> dict:
        """
        Ambil semua situs unduhan dari halaman web

        Args:
              id: jalur url dimulai setelah host, type 'str'

        Returns:
              dict: hasil 'scrape' halaman web
        """

        raw = self.session.get(f"{self.host}/{id}")
        soup = self.soup(raw)

        result = {}
        for dc in soup.findAll(class_="downloadcloud"):
            reso = {}
            for li in dc.findAll("li"):
                d = {}
                for a in li.findAll("a"):
                    d[a.text] = a["href"]
                reso[li.strong.text] = d
            result[dc.h2.text] = reso
        return result

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
            "s": query, "post_type": "post"})
        soup = self.soup(raw)

        r = []
        for article in soup.findAll(class_="artikel"):
            a = article.h2.find("a")

            result = {
                "title": a.text,
                "id": self.getPath(a["href"])
            }

            for li in article.find(class_="info").findAll("li"):
                k, v = self.re.split(r"\s*:\s*", li.text)
                if "," in v:
                    v = self.re.split(r"\s*,\s*", v)
                result[k] = v

            r.append(result)
        return r
