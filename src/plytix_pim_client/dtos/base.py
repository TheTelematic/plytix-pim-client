from dataclasses import asdict, dataclass, fields, field


@dataclass(frozen=True, slots=True, kw_only=True)
class BaseDTO:
    _undocumented_data: dict = field(default_factory=dict)  # Anything inside may change with no notice

    @classmethod
    def from_dict(cls, data: dict, *, include_undocumented=True):
        _fields = fields(cls)
        __fields = [f.name for f in _fields if f.name != "_undocumented_data"]
        filtered_data = {}
        _undocumented_data = {}
        for k, v in data.items():
            if k in __fields:
                filtered_data[k] = v
            elif include_undocumented:
                _undocumented_data[k] = v

        return cls(
            **{"_undocumented_data": _undocumented_data} if include_undocumented else {},
            **filtered_data,
        )

    def to_dict(self) -> dict:
        d = asdict(self)
        d.pop("_undocumented_data")
        return d
