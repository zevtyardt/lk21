from . import BaseExtractor


class Wibudesu(BaseExtractor):
    host = "https://wibudesu.com"
    tag = "anime"

    def extract_meta(self, id: str) -> dict:
        """
        Ambil semua metadata dari halaman web

        Args:
              id: type 'str'
        """

        raw = self.session.get(f"{self.host}/{id}")
        soup = self.soup(raw)

        content = soup.find("div", class_="lexot")
        meta = self.MetaSet()

        meta.register(None, content.text)
        meta.setItem("judul")
        meta.setItem("native title", "judul alternatif")
        meta.setItem("also known as", "judul alternatif")
        meta.setItem("genres", "genre")
        meta.setItem("movie")
        meta.setItem("country", "negara")
        meta.setItem("release date", "rilis")
        meta.setItem("duration", "durasi")
        meta.setItem("score")

        meta["image"] = content.img["data-lazy-src"]
        meta["judul"] = self.re.split(
            "(?i)(?:bd )?(?:batch )?subtitle", soup.title.text)[0]

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

        lexot = soup.find(class_="lexot")

        result = {}
        for p in lexot.findAll("p")[1:]:
            if (links := p.findAll("a")):
                title = p.strong.text
                d = {}
                for a in links:
                    d[a.text] = a["href"]
                result[title] = d
        return result

    def search(self, query: str, page: int = 1) -> list:
        """
        Cari item berdasarkan 'query' yang diberikan

        Args:
              query: kata kunci pencarian, type 'str'
              page: indeks halaman web, type 'int'
        """

        raw = self.session.get(f"{self.host}/page/{page}", params={
            "s": query, "post_type": "post"})
        soup = self.soup(raw)

        r = []
        for detpost in soup.findAll(class_="detpost"):
            a = detpost.find("a")
            result = {
                "title": a["title"],
                "id": self.getPath(a["href"])
            }

            if (morec := detpost.find(class_="morec")):
                result["genre"] = [a.text for a in morec.findAll("a")]

            r.append(result)
        return r
