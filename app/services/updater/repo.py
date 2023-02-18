from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.adapters.source import SourceAdapter
    from app.adapters.storage.specialists import SpecialistsAdapter


class RepoUdapterService:
    """Сервис обновления репозитория."""

    def __init__(self, source: "SourceAdapter", specialist: "SpecialistsAdapter") -> None:
        self._source = source
        self._specialist = specialist

    async def update(self) -> None:
        """Обновить данные."""

        specialists = self._source.get_specialists()
        print(specialists)
