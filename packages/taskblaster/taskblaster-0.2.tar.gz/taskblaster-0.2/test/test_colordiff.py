from taskblaster.conflict import highlight_differences, newcolor, oldcolor

string1 = 'orange eggs potato onion apple'
string2 = 'orange bacon potato banana onion'


def test_colordiff():
    import click

    old, new = highlight_differences(string1, string2)
    print(old)
    print(new)

    # First a sanity check:
    assert click.unstyle(old) == string1
    assert click.unstyle(new) == string2

    # The differ arbitrarily colors (or not) each space, so we strip
    # the spaces from this more strict comparison:
    assert old.replace(' ', '') == ''.join(
        ['orange', oldcolor('eggs'), 'potato', 'onion', oldcolor('apple')]
    )

    assert new.replace(' ', '') == ''.join(
        ['orange', newcolor('bacon'), 'potato', newcolor('banana'), 'onion']
    )
