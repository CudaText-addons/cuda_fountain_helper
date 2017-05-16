plugin for CudaText.
it gives features for Fountain lexer:

- event on pressing Shift+Enter: it converts cur line to upper-case and inserts a newline.

- command in Plugins menu, "Fountain Helper: Find talk of name". 
it finds all character names in cur file, then asks for a name. for entered name, it find all its places and gives menu with these places, to go to that line. enter names as lower- or upper-case (ignored). brackets at the end, e.g. "Edward (V.O.)", are stripped. @names are handled.

- command in Plugins menu, "Fountain Helper: Find talk of name under caret". 
it takes name, on separate line, under caret, and shows the dialog like before for this name.

- command in Plugins menu, "Fountain Helper: Find all names". 
it gives the menu with all character names. for chosen name, it shows the dialog like before.


author: Alexey (CudaText)
license: MIT
