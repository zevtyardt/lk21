from . import BaseExtractor

class Nekonime(BaseExtractor):
    host = "https://nekonime.site"
    tag = "anime"

    def search(self, query: str, page: int = 1) -> list:
        """
        Cari item berdasarkan 'query' yang diberikan
        Args:
              query: kata kunci pencarian, type 'str'
              page: indeks halaman web, type 'int'
        """
        raw = self.session.get(f"{self.host}/page/{page}", params={
            "s": query})
        soup = self.soup(raw)
        result = []
        for page in soup.find_all("h3", class_="article-title"):
            result.append({
                "title": page.a.get_text(),
                "id": self.getPath(page.a['href'])
            })
        return result

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
        if (para := soup.find_all("div", class_="bixbox mctn")):
            for boy in para:
                nth = boy.find("div", class_="sorattl collapsible").text
                result[nth] = {}
                for urls in boy.findAll(class_="soraurl"):
                    res = urls.find("strong").text
                    links = {}
                    for a in urls.find_all("a"):
                        links[a.get_text()] = a['href']
                    result[nth][res] = links

        if (para := soup.find_all(class_="mctnx")):
            for boy in para:
                nth = boy.find("div", class_="sorattlx").text
                result[nth] = {}
                for urls in boy.findAll(class_="soraurlx"):
                    res = urls.find("strong").text
                    links = {}
                    for a in urls.find_all("a"):
                        links[a.get_text()] = a['href']
                    result[nth][res] = links

        return result
