import os
from pathlib import Path

import pama


class _Config:

    def __init__(self):

        if  os.getenv("PAMAN_ENVIRONMENT", "") != "test":
            Path.home().joinpath(".pama").mkdir(parents=True, exist_ok=True)
            sk_path = Path.home().joinpath(".pama", "sk")

            # Default salt creation.
            if not sk_path.exists():
                sk_path.write_bytes(data=os.urandom(32))

        db_path = Path.home().joinpath(".pama", "database.db") if os.getenv("PAMAN_ENVIRONMENT", "") != "test" \
            else ""  # In memory if test

        self.database_url = f"sqlite+aiosqlite:///{db_path}"
        self.database_engine_kw = dict()

        self.salt = Path.home().joinpath(".pama", "sk").read_bytes() if os.getenv("PAMAN_ENVIRONMENT", "") != "test" \
            else os.urandom(32)




    @property
    def using_sqlite(self) -> bool:
        return self.database_url.startswith("sqlite")

#os.environ["PAMAN_ENVIRONMENT"] = "test"
#print("***",os.getenv("PAMAN_ENVIRONMENT", "a"))
config = _Config()
