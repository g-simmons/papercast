import re
import click
from tinydb.database import TinyDB
# from papercast.process import (

# )
from papercast.publish import (
    get_arxiv_article_properties,
    _check_article_in_db,
    _download_and_upsert_db,
    _get_episode_metadata_from_db,
)
from pathlib import Path
import os
import glob
from tinydb import TinyDB
import json
from jinja2 import Template
from papercast.template import TEMPLATE


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

    with open(project_dir / "template.xml.jinja", "w") as f:
        f.write(TEMPLATE)


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
    help="Path to article TinyDB. By default subfolders are checked for db.json.",
)
@click.option(
    "--xml",
    default=None,
    required=False,
    help="Path to feed XML file. By default subfolders are checked for feed.xml.",
)
@click.option(
    "--dry-run",
    default=False,
    required=False,
    help="Print output instead of writing to file.",
)
def update_xml(db, xml, dry_run):
    if not db:
        db = _find_and_open_db()
    template = _find_and_open_template()
    config = _find_and_open_config()
    episode_meta = _get_episode_metadata_from_db(db,config["base_url"])
    output = template.render(
                episode_meta=episode_meta,
                **config,
                # title=config["title"],
                # base_url=config["base_url"],
                # language=config["language"],
                # xml_link=config["base_url"] + "feed.xml",
                # subtitle=config["subtitle"],
                # copyright=config["copyright"],
                # author=config["author"],
                # email=config["email"],
                # description=config["description"],
                # cover_path=config["cover_path"],
                # categores=config["categories"],
            )
    if dry_run:
        print(output)
    else:
        with open("./feed.xml", "w") as f:
            f.write(output)

def _find_and_open_db():
    db_path = _find_db_path()
    db = TinyDB(db_path)
    return db


def _find_db_path(fname="db.json") -> str:
    globstr = os.path.join(os.getcwd(), "**/", fname)
    results = glob.glob(globstr)
    return results[0]


def _find_and_open_template(fname="template.xml.jinja") -> str:
    globstr = os.path.join(os.getcwd(), "**/", fname)
    results = glob.glob(globstr)
    return Template(open(results[0], "r").read())


def _find_and_open_config(fname="config.json") -> str:
    globstr = os.path.join(os.getcwd(), "**/", fname)
    results = glob.glob(globstr)
    with open(results[0], "r") as f:
        config = json.load(f)
    return config
