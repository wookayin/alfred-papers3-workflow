# -*- coding: utf-8 -*-

# papers3.py
# Copyright (c) 2016 Jongwook Choi (@wookayin)

"""
Usage:
    papers3.py <search_query>
"""

from __future__ import print_function
import sys
import workflow

sys.path.append("/System/Library/Frameworks/Python.framework/Versions/2.7/Extras/lib/python/PyObjC")
import applescript

FIELDS = ['citekey', 'title', 'author names',
          'bundle name', 'publication year', 'keyword names']

# Alfred logger
log = None

def read_papers_entries():
    scpt = applescript.AppleScript(
    '''
        tell application "Papers"
            set t to {%s} of every publication item
            return t
        end tell
    ''' % (', '.join(FIELDS)))

    t = scpt.run()
    result = [dict(zip(FIELDS, k)) for k in zip(*t)]
    # result[i] : {'citekey' : ..., 'title' : ..., ...}

    entries = []
    for entry in result:
        title = entry['title']
        if title == applescript.kMissingValue:
            title = ''
        if len(title) > 1 and title[0] == '{' and title[-1] == '}':
            title = title[1:-1]
        entry['title'] = title

        for k in ('publication year', 'author names'):
            if entry[k] == applescript.kMissingValue:
                entry[k] = ''

        if entry['keyword names']:
            keywords = entry['keyword names'].split(',')
            keywords = ['#' + unicode(k).strip() for k in keywords]
            entry['keyword names'] = ' '.join(keywords)

        entries.append(entry)
    return entries


def main(wf):
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('query', default=None, type=str)
    args = parser.parse_args()
    log.debug('args : {}'.format(args))

    items = wf.cached_data('papers_all', read_papers_entries,
                           max_age=600) # cache 600 seconds
    log.debug('Cached {} items from Papers3'.format(len(items)))

    # fuzzy-search by query
    # http://www.deanishe.net/alfred-workflow/user-manual/filtering.html?highlight=match_all
    ret = wf.filter(args.query, items,
                    key=lambda t: (t['title'] + ' ' +
                                   t['author names'] + ' ' +
                                   t['bundle name'] + ' ' +
                                   t['keyword names']),
                    match_on=(workflow.MATCH_ALL ^ workflow.MATCH_ALLCHARS),
                    min_score=20,
                    include_score=True)

    #ret.sort(key=lambda t: t[1], reverse=True)

    if not ret:
        wf.add_item('No matchings', icon=workflow.ICON_WARNING)

    for entry, score, _ in ret:
        title, authors = entry['title'], entry['author names']
        bundle, year = entry['bundle name'], entry['publication year']
        citekey = entry['citekey']
        wf.add_item(title=title,
                    subtitle=authors + (" (%s %s)" % (bundle, year)), #+ (" (%.3f)" % score),
                    modifier_subtitles={
                        'alt' : citekey,
                        'shift' : 'Copy the BibTeX record of ' + citekey,
                    },
                    valid=True,
                    arg=citekey,
                    uid=citekey,
                    type='file',
                    icon='icon.png'
                    )

    wf.send_feedback()
    return 0


if __name__ == '__main__':
    wf = workflow.Workflow()
    log = wf.logger
    sys.exit(wf.run(main))
