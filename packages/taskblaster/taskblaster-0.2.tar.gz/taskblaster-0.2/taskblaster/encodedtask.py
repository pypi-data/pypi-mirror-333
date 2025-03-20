from dataclasses import dataclass, replace


@dataclass
class EncodedTask:
    name: str
    serialized_input: str
    parents: tuple[str]
    source: str
    has_record: bool
    tags: set[str]  # or tuple?
    serialized_handlers: str

    def __post_init__(self) -> None:
        # We would be wise to check the parent specification very well.
        # Also, input storage can contain same parent twice, hence set().
        assert self.parents == tuple(sorted(set(self.parents)))
        assert self.has_record is not None
        from taskblaster import TB_STRICT

        if TB_STRICT:
            assert self.source is not None

    def replace(self, **kwargs) -> 'EncodedTask':
        return replace(self, **kwargs)
