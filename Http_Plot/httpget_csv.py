# coding:utf-8
import urllib2
import json
import csv
html = urllib2.urlopen(r'http://0.0.0.0:5000/')
hjson = json.loads(html.read())

# print hjson['results'][0]
items = hjson.items()
plot_data=[]

with open("/Users/yangli/PycharmProjects/machine_learning/Http_Plot/Data/results.csv","w") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["drop","time"])
    for key, value in items:
        if key == 'results':
            for i in value:
                print i['drp'],i['tm']
                writer.writerow([i['drp'],i['tm']])
    csvfile.close()
