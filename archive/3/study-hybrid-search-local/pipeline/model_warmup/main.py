from __future__ import annotations

import os

from sentence_transformers import SentenceTransformer

from ml.common import get_logger, resolve_sentence_transformer_source

logger = get_logger("pipeline.model_warmup")


def main() -> None:
    model_name = os.environ.get("E5_MODEL_NAME", "intfloat/multilingual-e5-small")
    source = resolve_sentence_transformer_source(model_name)
    model = SentenceTransformer(source)
    logger.info(
        "model_warmup done: model_name=%s source=%s dim=%s",
        model_name,
        source,
        model.get_sentence_embedding_dimension(),
    )


if __name__ == "__main__":
    main()
