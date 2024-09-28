from dataclasses import asdict, dataclass


@dataclass(frozen=True, slots=True, kw_only=True)
class BaseDTO:
    @classmethod
    def from_dict(cls, data: dict):
        return cls(**data)

    def to_dict(self) -> dict:
        return asdict(self)

    def clean_dict(self) -> dict:
        data = self.to_dict()
        return {k: v for k, v in data.items() if v is not None}
