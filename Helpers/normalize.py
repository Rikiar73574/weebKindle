import json

def create_manga_overview(title, author, thumbnail, status, url, source, last_chapter):
    manga_overview = {
        "title": title,
        "author": author,
        "thumbnail": thumbnail,
        "status": status,
        "url": url,
        "source": source,
        "last_chapter": last_chapter
    }
    return json.dumps(manga_overview, ensure_ascii=False)