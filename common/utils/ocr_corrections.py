import re

PatternType = type(re.compile(""))


def apply_ocr_corrections(text, corrections=None):
    """ This method is available on v32 that was not released in apt packages
    Method copied from stbt repository to use it locally

    Applies the same corrections as `stbt.ocr`'s ``corrections`` parameter.
    This is available as a separate function so that you can use it to
    post-process old test artifacts using new corrections.
    :param str text: The text to correct.
    :param dict corrections: See `stbt.ocr`.
    """
    if corrections:
        text = _apply_ocr_corrections(text, corrections)
    return text


def _apply_ocr_corrections(text, corrections):
    def replace_string(matchobj):
        old = matchobj.group(0)
        new = corrections[old]
        print("ocr corrections: %r -> %r" % (old, new))
        return new

    def replace_regex(matchobj):
        new = corrections[matchobj.re]
        print("ocr corrections: /%s/ -> %r" % (matchobj.re.pattern, new))
        return new

    # Match plain strings at word boundaries:
    pattern = "|".join(
        r"\b(" + re.escape(k) + r")\b" for k in corrections if isinstance(k, basestring)
    )
    if pattern:
        text = re.sub(pattern, replace_string, text)

    # Match regexes:
    for k in corrections:
        if isinstance(k, PatternType):
            text = re.sub(k, replace_regex, text)
    return text
