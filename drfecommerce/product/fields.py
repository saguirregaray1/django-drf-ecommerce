from django.db import models
from django.core import checks
from django.core.exceptions import ObjectDoesNotExist


class OrderField(models.PositiveIntegerField):
    description = "Order Field"

    def __init__(self, unique_for_field=None, *args, **kwargs):
        self.unique_for_field = unique_for_field
        super().__init__(*args, **kwargs)

    def check(self, **kwargs):
        return [
            *super().check(**kwargs),
            *self._check_unique_for_field_attribute(**kwargs),
        ]

    def _check_unique_for_field_attribute(self, **kwargs):
        if self.unique_for_field is None:
            return [
                checks.Error("Order field must define a unique_for_field attribute")
            ]
        elif self.unique_for_field not in [
            f.name for f in self.model._meta.get_fields()
        ]:
            return [
                checks.Error(
                    "Order field must define a unique_for_field attribute"
                    + "that is a valid field name"
                )
            ]
        return []

    def pre_save(self, model_instance, add):

        if getattr(model_instance, self.attname) is None:
            qs = self.model.objects.all()
            try:
                query = {
                    self.unique_for_field: getattr(
                        model_instance, self.unique_for_field
                    )
                }
                qs = qs.filter(**query)
                last_item = qs.latest(self.attname)
                value = last_item.order + 1
            except ObjectDoesNotExist:
                value = 1
            return value

        return super().pre_save(model_instance, add)
