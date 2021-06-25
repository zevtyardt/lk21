from . import BaseExtractor


class Samehadaku(BaseExtractor):
    tag = "anime"
    host = "https://samehadaku.vip"

    def extract_meta(self, id: str) -> dict:
        """
        Ambil semua metadata dari halaman web

        Args:
              id: type 'str'
        """

        raw = self.session.get(f"{self.host}/{id}")
        soup = self.soup(raw)

        alias = {
            'Japanese': "judul alternatif",
            'English': "judul alternatif",
            'Synonyms': "judul alternatif",
            'Season': 'musim',
            'Producers': 'produser',
            'type': 'tipe',
            'Duration': 'durasi',
        }
        meta = self.MetaSet()
        meta["image"] = soup.find("img", class_="anmsa")["src"]
        meta["judul"] = self.re.split(
            "(?i)(?:bd )?(?:batch )?subtitle", soup.title.text)[0]
        meta["sinopsis"] = soup.find(class_="desc").text

        content = soup.find(class_="spe")
        for span in content.findAll("span"):
            k = span.b.text.rstrip(":")
            span.b.decompose()
            k = alias.get(k, k)

            if span.a:
                v = [a.text for a in span.findAll("a")]
            else:
                v = span.text
            meta.add(k, v, split=k not in ["Rilis"])

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

        if id.startswith("anime/"):
            ch = {}
            if (listeps := soup.findAll(class_="epsleft")):
                for li in listeps:
                    a = li.find("a")
                    ch[a.text] = self.getPath(a["href"])
            if (batch := soup.find(class_="listbatch")):
                ch[batch.text] = self.getPath(batch.a["href"])
            return ch

        result = {}
        for dl in soup.findAll(class_="download-eps"):
            d = {}
            for li in dl.findAll("li"):
                item = {}
                for a in li.findAll("a"):
                    item[a.text] = a["href"]
                d[li.strong.text] = item
            result[dl.p.text] = d
        return result

    def search(self, query: str, page: int = 1) -> list:
        """
        Cari item berdasarkan 'query' yang diberikan

        Args:
              query: kata kunci pencarian, type 'str'
              page: indeks halaman web, type 'int'
        """

        raw = self.session.get(f"{self.host}/page/{page}", params={
            "s": query})
        soup = self.soup(raw)

        res = []
        for article in soup.findAll("article", class_="animpost"):
            result = {
                "id": self.getPath(article.find("a")["href"])
            }

            for k in ("score", "title", "type", "genres"):
                if (v := article.find(class_=k)):
                    name = " ".join(v["class"])
                    if (aa := v.findAll("a")):
                        result[name] = [a.text for a in aa]
                    elif v.text:
                        result[name] = v.text
            res.append(result)
        return res
