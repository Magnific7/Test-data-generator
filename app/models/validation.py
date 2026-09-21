from dataclasses import dataclass

from pydantic import BaseModel, ValidationError


@dataclass
class ValidationOutcome:
    data: dict
    instance: BaseModel | None
    error: str | None

    @property
    def is_valid(self) -> bool:
        return self.error is None


def validate_records(model_cls: type[BaseModel], records: list[dict]) -> list[ValidationOutcome]:
    """Attempt to build model_cls from each record, capturing pass/fail per record."""
    outcomes = []

    for record in records:
        try:
            instance = model_cls(**record)
            outcomes.append(ValidationOutcome(data=record, instance=instance, error=None))
        except ValidationError as exc:
            summary = "; ".join(
                f"{'.'.join(str(loc) for loc in err['loc']) or '(root)'}: {err['msg']}"
                for err in exc.errors()
            )
            outcomes.append(ValidationOutcome(data=record, instance=None, error=summary))

    return outcomes
