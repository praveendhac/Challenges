## Great Circle Distance Test
 
We have some customer records in a text file (customer_locations.txt) -- one customer per line, JSON-encoded. We want to invite any customer within 100km of our Dublin office for some food and drinks on us. Write a program that will read the full list of customers and output the names and user ids of matching customers (within 100km), sorted by User ID (ascending).
You can use the first formula from this Wikipedia article to calculate distance. Don't forget, you'll need to convert degrees to radians.
The GPS coordinates for our Dublin office are 53.339428, -6.257664.
You can find the Customer list here.

⭑ Please don’t forget, your code should be production ready, clean and tested!

References:
https://en.wikipedia.org/wiki/Great-circle_distance
https://gist.github.com/nickjevershed/6480846
https://introcs.cs.princeton.edu/python/12types/greatcircle.py.html
https://docs.scipy.org/doc/numpy-1.10.0/reference/routines.math.html

