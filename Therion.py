from bs4 import BeautifulSoup
from urllib.request import urlopen
from datetime import date, datetime

import time
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import random as rd

# Criar uma função que preenche com none todos os campos de uma data X pra trás de um produto recentemente adicionado

def steal_marker(marker_list):
    return marker_list[rd.randint(0, len(marker_list) - 1)]

def steal_style(style_list):
    return style_list[rd.randint(0, len(style_list) - 1)]

class Therion:
    def __init__(self):
        self.product_name = []
        self.product_link = []
        self.product_tag = []

        self.current_link = None
        self.current_link_bs = None
        self.current_produts = None

        self.therion_csv = None
        self.therion_list_csv = None
        self.therion_list = None
        self.therion_dates = None

        self.file = None

        self.linestyles = ['-', '--', '-.', ':']
        self.markers = ['.',',','o','v','^','<','>','1','2','3','4','8','s','p','P','*','h','H','+','x','X','D','d','|','_']

    def get_therion_list(self):
        self.therion_list_csv = pd.read_csv('therionlist.csv', sep=',')
        for counter in range(len(self.therion_list_csv)):
            name_aux = self.therion_list_csv.iloc[counter]['product_name']
            link_aux = self.therion_list_csv.iloc[counter]['product_link']
            tag_aux = self.therion_list_csv.iloc[counter]['product_tag']

            self.steal(name_aux, link_aux, tag_aux)
        self.heathcote()

    def get_prices(self, product_tag):
        inner_count = 0
        for link in self.product_link:
            self.steal_link(link, product_tag)

            p_name = self.product_name[inner_count]
            p_price = self.current_produts.get_text()
            self.therion_write(p_name, p_price)

            inner_count = inner_count + 1
        self.therion_cleanup()

    def steal(self, product_name, product_link, product_tag):
        self.product_name.append(product_name)
        self.product_link.append(product_link)
        self.product_tag.append(product_tag)

    def steal_link(self, product_link, product_tag):
        if product_tag in self.product_tag:
            if product_tag == 'card':
                self.current_link = urlopen("https://www.ligayugioh.com.br/?view=cards%2Fsearch&card=" + product_link)
                self.current_link_bs = BeautifulSoup(self.current_link.read(), "html.parser")
                self.current_produts = self.current_link_bs.find("div", {"class": "col-prc col-prc-menor"})

        else:
            return None

    def therion_write(self, p_name, p_price):
        product_check = len(self.therion_csv.loc[self.therion_csv['product'] == p_name])
        self.file = open("therion.csv", "a")
        if product_check != 0:
            self.file.write(p_name)
            self.file.write(",")
            self.file.write(p_price.replace('R$', '').replace(',', '.').replace(' ', ''))
            self.file.write(",")
            self.file.write((date.today()).strftime("%d-%m-%y"))
            self.file.write("\n")
        else:
            for data in self.therion_dates:
                self.file.write(p_name)
                self.file.write(",")
                if data != date.today():
                    self.file.write('0.00')
                    self.file.write(",")
                    self.file.write(data)
                    self.file.write("\n")
            self.file.write(p_name)
            self.file.write(",")
            self.file.write(p_price.replace('R$', '').replace(',', '.').replace(' ', ''))
            self.file.write(",")
            self.file.write((date.today()).strftime("%d-%m-%y"))
            self.file.write("\n")

        print("{} no valor de, {}".format(p_name,p_price))
        self.therion_break()

    def heathcote(self):
        self.therion_csv = pd.read_csv("therion.csv", sep=",").sort_values(by=['date'])
        self.therion_list = self.therion_csv.groupby('product').mean().index
        self.therion_dates = self.therion_csv['date'].unique()

    def dragonstone(self):
        for product in self.therion_list:
            product_plot = self.therion_csv.loc[self.therion_csv['product'] == product]
            figure = product_plot.plot(x='date', y='price', color='purple', title=('Prices ' + product), grid=True,
                                   marker='o').get_figure()
            figure.savefig('dragonstone_' + product + '.pdf')
            plt.yticks(np.arange(0, 110, 10))
        plt.show()

    def dragonstones(self):
        for product in self.therion_list:
            product_prices = self.therion_csv.loc[self.therion_csv['product'] == product]['price']
            plt.plot(self.therion_dates, product_prices, linestyle=steal_style(self.linestyles)
                     , marker=steal_marker(self.markers), color="purple", label=product)
            plt.grid()
            plt.xlabel("Dates")
            plt.ylabel("Price")
            plt.yticks(np.arange(0, 110, 10))
            plt.title("Prices combined")
            plt.legend()

        plt.show()

    def therion_break(self):
        self.file.close()
        
    def therion_cleanup(self):
        self.current_link = None
        self.current_link_bs = None
        self.current_produts = None



