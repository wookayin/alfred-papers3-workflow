# -*- coding: utf-8 -*-

# papers3.py
# Copyright (c) 2016 Jongwook Choi (@wookayin)

"""
Usage:
    papers3.py <search_query>
"""

from __future__ import print_function
import os.path
import pybtex.database
import sys
import workflow

# Alfred logger
log = None

# The bibtex file automatically exported from Papers 3 (in a virtual volume)
# TODO: write an applescript to directly query Papers to get the full metadata
PAPERS_LIBRARY = r'/Volumes/Papers Library/All Papers/Ω Export/All Papers.bib'

def read_bibtex():
    if not os.path.isfile(PAPERS_LIBRARY):
        raise RuntimeError('Cannot access to Papers Library. Check Papers3 application settings.')

    with open(PAPERS_LIBRARY, 'r') as f:
        bib = pybtex.database.parse_file(f)

    def _strauthor(p):
        return ' '.join(list(p.first_names) + list(p.last_names))

    for bibkey, entry in bib.entries.iteritems():
        title = entry.fields['title']
        if title[0] == '{' and title[-1] == '}':
            title = title[1:-1]

        try:
            authors = [_strauthor(p) for p in entry.persons['author']]
        except KeyError:
            authors = []

        yield bibkey, title, authors


def main(wf):
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('query', default=None, type=str)
    args = parser.parse_args()
    log.debug('args : {}'.format(args))

    items = list(read_bibtex())

    # search by query
    ret = wf.filter(args.query, items,
                    key=lambda t: ' '.join([t[1]] + t[2]),
                    min_score=10,
                    include_score=True)
    #ret.sort(key=lambda t: t[1], reverse=True)

    if not ret:
        wf.add_item('No matchings', icon=workflow.ICON_WARNING)

    for (key, title, authors), score, _ in ret:  # subset of cached_items
        wf.add_item(title, ', '.join(authors),
                    valid=True,
                    arg=key,
                    uid=key,
                    type='file',
                    icon='icon.png'
                    )

    wf.send_feedback()
    return 0


if __name__ == '__main__':
    wf = workflow.Workflow()
    log = wf.logger
    sys.exit(wf.run(main))
