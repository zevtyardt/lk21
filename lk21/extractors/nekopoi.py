from . import BaseExtractor

class Nekopoi(BaseExtractor):
    tag = "hentai, JAV"
    host = "http://nekopoi.care"
    required_proxy = True

    def extract_meta(self, id: str) -> dict:
        """
        Ambil semua metadata dari halaman web

        Args:
              id: type 'str'
        """

        raw = self.session.get(f"{self.host}/{id}")
        soup = self.soup(raw)

        meta = self.MetaSet()
        self._write(soup)
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
        self._write(soup)
        return result

    def search(self, query: str, page: int = 1) -> list:
        """
        Cari item berdasarkan 'query' yang diberikan

        Args:
              query: kata kunci pencarian, type 'str'
              page: indeks halaman web, type 'int'
        """

        raw = self.session.get(f"{self.host}/page/{page}", params={"s": query}, verify=False, allow_redirects=True)
        soup = self.soup(raw)

        result = []
        if (res := soup.find(class_="result")):
            for li in res.findAll("li"):
                if (a := li.a):
                    result.append({
                        "title": a.text,
                        "id": self.getPath(a["href"])
                    })
        return result
