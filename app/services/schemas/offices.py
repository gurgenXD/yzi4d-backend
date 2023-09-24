from pydantic import BaseModel


class OfficeSchema(BaseModel):
    """Схема филиала."""

    id: int
    description: str
    address: str
    work_time: str
    phone: str
    email: str
    main_doctor: str
    main_doctor_work_time: str
    coor_x: str
    coor_y: str

    class Config:
        from_attributes = True


class CitySchema(BaseModel):
    """Схема города."""

    id: int
    name: str
    offices: list[OfficeSchema]

    class Config:
        from_attributes = True
