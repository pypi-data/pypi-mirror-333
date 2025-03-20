from django.db import models
from .states import INDIAN_STATES

class StateField(models.CharField):
    def _init_(self, *args, **kwargs):
        kwargs["max_length"] = 2  # Use state code
        kwargs["choices"] = INDIAN_STATES
        super()._init_(*args, **kwargs)