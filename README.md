Geoloc
=========

Geoloc is a python package that identifies the places mentioned in a given text.

Dependencies
----
This software uses the following packages: wikipedia, re and json. They can be installed from the terminal with the commands:

```bash
	$ pip install wikipedia
	$ pip install re
	$ pip install json
```

Installation
----
Geoloc does not require any installation. Save the file geoloc.py in the folder where you want to use it.


Usage
----
Three possibilities:

### 1. On a terminal ###
Run ```python geoloc.py``` in your terminal and follow the on-screen instructions. As the program analyzes text, it saves all the expressions that it comes across in a dictionary, that we call knowledge. The created knowledge can be saved in json format after running the program. A json knowlege file can also be loaded before analyzing text.

### 2. On a GUI ###

The following packages are needed: spyre, pandas. Run the following commands on a terminal to install them:
```bash
	$ pip install spyre
	$ pip install pandas
```

To launch the app run python geoapp.py on a terminal. The output will indicate where the app is being served. Look for something like this:
```bash
	>>> ENGINE Serving on http://127.0.0.1:8080
```
Copy this address to a web browser. The script automatically checks whether there is a json knowledge file named ‘knowledge_xx.json’, where xx denotes the language code (ca for Catalan, es for Spanish, en for English, fr for French and de for German). If such a file exists, the program will load it. Otherwise an empty dictionary will be created. The new knowledge will not be saved.

### 3. Imported as a package ###

The file geoloc.py must be in the working directory. Import it as a package with
```python
import geoloc
```

The knowledge_dictionary class inherits the python dictionary structure and includes news methods to load, save and add information as needed during the execution of the program. Run
```python
knowledge=geoloc.knowledge_dictionary()
```
to create a dictionary for the knowledge to be stored.

New functions:
```python
knowledge.load_json(filename)
knowledge.load_tsv(filename)
knowledge.save_json(filename)
knowledge.load_tsv(filename)
```
- knowledge.load_json(filename) loads a json knowledge file to your dictionary. Previous information will be erased. To avoid that use knowledge.update(old_dictionary) function.
- knowledge.load_tsv(filename) loads a tsv.
- knowledge.save_json(filename) saves your dictionary to a json knowledge file.
- knowledge.save_tsv(filename) saves your dictionary to a tsv file.

Run
```python
geoloc.set_lang(‘xx’)
```
to set the language to be used, where xx denotes the language code (ca for Catalan, es for Spanish, en for English, fr for French and de for German). The default language is catalan.

Run
```python
geolocalize(text,knowledge)
```
to analyze a given text. This functions returns a python list with all the geolocating expressions found in the text. A knowledge must be provided, even if it is an empty one. The new words are searched in wikipedia and stored in knowledge.



Examples
----

```python
import geoloc
knowledge=geoloc.knowledge_dictionary()
knowledge.load_json(“knowledge_ca.json”)
x="""L’Ajuntament de Barcelona suspèn la construcció de nous hotels a tota la ciutat."""
print geoloc.geolocalize(x,knowledge)
```

```python
import geoloc
geoloc.set_lang(‘en’)
knowledge=geoloc.knowledge_dictionary()
print knowledge
x="""Eurozone finance chiefs have warned of tough negotiations ahead as they meet to decide whether Greece's new reform proposals merit a third debt bailout."""
print geoloc.geolocalize(x,knowledge)
print knowledge
```

Run geoloc.py to analyze the files contained in the folder example_news.
