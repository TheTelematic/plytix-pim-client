from dataclasses import asdict, dataclass, fields


@dataclass(frozen=True, slots=True, kw_only=True)
class BaseDTO:
    @classmethod
    def from_dict(cls, data: dict):
        _fields = fields(cls)
        filtered_data = {k: v for k, v in data.items() if k in [f.name for f in _fields]}
        return cls(**filtered_data)

    def to_dict(self) -> dict:
        return asdict(self)

    def clean_dict(self) -> dict:
        data = self.to_dict()
        return {k: v for k, v in data.items() if v is not None}
