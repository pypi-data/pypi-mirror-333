from taskblaster.clobber import can_patch_implicit_dependencies

old_input = """
[
  "define",
  {"param": 42, "__tb_implicit_remove__":
    [["task-001", {"__tb_type__": "ref", "index": [], "name": "task-001"}],
     ["task-004", {"__tb_type__": "ref", "index": [], "name": "task-004"}]],
  "obj": {"__tb_type__": "ref", "index": [], "name": "task2-004/result"}}
]
"""

new_input = """
[
  "define",
  {"param": 42,
   "__tb_implicit_remove__": [
     ["task-004", {"__tb_type__": "ref", "index": [], "name": "task-004"}]
   ],
   "obj": {"__tb_type__": "ref", "index": [], "name": "task2-004/result"}}
]
"""


def test_clobber_inputs():
    assert can_patch_implicit_dependencies(old_input, new_input)


def test_clobber_inputs_false():
    changed = new_input.replace('"param"', '"otherparam"')
    assert not can_patch_implicit_dependencies(old_input, changed)
