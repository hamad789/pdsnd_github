Explanation of steps implementation in bikeshare project. 

Step 1:
Get city, month and day input from the user using input() function and while loop to handle incorrect inputs.

Step 2: Filter dataframe, according to the user input i create a mask (pandas Series with boolean values) that indicate whether a row in dataframe must be considered or not.
To filter time, i use 'dt' attribute of the datetime format to access date only, which then allows to access month and day with month_name() and day_name() methods.

Step 3. Time stats

We consider stats with regard to the 'Start Time'. It was found out that there are only 21 out of 300,000 tours that end on the next day. This does not change the stats, hence,
it was decided to use 'Start Time' for convinience.
First, i extract month/day as described above and then apply value_counts() method to find frequency of unique values which are then sorted numerically.

Step 4. Station Stats. 

Same technique is applied to find most common Start and End Stations. To find the most common combination of them, i first group our data by Start and End station,
therefore retrieving all of their combinations; later nunique() method is applied on top of the grouped data, giving statistics about frequency of stations combination.

Step 5. Trip Duration Stats
Trip duration are simply calculated by selecting Trip Duration column and applying max() or mean() methods

Step 6. User Stats
Same techniques described above are applied to calculate user stats. There is an additional check to see whether Gender or Birth Year column exist.


Step 7. Testing
The program has been tested according to the several criteria:
1) Entering dummy inputs for cities, days and month
2) Combining various inputs for day and month: (monday, july), (all, july), (monday, all), (all, all) for each of the cities
This makes sure the program operates without errors while still handling all possible inputs. 