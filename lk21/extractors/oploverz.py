from . import BaseExtractor


class Oploverz(BaseExtractor):
    host = "https://www.oploverz.in"
    tag = "anime"
    required = ["proxy"]

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
        if (ep_list := soup.find(class_="episodelist")):
            for li in ep_list.findAll("li"):
                a = li.find("a")
                result[a.text.strip()] = a["href"]
            return result

        elif (all_eps := soup.find(class_="btn-full-eps")):
            result[all_eps.text] = "re:" + self.getPath(all_eps["href"])

        title = [
            a for a in self.re.findall(r"(?s)strong>([^>]+?)</strong", str(soup))
            if self.re.search(r"\([^)]+", a)
        ]

        for ttl, ddl in zip(title, soup.findAll(class_="soraddl")):
            d = {}
            for p in ddl.findAll("p"):
                if (t1 := p.find(class_="sorattl")):
                    d1 = {}
                    for a in p.findAll("a"):
                        d1[a.text] = a["href"]
                    d[t1.text] = d1
            result[ttl] = d
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

        raw = self.session.get(f"{self.host}/page/{page}/",
                               params={"s": query})
        soup = self.soup(raw)

        result = []
        for dtl in soup.findAll("div", class_="dtl"):
            a = dtl.find("a")
            result.append({
                "title": a.text,
                "id": self.getPath(a["href"]),
            })
        for bs in soup.findAll("article", class_="bs"):
            result.append({
                "id": self.getPath(bs.a["href"]),
                "title": bs.find(itemprop="headline").text
            })
        return result
