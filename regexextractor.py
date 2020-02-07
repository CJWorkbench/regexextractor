import re
from cjwmodule import i18n


def render(table, params):
    col = params['column']
    regex = params['expression']
    newcol = params['newcolumn']

    if not col or not regex or not newcol:
        return table

    try:
        compiled = re.compile(regex)
    except re.error as err:
        return i18n.trans(
            "badParam.regex.invalid", 
            'Invalid regex: {error}',
            {"error": str(err)}
        )

    if not compiled.groups:
        return i18n.trans(
            "badParam.regex.noCapturingGroup", 
            'Your regex needs a capturing group. Add (parentheses).'
        )
    elif compiled.groups > 1:
        return i18n.trans(
            "badParam.regex.tooManyCapturingGroups", 
            'Workbench only supports one (capturing group). '
            'Remove some parentheses, or add "?:" to the beginning '
            'of parentheses for a "(?:non-capturing group)"'
        )

    series = table[col]

    # Ensure series is str, overwriting if needed
    # TODO [adamhooper, 2018-12-19] delete this feature: require str input
    try:
        series.str
    except AttributeError:
        strs = series.astype(str)
        strs[series.isna()] = None
        series = strs

    table[newcol] = series.str.extract(compiled, expand=False)
    return table
