from dataclasses import dataclass, asdict


@dataclass(frozen=True, slots=True, kw_only=True)
class BaseDto:
    @classmethod
    def from_dict(cls, data: dict) -> "BaseDto":
        return cls(**data)

    def to_dict(self) -> dict:
        return asdict(self)

    def clean_dict(self) -> dict:
        data = self.to_dict()
        return {k: v for k, v in data.items() if v is not None}