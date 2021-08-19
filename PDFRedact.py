import os
import os.path
import PySimpleGUI as sg
from PIL import Image
import fitz


image_file = ''
path =''
redactions = dict()
sg.theme('DarkBlue3')



layout = [  [sg.Text('')],
            [sg.Text('File (.pdf)'), sg.Input(size=(80,1),key=1)],
            [sg.Text('Visualizza pagina: '), sg.Input(size=(5,1), key=8), sg.Text('Se non specifichi nulla sarà visualizzata la prima pagina e potrai cambiare manualmente le pagine')],
            [sg.Text('''Salva come: '''), sg.Input(size=(80,1),key=9)],
            [sg.Text('''                      Se non specifichi un nome, il file si chiamerà <nomefile>_redacted.pdf''')],
            [sg.Button('Apri file...'), sg.Button("Redact PDF"), sg.Button("Esci"), sg.Text('                                                                                                 https://github.com/fla-pi')]]


window = sg.Window('PDFRedact', layout)
window2_active = False



while True:
    event, values = window.read()
                
    if event in (None, 'Esci'):
        window.close()
        break
    elif event in (None, 'Apri file...'):
        def browse():
            
            window[8].update('')
            global path
            path = sg.popup_get_file(message = None,
            title='Browse File',
            default_path="",
            default_extension="",
            save_as=False,
            multiple_files=False,
            file_types=(("PDF Files", ".pdf .PDF"),("All Files", ".")),
            no_window=True,
            size=(50, 50),
            button_color=('Black','LightGrey'),
            background_color=('LightGrey'),
            text_color=('Black'),
            icon=None,
            font=None,
            no_titlebar=False,
            grab_anywhere=True,
            keep_on_top=False,
            location=(None, None),
            initial_folder=None)
            window[1].update(path)
            if type(path) == str:
                if len(path) > 0:
                    window[9].update(path[:-4]+'_redacted.pdf')
                else:
                    window[9].update('')
        browse()
    elif event in (None, "Redact PDF"):
        try:
            page_c = values[8]
            outpath = values[9]
            if os.path.exists(outpath):
                    sg.Popup('''Esiste già un file chiamato
    ''' + path[:-4]+'''_redacted.pdf !!
Torna indietro e rinomina l'output o verrà sovrascritto!''', title = 'Attento!')
        
            window2_active = True
            
        except:
            pass

        i = 0
        window3 = None
        
        def redactor():
            try:
                os.remove('PDFCROP_TEMP.png')    
            except:
                pass
            #try:
            global i
            i = i
            if (len(path) > 0):
                if (len(page_c) > 0) and (page_c != '0'):
                    p = int(page_c) - 1
                elif i != 0:
                    p = i
                else:
                    p=0
                doc = fitz.open(path)
                page = doc.loadPage(p)  # number of page
                pix = page.getPixmap()
                output = 'PDFCROP_TEMP.png'
                pix.writePNG(output)
                global image_file
                image_file = output
                image = Image.open(image_file)
                
                image.close()
                pa = doc[p]
                
                sizes = pa.MediaBox #(0.0, 0.0, width, height)
                global width
                width = sizes[2]
                global height
                height = sizes[3]
              
                a, b = 600, 650
                if width > height:
                    a,b = 900,650
            
            #except:
                #pass
        
        
            try:
                column = [
                            [sg.Graph(
                            canvas_size=(width, height),
                            graph_bottom_left=(0, 0),
                            graph_top_right=(width, height),
                            change_submits=True,  
                            drag_submits=True,
                            key="graph")]]
                layout2 = [[sg.Text('''Dopo aver tracciato il rettangolo (uno per pagina), clicca su 'Conferma selezione'
e passa alla prossima pagina per memorizzare. Quando hai finito, premi 'Applica' ''')],
                    [sg.Button('Conferma selezione'), sg.Button('<'), sg.Button('>'), sg.Text("", key="info", size=(28,1)),sg.Button('Applica'), sg.Button('Esci')],
                           
                           [ sg.Column(column, size=(width, height), scrollable=True)]]
            
                
                window2 = sg.Window('PDF Redact', layout2, size= (a,b),resizable=True)
                window2.finalize()
                global window3
                if window3 != None:
                    window3.close()
                
                graph = window2.Element("graph")
                graph.DrawImage(image_file, location=(0, height)) if image_file else None
                dragging = False
                start_point = end_point = prior_rect = None
            
                while True:
                    event1, values1 = window2.read()

                    if event == sg.WIN_CLOSED or event1 in (None, 'Esci'):
                        window2_active = False
                        window2.close()
                        
                        
                        try:
                            os.remove('PDFCROP_TEMP.png')     
                        except:
                            pass
                        break
                    
                    elif event1 in (None, '>'):
                        if i < ((doc.page_count)-1):
                            i +=1
                            window3 = window2
                            redactor()
                        

                    elif event1 in (None, '<'):
                        if i > 0:
                            i = i-1
                            window3 = window2
                            redactor()
                    elif event1 == "graph":
                        x, y = values1["graph"]
                        
                        if not dragging:
                            start_point = (x, y)
                            
                            dragging = True
                        else:
                            end_point = (x, y)
                        if prior_rect:
                            graph.DeleteFigure(prior_rect)
                        if None not in (start_point, end_point):
                            prior_rect = graph.DrawRectangle(start_point, end_point, line_color='blue', fill_color = 'white')
                    elif event1 != None and event1.endswith('+UP'):
                        try:
                            if start_point[1] < end_point[1]:
                                y1 = end_point[1]
                                y2 = start_point[1]
                            else:
                                y1 = start_point[1]
                                y2 = end_point[1]
                            if start_point[0] < end_point[0]:
                                x1 = start_point[0]
                                x2 = end_point[0]
                            else:
                                x1 = end_point[0]
                                x2 = start_point[0]
                           
                            info = window2.Element("info")
                            info.Update(value=" (X1: " + str(x1) + ", Y1: " + str(y1) + "), (X2: " + str(x2) + ", Y2: " + str(y2)+ ")")
                            # enable grabbing a new rect
                            start_point, end_point = None, None
                            dragging = False
                            y_1 = height - y1
                            y_2 = height - y2
                           
                        except:
                            pass
                        
                    elif event1 in (None, 'Conferma selezione'):
                        rect = fitz.Rect(x1, y_1, x2, y_2)
                        redactions[p] = rect
                        #print(redactions)
                    
                    elif event1 in (None, 'Applica'):
                        try:
                            doc = fitz.open(path)
                            red = rect
            
                        except:
                            sg.Popup('''Errore! 
Non hai selezionato un'area da tagliare''' , title = 'Attento!')
                        
                        else:
                            try:
                                for key in redactions:
                                    paginet = doc.loadPage(key)
                                    rect2 = redactions[key]
                                    paginet.add_redact_annot(rect2, text=" ")
                                    paginet.apply_redactions()
                                doc.save(outpath)
                                sg.Popup('''Operazione portata a termine!''' , title = ' ')
    
                            except:
                                sg.Popup('''Errore! 
Il file potrebbe essere danneggiato!''' , title = 'Attento!')
                                pass                
            except:
                pass
        redactor()
    




