import json
from urllib.parse import urlparse, quote_plus
import requests
from .. import LOGGER
from .utils.xtra import _sync_to_async

_BYPASS_CMD_TO_SERVICE = {
    "gdflix": "gdflix",
    "gdf": "gdflix",
    "extraflix": "extraflix",
    "hubcloud": "hubcloud",
    "hc": "hubcloud",
    "hubdrive": "hubdrive",
    "hd": "hubdrive",
    "hubcdn": "hubcdn",
    "hcdn": "hubcdn",
    "transfer_it": "transfer_it",
    "ti": "transfer_it",
    "vcloud": "vcloud",
    "vc": "vcloud",
    "driveleech": "driveleech",
    "dleech": "driveleech",
    "neo": "neo",
    "neolinks": "neo",
    "gdrex": "gdrex",
    "gdex": "gdrex",
    "pixelcdn": "pixelcdn",
    "pcdn": "pixelcdn",
    "extralink": "extralink",
    "luxdrive": "luxdrive",
    "nexdrive": "nexdrive",
    "nd": "nexdrive",
    "hblinks": "hblinks",
    "hbl": "hblinks",
    "vegamovies": "vegamovies",
}

_BYPASS_ENDPOINTS = {
    "gdflix": "https://hgbots.vercel.app/bypaas/gd.php?url=",
    "hubdrive": "https://hgbots.vercel.app/bypaas/hubdrive.php?url=",
    "transfer_it": "https://transfer-it-henna.vercel.app/post",
    "hubcloud": "https://pbx1botapi.vercel.app/api/hubcloud?url=",
    "vcloud": "https://pbx1botapi.vercel.app/api/vcloud?url=",
    "hubcdn": "https://pbx1botapi.vercel.app/api/hubcdn?url=",
    "driveleech": "https://pbx1botapi.vercel.app/api/driveleech?url=",
    "neo": "https://pbx1botapi.vercel.app/api/neo?url=",
    "gdrex": "https://pbx1botapi.vercel.app/api/gdrex?url=",
    "pixelcdn": "https://pbx1botapi.vercel.app/api/pixelcdn?url=",
    "extraflix": "https://pbx1botapi.vercel.app/api/extraflix?url=",
    "extralink": "https://pbx1botapi.vercel.app/api/extralink?url=",
    "luxdrive": "https://pbx1botapi.vercel.app/api/luxdrive?url=",
    "nexdrive": "https://pbx1botsapi2.vercel.app/api/nexdrive?url=",
    "hblinks": "https://pbx1botsapi2.vercel.app/api/hblinks?url=",
    "vegamovies": "https://pbx1botsapi2.vercel.app/api/vega?url=",
}

_LINK_KEYS = ("url", "link", "google_final", "edited", "telegram_file", "gofile_final")

def _bp_srv(cmd):
    return _BYPASS_CMD_TO_SERVICE.get(cmd.lower().lstrip("/"))

def _unwrap(data):
    if isinstance(data, list):
        for i in data:
            if isinstance(i, dict):
                return i
        return {}
    return data if isinstance(data, dict) else {}

def _clean(u):
    return u.rstrip("\\/") if isinstance(u, str) else u

def _extract_url(v):
    if isinstance(v, str) and v.startswith(("http://", "https://")):
        return _clean(v)
    if isinstance(v, dict):
        for k in _LINK_KEYS:
            u = v.get(k)
            if isinstance(u, str) and u.startswith(("http://", "https://")):
                return _clean(u)

def _bp_label_from_key(k):
    return {
        "instant_final": "Instant",
        "cloud_r2": "Cloud R2",
        "zip_final": "ZIP",
        "pixeldrain": "Pixeldrain",
        "telegram_file": "Telegram",
        "gofile_final": "Gofile",
    }.get(k, str(k).replace("_", " ").title())

def _bp_label_from_name(n):
    s = str(n).strip()
    l = s.lower()
    if "[" in s and "]" in s and "download" in l:
        a, b = s.find("["), s.rfind("]")
        if b > a:
            t = s[a + 1 : b].strip()
            if t:
                return t
    if l.startswith("download "):
        return s[8:].strip() or s
    return s

def _bp_links(links):
    if not isinstance(links, dict):
        return "╰╴ No direct links found."
    out = []
    for i, (k, v) in enumerate(links.items()):
        u = _extract_url(v)
        if not u:
            continue
        out.append(
            f"{'╰╴' if i == len(links)-1 else '╞╴'} <b>{k}:</b> <a href=\"{u}\">Click Here</a>"
        )
    return "\n".join(out) if out else "╰╴ No direct links found."

def _bp_norm(data, service):
    data = _unwrap(data)
    root = _unwrap(data.get("final", data))

    title = root.get("title") or root.get("file_name") or data.get("title") or "N/A"
    filesize = root.get("filesize") or root.get("file_size") or data.get("filesize") or "N/A"
    fmt = root.get("format") or root.get("file_format") or data.get("format") or "N/A"

    links = {}

    for src in (root.get("links"), data.get("links")):
        if isinstance(src, dict):
            for k, v in src.items():
                u = _extract_url(v)
                if u:
                    links[_bp_label_from_key(k)] = u

    if not links:
        for k, v in root.items():
            u = _extract_url(v)
            if u:
                links[_bp_label_from_key(k)] = u

    return {
        "title": str(title),
        "filesize": str(filesize),
        "format": str(fmt),
        "links": links,
        "service": service,
    }

async def _bp_info(cmd_name, target_url):
    service = _bp_srv(cmd_name)
    base = _BYPASS_ENDPOINTS.get(service)
    if not service or not base:
        return None, "Bypass endpoint not configured."

    try:
        p = urlparse(target_url)
        if not p.scheme or not p.netloc:
            return None, "Invalid URL."
    except Exception:
        return None, "Invalid URL."

    api_url = base if service == "transfer_it" else f"{base}{quote_plus(target_url)}"

    try:
        resp = await _sync_to_async(
            requests.post if service == "transfer_it" else requests.get,
            api_url,
            json={"url": target_url} if service == "transfer_it" else None,
            timeout=30,
        )
    except Exception as e:
        LOGGER.error(e, exc_info=True)
        return None, "Failed to reach bypass service."

    if resp.status_code != 200:
        return None, "Bypass service error."

    try:
        data = _unwrap(resp.json())
    except json.JSONDecodeError:
        return None, "Invalid response from bypass service."

    if not data:
        return None, "Unexpected response from bypass service."

    if service in ("transfer_it", "hblinks"):
        u = _extract_url(data)
        if not u:
            return None, "File Expired or Not Found"
        return _bp_norm({"links": {"Direct Link": u}}, service), None

    if service == "vegamovies":
        links = {}
        for i in data.get("results", []):
            if not isinstance(i, dict):
                continue
            base = i.get("file_name", "File")
            size = i.get("file_size")
            lbl = f"{base} ({size})" if size else base
            for l in i.get("links", []):
                u = _extract_url(l)
                if u:
                    links[f"{lbl} | {l.get('tag','Link')}"] = u
        if not links:
            return None, "No direct links found."
        return _bp_norm({"title": "Vegamovies Files", "links": links}, service), None

    return _bp_norm(data, service), None
