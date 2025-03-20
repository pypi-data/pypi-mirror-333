import json

# We will probably add many clobbering hacks when dataformats need updating.
# This module can contain them.  So far it's just implicit dependency
# clobbering.


def normalize_json(json_text: str) -> str:
    return json.dumps(json.loads(json_text), sort_keys=True)


def can_patch_implicit_dependencies(old_input: str, new_input: str) -> bool:
    old_input = normalize_json(old_input)
    new_input = normalize_json(new_input)

    assert old_input != new_input

    old = json.loads(old_input)
    new = json.loads(new_input)
    assert old[0] == new[0]  # (target should be the same)

    oldkwargs = old[1]
    newkwargs = new[1]
    # We should probably be able to patch both __tb_implicit_remove__ and
    # the regular __tb_implicit__.
    patch_key = '__tb_implicit_remove__'
    if patch_key in newkwargs:
        oldkwargs[patch_key] = newkwargs[patch_key]
    else:
        if patch_key in oldkwargs:
            del oldkwargs[patch_key]

    updated = json.dumps([old[0], oldkwargs], sort_keys=True)

    # We may need to relax this comparison at some point e.g.
    # if we want to patch things that have other changes in them (and
    # keep them as a conflict).
    return updated == new_input


def dangerously_clobber_implicit_dependencies(cache, encoded_task):
    registry = cache.registry
    name = encoded_task.name
    previous_indexnode = registry.index.node(name)
    registry.clear_conflict(name)

    action, indexnode = registry.add_or_update(
        encoded_task,
        force_overwrite=True,
    )

    # The add_or_update() questionably punts the
    # task state to new.  Fix that using low-level hack:
    from taskblaster.state import State

    assert registry.index.node(name).state == State.new
    registry.index.update_state(name, previous_indexnode.state.value)

    # XXX This will error out if awaitcount is botched,
    # it is best if we crash here:
    for desc_indexnode in registry.index.nodes():
        registry.parent_states(desc_indexnode.name)

    assert action == 'update'

    inputfile = cache.entry(indexnode.name).inputfile
    if inputfile.exists():
        inputfile.write_text(encoded_task.serialized_input)
        # Now we should force a database commit because
        # we wrote a file, and we wouldn't want a failure
        # which then causes a rollback so we have written
        # many files that are outdated.
        registry.conn.sneaky_commit()
