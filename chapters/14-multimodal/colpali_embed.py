"""Embed page images and queries with ColSmol (ColPali family) in an ISOLATED env. Used by 14.05.

colpali-engine pins torch<2.14 and peft<0.21, which would downgrade the repo, so it runs on its own (same pattern as Inspect in 10.05):
    uv run --no-project --with colpali-engine --with numpy python colpali_embed.py PAGES_DIR QUERIES.json OUT.npz

Writes multi-vector embeddings: pages (n_pages, max_tokens, 128) + page_lens, queries (n_queries, max_tokens, 128) + query_lens.
"""
import json
import sys
from pathlib import Path

import numpy as np
import torch
from colpali_engine.models import ColIdefics3, ColIdefics3Processor
from PIL import Image

MODEL = "vidore/colSmol-256M"


def pad(embs):
    lens = np.array([len(e) for e in embs])
    out = np.zeros((len(embs), lens.max(), embs[0].shape[1]), dtype=np.float32)
    for i, e in enumerate(embs):
        out[i, : len(e)] = e
    return out, lens


def main(pages_dir, queries_path, out_path):
    device = "mps" if torch.backends.mps.is_available() else "cuda" if torch.cuda.is_available() else "cpu"
    model = ColIdefics3.from_pretrained(MODEL, dtype=torch.bfloat16).to(device).eval()
    proc = ColIdefics3Processor.from_pretrained(MODEL)
    paths = sorted(Path(pages_dir).glob("*.png"))
    pages, queries = [], []
    with torch.no_grad():
        for i in range(0, len(paths), 4):
            batch = proc.process_images([Image.open(p).convert("RGB") for p in paths[i: i + 4]]).to(device)
            out = model(**batch).float().cpu()
            mask = batch["attention_mask"].bool().cpu()
            pages += [o[m].numpy() for o, m in zip(out, mask)]  # drop padding tokens
        for q in json.loads(Path(queries_path).read_text()):
            batch = proc.process_queries([q]).to(device)
            queries.append(model(**batch).float().cpu()[0][batch["attention_mask"][0].bool().cpu()].numpy())
    p, pl = pad(pages)
    q, ql = pad(queries)
    np.savez(out_path, pages=p, page_lens=pl, queries=q, query_lens=ql, names=np.array([p_.name for p_ in paths]))
    print(f"embedded {len(paths)} pages ({pl.mean():.0f} vectors each) and {len(queries)} queries -> {out_path}")


if __name__ == "__main__":
    main(*sys.argv[1:4])
