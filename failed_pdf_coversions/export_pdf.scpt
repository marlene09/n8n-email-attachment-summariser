-- save as export_pdf.scpt
set pdfPath to "/Users/marlenepostop/Documents/n8n-agent/old.pdf"
set exportFolder to "/Users/marlenepostop/Documents/n8n-agent/pdf_pages/"

tell application "Finder"
    if not (exists folder exportFolder) then
        make new folder at (POSIX file "/Users/marlenepostop/Documents/n8n-agent/") with properties {name:"pdf_pages"}
    end if
end tell

tell application "Preview"
    activate
    open POSIX file pdfPath
    delay 2 -- wait for PDF to load
    
    set theDocs to documents
    set theDoc to item 1 of theDocs
    
    set pageCount to count of pages of theDoc
    repeat with i from 1 to pageCount
        set exportPath to exportFolder & "page_" & i & ".jpg"
        save page i of theDoc in POSIX file exportPath as JPEG
    end repeat
    
    close theDoc
end tell
