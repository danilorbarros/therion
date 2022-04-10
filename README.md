# Therion

Since Therion (a thief character from Octopath Traveler) i named this web scraping code as such.

Therion is a class that created a code based in two .CSV files, that are used as input and output.
  - Input: 
    - product_name: Name that will be displayed
    - product_link: Link that will be used to the search
    - product_tag: Tag that will correctly guide the scrapping to its correct flow
  - Output (aswell as the PDF generated with the graphs): 
    - product
    - price
    - date 

Each product will generate a single graphic by calling Therion.dragonstone() for its on but you can also see all graphics at one, using Therion.dragonstones()

# How to use

1. Input data at therionlist.csv
2. Execute the following commands: 
    - import Therion as Octopinho
    - therion = Octopinho.Therion()
    - therion.get_therion_list()
    - therion.get_prices('tag')
    - therion.heathcote()
    - therion.dragonstone() or therion.dragonstones()
