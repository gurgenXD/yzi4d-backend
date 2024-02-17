from pydantic import BaseModel


class OfficeEntity(BaseModel):
    """Сущность филиала."""

    id: int
    description: str
    address: str
    work_time: str
    phone: str
    email: str
    main_doctor: str
    main_doctor_work_time: str
    point_x: float
    point_y: float

    class Config:
        from_attributes = True


class CityEntity(BaseModel):
    """Сущность города."""

    id: int
    name: str
    offices: list[OfficeEntity]

    class Config:
        from_attributes = True
