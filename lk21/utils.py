from collections import UserDict
import re
import logging


def title(text, rtn=False):
    r = f" [\x1b[92m{text}\x1b[0m]"
    if rtn:
        return r
    logging.info(r)


def removeprefix(s, p):
    return re.sub(r"^%s" % p, "", s)


def removesuffix(s, p):
    return re.sub(r"%s$" % p, "", s)


def _check_version():
    try:
        base = BaseExtractor()
        raw = base.session.get("https://pypi.org/project/lk21", timeout=2)
        soup = base.soup(raw)

        if (name := soup.find(class_="package-header__name")):
            version = name.text.split()[-1]
            if parse_version(__version__) < parse_version(version):
                return (
                    "\x1b[93m"
                    f"WARNING: Anda menggunakan lk21 versi {__version__}, sedangkan versi {version} telah tersedia.\n"
                    "Anda harus mempertimbangkan untuk mengupgrade melalui perintah 'python -m pip install --upgrade lk21'."
                    "\x1b[0m")
    except Exception:
        return


class MetaSet(UserDict):
    def __init__(self, *args, **kwargs):
        self.store = dict()
        self.update(dict(*args, **kwargs))  # use the free update to set keys

        self._pattern = r"(?i){id} *: *(.+?)\n"
        self._content = ""

    def __getitem__(self, key):
        return self.store[key]

    def __setitem__(self, key, value):
        self.store[key] = value.strip() if isinstance(value, str) else value

    def __delitem__(self, key):
        del self.store[key]

    def __iter__(self):
        return iter(self.store)

    def __len__(self):
        return len(self.store)

    def __repr__(self):
        return repr(self.store)

    def register(self, pattern: str, content: str) -> None:
        """
        Menyetel pola Regex
        """

        if pattern:
            self._pattern = pattern
        if content:
            self._content = content

    def add(self, key: any, value: any, split: bool = True) -> None:
        key = re.sub(r" ", "_", key).lower()
        if isinstance(value, str):
            value = re.split(r"\s*,\s+", value
                             ) if split else [value]
        if not value:
            return
        if len(value) == 1:
            value = value[0].strip()
        if (pre := self.store.get(key)):
            if not isinstance(pre, list):
                self.store[key] = [pre]
            self.store[key].extend(
                [value] if not isinstance(value, list) else value)
        else:
            self.store[key] = value

    def setItem(self, id: str, key: str = None, split: bool = True) -> None:
        """
        Tambah item jika ditemukan
        """

        if (value := re.search(self._pattern.format(id=id), self._content)):
            self.add(key or id, value.group(1), split)

    def pop(self, key, default=None, force=False):
        if not self.store.get(key):
            return default
        else:
            return self.store.pop(key) or default


def parse_range(raw):
    assert re.match(r"[\s\d:]+", raw), f"invalid syntax: {raw!r}"
    if "," in raw:
        for rg in re.split(r"\s*,\s*", raw):
            if ":" not in rg:
                yield rg
            else:
                assert len(re.findall(r":", raw)
                           ) <= 1, f"invalid syntax: {raw!r}"
                yield from parse_range(rg)
    else:
        spl = re.split(r"\s*:\s*", raw)
        if not spl[0]:
            spl[0] = "1"

        start, end = map(lambda x: int(x) if x else None, spl)
        if end:
            assert start < end, "angka pertama tidak boleh lebih dari angka kedua"
            yield from range(start, end + 1)
        else:
            while True:
                yield start
                start += 1
