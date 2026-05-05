from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path

from ml.common import generate_run_id, get_logger
from ml.common.config import TrainSettings
from ml.data.loaders.ranker_repository import create_rank_repository

logger = get_logger("pipeline.training_dataset_job")


def run(*, window_days: int = 90, output_root: Path | None = None) -> Path:
    settings = TrainSettings()
    repository = create_rank_repository(settings)
    df = repository.fetch_training_rows(window_days=window_days)
    if "label" in df.columns:
        df = df.rename(columns={"label": "relevance_label"})

    root = output_root or Path("dist/training_datasets")
    output_dir = root / generate_run_id()
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / "training_dataset.csv"
    df.to_csv(output_path, index=False)
    logger.info(
        "training_dataset_job done: rows=%d output=%s generated_at=%s",
        len(df),
        output_path,
        datetime.now(UTC).isoformat(),
    )
    return output_path


def main() -> None:
    run()


if __name__ == "__main__":
    main()
