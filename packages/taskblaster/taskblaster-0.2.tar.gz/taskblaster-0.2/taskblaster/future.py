from taskblaster import Reference
from taskblaster.state import State


def parent_state_info(registry, name):
    indexnode = registry.index.node(name)

    parent_states, okcount = registry.parent_states(name)
    nparents = len(parent_states)

    from taskblaster.registry import UNKNOWN_AWAITCOUNT

    if not (
        indexnode.awaitcount == len(parent_states) - okcount
        or (indexnode.awaitcount == UNKNOWN_AWAITCOUNT)
    ):
        deps_color = 'white:red'
    elif okcount == nparents:
        deps_color = State.done.color
    elif any(state.unsuccessful for state in parent_states.values()):
        deps_color = State.fail.color
    else:
        deps_color = State.new.color

    return okcount, nparents, deps_color


class Future:
    def __init__(self, node, cache):
        self.node = node
        self._cache = cache

    def _tb_pack(self):
        # I think we are not actually calling this except in legacy test.
        # Maybe we can remove it.
        return Reference(self.node.name, index=None)

    @property
    def directory(self):
        return self._entry.directory

    @property
    def _actual_output(self):
        return self._entry.output()

    @property
    def _entry(self):
        return self._cache.entry(self.node.name)

    @property
    def _actual_inputs(self):
        target, namespace = self._cache.load_inputs_and_resolve_references(
            self.node.name
        )
        # assert target == self.node.target
        return namespace

    @property
    def index(self):
        # Reference objects have indices that are tuples.
        # We distinguish ourselves by having an index which is None.
        return None

    def has_output(self):
        return self._entry.has_output()

    @property
    def indexnode(self):
        return self._cache.registry.index.node(self.node.name)

    def describe(self):
        from taskblaster.listing import NodeInfo, TaskListing

        return NodeInfo(
            indexnode=self.indexnode,
            cache=self._cache,
            treedir=self._cache.directory,
            fromdir=self._cache.directory.parent,
            columns=TaskListing.select_columns('sif'),
        ).to_string()
