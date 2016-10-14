(* given citekey, return the bibtex string of the publication *)
on run argv
    set query to item 1 of argv

    tell application "Papers"
        set b to bibtex string of every publication item whose citekey is query
        return b
    end tell

end run
