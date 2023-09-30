from sqladmin import ModelView

from app.adapters.storage.models.specialists import Specialist, Certificate, Specialization


class SpecializationAdmin(ModelView, model=Specialization):
    """Специальности в админ панели."""

    name = "Specialization"
    name_plural = "Specializations"
    icon = "fa-solid fa-stethoscope"
    category = "Specialists"

    can_edit = False
    can_create = False
    can_delete = False
    can_export = False

    column_list = ("id", "name", "is_active")
    column_labels = {"id": "ID", "name": "Specialization", "specialists": "Specialists", "is_active": "Is active"}
    column_default_sort = [("name", False)]


class SpecialistCertificateAdmin(ModelView, model=Certificate):
    """Сертификаты специалистов в админ панели."""

    name = "Certificate"
    name_plural = "Certificates"
    icon = "fa-solid fa-file-medical"
    category = "Specialists"

    can_edit = False
    can_create = False
    can_delete = False
    can_export = False

    column_list = ("id", "name", "file")
    column_details_exclude_list = ("specialist_id",)
    column_labels = {"id": "ID", "specialist": "Specialist", "name": "Name", "file": "File"}


class SpecialistAdmin(ModelView, model=Specialist):
    """Специалисты в админ панели."""

    name = "Specialist"
    name_plural = "Specialists"
    icon = "fa-solid fa-user-doctor"
    category = "Specialists"

    can_edit = False
    can_create = False
    can_delete = False
    can_export = False

    column_list = ("surname", "name", "patronymic", "id", "on_main", "is_active")
    column_default_sort = [("surname", False)]
    column_searchable_list = ["surname", "name", "patronymic", "id"]
    column_labels = {
        "id": "ID",
        "surname": "Surname",
        "name": "Name",
        "patronymic": "Patronymic",
        "description": "Description",
        "education": "Education",
        "activity": "Activity",
        "titles": "Titles",
        "photo": "Photo",
        "on_main": "On main",
        "is_active": "Is active",
        "can_adult": "Can adult",
        "can_child": "Can child",
        "can_online": "Can online",
        "start_work_date": "Start work date",
        "specializations": "Specializations",
        "certificates": "Certificates",
    }
