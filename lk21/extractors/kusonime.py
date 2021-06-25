from . import BaseExtractor


class Kusonime(BaseExtractor):
    tag = "anime"
    host = "https://kusonime.com"

    def extract_meta(self, id: str) -> dict:
        """
        Ambil semua metadata dari halaman web

        Args:
              id: type 'str'
        """

        raw = self.session.get(f"{self.host}/{id}")
        soup = self.soup(raw)

        alias = {
            'japanese': "judul alternatif",
            'seasons': 'musim',
            'producers': 'produser',
            'type': 'tipe',
            'duration': 'durasi',
            'released on': 'tayang'
        }
        meta = self.MetaSet()
        meta["image"] = soup.find(class_="wp-post-image")["src"]
        meta["judul"] = self.re.split(
            "(?i)(?:bd )?(?:batch )?subtitle", soup.title.text)[0]

        content = soup.find(class_="info")
        for p in content.findAll("p"):
            if ":" not in p.text:
                continue
            k, v = map(lambda x: x.lower().strip(),
                       self.re.split("\s*:\s*", p.text))
            k = alias.get(k, k)
            meta.add(k, v, split=k not in ["score", "tayang"])
        content.decompose()
        if (clear := soup.find(class_="clear")):
            sinop = []
            for p in clear.findAllNext("p"):
                if p.find("a"):
                    break
                sinop.append(p.text)
            meta["sinopsis"] = " ".join(sinop)

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

        d = {}
        for n, smokeddl in enumerate(soup.findAll("div", class_="smokeddl")[:-1], start=1):
            title = f"{n}. " + smokeddl.find(class_="smokettl").text
            d[title] = {}
            for smokeurl in smokeddl.findAll(class_="smokeurl"):
                res = smokeurl.strong.text
                links = {}
                for a in smokeurl.findAll("a"):
                    links[a.text] = a["href"]
                d[title][res] = links
        return d

    def search(self, query: str, page: int = 1) -> list:
        """
        Cari item berdasarkan 'query' yang diberikan

        Args:
              query: kata kunci pencarian, type 'str'
              page: indeks halaman web, type 'int'

        Returns:
              list: daftar item dalam bentuk 'dict'
        """

        raw = self.session.get(self.host + f"/page/{page}/", params={
            "s": query})
        soup = self.soup(raw)

        result = []
        for item in soup.findAll("div", class_="content"):
            d = {
                "title": item.h2.text,
                "id": self.getPath(item.a["href"])
            }
            for p in item.findAll("p"):
                if "genre" in p.text:
                    d["genre"] = [a.text for a in p.findAll(p)]
                elif "release" in p.text:
                    d["released"] = p.text.split("on ")[-1]
            result.append(d)
        return result
