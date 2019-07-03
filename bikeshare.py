import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

MONTH_LIST = ['all', 'january', 'february', 'march', 'april', 'may', 'june']

DAY_LIST = ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']

# prints 5 rows of the Dataframe/Series

def print_head(data):
    isprint = input('\nWould you like to have 5 top rows of data printed (yes/no) ? :\n')
    i=0
    if isprint.lower() == 'yes':
        print('\n')
        chunk = data.iloc[5*i:5*(i+1)]
        print(chunk)
        more = input('\nWould like to display 5 more lines (yes/no)?\n')
        nextchunk = data.iloc[5*(i+1):5*(i+2)]
        while more.lower() == 'yes' and not nextchunk.empty:
            i+=1
            print('\n')
            chunk = data.iloc[5*i:5*(i+1)]
            print(chunk)
            nextchunk = data.iloc[5*(i+1):5*(i+2)]
            more = input('\nWould like to display 5 more lines (yes/no)?\n')
        print('No more data to print')

    else:
        return

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')

    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = input("Please name of the city to analyze: \n")
    while city.lower() not in  CITY_DATA.keys():
        city = input("Cities can be 'Chicago', 'New York City',or 'Washington'. Please enter name again: \n")
    city = CITY_DATA[city.lower()]


    # get user input for month (all, january, february, ... , june)
    month = input("Please name of the month to filter the city data: \n").lower()
    while month.lower() not in MONTH_LIST:
    	month = input("Months can take values 'all', 'january',...,'june'. Please enter the month again: \n")



    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = input("Please name of the weekday to filter the data: \n")
    while day.lower() not in DAY_LIST:
        day = input("Days can take values 'all', 'monday',...,'sunday'. Please enter the day again: \n")

    print('-'*40)

    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """

    #Loading dataframe, converting dates to pandas datetime format
    df = pd.read_csv(city, parse_dates = ['Start Time', 'End Time'])
    df = df.rename(columns = {'Unnamed: 0': 'id'})

    #capitalize names to match with pandas months
    month, day = month.lower(), day.lower()
    month = MONTH_LIST.index(month)
    day = DAY_LIST.index(day)


    # Filtering datasets:

    """ 1. Creating mask to filter dataframes rows We use month_name() and day_name() 
        from pandas to filter the the data by entered month and day
    """
    mask = None 
    if month != 0 and day != 0:
        mask =  (df['Start Time'].dt.weekday == day-1) & (df['Start Time'].dt.month == month)&\
                (df['End Time'].dt.weekday == day-1) & (df['End Time'].dt.month ==   month)

    elif month != 0:
        mask =  (df['Start Time'].dt.month == month) & (df['End Time'].dt.month == month)

    elif day  != 0:
        mask =  (df['Start Time'].dt.weekday == day-1) & (df['End Time'].dt.weekday == day-1)

    if mask is not None: 
        df = df[mask]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month - we use value_counts() method to count unique values in 
    # pandas Series which are then sorted 
    result = df['Start Time'].dt.month.value_counts().sort_values(ascending=False)
    print('Most Common Month:\n%s' % (MONTH_LIST[result.index[0]]))
    print_head(result)

    # display the most common day of week
    result = df['Start Time'].dt.weekday.value_counts().sort_values(ascending=False)
    print('\nMost Common Day of Week:\n%s' % (DAY_LIST[result.index[0]+1]))
    print_head(result)

    # display the most common start hour
    result = df['Start Time'].dt.hour.value_counts().sort_values(ascending=False)
    print('\nMost Common Start Hour:\n%i' % (result.index[0]))
    print_head(result)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    result = df['Start Station'].value_counts().sort_values(ascending=False)
    print('\nMost Commonly Used Start Station:\n%s' % (result.index[0]))
    print_head(result)

    # display most commonly used end station
    result = df['End Station'].value_counts().sort_values(ascending=False)
    print('\nMost Commonly Used End Station:\n%s' % (result.index[0]))
    print_head(result)

    # display most frequent combination of start station and end station trip
    result = df.groupby(['Start Station', 'End Station'])['id'].nunique().sort_values(ascending=False)
    start_end_station = result.index[0]

    print('\nMost Frequent Combination of Start Station and End Station Trip:\n\'%s\' and \'%s\'' \
                    % (start_end_station[0], start_end_station[1]))
    print_head(result)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    print('Total Travel Time:\n%s seconds' % (df['Trip Duration'].sum()))

    # display mean travel time
    print('\nMean Travel Time:\n%s seconds' % (df['Trip Duration'].mean()))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print('Counts of User Types:')
    print(df['User Type'].value_counts().to_dict())


    # Display counts of gender
    if 'Gender' in df.columns: #washington data does not have a Gender column
        print('\nCounts of Gender:')
        print(df['Gender'].value_counts().to_dict())

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:                  #washington data does not have a Birth Year column
        earliest    = df['Birth Year'].min()
        most_recent = df['Birth Year'].max()
        result_most_common = df.groupby(['Birth Year'])['id'].nunique().sort_values(ascending=False)
        most_common = result_most_common.index[0]

        print('\n\nYear of birth:\nEarliest: %i\nMost Recent:%i\nMost Common:%i'\
                                    % (earliest, most_recent, most_common))
        print_head(result_most_common)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
