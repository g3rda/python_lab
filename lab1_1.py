from urllib.request import urlopen
import pandas as pd
from datetime import datetime
import glob
from spyre import server

di = {1: 22, 2: 24, 3: 23, 4: 25, 5: 3, 6: 4, 7: 8, 8: 19, 9: 20, 10: 21, 11: 9, 13: 10, 14: 11,15:12, 16:13, 17:14, 18:15, 19:16, 21:17, 22:18, 23: 6, 24:1, 25:2, 26:7, 27:5}

def getcsv(n):
	url="https://www.star.nesdis.noaa.gov/smcd/emb/vci/VH/get_provinceData.php?country=UKR&provinceID=" + str(n) +"&year1=1981&year2=2019&type=Mean";
	vhi_url = urlopen(url)
	now = datetime.now()
	date_time = now.strftime("%m.%d.%Y-%H:%M:%S")
	fileout='vhi_id_' +str(n)+'_' + date_time+'.csv';
	out = open(fileout,'wb')
	out.write(vhi_url.read())
	out.close()
	df=pd.read_csv(fileout,  skiprows=1, skipfooter=1, engine='python', names=['year', 'SMT', 'VCI', 'TCI', 'VHI'])
	df[['year', 'week', 'SMN']] = pd.DataFrame([ x.split() for x in df['year'].tolist() ])
	df['provinceID']=n
	df = df[['year', 'week', 'provinceID', 'SMN', 'SMT', 'VCI', 'TCI', 'VHI']]
	df.to_csv(fileout)


def todf(path):
	filenames = glob.glob(path+"vhi_id_*.csv")
	dfs = [pd.read_csv(f) for f in filenames]
	data = pd.concat(dfs, ignore_index=True)
	data.drop(data.columns[[0]], axis=1,inplace=True)
	print(data)
	now = datetime.now()
	date_time = now.strftime("%m.%d.%Y-%H:%M:%S")
	fileout='all_in_one_'+ date_time+'.csv';
	data.to_csv(fileout)

def replid(path):
	filename = glob.glob(path+"all_in_one*.csv")
	df=pd.read_csv(filename[0])
	df['provinceID']=df['provinceID'].map(di)
	df.drop(df.columns[[0]], axis=1,inplace=True)
	df.to_csv(filename[0])
	print(df)


def vhi(prid, year, path):
	filename = glob.glob(path+"vhi_id_"+str(prid)+ "*.csv")
	df=pd.read_csv(filename[0])
	data = df[df['year'] == year]
	print(data)
	print(data['VHI'].min())
	print(data['VHI'].max())


def dry(prid, path):
	filename = glob.glob(path+"vhi_id_"+str(prid)+ "*.csv")
	df=pd.read_csv(filename[0])
	data = df[df['VHI'] < 15]
	print(data[['year']].drop_duplicates())
	

def middledry(prid, path):
	filename = glob.glob(path+"vhi_id_"+str(prid)+ "*.csv")
	df=pd.read_csv(filename[0])
	data = df[df['VHI'] < 35]
	print(data[['year']].drop_duplicates())
	

print ("Done.");


class SimpleApp(server.App):
	title = "Simple App"
	inputs = [{
		"type": "text",
		"key": "words",
		"label": "write words here",
		"value": "hello world", 
		"action_id": "simple_html_output"
	}]

	outputs = [{
		"type": "html",
		"id": "simple_html_output"
	}]

	def getHTML(self, params):
		words = params["words"]
		return "Here's what you wrote in the textbox: <b>%s</b>" % words

app = SimpleApp()
app.launch()