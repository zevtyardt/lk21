from . import BaseExtractor


class Anitoki(BaseExtractor):
    tag = "anime"
    host = "https://www.anitoki.com"

    def extract_meta(self, id: str) -> dict:
        """
        Ambil semua metadata dari halaman web

        Args:
              id: type 'str'
        """

        raw = self.session.get(f"{self.host}/{id}")
        soup = self.soup(raw)

        meta = self.MetaSet()
        if (sinop := soup.find(text=self.re.compile(r"Sinopsis[^>]+"))):
            meta["sinopsis"] = " ".join(
                p.text for p in sinop.findAllNext("p", style="text-align: justify;") if not p.span
            )

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
        for dl in soup.findAll(class_="dlbod"):
            for smokeurl in dl.findAll(class_="smokeurl"):
                smokettl = smokeurl.findPrevious(class_="smokettl").text
                if not result.get(smokettl):
                    result[smokettl] = {}

                r = {}
                for a in smokeurl.findAll("a"):
                    r[a.text] = a["href"]
                if smokeurl.strong:
                    result[smokettl][smokeurl.strong.text] = r
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
        for kover in soup.findAll("div", class_="kover"):
            a = kover.a
            result.append({
                "id": self.getPath(a["href"]),
                "title": a["title"]
            })
        return result
