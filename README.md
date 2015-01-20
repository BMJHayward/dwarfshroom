Under the file 'pyjsdl-test' is the client-side web version. It's all in one 
file. 

For the pyjsdl version:

Used with pyjamas, pyjsdl and pygame. To transpile into javascript, 
run 'pyjsbuild 'sprite_collect_blocks.py' and pyjs will create the .js version
packaged with the needed js libraries and creates .html pages for you as well.

For the desktop version:

It's split into a few files, though you could have them all in one file if
you like. Simply call it from the command line:

"python sprite_collect_blocks.py"

Both versions need the pygame library (pygame.org), also add your own image 
and audio files in place of the ones I've used.
