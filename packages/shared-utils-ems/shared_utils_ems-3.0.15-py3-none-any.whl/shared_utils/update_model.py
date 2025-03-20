# from django.db import models
# from django.utils import timezone
# from rest_framework.exceptions import ValidationError
# from rest_framework.response import Response
# from rest_framework import status


# class NotModifiedError(ValidationError):
#     """Custom exception for unchanged data."""
#     status_code = status.HTTP_204_NO_CONTENT
#     default_detail = "No changes detected. User data remains the same."
#     default_code = "not_modified"


# def model_update(instance, fields, data, auto_updated_at=True):
#     """
#     Generic update service meant to be reused in local update services.

#     For example:

#     def user_update(*, user: User, data) -> User:
#         fields = ['first_name', 'last_name']
#         user, has_updated = model_update(
#             instance=user, fields=fields, data=data)

#         // Do other actions with the user here

#         return user

#     Return value: Tuple with the following elements:
#         1. The instance we updated.
#         2. A boolean value representing whether we performed an update or not.

#     Some important notes:

#         - Only keys present in `fields` will be taken from `data`.
#         - If something is present in `fields` but not present in `data`, we simply skip.
#         - There's a strict assertion that all values in `fields` are actual fields in `instance`.
#         - `fields` can support m2m fields, which are handled after the update on `instance`.
#         - If `auto_updated_at` is True, we'll try bumping `updated_at` with the current timestmap.
#     """

#     has_updated = False
#     m2m_data = {}
#     update_fields = []

#     model_fields = {field.name: field for field in instance._meta.get_fields()}

#     for field in fields:
#         if field not in data:
#             continue

#         model_field = model_fields.get(field)

#         if model_field is None:
#             raise ValidationError(
#                 {field: f"'{field}' is not a valid field for {instance.__class__.__name__}."}
#             )

#         if isinstance(model_field, models.ManyToManyField):
#             m2m_data[field] = data[field]
#             continue

#         if getattr(instance, field) != data[field]:
#             has_updated = True
#             update_fields.append(field)
#             setattr(instance, field, data[field])

#     if not has_updated:
#         raise NotModifiedError()

#     if auto_updated_at and "updated_at" in model_fields:
#         if "updated_at" not in update_fields:
#             update_fields.append("updated_at")
#             instance.updated_at = timezone.now()

#     instance.full_clean()
#     instance.save(update_fields=update_fields)

#     for field_name, value in m2m_data.items():
#         related_manager = getattr(instance, field_name)
#         related_manager.set(value)

#         has_updated = True

#     return instance


from django.db import models
from django.utils import timezone
from rest_framework.exceptions import ValidationError


def model_update(instance, fields, data, auto_updated_at=True):
    """
    Safely update a Django model instance with validation.

    - Ensures only valid fields are updated.
    - Skips updating unchanged values.
    - Properly handles ManyToMany relationships.
    - Auto-updates 'updated_at' field if enabled.
    """

    model_fields = {field.name: field for field in instance._meta.get_fields()}
    has_updated = False
    m2m_data = {}
    update_fields = []

    # Check if any provided field is invalid
    # invalid_fields = [field for field in fields if field not in model_fields]
    # if invalid_fields:
    #     raise ValidationError(
    #         {"invalid_fields":
    #             f"These fields are invalid: {', '.join(invalid_fields)}"}
    #     )

    for field in fields:
        if field not in data:
            continue

        model_field = model_fields[field]

        if model_field == field:
            raise ValidationError(
                {field: f"'{field}' is not a valid field for {instance.__class__.__name__}."})

        if isinstance(model_field, models.ManyToManyField):
            m2m_data[field] = data[field]
            continue

        if getattr(instance, field) != data[field]:
            setattr(instance, field, data[field])
            update_fields.append(field)
            has_updated = True

    if not has_updated and not m2m_data:
        return None  # No changes detected

    if has_updated:
        if auto_updated_at:
            if "updated_at" in model_fields and "updated_at" not in update_fields:
                update_fields.append("updated_at")
                instance.updated_at = timezone.now()

    instance.full_clean()
    instance.save(update_fields=update_fields)

    for field_name, value in m2m_data.items():
        related_manager = getattr(instance, field_name)
        related_manager.set(value)
        has_updated = True

    return instance if has_updated else None
