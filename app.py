import requests,json

from bokeh.io import push_notebook, show, output_notebook
from bokeh.layouts import row, gridplot
from bokeh.plotting import figure, output_file, show
from bokeh.sampledata.autompg import autompg as df

from api_key import API_KEY

from bokeh.models import Legend


header = {"TRN-Api-Key": API_KEY}

class Picker():

    def __init__(self, title, options=""):
        self.title = title
        self.options = options

    def log(self):
        print(self.title)
        print(self.options)

    def get_inp(self):
        self.choice = str(input(self.title + " " + (str(self.options)) + "\n" ))


class FortniteDataExtracter():
    
    def __init__(self, fornite_json_data):
        self.data = fornite_json_data

    def get_solo_values(self):
        data_temp = self.data["stats"]["p2"]

        trnRating = data_temp["trnRating"]["value"]

        score = data_temp["score"]["value"]

        wins = data_temp["top1"]["value"]

        kdr = data_temp["kd"]["value"]

        kills = data_temp["kills"]["value"]

        return({
            "trnRating": trnRating,
            "score": score,
            "wins": wins,
            "kdr": kdr,
            "kills": kills
        })
    
    def get_duo_values(self):        
        data_temp = self.data["stats"]["p10"]

        trnRating = data_temp["trnRating"]["value"]

        score = data_temp["score"]["value"]

        wins = data_temp["top1"]["value"]

        kdr = data_temp["kd"]["value"]

        kills = data_temp["kills"]["value"]

        return({
            "trnRating": trnRating,
            "score": score,
            "wins": wins,
            "kdr": kdr,
            "kills": kills
        })
    
    def get_squad_values(self):        
        data_temp = self.data["stats"]["p9"]

        trnRating = data_temp["trnRating"]["value"]

        score = data_temp["score"]["value"]

        wins = data_temp["top1"]["value"]

        kdr = data_temp["kd"]["value"]

        kills = data_temp["kills"]["value"]

        return({
            "trnRating": trnRating,
            "score": score,
            "wins": wins,
            "kdr": kdr,
            "kills": kills
        })
        

plat_picker = Picker( "Please choose your platform: " , ['pc', 'xbl', 'psn'])
plat_picker.get_inp()

user_picker = Picker("Please enter your username: ", )
user_picker.get_inp()

platform = plat_picker.choice
epic_nickname = user_picker.choice

url = "https://api.fortnitetracker.com/v1/profile/%s/%s" %(platform, epic_nickname)

r = requests.get(url, headers=header)

data = json.loads(r.text)

fortnite_data = FortniteDataExtracter(data)

solo_values = fortnite_data.get_solo_values()
duo_values = fortnite_data.get_duo_values()
squad_values = fortnite_data.get_squad_values()

opts = dict(plot_width=680, plot_height=int(680/2), min_border=0)

output_file("graph.html")

# This is the score graph
p = figure(**opts)
#options
p.title.text = "Fortnite Score Graph - User: %s" %(epic_nickname)
p.title.align = "center"
p.title.text_color = "orange"
p.title.text_font_size = "25px"
#solo
# command : "{:,}".format(int(solo_values["score"]))
solo = p.vbar(x=[5], width=0.1, bottom=0,
       top=[solo_values["score"]], color="red")
#duo
duo = p.vbar(x=[15], width=0.1, bottom=0,
       top=[duo_values["score"]], color="blue")
#squad
squad = p.vbar(x=[25], width=0.1, bottom=0,
       top=[squad_values["score"]], color="green")
#legend
legend = Legend(items=[
    ("Solo - %s" %("{:,}".format(int(solo_values["score"]))) ,   [solo]),
    ("Duo - %s" %("{:,}".format(int(duo_values["score"]))) , [duo]),
    ("Squad - %s" %("{:,}".format(int(squad_values["score"]))) , [squad])
], location=(10, 0))
p.add_layout(legend, 'right')

# end score graph

#This is the kdr graph
p1 = figure(**opts)
#options
p1.title.text = "Fortnite KDR Graph - User: %s" %(epic_nickname)
p1.title.align = "center"
p1.title.text_color = "orange"
p1.title.text_font_size = "25px"
#graph

#solo
solo1 = p1.vbar(x=[5], width=0.1, bottom=0,
       top=[solo_values["kdr"]], color="red")
#duo
duo1 = p1.vbar(x=[15], width=0.1, bottom=0,
       top=[duo_values["kdr"]], color="blue")
#squad
squad1 = p1.vbar(x=[25], width=0.1, bottom=0,
       top=[squad_values["kdr"]], color="green")

#legend
legend1 = Legend(items=[
    ("Solo - %s" %(solo_values["kdr"]) ,   [solo1]),
    ("Duo - %s" %(duo_values["kdr"]) , [duo1]),
    ("Squad - %s" %(squad_values["kdr"]) , [squad1])
], location=(10, 0))

p1.add_layout(legend1, "right")

#end kdr graph

#Grid Plot of all graphs
grid = gridplot([[p, p1], [None, None]])

show(grid)
