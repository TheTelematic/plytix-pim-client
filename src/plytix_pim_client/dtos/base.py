from dataclasses import asdict, dataclass, fields, field


@dataclass(frozen=True, slots=True, kw_only=True)
class BaseDTO:
    _undocumented_data: dict = field(default_factory=dict)  # Anything inside may change with no notice

    @classmethod
    def from_dict(cls, data: dict):
        _fields = fields(cls)
        __fields = [f.name for f in _fields if f.name != "_undocumented_data"]
        filtered_data = {}
        _undocumented_data = {}
        for k, v in data.items():
            if k in __fields:
                filtered_data[k] = v
            else:
                _undocumented_data[k] = v

        return cls(_undocumented_data=_undocumented_data, **filtered_data)

    def to_dict(self) -> dict:
        return asdict(self)

    def clean_dict(self) -> dict:
        data = self.to_dict()
        return {k: v for k, v in data.items() if v is not None}
