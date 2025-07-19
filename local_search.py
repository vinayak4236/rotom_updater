from whoosh.index import open_dir
from whoosh.qparser import QueryParser

def search_local(query):
    ix = open_dir("indexdir")
    with ix.searcher() as searcher:
        parser = QueryParser("content", ix.schema)
        myquery = parser.parse(query)
        results = searcher.search(myquery, limit=1)
        if results:
            return results[0]['content']
        else:
            return "I couldn't find anything in local memory."
