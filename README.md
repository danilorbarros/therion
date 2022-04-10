# Therion

Since Therion (character of Octopath Traveler) i named this web scraping code as such.

Therion is a class that created a code based in two .CSV files, that are used as input and output.
  - Input: product_name,product_link,product_tag
  - Output: product,price,date (aswell as the PDF generated with the graphs)

Each product will generate a single graphic by calling Therion.dragonstone() for its on but you can also see all graphics at one, using Therion.dragonstones()
