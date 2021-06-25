from . import BaseExtractor


class Layarkaca21(BaseExtractor):
    tag = "movie"
    host = "http://149.56.24.226/"

    def extract_meta(self, id: str) -> dict:
        """
        Ambil semua metadata dari halaman web

        Args:
              id: type 'str'
        """

        raw = self.session.get(f"{self.host}/{id}")
        soup = self.soup(raw)

        img = soup.find(class_="img-thumbnail")

        meta = self.MetaSet()
        meta["judul"] = img["alt"]
        meta["image"] = "https:" + img["src"]

        content = soup.find(class_="content")
        for div in content.findAll("div"):
            if (k := div.h2) and (k := k.text) and k not in ["Oleh", "Diunggah"]:
                value = ", ".join(h3.text for h3 in div.findAll("h3"))
                meta.add(k, value, split=k not in ["Imdb", "Diterbitkan"])
        if (block := soup.find("blockquote")):
            block.strong.decompose()
            block.span.decompose()

            meta["sinopsis"] = block.text

        return meta

    def extract_data(self, id: str) -> dict:
        """
        Ambil semua situs unduhan dari halaman web

        Args:
              id: jalur url dimulai setelah host, type 'str'

        Returns:
              dict: hasil 'scrape' halaman web
        """

        raw = self.session.post("http://dl.sharemydrive.xyz/verifying.php",
                                headers={
                                    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                                    "Accept": "*/*",
                                    "X-Requested-With": "XMLHttpRequest"
                                },
                                params={"slug": id},
                                data={"slug": id}
                                )
        soup = self.soup(raw)
        tb = soup.find("tbody")

        result = {}
        for tr in tb.findAll("tr"):
            title = tr.find("strong").text
            result[title] = {}
            for td in tr.findAll("td")[1:]:
                if (a := td.a):
                    result[title][a["class"]
                                  [-1].split("-")[-1]] = a["href"]
        return result

    def search(self, query: str, page: int = 1) -> list:
        """
        Cari item berdasarkan 'query' yang diberikan

        Args:
              query: kata kunci pencarian, type 'str'
              page: indeks halaman web, type 'int'
        """

        raw = self.session.get(self.host,
                               params={"s": query})

        soup = self.soup(raw)

        r = []
        for item in soup.findAll(class_="search-item"):
            a = item.a
            extra = {"genre": [], "star": [], "country": [],
                     "size": [""], "quality": [""], "year": [""]}
            for tag in item.find(class_="cat-links").findAll("a"):
                name, it = self.re.findall(r"/([^/]+)/([^/]+)", str(tag))[0]
                extra[name].insert(0, it)

            for p in filter(lambda x: x.strong is not None, item.findAll("p")):
                np, vl = self.re.findall(
                    r"^([^:]+):\s+(.+)", p.text.strip())[0]
                np = "star" if np == "Bintang" else "director" if np == "Sutradara" else np
                extra[np] = self.re.split(r"\s*,\s*", vl) if "," in vl else vl

            extra["id"] = self.re.search(
                r"\w/([^/]+)", a["href"]).group(1)
            result = {
                "title": (item.find("h2").text or a.img["alt"]).strip(),
            }
            result.update(extra)
            r.append(result)
        return r
