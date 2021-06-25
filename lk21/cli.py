#!/usr/bin/python
from .thirdparty.exrex import generate as generate_strings
from .extractors import BaseExtractor
from .options import ArgumentParser
from .utils import parse_range, title, _check_version
from urllib.parse import urlparse
from pkg_resources import parse_version
from . import __version__
import logging
import questionary
import sys
import re
import json
import colorama
import os
colorama.init()


logging.basicConfig(format=f"\x1b[K%(message)s", level=logging.INFO)
logging.getLogger("requests").setLevel(logging.WARNING)

logging.info(f"""
  _____     ___  ____    _____    __
 |_   _|   |_  ||_  _|  / ___ `. /  |
   | |       | |_/ /   |_/___) | `| |
   | |   _   |  __'.    .'____.'  | |
  _| |__/ | _| |  \ \_ / /_____  _| |_
 |________||____||____||_______||_____| {__version__}
""")


def main():
    global Bypasser

    extractors = {
        obj.__name__.lower(): obj for obj in BaseExtractor.__subclasses__() if obj
    }
    Bypasser = extractors.pop("bypass")(logging)
    Bypasser.run_as_module = False
    _version_msg = _check_version()

    parser = ArgumentParser(**{
        "extractors": extractors,
        "version_msg": _version_msg,
    })
    args = parser.parse_args()

    if args.version:
        sys.exit(__version__)

    if args.list_bypass:
        def add_color(x): return re.sub(
            r"\[[^]]+\]", lambda p: f"\x1b[33m{p[0]}\x1b[0m", x)
        for funcname, item in Bypasser.bypassPattern.items():
            logging.info(title(funcname.removeprefix("bypass_"), rtn=True))
            for rule in item["pattern"]:
                valid_url = re.sub(
                    r"\[.+?\][+*]\??|\\[a-zA-Z][+*]\??", "\[id\]", rule.pattern)
                valid_url = re.sub(r"\.[*+]\??", "\[any\]", valid_url)
                valid_url = re.sub(r"^https\??://",  "", valid_url)
                for s in generate_strings(valid_url):
                    logging.info(f"  • {add_color(s)}")
        sys.exit(0)
    elif args.bypass:
        result = Bypasser.bypass_url(args.bypass)
        logging.info(
            f"\n{result}\n")
        if args._exec:
            os.system(args._exec.format(result))
        sys.exit(0)

    if not args.query or (args._exec and "{}" not in args._exec):
        parser.print_help()
        sys.exit(0)

    extractor = extractors["layarkaca21"]
    for egn, kls in extractors.items():
        if args.__dict__[egn]:
            extractor = kls
            break

    extractor = extractor(logging, args)
    if "proxy" in getattr(extractor, "required", []) and not args.skip_proxy:
        if not args.proxy:
            parser.error(
                f"{extractor.__class__.__name__} required arguments --proxy, or skip using the --skip-proxy argument if already using vpn")
    extractor.run_as_module = args.json or args.json_dump

    if not extractor.tag and not args.debug:
        sys.exit(f"Module {extractor.__module__} belum bisa digunakan")
    query = " ".join(args.query)
    extractor.prepare()

    id = False
    nextPage = True
    Range = parse_range(args.page)
    netloc = urlparse(extractor.host).netloc
    try:
        page = Range.__next__()
        cache = {page: extractor.search(query, page=page)}
        while not id:
            print(
                f"Mencari {query!r} -> {netloc} halaman {page}")
            logging.info(
                f"Total item terkumpul: {sum(len(v) for v in cache.values())} item dari total {len(cache)} halaman")
            if not cache[page]:
                sys.exit("Tidak ditemukan")

            if len(cache[page]) == 1:
                response = f"1. " + cache[page][0]["title"]
            else:
                response = extractor.choice([
                    i['title'] for i in cache[page]] + [
                    questionary.Separator(), "00. Kembali", "01. Lanjut", "02. Keluar"], reset_counter=False)
            pgs = list(cache.keys())
            index = pgs.index(page)
            if response.endswith("Keluar"):
                break
            elif response.endswith("Kembali"):
                if extractor.counter > -1:
                    extractor.counter -= len(cache[page])
                print("\x1b[3A\x1b[K", end="")
                if index > 0 and len(pgs) > 1:
                    page = pgs[index - 1]
                    extractor.counter -= len(cache[page])
            elif response.endswith("Lanjut") and nextPage is True:
                if index >= len(pgs) - 1:
                    try:
                        ppage = Range.__next__()
                        if len(res := extractor.search(query, page=page)) > 0:
                            page = ppage
                            cache[page] = res
                        else:
                            extractor.counter -= len(cache[page])
                    except StopIteration:
                        nextPage = False
                else:
                    page = pgs[index + 1]
                if nextPage:
                    print("\x1b[3A\x1b[K", end="")
            else:
                for r in cache[page]:
                    if r.get("title") == re.sub(r"^\d+\. ", "", response):
                        id = r["id"]
                        break
        if id:
            logging.info(f"Mengekstrak link unduhan: {id}")
            result = extractor.extract(id)

            if args.json:
                sys.exit(f"\n{result}\n")
            elif args.json_dump:
                with open(args.json_dump, "w") as file:
                    file.write(json.dumps(result, indent=2, default=lambda o: o.store
                                          if isinstance(getattr(o, "store"), dict) else o.__dict__))
                sys.exit(
                    f"Menyimpan hasil unduhan kedalam file: {args.json_dump!r}")

            # cetak informasi jika ada
            extractor.info(f"\n [\x1b[92m{r.pop('title')}\x1b[0m]")
            for k, v in result.get("metadata", {}).items():
                extractor.info(
                    f"   {k}: {', '.join(filter(lambda x: x, v)) if isinstance(v, list) else v}")
            extractor.info("")

            result = result.get("download", {})
            dlurl = Bypasser.recursive_choice(extractor,  result)
            url = Bypasser.bypass_url(dlurl)

            if args._exec:
                os.system(args._exec.format(url))
            else:
                logging.info("")
                title("Url Dipilih")
                logging.info(f"\n{url}\n")

    except Exception as e:
        logging.info(f"{e}")
        if args.debug:
            raise

    if _version_msg:
        logging.warning(_version_msg)
