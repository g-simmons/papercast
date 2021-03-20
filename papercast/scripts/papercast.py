import re
import click
from tinydb.database import TinyDB
from papercast.utils import (
    get_arxiv_article_properties,
    _check_article_in_db,
    _download_and_upsert_db,
)
from pathlib import Path
import os
import glob
from tinydb import TinyDB


@click.group()
def papercast():
    pass


def _safe_mkdir(dir, force: bool) -> None:
    if not os.path.isdir(dir):
        if not force:
            raise ValueError("Project already exists")
        else:
            raise NotImplementedError("Force overwrite not implemented")
    else:
        dir.mkdir()


@papercast.command()
@click.option("--project-name", default="papercast")
@click.option("--force", default=False)
def init(project_name, force):
    cwd = Path(os.getcwd())
    project_dir = cwd / project_name
    _safe_mkdir(project_dir)
    for sub in ["pdfs", "mp3s"]:
        subdir = project_dir / sub
        _safe_mkdir(subdir)


@papercast.command()
@click.option("--arxiv-id", default=None, required=True)
@click.option("--pdf-dir", default=None, required=False)
@click.option("--overwrite", default=False, required=False)
def add(arxiv_id, pdf_dir, overwrite):
    db = _find_and_open_db()
    article_meta = get_arxiv_article_properties(arxiv_id)
    if _check_article_in_db(db, article_meta):
        raise KeyError("Article already in DB")
    else:
        _download_and_upsert_db(db, arxiv_id, overwrite)


@papercast.command()
@click.option(
    "--db",
    default=None,
    required=False,
    help="Path to article TinyDB. By default subfolders are checked for db.json",
)
@click.option(
    "--xml",
    default=None,
    required=False,
    help="Path to feed XML file. By default subfolders are checked for feed.xml",
)
def update_xml(db, xml):
    if not db:
        db = _find_and_open_db()
    if not xml:
        xml = _find_xml()


def _find_and_open_db():
    db_path = _find_db_path()
    db = TinyDB(db_path)
    return db


def _find_db_path(fname="db.json") -> str:
    globstr = os.path.join(os.getcwd(), "**/", fname)
    results = glob.glob(globstr)
    return results[0]


def _find_xml(fname="feed.xml") -> str:
    globstr = os.path.join(os.getcwd(), "**/", fname)
    results = glob.glob(globstr)
    return results[0]
