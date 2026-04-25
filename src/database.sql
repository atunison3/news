PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS articles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    url TEXT NOT NULL UNIQUE,
    title TEXT NOT NULL,
    source TEXT NOT NULL,
    published_at TEXT,
    first_seen_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    last_seen_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    summary TEXT,
    read_time TEXT,
    content_type TEXT,
    image_url TEXT,
    tags TEXT
);

CREATE TABLE IF NOT EXISTS article_user_state (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    article_url TEXT NOT NULL UNIQUE,
    is_read INTEGER NOT NULL DEFAULT 0 CHECK (is_read IN (0, 1)),
    read_at TEXT,
    vote TEXT CHECK (vote IN ('up', 'down')),
    saved INTEGER NOT NULL DEFAULT 0 CHECK (saved IN (0, 1)),
    archived INTEGER NOT NULL DEFAULT 0 CHECK (archived IN (0, 1)),
    notes TEXT,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (article_url)
        REFERENCES articles(url)
        ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_articles_source
    ON articles(source);

CREATE INDEX IF NOT EXISTS idx_articles_published_at
    ON articles(published_at);

CREATE INDEX IF NOT EXISTS idx_articles_last_seen_at
    ON articles(last_seen_at);

CREATE INDEX IF NOT EXISTS idx_article_user_state_is_read
    ON article_user_state(is_read);

CREATE INDEX IF NOT EXISTS idx_article_user_state_saved
    ON article_user_state(saved);

CREATE INDEX IF NOT EXISTS idx_article_user_state_archived
    ON article_user_state(archived);

CREATE TRIGGER IF NOT EXISTS trg_article_user_state_updated_at
AFTER UPDATE ON article_user_state
FOR EACH ROW
BEGIN
    UPDATE article_user_state
    SET updated_at = CURRENT_TIMESTAMP
    WHERE id = OLD.id;
END;