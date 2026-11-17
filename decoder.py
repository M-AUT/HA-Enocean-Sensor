"""EnOcean STM 550B BLE advertisement decoder (AES-128 CCM, 4 byte signature)."""
from __future__ import annotations

import struct
from cryptography.hazmat.primitives.ciphers.aead import AESCCM

MANUFACTURER_ID = 0x03DA


def build_adv(payload: bytes) -> bytes:
    """payload = manufacturer data after company id."""
    return bytes([3 + len(payload), 0xFF, 0xDA, 0x03]) + payload


def verify(key: bytes, address: str, adv: bytes) -> bool:
    addr_le = bytes.fromhex(address.replace(":", ""))[::-1]
    nonce = addr_le + adv[4:8] + b"\x00\x00\x00"
    try:
        tag = AESCCM(key, tag_length=4).encrypt(nonce, b"", adv[:-4])
    except Exception:  # noqa: BLE001
        return False
    return tag == adv[-4:]


def parse(adv: bytes) -> dict:
    seq = struct.unpack("<I", adv[4:8])[0]
    d = adv[8:-4]
    i = 0
    out: dict = {"seq": seq}
    while i < len(d):
        h = d[i]
        i += 1
        size, typ = h >> 6, h & 0x3F
        n = (1, 2, 4)[size] if size < 3 else d[i]
        if size == 3:
            i += 1
        v = d[i : i + n]
        i += n
        if len(v) != n:
            break
        if typ == 0x00:
            out["temperature"] = struct.unpack("<h", v)[0] / 100
        elif typ == 0x02:
            out["energy"] = v[0] / 2
        elif typ == 0x04:
            out["solar_lux"] = struct.unpack("<H", v)[0]
        elif typ == 0x05:
            out["illuminance"] = struct.unpack("<H", v)[0]
        elif typ == 0x06:
            out["humidity"] = v[0] / 2
        elif typ == 0x0A:
            x = struct.unpack("<I", v)[0]
            out["acc_x"] = ((x & 0x3FF) - 512) / 100
            out["acc_y"] = (((x >> 10) & 0x3FF) - 512) / 100
            out["acc_z"] = (((x >> 20) & 0x3FF) - 512) / 100
            out["acc_status"] = x >> 30  # 1 periodic, 2 wake
        elif typ == 0x23:
            out["contact_open"] = v[0] == 1
    return out
