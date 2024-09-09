import os

from alembic import command
from alembic.config import Config

alembic_cfg = Config("alembic.ini")

migration_path = os.getenv("MIGRATION_PATH")
if migration_path is None:
    raise ValueError("MIGRATION_PATH missing from env vars")

alembic_cfg.set_main_option("script_location", migration_path)

command.upgrade(alembic_cfg, "head")
