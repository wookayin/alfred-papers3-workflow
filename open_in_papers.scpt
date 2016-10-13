(* given citekey, open the item in Papers3 application *)
on run argv
    set query to item 1 of argv

    tell application "Papers"
        set u to item url of every publication item whose citekey is query
    end tell

    tell application "Finder" to open location u
end run
