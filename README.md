Alfred Papers3 Workflow
=======================

This is an Alfred 3 workflow to search Papers3 items. Still experimental :-)

[Download at Here](https://github.com/wookayin/alfred-papers3-workflow/releases)

![Papers3 Workflow](https://raw.github.com/wookayin/alfred-papers3-workflow/master/screenshots/search.png)


Features
--------

Usage: `pp <query>`

- Search for papers in Papers3 Library, by title and authors (fuzzy matching)
- Open the selected item in Papers3.app
- Copy citekey or BibTeX strings into the clipboard
    - Select the item with the modifier `<alt>` to copy citekey
    - Select the item with the modifier `<shift>` to copy BibTeX strings

TODO
----

- [x] Make it faster (currently, querying is too slow), and support cache
- [ ] Better ranking and string matchers (e.g. exact match doesn't show up)
- [x] Fix applescript import issue

Authors
-------

Jongwook Choi (@wookayin)


License
-------

MIT
