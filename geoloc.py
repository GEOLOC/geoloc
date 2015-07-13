# coding: utf8

import wikipedia
import re
import json




our_language='ca'
wikipedia.set_lang(our_language)
stopwords=['El','La','En', 'Na', 'Els', 'Les', 'L', 'N', 'Un', 'Una', 'Uns', 'Unes', 'De', 'D', 'Es', 'Se', 'A', u'És', 'Avui', 'Aquest', 'Aquesta', 'Aquests', 'Aquestes', 'Tot', 'Tota', 'Tots', 'Totes', 'Mor', 'Fins', 'Nevada', 'Grossa', 'Hola', 'Avui', u'Reunió', 'Trets', 'Sens', 'Posa', 'Clam', 'Cercles', 'Ves', 'Quin', 'Quina', 'Quins', 'Quines', 'Cal', 'Calen', 'Corre', 'Segur', 'Hem', 'Elles', 'Mals', 'Surt', 'Escrita', 'Parlem', 'Diu', 'Las', 'Casos']
connectors=["de", "del", "dels", "d", "el", "la", "els", "les", "l", "n", u"'"]
string_connectors=r" de l\x27| de la | de les | de | del | dels | d\x27"
startwords=['avinguda',u'plaça','carrer','conselleria','departament','ministeri']



def set_lang(x):
    
    global our_language
    our_language=x
    wikipedia.set_lang(our_language)
    
    global stopwords
    global connectors
    global string_connectors
    global startwords
    
    if x=='ca':
        stopwords=['El','La','En', 'Na', 'Els', 'Les', 'L', 'N', 'Un', 'Una', 'Uns', 'Unes', 'De', 'D', 'Es', 'Se', 'A', u'És', 'Avui', 'Aquest', 'Aquesta', 'Aquests', 'Aquestes', 'Tot', 'Tota', 'Tots', 'Totes', 'Mor', 'Fins', 'Nevada', 'Grossa', 'Hola', 'Avui', u'Reunió', 'Trets', 'Sens', 'Posa', 'Clam', 'Cercles', 'Ves', 'Quin', 'Quina', 'Quins', 'Quines', 'Cal', 'Calen', 'Corre', 'Segur', 'Hem', 'Elles', 'Mals', 'Surt', 'Escrita', 'Parlem', 'Diu', 'Las', 'Casos']
        connectors=["de", "del", "dels", "d", "el", "la", "els", "les", "l", "n", u"'"]
        string_connectors=r" de l\x27| de la | de les | de | del | dels | d\x27"
        startwords=['avinguda',u'plaça','carrer','conselleria','departament','ministeri']
    elif x=='es':
        stopwords=['El','La','Los','Las','Un','Una','Unos','Unas','De','Se','A','Es','Este','Esta','Estos','Estas','Todo','Toda','Todos','Todas','Hasta','Nevada','Hola',u'Reunión','Sin','Ve','Cual','Corre','Seguro','Ellas','Ella','Mal','Sal','Escrita','Casos']
        connectors=["de", "del", "el", "la", "los", "las"]
        string_connectors=r" de | del | de los | de la | de las "
        startwords=['avenida','plaza','calle',u'consejería','departamento','ministerio']
    elif x=='en':
        stopwords=['The', 'A','This', 'In', 'That', 'These', 'Those', 'All']
        connectors=["of", 'the', 's', u"'"]
        string_connectors=r" of the | of |\x27s "
        startwords=[]
    elif x=='fr':
        stopwords=['Le','La','Les','L','Un','Une','De','D', 'Du', 'Se', u'À', 'Ce', 'Cet', 'Cette', 'Tout', 'Tous', 'Toute', 'Sans', 'Va', 'Quel', 'Quelle', 'Quels', 'Quelles', 'Il', 'Elle', 'Ils', 'Elles', 'Mals']
        connectors=["de", "du", "des", "d", "le", "la", "les", "l", u"'"]
        string_connectors=r" de l\x27| de la | de | du | des | d\x27"
        startwords=['avenue', 'place','rue', u'départament',u'ministère']
    elif x=='de':
        stopwords=['Der','Die','Das','Ein','Eine','Von','In', 'An', 'Aus', 'Auf', 'Dies','Dieser','Diese','Dieses','Alle','Ganz','Ganze','Ganzer','Ganzes','Welcher','Welche','Welches']
        connectors=["von", "vom", "der", "die", "das", "den", "des"]
        string_connectors=r" von der | von den | vom | von "
        startwords=[]
        
        

def split_words(text):
    return re.findall(r"\w+(?:(?:\xb7|-)\w+)?|(?<=\w)\'(?=\w)", text, flags=re.UNICODE)

def split_sentences(text):
    return re.split(r'\n|  |\. |, |; |\... |: | -|- |\? |\! | \"|\" | \'|\' ', text, flags=re.UNICODE)

def two_parts(text):
    return re.split(string_connectors, text, 1, flags=re.UNICODE)




        
        
class knowledge_dictionary(dict):
    'Common base class for all knowledges that we may use. It inherits the dictionary structure'

    def load_json(self,filename):
        f=open(filename,'r')
        self.update(json.load(f))
        f.close()
        print "Loaded from json"

    def save_json(self,filename):
        f=open(filename,'w')
        json.dump(self, f, indent=2)
        f.close()
        print "Saved to json"
        
    def save_tsv(self,filename):
        f=open(filename,'w')
        for key in self:
            if self[key]==0:
                f.write(key.encode('utf-8')+"\t"+str(0)+"\t"+"\n")
            else:
                f.write(key.encode('utf-8')+"\t"+str(self[key][0])+"\t"+str(self[key][1])+"\t"+"\n")
        f.close()
        print "Saved to tsv"

    def load_tsv(self,filename):
        f=open(filename,'r')
        for line in f:
            entry=line.split("\t")
            if len(entry)==3:
                self[entry[0]]=0
            else:
                self[entry[0]]=[float(entry[1]),float(entry[2])]
        f.close()
        print "Loaded from tsv"
    
    def has_key_add_wiki(self,key):
        if self.has_key(key)==False:
            try:
                coord=wikipedia.page(key,auto_suggest=False).coordinates
                self[key]=[round(coord[0],6),round(coord[1],6)]
            except wikipedia.exceptions.DisambiguationError as e:
                self[key]=0
            except wikipedia.exceptions.PageError as e:
                self[key]=0
            except KeyError as e:
                self[key]=0
            return False
        else:
            return True
            
    def is_place(self,key):
        if self.has_key(key)==True:
            if self[key]==0:
                return False
            else:
                return True
        else:
            raise Exception("Key not in dictionary")
    
            

            
            

def geolocalize(text, knowledge):
    llocs=[]
    sentences=split_sentences(text.decode('utf-8'))
    for sentence in sentences:
        words=split_words(sentence)
        pos=0
        while pos < len(words):
            if (words[pos][0].isupper() or (words[pos] in startwords)):
                if (pos==0 and (words[pos] in stopwords)):
                    pos=pos+1
                    continue
                word=''
                word=words[pos]
                temporal=' '
                pos=pos+1
                while pos < len(words):
                    if words[pos][0].isupper():
                        word=word+temporal+words[pos]
                        temporal=' '
                    elif words[pos] in connectors:
                        if words[pos]==u"'":
                            temporal=temporal[0:-1]+words[pos]
                        else:
                            temporal=temporal+words[pos]+" "               
                    else:
                        break
                    pos=pos+1

                    
                while 1:
                    
                    was=knowledge.has_key_add_wiki(word)
                    
                    if knowledge.is_place(word)==True:
                        if word.encode('utf-8') in llocs:
                            break
                        llocs=llocs+[word.encode('utf-8')]
                        break
                    else:
                        parts=two_parts(word)
                        if len(parts)==1:
                            break
                        word=parts[1]
     
            pos=pos+1        
    return llocs








if __name__=='__main__':
    user_input=raw_input("La llengua seleccionada per defecte és: català.\nWould you like to select another language? [y/n] ")
    if user_input=='y':
        user_input=raw_input("Escriba 'es' para seleccionar español.\nType 'en' to select English.\nEcrivez 'fr' pour choisir français.\nSchreiben Sie 'de', um Deutsch zu wählen.\n")
        if len(user_input)==4:
            user_input=user_input[1:-1]
        try:
            set_lang(user_input)
        except:
            print "Error"
    
    knowledge=knowledge_dictionary()
    user_input=raw_input("Load json knowledge dictionary? [y/n] ")
    if user_input=='y':
        user_input=raw_input("Name of the file containing the dictionary: ")
        knowledge.load_json(user_input)
    
    user_input=raw_input("Would you like to analyze the text contained in a file or do you prefer to introduce a text manually? [file/screen] ")
    if user_input=='file':
        user_input=raw_input("The text must use the utf-8 encoding. Type in the name of the file containing the text you would like to analyze: ")
        user_file=open(user_input, "r")
        text=user_file.read().replace('\n', '  ')
        places=geolocalize(text,knowledge)
    else:
        user_input=raw_input("Type in your text:\n\n")
        places=geolocalize(user_input,knowledge)
    
    print "\nPLACES"
    print "------"
    if len(places)==0:
        print "None"
    for place in places:
        print place
    print ""
    
    user_input=raw_input("Save knowledge to a json file? [y/n] ")
    if user_input=="y":
        user_input=raw_input("Name of the file where you want to save your knowledge: ")
        knowledge.save_json(user_input)

