from click.types import Path
import scipdf
from scipdf.pdf import GROBID_URL
import arxiv
from tinydb import TinyDB, Query
import subprocess
import time
import urllib
import os
from mutagen.mp3 import MP3


def _start_grobid():
    cmd = ["bash", "-c", "./scipdf_parser/serve_grobid.sh"]
    subprocess.Popen(cmd)
    while not _grobid_online():
        time.sleep(1)


def get_text_from_dict(article_dict):
    ret = [article_dict["title"], article_dict["abstract"]]
    for section in article_dict["sections"]:
        ret.append(section["heading"])
        ret.append(section["text"])
    return "\n\n".join(ret)


def _grobid_online():
    try:
        urllib.request.urlopen(GROBID_URL).getcode()
        return True
    except:
        return False


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

    doc["title"] = result["title"]
    doc["arxiv_id"] = arxiv_id
    doc["authors"] = result["authors"]

    outpath = arxiv.arxiv.download(results, dirpath="./data/pdfs")

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


def _get_article_dict(pdf_path):
    try:
        article_dict = scipdf.parse_pdf_to_dict(pdf_path)
    except:
        print("GROBID server not started, starting now...")
        _start_grobid()
        article_dict = scipdf.parse_pdf_to_dict(pdf_path)
    print(f"Parsed pdf at {pdf_path}")
    return article_dict


def _parse_to_txt(db, article_dict):
    article_dict = _get_article_dict(pdf_path)
    txt = get_text_from_dict(article_dict)


#     doc['article_content'] = article_dict
#     doc['text'] = txt

#     txtpath = outpath.replace('pdf','txt')

#     with open(txtpath,'w') as f:
#         f.write(txt)
#     print(f'Wrote txt to {txtpath}')


def _say(txtpath):
    aiffpath = txtpath.replace("txt", "aiff")
    cmd = ["say", "-f", txtpath, "-o", aiffpath]
    subprocess.run(cmd)


def _get_mp3_size_length(mp3_path: str):
    statinfo = os.stat(mp3_path)
    size = str(statinfo.st_size)

    audio = MP3(mp3_path)
    length = str(audio.info.length)
    return size, length


def _generate_feed_xml(db, base_url):
    base = Path(base_url)
    for i, doc in enumerate(iter(db)):
        size, length = _get_mp3_size_length(doc["mp3_path"])
        episode_meta = [
            {
                "title": doc["article_content"]["title"],
                "subtitle": "",
                "description": doc["article_content"]["abstract"],
                "mp3path": str(base / "data/mp3s/" / Path(doc["mp3_path"]).split()[-1]),
                "duration": str(length),
                "season": 1,  # TODO
                "episode": i,  # TODO
            }
        ]
