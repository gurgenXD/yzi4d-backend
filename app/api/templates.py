from fastapi.templating import Jinja2Templates

from utils.constants import MAIN_TEMPLATES_DIR
from utils.template_filters.humanize import calculate_ages, humanize_age

TEMPLATES = Jinja2Templates(directory=MAIN_TEMPLATES_DIR)

TEMPLATES.env.filters["calculate_ages"] = calculate_ages
TEMPLATES.env.filters["humanize_age"] = humanize_age
