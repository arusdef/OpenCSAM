import re


CONTENTS = ['table of contents', 'contents']
RECOMMENDATIONS = ['recommendations', 'detailed recommendations', 'general recommendations']
SUMMARY = ['executive summary', 'management summary', 'summary', 'conclusions', 'preface']


def remove_multiple_empty_lines(s):
    """Remove multiple empty lines.

    The pdf documents contain a lot of whitespace. This function removes multiple empty lines.
    The idea is to keep at most two consecutive newline characters because
    two consecutive newline characters will be used to split the text into an array of paragraphs.
    """

    return re.sub(r'\n(\n)+', r'\n\n', s, flags=re.MULTILINE)


def is_whitespace(s):
    """Returns true if the string consists of whitespace characters only."""
    return bool(re.match("^\s+$", s)) | (len(s) == 0)


def to_paragraphs(s):
    """Split the text of the document into paragraphs."""
    ps = remove_multiple_empty_lines(s).split('\n\n')
    return [p for p in ps if not is_whitespace(p)]


def to_lines(s):
    """Split the text of the document into lines."""
    ps = remove_multiple_empty_lines(s).split('\n')
    return [p for p in ps if not is_whitespace(p)]


def is_title(s):
    """Returns true if the string is a chapter title.

    Any string starting with a number is considered a title if it does not contain a URL.
    Apart from such strings, we also check for common titles that often appear in the pdf documents
    and are not preceded with any chapter number.
    """

    common_titles = CONTENTS + RECOMMENDATIONS + SUMMARY + [
        'about ENISA', 'contact details', 'credits', 'acknowledgements', 'legal notice',
        'glossary', 'annex', 'appendix']
    for ct in common_titles:
        # if bool(re.match("^[0-9,.]*\s*{}".format(ct), s.lower())):
        # Ignore subsections.
        if bool(re.match("^[0-9]*[.]*\s*{}".format(ct), s.lower())):
            return True

    return (
        # bool(re.match("^[0-9,.]+\s+\S+", s)) and
        # Ignore subsections.
        bool(re.match("^[0-9]+[.]*\s+\S+", s)) and
        # Ignore URLs.
        not bool(re.match(r'.*\s+\bhttp\S+', s)))


def strip_title(s):
    title = s.lower().strip()

    # Remove whitespace and anything beyond ...
    i = title.find("...")
    if i > -1:
        title = title[:i].strip()

    # Remove page number at the end.
    title = re.compile("([0-9]+|[ivxlcdm]+)$").sub("", title).strip()

    # Remove the section number at the beginning
    #title = re.compile("^[0-9,.]+\s+").sub("", title).strip()

    return title


def get_titles(ps, found_table_of_contents, stop_on_duplicates):
    """Find chapter titles.

    Parameters:
        found_table_of_contents: If true, the chapter title search will start from the beginning of the document,
            i.e. as if the table of contents have been found already.
            If false, the chapter title search will start after the table of contents are found.
        stop_on_duplicates: If true, the chapter title search will stop once duplicate titles are found.
            This usually appears once the actual titles start appearing after the listing in the table of contents.
            Note that duplicates will never be returned.
            This flag is introduced only to avoid getting false titles from the body text.

    Returns:
        List of unique chapter titles.
    """

    titles = list()
    for p in ps:
        if is_title(p):
            title = strip_title(p)

            if title in CONTENTS:
                found_table_of_contents = True

            # If found_table_of_contents == True,
            # start adding titles to the list once the table of contents section starts.
            if found_table_of_contents:
                # If stop_on_duplicates == True,
                # stop searching for chapter titles once duplicates are detected after the table of contents.
                # We assume that once a duplicate appears, we are already beyond the table of contents section,
                # in the first chapter of the document.
                # This is to protect against getting false titles identified in the body text.
                if title in titles and stop_on_duplicates:
                    break
                if not title in titles:
                    titles.append(title)
    return titles


def has_table_of_contents(titles):
    """Returns true if a table of contents appears among the titles."""
    for key in titles:
        # Remove the section number at the beginning
        key_without_number = re.compile("^[0-9,.]+\s+").sub("", key).strip()
        if key_without_number in CONTENTS:
            return True
    return False


def get_chapters(ps, titles):
    """Returns a dictionary with the chapter titles as keys and the chapter text as values."""
    chapter_start = list()
    for i, p in enumerate(ps):
        # Apply the changes that are used for the titles to every paragraph.
        # This is necessary because we will be comparing every paragraph to the titles.
        s = strip_title(p)

        if s in titles:
            chapter_start.append(i)

    chapter_end = [i for i in chapter_start[1:]]
    chapter_end.append(len(ps))

    chapters = dict()
    for start, end in zip(chapter_start, chapter_end):
        title = strip_title(ps[start])
        text = "\n\n".join(ps[start:end])
        if title in chapters.keys():
            chapters[title] += "\n" + text
        else:
            chapters[title] = text

    return chapters


def get_recommendations(chapters):
    keys = chapters.keys()
    s = ""
    for key in keys:
        # Remove the section number at the beginning
        key_without_number = re.compile("^[0-9,.]+\s+").sub("", key).strip()
        if key_without_number in RECOMMENDATIONS:
            s += chapters[key]
    return s


def get_summary(chapters):
    keys = chapters.keys()
    s = ""
    for key in keys:
        # Remove the section number at the beginning
        key_without_number = re.compile("^[0-9,.]+\s+").sub("", key).strip()
        if key_without_number in SUMMARY:
            s += chapters[key]
    return s


def add_chapter_fields(df, paragraphs=True, found_table_of_contents=True, stop_on_duplicates=False):
    """Take a dataframe with plain text and add fields related to the chapters."""
    def add_columns(x):
        if paragraphs:
            ps = to_paragraphs(x['text'])
        else:
            ps = to_lines(x['text'])
        titles = get_titles(ps, found_table_of_contents, stop_on_duplicates)
        x['chapter_titles'] = titles
        x['num_chapters'] = len(titles)
        x['has_table_of_contents'] = has_table_of_contents(titles)
        chapters = get_chapters(ps, titles)
        summary = get_summary(chapters)
        x['summary'] = summary
        x['has_summary'] = (summary != '')
        recommendations = get_recommendations(chapters)
        x['recommendations'] = recommendations
        x['has_recommendations'] = (recommendations != '')
        x['all_chapters'] = '\n\n'.join(list(chapters.values()))
        return x
    return df.apply(add_columns, axis=1)