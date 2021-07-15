from . import BaseExtractor


class Dramaindo(BaseExtractor):
    tag = "anime, movie"
    host = "https://dramaindo.cn"

    def extract_meta(self, id: str) -> dict:
        """
        Ambil semua metadata dari halaman web

        Args:
              id: type 'str'
        """

        raw = self.session.get(f"{self.host}/{id}")
        soup = self.soup(raw)

        meta = self.MetaSet()
        meta["image"] = soup.find(class_="wp-post-image")["src"]

        if (info := soup.find(class_="info-content")):
            meta["judul"] = soup.find(class_="alter").text
            meta["genre"] = [a.text for a in info.find(
                class_="genxed").findAll("a")]

            alias = {
                "Status": "status",
                "Released": "rilis",
                "Duration": "durasi",
                "Season": "season",
                "Country": "negara",
                "Type": "tipe",
                "Episodes": "total_episode",
                "Casts": "pemeran",
            }
            for span in info.findAll("span"):
                k, v = self.re.split("\s*:\s*", span.text)
                if alias.get(k):
                    meta[alias[k]] = v
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
        if (dlbox := soup.find(class_="dlbox")):
            for li in dlbox.findAll("li"):
                if not li.a:
                    continue

                q = li.find(class_="q").text
                w = li.find(class_="w").text
                e = li.find(class_="e")

                if not result.get(q):
                    result[q] = {}
                result[q][w] = e.a["href"]

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
        for article in soup.findAll("article"):
            result.append({
                "title": article.find(itemprop="headline").text,
                "id": self.getPath(article.a["href"])
            })
        return result
