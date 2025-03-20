import pathlib
import re
from hakisto import Logger
from pykeepass import PyKeePass
from pykeepass.entry import reserved_keys

logger = Logger("imuthes.keepass")

reserved_keys = set([i.lower() for i in reserved_keys if i not in ("History", "IconID", "Times", "otp")])

URL_RE = re.compile(r"\{.+?}")


class KeePass(PyKeePass):
    def __init__(
        self,
        filename: pathlib.Path,
        password: str,
        keyfile: pathlib.Path = None,
    ):
        super().__init__(filename=filename, password=password, keyfile=keyfile)

    def get(self, path: str | list[str]) -> dict[str, str]:
        """Get Entry as Dict"""
        logger.verbose(f"getting {path}")
        if isinstance(path, str):
            path = path.strip("/").split("/")
        entry = self.find_entries(path=path)
        if not entry:
            raise KeyError("/".join(path))
        result = {k: getattr(entry, k) for k in reserved_keys}
        result.update(entry.custom_properties)
        for k in result:  # resolve internal refs
            if result[k] and result[k].startswith("{REF:"):
                result[k] = entry.deref(k)
        if result["url"]:
            for m in URL_RE.finditer(result["url"]):
                var = m.group()[3:-1] if m.group().startswith("{S:") else m.group()[1:-1].lower()
                if var in result:
                    result["url"] = result["url"].replace(m.group(), result[var])
        return result

    # noinspection PyShadowingBuiltins
    def get_property(self, path: str | list[str], property: str) -> str:
        """Get Property as String"""
        logger.verbose(f'Getting property "{property}" from "{path}"')
        entry = self.get(path=path)
        return entry[property]
