# TPAK v7 archive format

> Status: **verified** — a reader parses all 588 depot paks
> and extracts `strings.pak` byte-exactly (file sizes match the tables).
> Derived by reading the client's loader (`game.exe`, loader function near
> VA `0x140032b00`; error strings *"Failed to read name register / file table /
> file chunks table for pak"*). Community reports of "TPAK v7" are thereby
> confirmed. Only the format is documented here — no game assets.

## 1. Overview

All integers are little-endian. A pak is a header followed by three
deflate-compressed tables (name register, file table, chunk table) and then the
chunk data. Compression is **raw deflate** (zlib window bits −15, no zlib
header). Each compressed table has its **first dword XOR-ed with a key** before
inflating (a light obfuscation).

```
offset 0   u32  magic            'TPAK' (0x4B415054)
       4   u32  version          7
       8   u32  reserved        0 in all depot paks (loader requires multiple of 16)
      12   u32  N               number of files; also XOR key of table 1
      16   u32  check           0xFFFFFFE3  ((~check)>>2 must equal 7)
      20   u32  U1              uncompressed size of the name register
      24   u32  C1              compressed size of the name register
      28   C1 bytes             name register (raw deflate; first dword ^= N)
  align4
       .   N x u32              permutation (indices of files sorted by name; used for lookup)
       .   u32  C2              compressed size of the file table
       .   C2 bytes            file table  (raw deflate; first dword ^= (C2 + N)); inflates to N*16 bytes
  align4
       .   u32  C3              compressed size of the chunk table
       .   u32  M               number of chunks
       .   C3 bytes            chunk table (first dword ^= (M + C3 + N)); inflates to M*16 bytes (absent if M = 0)
  align4 = data_base
       .   chunk data           chunk i at data_base + chunk[i].data_offset
```

## 2. Tables

### Name register (U1 bytes after inflate)

Sequence of N records: `u32 len`, `len` name bytes, one `0x00` terminator.
Names are **obfuscated**; for record index `idx` (0-based) and byte `j`:

```
k       = (len % 5 + idx) & 0xFF
plain_j = stored_j XOR ((2*(j + len) + k) & 0xFF)
```

Decoded names use backslashes, e.g. `strings\english\string.txt`,
`fonts\font_5_bold_euro_42.tfd`.

### File table (N × 16 bytes)

| Field | Meaning |
|-------|---------|
| u32 `size` | uncompressed file size |
| u32 `name_offset` | offset of the name's characters inside the (decoded) name register |
| u32 `chunk_count` | number of chunks of this file |
| u32 `first_chunk` | index of the first chunk in the chunk table |

### Chunk table (M × 16 bytes)

| Field | Meaning |
|-------|---------|
| u32 `file_offset` | where this chunk's data goes inside the uncompressed file |
| u32 `size` | uncompressed size of the chunk |
| u32 `data_offset` | offset relative to `data_base` |
| u32 `csize` | stored size; `csize == size` ⇒ stored uncompressed, else raw deflate |

Large files are split into chunks (e.g. a 2 MB font data file has 2 chunks).
The loader additionally computes a MurmurHash2-style hash over the three
decoded tables (constant `0x5bd1e995`) — an integrity value, not needed for
reading.

## 3. Verification

A reader written from this description opened **all 588 paks** of the
release build (106 879 files, 20.7 GB unpacked) without error, and file sizes
matched the directory entries (for example `strings.pak` -> 13 `string.txt`
files). A reader should refuse entry names that would escape its output
directory. The archive list is in
[pak-contents.md](../02-inventory/pak-contents.md).

## 4. Writing a pak (not implemented)

Re-packing needs: name obfuscation (self-inverse XOR), per-table first-dword
XOR (self-inverse), raw deflate, and the sorted permutation. The client may
check the hash; verify with the client before relying on repacked paks.

## 5. How the loader was located

The format was derived from the client's loader: the `TPAK` constant and the
loader's error strings in `game.exe` lead to the reading function; its
inflate wrapper (`0x1400455e0`) calls zlib `inflateInit2` with negative
window bits (raw deflate).
