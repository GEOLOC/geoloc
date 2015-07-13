from spyre import server
from geoloc import *

import pandas as pd
import math
import os
from skimage import io
from skimage.draw import (line, polygon, circle,
                          circle_perimeter,
                          ellipse, ellipse_perimeter,
                          bezier_curve)


class SimpleSineApp(server.App):
    title = "Geolocate news"
    inputs = [{ "input_type":"text",
                "label":"Introduce a text or a filepath",
                "variable_name":"body",
                "value":"",
                "action_id":"update_data"},
              {"input_type":'dropdown',
               "label": 'Language', 
               "options" : [ {"label": "Catalan", "value":"ca"},
                             {"label": "Spanish", "value":"es"},
                             {"label": "English", "value":"en"},
                             {"label": "French", "value":"fr"},
                             {"label": "German", "value":"de"}],
               "variable_name": 'language', 
               "action_id": "update_data" }]


    controls = [{ "control_type" : "hidden",
                  "label" : "Update List",
                  "control_id" : "update_data"}]


    tabs = ["List", "Map"]


    outputs = [{"output_type":"table",
                "output_id":"names",
                "control_id":"update_data",
                "tab":"List",
                "on_page_load":False},
               {"output_type":"image",
                "output_id":"map",
                "control_id":"update_data",
                "tab":"Map",
                "on_page_load":False}]

    

    def getData(self, params):
        

        knowledge=knowledge_dictionary()
        lan=str(params['language'])
        try:
            knowledge.load_json("knowledge_"+lan+".json")
        except IOError:
            pass
        body = str(params['body'])
        set_lang(lan)
        
        try:
            f=open(body)
            text=f.read()
        except IOError:
            text=body

        names=geolocalize(text.decode('utf-8'),knowledge)
        names=list(set(names))

        if len(names)>0:
            df=pd.DataFrame(names,columns=['Geolocating entities'])
        else:
            df=pd.DataFrame(names)

        return df
    

    def getImage(self, params):
        
  
        knowledge=knowledge_dictionary()
        lan=str(params['language'])
        try:
            knowledge.load_json("knowledge_"+lan+".json")
        except IOError:
            pass

        body = str(params['body'])
        set_lang(lan)

        try:
            f=open(body)
            text=f.read()
        except IOError:
            text=body

        names=geolocalize(text.decode('utf-8'),knowledge)
        names=list(set(names))


        world = io.imread("worldmap.jpg")

        mapWidth    = float(world.shape[1])
        mapHeight   = float(world.shape[0])

   
        for place in names:
            latitude    = knowledge[place.decode('utf-8')][0]
            longitude   = knowledge[place.decode('utf-8')][1]
            x = (longitude+180)*(mapWidth/360)

  
            latRad = latitude*math.pi/180

            mercN = math.log(math.tan((math.pi/4)+(latRad/2)))
            y     = (mapHeight/2)-(mapWidth*mercN/(2*math.pi))
      
            
            rr, cc = circle(y, x, 6,world.shape)
            world[rr, cc] = [255, 0, 255]
        return world
        
app = SimpleSineApp()
app.launch()

