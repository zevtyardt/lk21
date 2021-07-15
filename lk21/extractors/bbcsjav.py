from . import BaseExtractor


class Bbcsjav(BaseExtractor):
    tag = "JAV"
    host = "https://bbcsjav.com"
    required_proxy = True

    def getCode(self, text):
        if (code := self.re.search(r"([A-Z]+-[0-9]+)", text)):
            return code.group()

    def extract_meta(self, id: str) -> dict:
        """
        Ambil semua metadata dari halaman web

        Args:
              id: type 'str'
        """

        raw = self.session.get(f"{self.host}/{id}")
        soup = self.soup(raw)

        meta = self.MetaSet()
        meta["title"] = "-".join(soup.title.text.split("-")[:-1]).strip(". ")
        meta["image"] = soup.find("img", class_="wp-post-image")["src"]
        meta["code"] = self.getCode(soup.title.text)

        info = soup.find(class_="info_vids")
        aliases = {
            "release": "rilis",
            "duration": "durasi",
            "genres": "genre",
            "quality": "kualitas"
        }
        for p in info.findAll("p"):
            if ":" in p.text:
                k, v = self.re.split("\s*:\s*", p.text)
                k = k.lower()
                k = aliases.get(k, k)
                if "," in v:
                    v = self.re.split("\s*,\s*", v)
                meta[k] = v

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

        kontent = soup.find(class_="kontent")
        for h3 in kontent.findAll("h3"):
            items = {}
            for tr in h3.findNext("div").tbody.findAll("tr"):
                subitem = {}
                quality = None
                for td in tr.findAll("td"):
                    if not td.a:
                        quality = td.text
                    else:
                        for a in td.findAll("a"):
                            subitem[a.text] = a["href"]
                items[quality] = subitem
            result[h3.text] = items
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
        for post_id in soup.findAll(id="post-ID"):
            a = post_id.a
            title = post_id.find(class_="title")
            result.append({
                "id": self.getPath(a["href"]),
                "title": title.text.strip(),
                "tag": [tag.text for tag in post_id.findAll(rel="tag")],
                "code": self.getCode(title.text)
            })
        return result
