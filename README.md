# PDFRedact
Programma in Python che permette di applicare manualmente la redaction a file PDF con una o più pagine.
Basato sul codice di https://github.com/fla-pi/PDFCropandSplit.

## Istruzioni per l'installazione
Per utilizzare lo **script Python**, installare le dipendenze:
```
PySimpleGUI
PyMuPDF
Pillow
```
può essere fatto installandole direttamente da requirements.txt:

```
python pip install -r requirements.txt
```
Per l'utilizzo su macOS potrebbe essere necessario installare differentemente PyMuPDF:
```
brew install mupdf swig freetype
pip install https://github.com/pymupdf/PyMuPDF/archive/master.tar.gz
```
## Utilizzo
Aprire il file PDF e in caso non si voglia aprire la prima pagina, specificare il numero di pagina da visualizzare. Altrimenti sarà possibile navigare con i tasti "<" e ">" tra le pagine.
Sulla pagina corrente tracciare il rettangolo della zona da cancellare (uno per pagina), poi premere 'Conferma selezione' e passare eventualmente alla pagina successiva. Al termine della selezione di tutte le zone da nascondere, premere 'Applica' e verrà generato un file <nomefile>_redacted.pdf con tutte le correzioni applicate.
