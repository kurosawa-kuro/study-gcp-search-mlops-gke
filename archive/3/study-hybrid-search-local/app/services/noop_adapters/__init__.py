"""Phase 3 — production noop / in-memory adapters.

これは「テスト用」ではなく「production 環境で adapter が disabled なときの fallback」。
test stubs は `tests/_fakes/` 側に分離されている。
"""

from .noop_event_repository import NoopEventRepository
from .noop_event_writer import NoopEventWriter
from .noop_feedback_recorder import NoopFeedbackRecorder
from .noop_label_repository import NoopLabelRepository
from .noop_lexical_search import NoopLexicalSearch
from .noop_property_repository import NoopPropertyRepository
from .noop_ranking_log_publisher import NoopRankingLogPublisher
from .noop_search_cache import NoopSearchCache
from .noop_synonym_expander import NoopSynonymExpander

__all__ = [
    "NoopFeedbackRecorder",
    "NoopEventRepository",
    "NoopEventWriter",
    "NoopLabelRepository",
    "NoopLexicalSearch",
    "NoopPropertyRepository",
    "NoopRankingLogPublisher",
    "NoopSearchCache",
    "NoopSynonymExpander",
]
