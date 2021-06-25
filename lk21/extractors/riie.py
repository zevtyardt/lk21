from . import BaseExtractor


class Riie(BaseExtractor):
    tag = "anime"
    host = "https://riie.jp"

    def extract_meta(self, id: str) -> dict:
        """
        Ambil semua metadata dari halaman web

        Args:
              id: type 'str'

        """

        raw = self.session.get(f"{self.host}/{id}")
        soup = self.soup(raw)

        meta = self.MetaSet()
        meta["image"] = soup.find(class_="dc-thumb").img["src"]
        meta["judul"] = soup.find(class_="dc-title").text
        meta["sinopsis"] = soup.find(class_="dci-desc").text
        meta["rating"] = soup.find(id="vote_percent").text

        def setItem(text, alias=None):
            td = soup.find("td", text=text)
            v = td.findNext("td")
            if v.a:
                v = [a.text for a in v.findAll("a")]
            else:
                v = v.text
            meta.add(text, v)

        setItem("Judul Alternatif")
        setItem("Status")
        setItem("Genre")

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

        if (eps := soup.findAll(id="episodes-list")):
            lst = {}
            for ep in eps:
                if (items := ep.findAll("li", class_="ep-item")):
                    title = ep.find(class_="gh-title").text

                    raw = {}
                    for item in items:
                        a = item.find("a")
                        if "download" in title.lower():
                            raw[a.text] = a["href"]
                        else:
                            raw[a.text] = "re:" + self.getPath(a["href"])
                    lst[title] = raw
            return lst

    def search(self, query: str, page: int = 1) -> list:
        """
        Cari item berdasarkan 'query' yang diberikan

        Args:
              query: kata kunci pencarian, type 'str'
              page: indeks halaman web, type 'int'
        """

        raw = self.session.get(f"{self.host}/search/{page}/{query}")
        soup = self.soup(raw)

        res = []
        if (result := soup.find(class_="filter-result")):
            for ul in result.findAll("ul"):
                for li in ul.findAll("li"):
                    a = li.find(class_="item-title").a
                    r = {
                        "id": self.getPath(a["href"]),
                        "title": a.text
                    }
                    for kl in ("tv-type", "gr-eps", "gr-type", "gr-sub"):
                        if (it := li.find(class_=kl)):
                            r[kl] = it.text
                    res.append(r)
        return res
