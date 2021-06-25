from . import BaseExtractor


class Animeindo(BaseExtractor):
    tag = "anime"
    host = "https://animeindo.asia"

    def extract_meta(self, id: str) -> dict:
        """
        Ambil semua metadata dari halaman web

        Args:
              id: type 'str'
        """

        raw = self.session.get(f"{self.host}/{id}")
        soup = self.soup(raw)

        meta = self.MetaSet()
        meta["judul"] = soup.find(class_="entry-title").text

        if (infox := soup.find(class_="cat_box_desc")):
            meta.register(r"(?si){id}\s*:\s*([^>]+?)\s*?\n", infox.text)

            meta.setItem("status")
            meta.setItem("type", "tipe")
            meta.setItem("score")
            meta.setItem("aired", "tayang")
            meta.setItem("duration", "durasi")
            meta.setItem("genres", "genre")
            meta.setItem("season", "musim")

        if (sinops := soup.find(class_="sinops")):
            meta["sinopsis"] = sinops.div.text

        return meta

    def extract_data(self, id: str) -> dict:
        """
        Ambil semua situs unduhan dari halaman web

        Args:
              id: jalur url dimulai setelah host, type 'str'
        """

        raw = self.session.get(f"{self.host}/{id}")
        soup = self.soup(raw)

        if (eps := soup.findAll(class_="episode_list")):
            d = {}
            for ep in eps:
                d[ep.a.text.split(" -")[0]] = "re:" + \
                    self.getPath(ep.a["href"])
            return d

        formats = self.re.findall(r"(Format .+?):", str(soup))
        result = {fm: {} for fm in formats}
        for p in soup.findAll("p", class_="has-text-align-center"):
            if (aa := p.findAll("a")):
                info = [self.re.split(r"\s*:", i)[0] for i in
                        self.re.findall(r">\s*(\d+p(?:\s+.+?)?)\s*:", str(p))]
                if len(info) == 1:
                    d = {info[0]: {
                        a.text: a["href"] for a in aa
                    }}
                else:
                    formats.pop(0)
                    d = {}
                    for sub, dom in self.re.findall(r"(\d+p.+?):.+?((?:<a.+?>.+?</a>(?:\s*\|\s*)?)+)", str(p)):
                        aa = self.soup(dom).findAll("a")
                        d[sub] = {
                            a.text: a["href"] for a in aa
                        }
                result[formats[0]] = d
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
            "s": query})
        soup = self.soup(raw)

        result = []
        for animposx in soup.findAll(class_="animposx"):
            a = animposx.find("a")
            result.append({
                "title": a["title"],
                "id": self.getPath(a["href"])
            })
        return result
