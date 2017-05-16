plugin for CudaText.
it gives features for Fountain lexer:

- event on pressing Shift+Enter: it converts cur line to upper-case and inserts a newline.

- command in Plugins menu, "Fountain Helper: Find occurences of name". 
it finds all character names in cur file, then asks for a name. for entered name, it find all its places and gives menu with these places, to go to that line. enter names as lower- or upper-case (ignored). brackets at the end, e.g. "Edward (V.O.)", are stripped. @names are handled.


author: Alexey (CudaText)
license: MIT
