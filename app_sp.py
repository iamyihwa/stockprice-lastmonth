from flask import Flask, render_template, request, redirect
from bokeh.plotting import figure, output_file, show
import pandas as pd
import datetime
import requests
from bokeh.embed import components

app_sp = Flask(__name__)

app_sp.vars = {}

@app_sp.route('/index_sp', methods = ['GET', 'POST'])
def index_sp():
    if request.method == 'GET':
        return render_template('companyname_sp.html')
    else:
        #request was a POST
        app_sp.vars['comp'] = request.form['name_comp']
        return redirect('/next_sp')

@app_sp.route('/next_sp', methods = ['GET'])
def next_sp():
    #Gaining data from the quandl
    today = datetime.datetime.now()#.strftime("%Y-%m-%d")
    diff = datetime.timedelta(days = 30)#.strftime("%Y-%m-%d")
    one_month_ago = today - diff
    today_str = today.strftime("%Y-%m-%d")
    one_month_ago_str = one_month_ago.strftime("%Y-%m-%d")
    comp_name = app_sp.vars['comp']
    addr = 'https://www.quandl.com/api/v3/datasets/WIKI/%s.json?column_index=4&start_date=%s&end_date=%s&order=asc' %(comp_name,one_month_ago_str,today_str)
    payload = {'key': 'ebqitznYEsv3W_rfKXc8'}

    response = requests.get(addr, params=payload) #headers = headers)
    response.status_code
    data = response.json()

    #Convert data to data frame
    pd_data = pd.DataFrame(data['dataset']['data'])

    def parse_full_date(row):
        date = datetime.datetime.strptime(row[0], "%Y-%m-%d")
        return date
    pd_data[0] = pd_data.apply(parse_full_date, axis = 1)

    #output_file('./templates/result_plot.html')
    #output_file('result_plot.html')
    TOOLS = "hover"
    x = pd_data[0]
    y = pd_data[1]
    p = figure(
        title = "Stock price last 1 month: "+ comp_name,
        x_axis_label = 'date', y_axis_label = 'closing price',
        tools = TOOLS , x_axis_type="datetime"
    )

    p.line(x, y,  line_width = 2)
    #show(p)
    comp = app_sp.vars['comp']
    script,div = components(p)
    return render_template('result_plot.html', script=script, div=div, comp = comp)
    #return "Ay madre, la fruta"

if __name__ == '__main__':
    app_sp.run()
