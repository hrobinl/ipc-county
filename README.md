<h1>Project 3</h1>
<h2>By: Luis Rodriguez, Benny Grullon, Hannah Robinson, and Michelle Taylor</h2>

We started the project by deciding to look at County-level data, so that there was a dataset that impacted everyone on our team. We found the original dataset [here](https://www.ers.usda.gov/data-products/county-level-data-sets/county-level-data-sets-download-data/), which gave us the poverty, population, education, unemployment, and mediant household income for each county in the US for 2020-2022.We then set about cleaning the data using Pandas. We merged the data, dropped nulls, and converted it to a CSV. 

![image](https://github.com/hrobinl/ipc-county/assets/132225207/bf88b9e8-dfe7-42f9-acac-7bc88b5e453c)

The CSV file was then turned into a database using SQLite. Once the database was created, we were able to create our Flask API using Python Flask. 

![image](https://github.com/hrobinl/ipc-county/assets/132225207/c0486602-320d-4613-a51f-0b4c64df8640)

Once the data had been cleaned and the database created, we started planning our dynamic features and visualizations. We chose to do a map, bar chart, and scatter plot to show the data sets from different viewpoints. Our new library was Observable Plot. We created a hover function for the map, and a drop down that would change the data on the map, bar chart, and scatter plot depending on the category and year selected. 

**image of maps, etc**

Once we knew the visualizations we wanted, we started creating HTML and CSS to support those items. In the HTML, we have the spaces (divs) created for the different visualizations (“map”, “bar”, “scatter”), as well as creating a navigation bar and the drop-down menu. We created a home page, which holds the visualizations, and an about page, which holds information about the project and our analysis. We used CSS to style the page by using different font weights, styles, and colors, as well as placement of the maps and charts on the page. 
 
![image](https://github.com/hrobinl/ipc-county/assets/132225207/2bd8e57b-b3e5-4c5b-98d2-ff035211a272)
