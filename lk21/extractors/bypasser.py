from ..thirdparty import exrex
from ..utils import removeprefix
from . import BaseExtractor
from urllib.parse import urlparse
from collections import defaultdict
import re
import inspect
import math
import questionary
import logging


class Bypass(BaseExtractor):
    bypassPattern = defaultdict(lambda: defaultdict(set))
    allBypassPattern = None

    def bypass_antfiles(self, url):
        """
        regex: https?://antfiles\.com/\?dl=[^>]+
        """

        raw = self.session.get(url)
        soup = self.soup(raw)

        if (a := soup.find(class_="main-btn", href=True)):
            return "{0.scheme}://{0.netloc}/{1}".format(
              urlparse(url), a["href"])

    def bypass_ouo(self, url):
        """
        regex: https?://ouo\.(?:press|io)/[^>]+
        """

        def getData(form):
            if not form:
                return None, None
            data = {}
            for input in form.findAll("input", {"name": re.compile(r"token$")}):
                k = input.get("id") or input.get("name")
                data[k] = input["value"]
            return form["action"], data

        raw = self.session.get(url)
        soup = self.soup(raw)
        action, data = getData(soup.form)

        for _ in range(2):
            self.report_bypass(action)
            raw = self.session.post(action, data=data)
            soup = self.soup(raw)
            action, data = getData(soup.form)

        return raw.url

    def bypass_anonfiles(self, url):
        """
        regex: https?://anonfiles\.com/[^>]+
        """

        raw = self.session.get(url)
        soup = self.soup(raw)

        if (dlurl := soup.find(id="download-url")):
            return dlurl["href"]

    def bypass_letsupload(self, url):
        """
        regex: https?://letsupload\.[ic]o/[0-9A-Za-z]+(?:/|\?pt=)[^>]+
        """

        raw = self.session.get(url)
        if (fileId := re.search(r"(?i)showFileInformation\((\d+)\)", raw.text)):
            return self.bypass_redirect('https://letsupload.io/account/direct_download/' + fileId.group(1))
        if (nextUrl := re.search(r"window.location += ['\"]([^\"']+)", raw.text)):
            return nextUrl.group(1)

    def bypass_streamtape(self, url):
        """
        regex: https?://streamtape\.com/v/[^/]+/[^>]+
        """

        raw = self.session.get(url)

        if (videolink := re.findall(r"document.*((?=id\=)[^\"']+)", raw.text)):
            nexturl = "https://streamtape.com/get_video?" + videolink[-1]
            self.report_bypass(nexturl)
            if (redirect := self.bypass_redirect(nexturl)):
                return redirect

    def bypass_sbembed(self, url):
        """
        regex: https?://sbembed\.com/[^>]+\.html
        regex: https?://streamsb\.net/[^>]+\.html
        """

        raw = self.session.get(url)
        soup = pself.soup(raw)

        result = {}
        for a in soup.findAll("a", onclick=re.compile(r"^download_video[^>]+")):
            data = dict(zip(["id", "mode", "hash"], re.findall(
                r"[\"']([^\"']+)[\"']", a["onclick"])))
            data["op"] = "download_orig"

            raw = self.session.get("https://sbembed.com/dl", params=data)
            soup = self.soup(raw)

            if (direct := soup.find("a", text=re.compile("(?i)^direct"))):
                result[a.text] = direct["href"]
        return result

    def bypass_filesIm(self, url):
        """
        regex: https?://(?:files\.im|racaty\.net|hxfile\.co)/[^>]+
        """

        headers = {
            'content-type': 'application/x-www-form-urlencoded',
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.152 Safari/537.36',
        }

        data = {
            'op': 'download2',
            'id': self.getPath(url),
            'rand': '',
            'referer': '',
            'method_free': '',
            'method_premium': '',
        }

        response = self.session.post(url, headers=headers, data=data)
        soup = self.soup(response)

        if (btn := soup.find(class_="btn btn-dow")):
            return btn["href"]
        if (unique := soup.find(id="uniqueExpirylink")):
            return unique["href"]

    def bypass_redirect(self, url):
        """
        regex: https?://bit\.ly/[^>]+
        regex: https?://(?:link\.zonawibu\.cc/redirect\.php\?go|player\.zafkiel\.net/blogger\.php\?yuzu)\=[^>]+
        """
        head = self.session.head(url)
        return head.headers.get("Location", url)

    def bypass_uservideo(self, url):
        """
        regex: https?://(?:www\.)?uservideo\.xyz/file/[^>]+
        """

        raw = self.session.get(url)
        if (match := re.search(r"innerHTML\s*=\s*'([^']+)", raw.text)):
            soup = self.soup(match.group(1))

            d = {}
            for div in soup.findAll("div"):
                title = div.findPrevious(class_="download-title")
                r = {}
                for a in div.findAll("a", href=True):
                    r[a.text] = a["href"]
                d[title.text] = r
            return d

        return self.bypass_linkpoi(url)

    def bypass_linkpoi(self, url):
        """
        regex: https?://linkpoi\.me/[^>]+
        """

        raw = self.session.get(url)
        soup = self.soup(raw)

        if (a := soup.find("a", class_="btn-primary")):
            return a["href"]

    def bypass_mediafire(self, url):
        """
        regex: https?://(?:www\.)?mediafire\.com/file/[^>]+(?:/file)?
        """

        raw = self.session.get(url)
        soup = self.soup(raw)

        if (dl := soup.find(id="downloadButton")):
            return dl["href"]

    def bypass_zippyshare(self, url):
        """
        regex: https?://www\d+\.zippyshare\.com/v/[^/]+/file\.html
        """

        raw = self.session.get(url)
        if (dlbutton := re.search(r'href = "([^"]+)" \+ \(([^)]+)\) \+ "([^"]+)', raw.text)):
            folder, math_chall, filename = dlbutton.groups()
            math_chall = eval(math_chall)
            return "%s%s%s%s" % (
                re.search(r"https?://[^/]+", raw.url).group(0), folder, math_chall, filename)

        soup = self.soup(raw)
        if (script := soup.find("script", text=re.compile("(?si)\s*var a = \d+;"))):
            sc = str(script)
            var = re.findall(r"var [ab] = (\d+)", sc)
            omg = re.findall(r"\.omg (!?=) [\"']([^\"']+)", sc)
            file = re.findall(r'"(/[^"]+)', sc)
            if var and omg:
                a, b = var
                if eval(f"{omg[0][1]!r} {omg[1][0]} {omg[1][1]!r}") or 1:
                    a = math.ceil(int(a) // 3)
                else:
                    a = math.floor(int(a) // 3)
                divider = int(re.findall(f"(\d+)%b", sc)[0])
                return re.search(r"(^https://www\d+.zippyshare.com)", raw.url).group(1) + \
                    "".join([
                        file[0],
                        str(a + (divider % int(b))),
                        file[1]
                    ])

    def bypass_fembed(self, url):
        """
        regex: https?://(?:www\.naniplay|naniplay)(?:\.nanime\.(?:in|biz)|\.com)/file/[^>]+
        regex: https?://layarkacaxxi\.icu/[fv]/[^>]+
        regex: https?://fem(?:bed|ax20)\.com/[vf]/[^>]+
        """

        url = url.replace("/v/", "/f/")
        raw = self.session.get(url)
        api = re.search(r"(/api/source/[^\"']+)", raw.text)
        if api is not None:
            result = {}
            raw = self.session.post(
                "https://layarkacaxxi.icu" + api.group(1)).json()
            for d in raw["data"]:
                f = d["file"]
                direct = self.bypass_redirect(f)
                result[f"{d['label']}/{d['type']}"] = direct
            return result

    def report_bypass(self, url):
        if hasattr(self.logger, "info"):
            self.logger.info(f"Bypass link {urlparse(url).netloc}: {url}")

    def bypass_url(self, url):
        """
        Bypass url

        Args:
              url: type 'str'
        """

        self.host = "{0.scheme}://{0.netloc}".format(urlparse(url))
        patterns = {k: v['pattern'] for k, v in self.bypassPattern.items()}

        previous = url
        stop = False
        while not stop:
            _break = False
            for fname, pattern in patterns.items():
                if isinstance(url, dict) or _break:
                    break

                if any(_re.search(url) for _re in pattern):
                    self.report_bypass(url)

                    func = getattr(self, fname, self.bypass_redirect)
                    try:
                        result = func(url)
                    except Exception:
                        result = None
                        raise

                    if not result:
                        stop = True
                        break

                    if self.run_as_module or not isinstance(result, dict):
                        url = result
                    else:
                        url = self.recursive_choice(self, result)
                    if url == previous:
                        stop = not stop
                    else:
                        previous = url
                    _break = True
            if not _break:
                break

        if isinstance(url, str):
            return re.sub(r" ", "%20", url)
        else:
            return self.dict_to_list(url)

    def recursive_choice(self, extractor, result):
        prevresult = None
        index = 0
        last = False

        #selected_items = []
        while True:
            # if last is True:
            #    otype = "checkbox"
            #    keys = [{
            #            "name": f"{key} (bypass)" if isinstance(
            #                value, str) and allDirectRules.search(value) else key,
            #            "checked": result.get(key) in selected_items
            #        } for key, value in result.items() if value]
            #    keys.extend([questionary.Separator(), {
            #        "name": "00. Kembali",
            #        "checked": False
            #    }])
            #    print (keys, selected_items)
            # else:
            #   otype = "list"

            keys = [
                f"{key} (bypass)" if isinstance(
                    value, str) and self.allBypassPattern.search(value) else key
                for key, value in result.items() if value
            ]
            if prevresult and index > 0:
                keys.extend([questionary.Separator(), "00. Kembali"])

            key = extractor.choice(keys)

            # if isinstance(key, list):
            #    for k in key:
            #        if (v := result.get(k)):
            #            selected_items.append(v)

            if "00. Kembali" in key:
                last = False
                result = prevresult
                index -= 1
            else:
                prevresult = result
                index += 1
                result = result[key]

            if (index == 1 and isinstance(result, str)) or last is True:
                break

            if not all(isinstance(v, dict) for v in result.values()):
                last = True

        if hasattr(extractor, "host"):
            prefix = re.compile(
                "^(?:" + r"|".join([extractor.host, "re\:"]) + ")")
            if prefix.search(result):
                id = extractor.getPath(prefix.sub("", result))
                logging.info(f"Mengekstrak link unduhan: {id}")
                result = extractor.extract(id).get("download", {})
                result = recursive_choice(extractor, result)
        return result


# lazy method
allBypassPattern = []
pattern = re.compile(r"regex *: *(.+)(?:\n|$)")
for key, value in inspect.getmembers(Bypass):
    if key.startswith("bypass_") and key != "bypass_url":
        for urlPattern in pattern.findall(value.__doc__ or ""):
            Bypass.bypassPattern[key]["pattern"].add(
                re.compile(urlPattern)
            )
            allBypassPattern.append(urlPattern)
        if (allPattern := Bypass.bypassPattern.get(key)):
            for rule in allPattern["pattern"]:
                valid_regex = re.sub(
                    r"\[.+?\][+*]\??|\\[a-zA-Z][+*]\??", "\[id\]", rule.pattern)
                valid_regex = re.sub(r"\.[*+]\??", "\[any\]", valid_regex)
                for url in exrex.generate(valid_regex):
                    Bypass.bypassPattern[key]["support"].add(
                        removeprefix(urlparse(url).netloc, "www."))

Bypass.allBypassPattern = re.compile(r"|".join(allBypassPattern))
