-- Phase 3 Wave 5-7 event / labeling schema.
-- 既存 ranking_log / feedback_events は back-compat のため残し、
-- search_events / search_impressions / user_actions / ranking_labels を追加する。

DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'action_type_enum') THEN
        CREATE TYPE action_type_enum AS ENUM (
            'click',
            'detail_view',
            'favorite',
            'request_button_click',
            'request_complete',
            'inquiry_complete',
            'contract',
            'bounce'
        );
    END IF;
END $$;

CREATE TABLE IF NOT EXISTS search_events (
    search_id       TEXT PRIMARY KEY,
    user_id         TEXT,
    session_id      TEXT,
    query           TEXT NOT NULL,
    filters_json    JSONB NOT NULL DEFAULT '{}'::jsonb,
    app_version     TEXT,
    model_version   TEXT,
    timestamp       TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS search_events_timestamp_idx ON search_events (timestamp);

CREATE TABLE IF NOT EXISTS search_impressions (
    event_id             BIGSERIAL PRIMARY KEY,
    search_id            TEXT NOT NULL,
    property_id          TEXT NOT NULL,
    rank                 INTEGER NOT NULL,
    lexical_rank_orig    INTEGER,
    semantic_rank_orig   INTEGER,
    lexical_score        REAL,
    vector_score         REAL,
    rrf_score            REAL,
    rerank_score         REAL,
    timestamp            TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE (search_id, property_id)
);

CREATE INDEX IF NOT EXISTS search_impressions_search_idx ON search_impressions (search_id);
CREATE INDEX IF NOT EXISTS search_impressions_property_idx ON search_impressions (property_id);

CREATE TABLE IF NOT EXISTS user_actions (
    event_id       BIGSERIAL PRIMARY KEY,
    search_id      TEXT NOT NULL,
    property_id    TEXT NOT NULL,
    action_type    action_type_enum NOT NULL,
    action_value   REAL,
    timestamp      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE (search_id, property_id, action_type)
);

CREATE INDEX IF NOT EXISTS user_actions_search_idx ON user_actions (search_id);
CREATE INDEX IF NOT EXISTS user_actions_action_type_idx ON user_actions (action_type);

CREATE TABLE IF NOT EXISTS ranking_labels (
    search_id         TEXT NOT NULL,
    property_id       TEXT NOT NULL,
    relevance_label   REAL NOT NULL,
    label_source      TEXT NOT NULL,
    created_at        TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    PRIMARY KEY (search_id, property_id)
);

CREATE INDEX IF NOT EXISTS ranking_labels_search_idx ON ranking_labels (search_id);
