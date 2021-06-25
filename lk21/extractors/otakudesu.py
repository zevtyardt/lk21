from . import BaseExtractor


class Otakudesu(BaseExtractor):
    tag = "anime"
    host = "https://otakudesu.moe"

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

        if (eps := soup.findAll(class_="episodelist")[1:]):
            ch = {}
            for li in eps[0].findAll("li"):
                ch[li.a.text] = li.a["href"]
            return ch
        else:
            dls = {}
            for dl in soup.findAll("div", class_="download"):
                title = [h4.text for h4 in dl.findAll("h4")]
                for n, ul in enumerate(dl.findAll("ul")):
                    if len(title) == 1:
                        n = 0
                    n = title[n]
                    if not dls.get(n):
                        dls[n] = {}
                    for li in ul.findAll("li"):
                        dls[n][f"{li.strong.text}/{li.i.text}"] = {
                            a.text: a["href"] for a in li.findAll("a")
                        }
            return dls

    def search(self, query: str, page: int = 1) -> list:
        """
        Cari item berdasarkan 'query' yang diberikan

        Args:
              query: kata kunci pencarian, type 'str'
              page: indeks halaman web, type 'int'
        """

        raw = self.session.get(self.host, params={
            "s": query, "post_type": "Anime"})
        soup = self.soup(raw)

        result = []
        if (ul := soup.find("ul", class_="chivsrc")):
            for li in ul.findAll("li"):
                result.append({
                    "title": li.a.text,
                    "id": self.getPath(li.a["title"])
                })
        return result
