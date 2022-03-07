# HeaderRemover For COMP30027
a very simple header remover , designed only for Dr.Ding's version, COMP30027ML, UOM 2022-SEM1

workflow:
Convert PDF to images ->
Traverse harded-coded image area px by px ->
replace px with pointed color to blank ->
combine processed images into new PDF.

please install the following dependencies before use:
Pillow, pathlib, pdf2image
```
pip install pillow
pip install pathlib
pip install pdf2image
```
