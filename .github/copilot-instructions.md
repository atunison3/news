# AI Coding Guidelines for News Aggregator

## Architecture Overview
This is a FastAPI-based news feed reader that displays articles from an external SQLite database. Core components:
- **Repository Layer** (`src/repositories/article_repository.py`): Reads `Article` pydantic models from external DB
- **Service Layer** (`src/services/news_service.py`): Business logic for fetching feed
- **Web Layer**: FastAPI routes with Jinja2 templates

Data flow: External DB → ArticleRepository.get_all() → NewsService.get_feed() → Templates

## Key Patterns
- **External DB Reading**: ArticleRepository connects to '/Users/andrewtunison/app_data/new_articles_dev.db' for articles
- **Datetime Handling**: Use `helper_functions.str_to_dt()`/`dt_to_str()` for ISO format conversion (if needed)
- **Filtering**: Apply `should_filter_article()` to feed before display

## Developer Workflows
- **Run App**: `export PYTHONPATH=src; fastapi dev src/main.py`
- **Database**: External SQLite at '/Users/andrewtunison/app_data/new_articles_dev.db'
- **Logging**: Logs to `logs/app.log`; use `setup_logger()` for consistent setup

## Conventions
- **Imports**: Relative imports within `src/`; absolute from project root with `PYTHONPATH=src`
- **Connections**: ArticleRepository manages its own connection to external DB
- **Error Handling**: Wrap operations in try/except; log errors but continue processing
- **Routes**: GET `/news` loads and displays feed
- **Templates**: Extend `base.html`; use Jinja filters like `|unique` for dynamic options

Reference: `src/main.py` for app structure, `src/services/news_service.py` for service patterns, `src/repositories/article_repository.py` for repository examples.