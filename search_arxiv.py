
import arxiv
import json

search = arxiv.Search(
  query = "((\"jailbreaking\" OR \"adversarial attacks\") AND \"interpretability\") OR (\"nonsense commands\" AND \"LLM\")",
  max_results = 20,
  sort_by = arxiv.SortCriterion.Relevance,
  sort_order = arxiv.SortOrder.Descending
)

results = []
for result in search.results():
    results.append({
        "title": result.title,
        "authors": [author.name for author in result.authors],
        "summary": result.summary,
        "arxiv_id": result.entry_id.split('/')[-1],
        "pdf_url": result.pdf_url
    })

print(json.dumps(results, indent=2))
