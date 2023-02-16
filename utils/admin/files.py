from pathlib import Path
from typing import TYPE_CHECKING
from uuid import uuid4

import aiofiles

from utils.constants import MEDIA_DIR

if TYPE_CHECKING:
    from starlette.datastructures import UploadFile


async def save_file(fields: tuple[str], data: dict, file_dir: str) -> None:
    """Сохранение медиа."""

    file_path = MEDIA_DIR / file_dir
    file_path.mkdir(parents=True, exist_ok=True)

    for field in fields:
        file: "UploadFile" = data.pop(field, None)

        if file.filename:
            filename = str(uuid4()) + "." + file.filename.split(".")[-1]
            async with aiofiles.open(file_path / filename, "wb+") as out_file:
                content = await file.read()
                await out_file.write(content)
                data[field] = str(Path(file_dir) / filename).replace("\\", "/")
