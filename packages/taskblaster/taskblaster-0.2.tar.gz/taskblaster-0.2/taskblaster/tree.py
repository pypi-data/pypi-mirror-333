from pathlib import Path
from typing import Union

from taskblaster import UNREACHABLE_REF, Node, create_record_for_task
from taskblaster.conflict import ConflictState
from taskblaster.listing import ls_listing
from taskblaster.namedtask import Task
from taskblaster.registry import UNKNOWN_AWAITCOUNT, UNKNOWN_DEPTH
from taskblaster.state import State
from taskblaster.util import absolute, color, is_subpath


def normalize_patterns(repo, directories, relative_to=None):
    if relative_to is None:
        cwd = Path.cwd()
    else:
        cwd = Path(relative_to)

    # XXX What if directories is [], we should not suddenly select everything
    # when user said to select nothing.
    if not directories:
        directories = ['.']

        if not is_subpath(cwd, repo.cache.directory):
            cwd = repo.root

    def patternize(pattern):
        path = absolute(cwd / pattern)
        if path == repo.root:
            path = repo.cache.directory

        relpath = path.relative_to(repo.cache.directory)
        pattern = str(relpath)
        if pattern == '.':
            pattern = '*'  # XXX not very logical
        return pattern

    return [patternize(directory) for directory in directories]


class Tree:
    def __init__(
        self,
        repo,
        directories: Union[list, str],
        states=None,
        relative_to=None,
        failure=None,
        tags=set(),
        sort='name',
    ):
        self.repo = repo

        if isinstance(directories, str):
            directories = [directories]

        # Some of these are actually patterns that we use to glob
        # inside the registry, which is a bit misleading.
        self.directories = normalize_patterns(
            repo, directories, relative_to=relative_to
        )

        self.registry = repo.registry
        self.cache = repo.cache

        if failure is not None and states is None:
            states = {State.fail}

        self.states = states
        self.failure = failure
        self.sort = sort
        self.tags = tags

    def nodes(self):
        return self._nodes(False, set())

    def nodes_topological(self, reverse=False, records=False):
        return self._nodes(
            topological_order=True,
            seen=set(),
            reverse=reverse,
            records=records,
        )

    def _recurse_kin(self, node, seen, reverse=False, records=False):
        if node.name in seen:
            return

        ancestry = self.registry.ancestry
        if reverse:
            kin_names = ancestry.descendants(node.name)
        else:
            kin_names = ancestry.ancestors(node.name)

        for kin_name in kin_names:
            if kin_name in seen:
                continue
            if kin_name == UNREACHABLE_REF:
                continue
            kin = self.registry.index.node(kin_name)
            yield from self._recurse_kin(
                kin, seen, reverse=reverse, records=records
            )

        seen.add(node.name)
        yield node
        if reverse and records:
            if self.registry.contains(node.name + '.record'):
                record_node = self.registry.index.node(node.name + '.record')
                if record_node.name not in seen:
                    yield from self._recurse_kin(
                        record_node, seen, reverse=reverse, records=records
                    )
                    seen.add(record_node.name)

    def submit(self):
        # XXX We need only loop recursively over nodes that are new.
        nodes = [
            node
            for node in self.nodes_topological()
            if (
                node.state == State.new
                and node.awaitcount != UNKNOWN_AWAITCOUNT
                and self.registry.topological_depth[node.name] != UNKNOWN_DEPTH
            )
        ]
        self.registry.index.update_states(
            [node.name for node in nodes], State.queue.value
        )
        return [node.replace(state=State.queue) for node in nodes]

    def _update_conflict(self, oldstate, newstate):
        nodes = [node for node in self.nodes() if node.state != State.new]
        for node in nodes:
            task_name = node.name
            conflict = self.registry.conflict_info(task_name)
            # XXX Surely we need to update it if conflict != newstate, or what?
            if conflict.state.value == oldstate:
                newconflict = conflict.replace(state=ConflictState(newstate))
                self.registry.update_conflict(task_name, newconflict)

    def resolve_conflict(self):
        self._update_conflict('c', 'r')

    def unresolve_conflict(self):
        self._update_conflict('r', 'c')

    def select_unrun(self):
        unrun_cnt = 0
        removed_cnt = 0
        nodes = [
            node for node in self.nodes_topological(reverse=True, records=True)
        ]

        nodes_dct = {node.name: node for node in nodes}

        affected_nodes, records_to_remove = [], []
        for indexnode in nodes:
            encoded_task = self.cache.encoded_task(indexnode.name)

            # XXX change surrounding "node" variable names
            actual_node = self.cache.json_protocol.deserialize_node(
                encoded_task.serialized_input, encoded_task.name
            )
            kwargs = actual_node.kwargs
            implicit_remove = kwargs.get('__tb_implicit_remove__', [])
            reset_record = bool(kwargs.get('__tb_record__'))

            external = kwargs.get('__tb_external__', None)
            indexnode.external = external
            reset_external = False
            if external:
                for name, _ in implicit_remove:
                    if name in nodes_dct:
                        reset_external = True

            to_be_removed = False
            if len(implicit_remove) > 0 and not external:
                for name, _ in implicit_remove:
                    if name in nodes_dct:
                        to_be_removed = True

            if to_be_removed:
                # Now a task will be removed
                # If it has a record, this record also needs to be removed
                records_to_remove.append(indexnode.name + '.record')

            affected_nodes.append(
                (reset_external, reset_record, to_be_removed, indexnode)
            )
            removed_cnt += 1 * to_be_removed
            unrun_cnt += 1 * (not to_be_removed)

        postfix = []
        for (
            reset_external,
            reset_record,
            to_be_removed,
            indexnode,
        ) in affected_nodes:
            if indexnode.name in records_to_remove:
                to_be_removed = True
            postfix.append(
                (reset_external, reset_record, to_be_removed, indexnode)
            )
        affected_nodes = postfix
        cache = self.cache
        registry = cache.registry

        def unrun():
            for (
                reset_external,
                reset_record,
                to_be_removed,
                node,
            ) in affected_nodes:
                name = node.name
                entry = cache.entry(name)
                if not node.external and to_be_removed:
                    cache.delete_nodes([name])
                    continue

                registry.unrun(name)

                if reset_external:
                    UNREACHABLE_KWARGS = {
                        'obj': {
                            '__tb_type__': 'ref',
                            'name': UNREACHABLE_REF,
                            'index': tuple(),
                        }
                    }

                    # XXX This code appears to be untested.
                    # It is probably essential to test it.
                    task = Task(
                        name=name,
                        node=Node('fixedpoint', kwargs=UNREACHABLE_KWARGS),
                        branch='entry',
                        source=registry.sources.get(name),
                        has_record=registry.has_records.get(name, False),
                        tags=registry.resources.get_tags(name),
                    )

                    cache.add_or_update(
                        cache.json_protocol.encode_task(task),
                        force_overwrite=True,
                    )

                if reset_record and to_be_removed:
                    cache.delete_nodes([name])
                elif reset_record:
                    external_node = create_record_for_task(
                        name.split('.record')[0],
                        parent_state='n',
                        cache=cache,
                        output_as='EncodedTask',
                    )

                    cache.add_or_update(external_node, force_overwrite=True)

                # (If we are strict about state <--> files,
                # then we don't always need to talk to the FS.)
                entry.delete()

            return len(nodes)

        return (unrun_cnt, removed_cnt), affected_nodes, unrun

    def remove(self):
        nodes = list(self.nodes_topological(reverse=True, records=True))

        def delete():
            self.cache.delete_nodes([node.name for node in nodes])
            print(f'{len(nodes)} task(s) were deleted.')

        return nodes, delete

    def _nodes(self, topological_order, seen, reverse=False, records=False):
        for directory in self.directories:
            nodes = self.registry.index.glob(
                [directory],
                states=self.states,
                sort=self.sort,
                failure=self.failure,
                tags=self.tags,
            )

            for node in nodes:
                if records and node.name.endswith('.record'):
                    continue
                if node.name in seen:
                    continue

                if topological_order:
                    yield from self._recurse_kin(
                        node, seen, reverse=reverse, records=records
                    )
                else:
                    seen.add(node.name)
                    yield node

    def ls(self, parents=False, *, columns, fromdir=None):
        # each element is either a task or a subdirectory to recurse.
        if fromdir is None:
            fromdir = Path.cwd()

        if parents:
            iternodes = self.nodes_topological()
        else:
            iternodes = self.nodes()

        ls_info = ls_listing(
            cache=self.cache,  # XXX remove treedir (being redundant)
            treedir=self.cache.directory,
            fromdir=fromdir,
            columns=columns,
        )

        return ls_info.to_string(iternodes)

    def stat(self) -> 'Stats':
        return Stats(self.nodes())

    def add_tag(self, tag):
        resources = self.registry.resources
        for node in self.nodes():
            if resources.has_tag(node.name, tag):
                print(f'{node.name} already tagged as {tag!r}')
            else:
                resources.add_tag(node.name, tag)
                print(f'{node.name} tagged as {tag!r}')

    def list_tag(self, tag):
        names = self.registry.resources.select_tag(tag)
        for name in names:
            print(name)

    def untag(self, tag):
        resources = self.registry.resources
        for node in self.nodes():
            if resources.has_tag(node.name, tag):
                resources.untag(node.name, tag)
                print(f'{node.name} untagged as {tag!r}')
            else:
                print(f'{node.name} already not tagged as {tag!r}')

    def list_tags(self):
        alltags = {
            node.name: self.registry.resources.get_tags(node.name)
            for node in self.nodes()
        }

        if not alltags:
            print('There are no tagged tasks.')

        fmt = '{:<24s} {}'
        print(fmt.format('Name', 'Tags'))
        print('─' * 79)
        for name, tags in alltags.items():
            print(fmt.format(name, ' '.join(sorted(tags))))

    def freeze(self, why):
        for node in self.nodes():
            self.registry.freeze(node.name, why)

    def unfreeze(self, why):
        for node in self.nodes():
            self.registry.unfreeze(node.name, why)

    def dry_run(self, rules, echo):
        # Not so efficient because we do not perform a combined
        # query for names.

        # Here we are deciding whether we can run a task or not, but it is
        # actually the query in registry which implements the decision in
        # reality.  So it would be wise for all that code to live e.g.
        # in resources.py

        # REFACTOR: We check whether a task can run here, but also
        # in repository's run_worker() method.
        # Furthermore it would be wise to verify eligibility of tasks
        # picked up by worker.  We could achieve this by consolidating
        # task pickup rules in one place and calling them from all three.

        for node in self.nodes_topological():
            tags = self.registry.resources.get_tags(node.name)
            frozen_why = self.registry.frozentasks.get_tags(node.name)

            unsupported_tags = tags - rules.get_compatible_tags()
            missing_req = rules.required_tags - tags

            if node.awaitcount:
                awaitstate = color(
                    f'awaits:{node.awaitcount}', 'bright_yellow'
                )
            else:
                awaitstate = color('awaits:0', 'bright_green')

            if missing_req:
                tagstring = ' '.join(missing_req)
                conclusion = color(f'Task missing tag: {tagstring}', 'red')
            elif unsupported_tags:
                tagstring = ' '.join(unsupported_tags)
                conclusion = color(f'Worker missing tag: {tagstring}', 'red')
            elif frozen_why:
                frozen_msg = ' '.join(frozen_why)
                conclusion = color(f'Task frozen: {frozen_msg}', 'red')
            elif node.state not in {State.new, State.queue}:
                conclusion = color('Task not new or queued', 'bright_yellow')
            elif node.awaitcount > 0:
                conclusion = color('Dependencies not done', 'bright_yellow')
            else:
                conclusion = color('Ready', 'bright_green')

            echo(
                f'{node.name:30} {node.state.ansiname:16} {awaitstate:18} '
                f'{conclusion}'
            )


class Stats:
    def __init__(self, nodes):
        counts = {state: 0 for state in State}

        for node in nodes:
            counts[node.state] += 1

        self.counts = counts
        self.ntasks = sum(counts.values())

    def tostring(self):
        lines = []
        for state in State:
            num = self.counts[state]
            # The strings are long because of the ANSI codes.
            # Could/should we be able to get the printed string length
            # somehow?
            lines.append(f'{state.ansiname:18s} {num}')
        return '\n'.join(lines)
