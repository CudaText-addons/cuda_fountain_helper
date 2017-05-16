plugin for CudaText.
it gives features for Fountain lexer:

- event on pressing Shift+Enter: it converts cur line to upper-case and inserts a newline.

and commands in "Plugins - Fountain Helper":

- "Find talk of name". 
it finds all character names in cur file, then asks for a name. for entered name, it find all its places and gives menu with these places, to go to that line. enter names as lower- or upper-case (ignored). brackets at the end, e.g. "Edward (V.O.)", are stripped. @name and name^ are handled.

- "Find talk of name under caret". 
it takes name, on separate line, under caret, and shows the dialog like before for this name.

- "Extract talks of name".
it asks for a name, then finds all talks of that name. talks are shown in a new editor tab separated with empty lines. 


author: Alexey T. (CudaText)
license: MIT
