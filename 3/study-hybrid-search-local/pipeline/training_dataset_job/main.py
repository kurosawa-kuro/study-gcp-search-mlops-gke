from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path

from ml.common import generate_run_id, get_logger
from ml.common.config import TrainSettings
from ml.data.loaders import PostgresRankerRepository

logger = get_logger("pipeline.training_dataset_job")


def main() -> None:
    settings = TrainSettings()
    repo = PostgresRankerRepository(dsn=settings.postgres_dsn)
    df = repo.read_training_data()
    run_id = generate_run_id()
    root = Path(settings.model_artifacts_root)
    output_dir = root / "datasets" / run_id
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / "training_dataset.csv"
    df.to_csv(output_path, index=False)
    logger.info(
        "training_dataset_job done: rows=%d output=%s generated_at=%s",
        len(df),
        output_path,
        datetime.now(UTC).isoformat(),
    )


if __name__ == "__main__":
    main()
