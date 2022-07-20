import time
import pandas as pd
import numpy as np
import tabulate

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york': 'new_york_city.csv',
              'washington': 'washington.csv' }
months = ['january', 'february', 'march', 'april', 'may', 'june']
days = ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    
    print('Hello! Let\'s explore some US bikeshare data!')
    while(True):
        # Get user input for city (chicago, new york, washington). HINT: Use a while loop to handle invalid inputs
        city =input("Would you like to see data for: Chicago, New York,or Washington\n").lower()
        if city in CITY_DATA:
            break
        else:
            print('Please enter valid city.')

    # Get user input for filtering data by month, day, both, or not at all
    while (True):
        filterby = input("Would you like to filter the data by month, day, \"both\", or \"none\" for no time filters\n").lower()
        if filterby == 'month':
            # Get user input for month (january, february, ... , june)
            month = input("Which month?  January, February, March, April, May, or June?\n").lower()
            day = 'all'
            if month in months:
                break
            else:
                print('Please enter a valid month.')
        elif filterby == 'day':
            # Get user input for day of week (sunday, monday, tuesday, ... saturday)
            #***day = input("Which day? please type your respose as an integer (e.g., 1=Sunday)\n").lower()
            day = eval(input("Which day? please type your respose as an integer (e.g., 1=Sunday)\n"))
            month = 'all'
            if day in range(1,8):
                day = days[day-1]
                break
            else:
                print('Please enter a valid day')
        
        elif filterby == 'both':
            #
            month = input("Which month?  January, February, March, April, May, or June?\n").lower()
            if month in months:
                None
            else:
                print('Please enter a valid month.')
                continue
            
            day = eval(input("Which day? please type your respose as an integer (e.g., 1=Sunday)\n"))
            if day in range(1,8):
                day = days[day-1]
                None
            else:
                print('Please enter a valid day')
                continue
            
            break
    
        elif filterby == 'none':
            month= 'all'
            day='all'
            break
        else: 
            print('Please enter valid choice for filtering.')
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
    # Load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])
    
    #no filterting applied if none is choosen
    if month == 'all' and day == 'all':
        return df

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # Extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    #df['day_of_week'] = df['Start Time'].dt.weekday_name
    df['day_of_week'] = df['Start Time'].dt.day_name()
    #***print("\n day of week\n", df['day_of_week'])
    
    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        #**months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month)
        #**print( "\n month ",month)
            
        # filter by month to create the new dataframe
        df = df.loc[df['month'] == (month+1) ]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df.loc[df['day_of_week'] == day.title()]
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""
    print("\nCalculating statistic ...")
    print('Calculating The Most Frequent Times of Travel...')
    start_time = time.time()
    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # Display the most common month
    df['month'] = df['Start Time'].dt.month
    common_month = df['month'].value_counts().idxmax()

    # Display the most common day of week
    #df['day_of_week'] = df['Start Time'].dt.weekday_name
    df['day_of_week'] = df['Start Time'].dt.day_name()
    common_day = df['day_of_week'].value_counts().idxmax()

    # Display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    common_hour = df['hour'].value_counts().idxmax()
    # Convert hour from 24 hour clock to 12 hour clock
    symbol = ""
    if common_hour < 12: 
        symbol = "AM"
    elif common_hour > 12:
        common_hour = common_hour-12
        symbol = "PM"
    elif common_hour == 12:
        symbol = "PM"

    print("Most popular Month: {},\nMost popular Day of Week: {}, \nMost popular Hour of day: {} {}".format(common_month, common_day, common_hour, symbol))
    print("This took %s seconds." % (time.time() - start_time))
    
def station_stats(df):
    """Displays statistics on the most popular stations and trip."""
    
    print("\nCalculating statistic ...")
    print('Calculating The Most Popular Stations and Trip...')
    start_time = time.time()

    # Display most commonly used start station
    common_start_station = df['Start Station'].value_counts().idxmax()
    
    # Display most commonly used end station
    common_end_station = df['End Station'].value_counts().idxmax()
    
    # Display most frequent combination of start station and end station trip
    df['complete_station'] = df['Start Station']  +" to "+  df['End Station']
    common_complete_station = df['complete_station'].value_counts().idxmax()
    #print("Most Common Trip from Start to End:\n {}".format(common_combo_station)) 

    print("Most Common Start Station: {},\nMost Common End Station: {},\nMost Common Trip from Start to End: {}"
    .format(common_start_station, common_end_station, common_complete_station))

    print("This took %s seconds." % (time.time() - start_time))
    
def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print("\nCalculating statistic ...")
    print('Calculating Trip Duration...')
    start_time = time.time()

    # Calculate total travel time
    total_duration = df['Trip Duration'].sum()
    # Calculate number of trips
    count_trips = df['Trip Duration'].count()
    
    # Calculate mean travel time
    average_duration = df['Trip Duration'].mean()
    print("Total Duration: ",total_duration, "Count of trips: ", count_trips, "Average Duration: ", average_duration)
    print("This took %s seconds." % (time.time() - start_time))
    
def user_stats(df,city):
    """Displays statistics on bikeshare users."""
    
    print("\nCalculating statistic ...")
    print('Calculating User Stats...')
    start_time = time.time()

    # Display counts of user types
    print('Counts of Each "User Type"')
    user_types = df['User Type'].value_counts().reset_index()
    user_types.columns = ['User_Type', 'Counts']
    print(user_types)

    # Display counts of gender
    try:
        print('Counts of Each User "Gender"')
        gender = df['Gender'].value_counts().reset_index()
        gender.columns = ['Gender', 'Counts']
        print(gender)
    except:
        print('Sorry, no "gender" data available for {} City'.format(city.title()))

    # Display earliest, most recent, and most common year of birth
    try:
        print('Counts of User "Birth Year":')
        earliest = df['Birth Year'].min() #earliest birth year
        recent = df['Birth Year'].max() #most recent birth Year
        common = df['Birth Year'].mode() #most Common Birth Year 
        print('Oldest User(s) Birth Year: ', int(earliest))
        print('Youngest User(s) Birth Year: ', int(recent))
        print('Most Common Birth Year: ', int(common))
    except:
        print("Sorry, no \"birth year\" data available for {} City".format(city.title()))
    print("This took %s seconds." % (time.time() - start_time))

def display_data(df):
    # Ask user if they want to see individual trip data.
    start_data = 0
    end_data = 5
    data_length = len(df.index)
    
    while start_data < data_length:
        display = input("\nWould you like to see individual trip data? Enter 'yes' or 'no'.\n")
        if display.lower() == 'yes':
            
            print("\nDisplaying only 5 rows of data.\n")
            if end_data > data_length:
                end_data = data_length
            for i in range (start_data, end_data):
                print(df.iloc[i].to_dict())
            #print(df.iloc[start_data:end_data])
            start_data += 5
            end_data += 5
        else:
            break

def main():
    while True:
        city, month, day = get_filters()
        print("\nLoad data for CITY: \"", city, "\" In Month: \"", month, "\" In a day: \"", day,"\"")
        df = load_data(city, month, day)
        print(df)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df,city)
        display_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
