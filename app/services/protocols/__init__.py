"""API-side Ports — Protocols consumed by services / handlers."""

from .candidate_retriever import CandidateRetriever
from .data_catalog_reader import DataCatalogReader
from .encoder_client import EncoderClient
from .event_repository import EventRepository
from .event_writer import EventWriter
from .feature_fetcher import FeatureFetcher, FeatureRow
from .feedback_recorder import FeedbackRecorder
from .label_repository import LabelRepository
from .lexical_search import LexicalSearchPort
from .metrics_repository import MetricsRepository
from .popularity_scorer import PopularityScorer
from .publisher import NoopPublisher, PredictionPublisher
from .ranking_log_publisher import RankingLogPublisher
from .reranker_client import RerankerClient, RerankerExplainer
from .retrain_queries import RetrainQueries
from .semantic_search import SemanticSearchPort
from .synonym_expander import SynonymExpanderPort
from .training_dataset_repository import TrainingDatasetRepository

__all__ = [
    "CandidateRetriever",
    "DataCatalogReader",
    "EncoderClient",
    "EventRepository",
    "EventWriter",
    "FeatureFetcher",
    "FeatureRow",
    "FeedbackRecorder",
    "LabelRepository",
    "LexicalSearchPort",
    "MetricsRepository",
    "NoopPublisher",
    "PopularityScorer",
    "PredictionPublisher",
    "RankingLogPublisher",
    "RerankerClient",
    "RerankerExplainer",
    "RetrainQueries",
    "SemanticSearchPort",
    "SynonymExpanderPort",
    "TrainingDatasetRepository",
]
