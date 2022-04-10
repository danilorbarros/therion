# [Library Instance]
from bs4            import BeautifulSoup
from urllib.request import urlopen
from datetime       import date

import pandas               as pd
import numpy                as np
import matplotlib.pyplot    as plt
import random               as rd

# [Auxiliar Function Instance]
# Auxiliar functions that randomly choose a style of marker and line
def steal_marker(marker_list):
    return marker_list[rd.randint(0, len(marker_list) - 1)]
def steal_style(style_list):
    return style_list[rd.randint(0, len(style_list) - 1)]

# [Therion Instance]
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

    '''
        This is the first fuction that might be called in order to extract the existent data at therionlist.csv.
            heathcote and steal will be explained later
    '''
    def get_therion_list(self):
        self.therion_list_csv = pd.read_csv('therionlist.csv', sep=',')
        for counter in range(len(self.therion_list_csv)):
            name_aux = self.therion_list_csv.iloc[counter]['product_name']
            link_aux = self.therion_list_csv.iloc[counter]['product_link']
            tag_aux = self.therion_list_csv.iloc[counter]['product_tag']

            self.steal(name_aux, link_aux, tag_aux)
        self.heathcote()

    '''
        This function is part of get_therion_list and is used just to set the existent data at the class lists
    '''
    def steal(self, product_name, product_link, product_tag):
        self.product_name.append(product_name)
        self.product_link.append(product_link)
        self.product_tag.append(product_tag)

    '''
        This function is part of get_therion_list and is used to:
            Initialize therion_csv (which is the CSV that will be used as output)
            Initialize therion_list (which is used just to get the indexes of each product)
            Initialize therion_dates (which stores all sampledates)
    '''
    def heathcote(self):
        self.therion_csv = pd.read_csv("therion.csv", sep=",").sort_values(by=['date'])
        self.therion_list = self.therion_csv.groupby('product').mean().index
        self.therion_dates = self.therion_csv['date'].unique()

    '''
        This function is used to actually get the prices of each product based on its tag
            steal_link, therion_write and therion_cleanup will be explained later
    '''
    def get_prices(self, product_tag):
        inner_count = 0
        for link in self.product_link:
            self.steal_link(link, product_tag)

            p_name = self.product_name[inner_count]
            p_price = self.current_produts.get_text()
            self.therion_write(p_name, p_price)

            inner_count = inner_count + 1
        self.therion_cleanup()

    '''
        This is the function that use of web scraping to get each product price based on its tag
    '''
    def steal_link(self, product_link, product_tag):
        if product_tag in self.product_tag:
            if product_tag == 'card':
                self.current_link = urlopen("https://www.ligayugioh.com.br/?view=cards%2Fsearch&card=" + product_link)
                self.current_link_bs = BeautifulSoup(self.current_link.read(), "html.parser")
                self.current_produts = self.current_link_bs.find("div", {"class": "col-prc col-prc-menor"})

        else:
            return None

    '''
        This is the function that writes therion.csv with output data
    '''
    def therion_write(self, p_name, p_price):
        # check if the product is already in the therion.csv or if it's a new one
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
            # in case the product is a new one, this function will create the current date and get all the past dates
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

    '''
        This is the function prints each graphic of each product price and also create a pdf of its figure
    '''
    def dragonstone(self):
        for product in self.therion_list:
            product_plot = self.therion_csv.loc[self.therion_csv['product'] == product]
            figure = product_plot.plot(x='date', y='price', color='purple', title=('Prices ' + product), grid=True,
                                   marker='o').get_figure()
            figure.savefig('dragonstone_' + product + '.pdf')
            plt.yticks(np.arange(0, 110, 10))
        plt.show()

    '''
        This is the function prints each product price in a single graphic
    '''
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

    '''
        This is the function responsible for close the opened file
            therion_cleanup will be explained later
    '''
    def therion_break(self):
        self.file.close()
        self.therion_cleanup()

    '''
        This is the function part of therion_break that put to none each current information stored
    '''
    def therion_cleanup(self):
        self.current_link = None
        self.current_link_bs = None
        self.current_produts = None



