import time
import subprocess
import urllib
import scipdf
from scipdf.pdf import GROBID_URL

def _start_grobid():
    cmd = ["bash", "-c", "./scipdf_parser/serve_grobid.sh"]
    subprocess.Popen(cmd)
    while not _grobid_online():
        time.sleep(1)

def _grobid_online():
    try:
        urllib.request.urlopen(GROBID_URL).getcode()
        return True
    except:
        return False

def get_text_from_dict(article_dict):
    ret = [article_dict["title"], article_dict["abstract"]]
    for section in article_dict["sections"]:
        ret.append(section["heading"])
        ret.append(section["text"])
    return "\n\n".join(ret)

def _get_article_dict(pdf_path):
    try:
        article_dict = scipdf.parse_pdf_to_dict(pdf_path)
    except:
        print("GROBID server not started, starting now...")
        _start_grobid()
        article_dict = scipdf.parse_pdf_to_dict(pdf_path)
    print(f"Parsed pdf at {pdf_path}")
    return article_dict