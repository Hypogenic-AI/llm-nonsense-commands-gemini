
import urllib.parse

query = '(("jailbreaking" OR "adversarial attacks") AND "interpretability") OR ("nonsense commands" AND "LLM")'
encoded_query = urllib.parse.quote(query)
url = f"http://export.arxiv.org/api/query?search_query={encoded_query}&max_results=20"
print(url)
