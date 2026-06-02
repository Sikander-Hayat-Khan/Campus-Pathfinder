from Core.required_fields import REQUIRED_FIELDS


def find_missing_fields(
    category,
    memory
):

    required = REQUIRED_FIELDS.get(
        category,
        []
    )

    missing = []

    for field in required:

        if not memory.get(field):

            missing.append(field)

    return missing