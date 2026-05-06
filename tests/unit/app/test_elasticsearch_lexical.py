"""Unit tests for Elasticsearch lexical adapter."""

from __future__ import annotations

from unittest.mock import MagicMock, patch

from app.domain.search import SearchFilters
from app.services.adapters.elasticsearch_lexical import ElasticsearchLexical


def test_elasticsearch_lexical_maps_hits_to_lexical_result() -> None:
    payload = {
        "hits": {
            "hits": [
                {"_id": "p001", "_source": {"property_id": "p001"}},
                {"_id": "p002", "_source": {}},
            ]
        }
    }
    mock_resp = MagicMock()
    mock_resp.raise_for_status = MagicMock()
    mock_resp.json.return_value = payload

    inner = MagicMock()
    inner.post.return_value = mock_resp
    mock_cm = MagicMock()
    mock_cm.__enter__.return_value = inner
    mock_cm.__exit__.return_value = None

    with patch("httpx.Client", return_value=mock_cm):
        lex = ElasticsearchLexical(base_url="http://localhost:9200", index_name="properties")
        out = lex.search(query="test", filters=SearchFilters(), top_k=10)

    assert [r.property_id for r in out] == ["p001", "p002"]
    assert out[0].rank == 1


def test_elasticsearch_lexical_returns_empty_on_exception() -> None:
    mock_resp = MagicMock()
    mock_resp.raise_for_status.side_effect = RuntimeError("upstream failure")

    inner = MagicMock()
    inner.post.return_value = mock_resp
    mock_cm = MagicMock()
    mock_cm.__enter__.return_value = inner
    mock_cm.__exit__.return_value = None

    with patch("httpx.Client", return_value=mock_cm):
        lex = ElasticsearchLexical(base_url="http://localhost:9200", index_name="properties")
        out = lex.search(query="x", filters=SearchFilters(), top_k=5)

    assert out == []
