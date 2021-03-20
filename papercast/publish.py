from click.types import Path
import arxiv
from tinydb import TinyDB, Query
import os
from mutagen.mp3 import MP3

def _check_article_in_db(db: TinyDB, article_meta: dict):
    pass


def _validate_doi(arxiv_result):
    try:
        arxiv_result["doi"]
    except:
        raise ValueError(
            """DOI object field must be populated to deposit article to database."""
        )
    return arxiv_result


def get_arxiv_article_properties(arxiv_id):
    return arxiv.query(id_list=[arxiv_id])[0]


def _download_and_upsert_db(db, arxiv_id, overwrite=False):
    doc = {}
    result = get_arxiv_article_properties(arxiv_id)
    doc["title"] = result["title"]
    doc["arxiv_id"] = arxiv_id
    doc["authors"] = result["authors"]

    outpath = arxiv.arxiv.download(result, dirpath="./data/pdfs")

    print(f"Downloaded pdf to {outpath}")
    doc["outpath"] = outpath

    _upsert_db(doc)

    return outpath


def _upsert_db(db, doc, overwrite=True):
    q = Query()
    if not overwrite and db.search(q.doi == doc["doi"]):
        raise KeyError("DOI already exists in database.")
    else:
        db.upsert(doc, q.doi == doc["doi"])


def _get_mp3_size_length(mp3_path: str):
    statinfo = os.stat(mp3_path)
    size = str(statinfo.st_size)

    audio = MP3(mp3_path)
    length = str(audio.info.length)
    return size, length


def _get_episode_metadata_from_db(db, base_url):
    base = Path(base_url)
    episode_meta = []
    for i, doc in enumerate(iter(db)):
        size, length = _get_mp3_size_length(doc["mp3_path"])
        episode_meta.append(
            {
                "title": doc["article_content"]["title"],
                "subtitle": "",
                "description": doc["article_content"]["abstract"],
                "mp3path": str(base / "data/mp3s/" / Path(doc["mp3_path"]).split()[-1]),
                "duration": str(length),
                "season": 1,  # TODO
                "episode": i,  # TODO
            }
        )
    return episode_meta
