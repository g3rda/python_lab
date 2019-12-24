# from spyre import spyre
# import spyre
import numpy as np
import pandas as pd
from numpy import pi

try:
    from spyre import server
except Exception:
    import server
server.include_df_index = True


class TestApp2(server.App):
    title = "My app"

    inputs = [
        {
            "type": 'slider',
            "label": 'from',
            "key": 'yfrom',
            "value": 2000, "min": 1982, "max": 2019,
            "action_id": "refresh"
        }, 
        {
            "type": 'slider',
            "label": 'to',
            "key": 'yto',
            "value": 2000, "min": 1982, "max": 2019,
            "action_id": "refresh"
        }, 
        {
            "type": 'dropdown',
            "label": 'province',
            "options": [
                {"label": "Cherkasy", "value": "1"},
                {"label": "Chernihiv", "value": "2"},
                {"label": "Chernivtsi", "value": "3"},
                {"label": "Crimea", "value": "4"},
                {"label": "Dripropetrovsk", "value": "5"},
                {"label": "Donetsk", "value": "6"},
                {"label": "Ivano-Frankivsk", "value": "7"},
                {"label": "Kharkiv", "value": "8"},
                {"label": "Kherson", "value": "9"},
                {"label": "Khmelnytskyy", "value": "10"},
                {"label": "Kiev", "value": "11"},
                {"label": "Kiev City", "value": "12"},
                {"label": "Kirovohrad", "value": "13"},
                {"label": "Luhansk", "value": "14"},
                {"label": "Lviv", "value": "15"},
                {"label": "Mykolayiv", "value": "16"},
                {"label": "Odessa", "value": "17"},
                {"label": "Poltava", "value": "18"},
                {"label": "Rivne", "value": "19"},
                {"label": "Sevastopol", "value": "20"},
                {"label": "Sumy", "value": "21"},
                {"label": "Ternopil", "value": "22"},
                {"label": "Transcarpathia", "value": "23"},
                {"label": "Vinnytsya", "value": "24"},
                {"label": "Volyn", "value": "25"},
                {"label": "Zaporizhzhya", "value": "26"},
                {"label": "Zhytomyr", "value": "27"},
            ],
            "key": 'province',
            "action_id": "refresh"
        }, {
            "type": 'dropdown',
            "label": 'years',
            "options": [
                {"label": "all years", "value": "1"},
                {"label": "every 5 years", "value": "2"},
                {"label": "every 10 years", "value": "3"},
                {"label": "every 15 years", "value": "4"},
                {"label": "every 20 years", "value": "5"},
            ],
            "key": 'years',
            "action_id": "refresh"
        }
    ]

    controls = [{"type": "button", "id": "refresh", "label": "refresh"}]
    tabs = ["Plot", "Table"]


    outputs = [
        {"type": "html", "id": "htmlx", "control_id": "refresh"},
        {"type": "plot", "id": "plot1", "control_id": "refresh", "tab" : "Plot"},
        {"type": "table", "id": "table1", "control_id": "refresh", "tab" : "Table","on_page_load" : True}
    ]

    def getData(self, params):
        df=pd.read_csv('/home/lemonade/python/all_in_one_12.24.2019-02:51:03.csv')
        df.drop(df.columns[[0]], axis=1,inplace=True)
        prov = params['province']
        years = params['years']
        yfrom=params['yfrom']
        yto=params['yto']
        data = df[df['provinceID'] == int(prov)]
        if years == "1":
            data =data [(data['year']>=yfrom) &(data['year']<=yto)]
        elif years == "2":
            data =data [(data['year'] %5==yfrom%5) & (data['year']>=yfrom) &(data['year']<=yto)]
        elif years == "3":
            data =data [(data['year'] %10==yfrom%10) & (data['year']>=yfrom) &(data['year']<=yto)]
        elif years == "4":
            data =data [(data['year'] %15==yfrom%15) & (data['year']>=yfrom) &(data['year']<=yto)]
        elif years == "5":
            data =data [(data['year'] %20==yfrom%20) & (data['year']>=yfrom) &(data['year']<=yto)]
        return data

    def getHTML(self, params):
        df=pd.read_csv('/home/lemonade/python/all_in_one_12.24.2019-02:51:03.csv')


    def getPlot(self, params):
        df = self.getData(params)
        plt_obj = df.plot(kind='bar',x='year',y='VHI', legend=False)
        fig = plt_obj.get_figure()
        return fig

        


if __name__ == '__main__':
    app = TestApp2()
    app.launch(port=9093)
