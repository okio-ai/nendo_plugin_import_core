from typing import Optional

from nendo import NendoConfig
from pydantic import Field

class ImportCoreConfig(NendoConfig):
    import_folder: Optional[str] = Field(None)

    