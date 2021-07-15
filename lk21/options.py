from .thirdparty.exrex import getone as regex_to_string
from shutil import get_terminal_size
from .extractors.bypasser import Bypass
from urllib.parse import urlparse
import argparse
import re


def ipPortType(arg_value, pat=re.compile(r"^(?:\d{1,3}\.?){4}:\d+$")):
    if not pat.match(arg_value):
        raise argparse.ArgumentTypeError("Invalid proxy format")
    return arg_value


def ArgumentParser(**kwargs):
    extractors = kwargs.pop("extractors")
    version_msg = kwargs.pop("version_msg")

    parser = argparse.ArgumentParser(
        formatter_class=lambda prog: argparse.RawTextHelpFormatter(
            prog, max_help_position=get_terminal_size().lines),
        epilog=version_msg)

    parser.add_argument("query", metavar="query",
                        nargs="*", help="kueri, judul, kata kunci")
    parser.add_argument("--version", action="store_true",
                        help="show version and exit")
    parser.add_argument("-d", "--debug", action="store_true",
                        help=argparse.SUPPRESS)
    parser.add_argument("-p", metavar="page", dest="page",
                        help=("halaman situs, contoh penggunaan:\n"
                              "  - 1,2,3\n"
                              "  - 1:2, 2:8\n"
                              "  - 1,2,3:8\n"
                              "  - default halaman pertama\n"
                              "    dan seterusnya"), type=str, default="1:")
    parser.add_argument("-i", "--information", dest="info",
                        action="store_true", help="cetak informasi dari item yang dipilih")
    parser.add_argument("--exec", metavar="cmd", dest="_exec",
                        help=("jalankan 'perintah' dengan argument berupa\n"
                              "url yang dipilih.\n\n"
                              "contoh: aria2c {}"))

    valid_e_rules = re.compile(
        r"\[\^.+?\][+*]")
    valid_allDirectRules = valid_e_rules.sub(
        "[A-Za-z0-9-.]{5,7}", Bypass.allBypassPattern.pattern)
    parser.add_argument("--bypass", metavar="url",
                        help=("bypass situs download\n\n"
                              f"contoh url: {regex_to_string(valid_allDirectRules, 3)!r}\n"
                              ))

    parser.add_argument("--list-bypass", action="store_true",
                        help="cetak semua daftar situs download yang dapat\ndi-bypass")

    parser.add_argument("--dump-json", metavar="filename", dest="json_dump",
                        help="simpan hasil ekstraksi unduhan")
    parser.add_argument("--json", action="store_true",
                        help="cetak hasil ekstraksi unduhan")

    network = parser.add_argument_group("Network Options")
    network.add_argument("--proxy", metavar="IP:PORT", type=ipPortType,
                         help="gunakan HTTP/HTTPS proxy")
    network.add_argument("--skip-proxy", action="store_true",
                         help="lewati penggunakan argument --proxy")

    extractor_group = parser.add_argument_group("Daftar Ekstraktor",
                                                description=(
                                                    f"pilih salah satu dari {len(extractors)} situs berikut:"
                                                ))

    extractor_exclusiveGroup = extractor_group.add_mutually_exclusive_group()
    extractor_exclusiveGroup.add_argument(
        "-a", "--all", help="Gunakan semua ekstraktor yg tersedia,\nhanya menampilkan hasil yang relevan", action="store_true")

    for extractorName, kls in extractors.items():
        extractorName = extractorName.replace("_", "-")
        if hasattr(kls, "host") and getattr(kls, "tag", None):
            pa = urlparse(kls.host)
            added = False
            for fullName in [extractorName, re.sub(r"[aioue-]", "", extractorName)]:
                for index in range(0, len(fullName), 2):
                    for shortName in (fullName[index:index+1], fullName[index:index+2]):
                        shortName = shortName.rstrip("-")
                        try:
                            arg = [f"-{shortName}"]
                            if arg[0] == f"-{extractorName}":
                                arg = [f"--{extractorName}"]
                            else:
                                arg.append(f"--{extractorName}")
                            extractor_exclusiveGroup.add_argument(*arg, action="store_true",
                                                                  help=f"site: {pa.scheme}://{pa.netloc} [{kls.tag}]")
                            added = True
                            break
                        except argparse.ArgumentError:
                            continue
                    if added:
                        break
                if added:
                    break
    return parser
