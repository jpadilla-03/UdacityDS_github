import time
import pandas as pd
import numpy as np
import sys
from datetime import timedelta

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_month():
    """
    Prompts user for month and returns a valid value.

    Returns:
        (int) month - name of the month to filter by
        (bool) valid_month - A T/F bool whether a valid month was chosen
    """
    months = ['january', 'february', 'march', 'april', 'may', 'june']
    month_choice = input('\nWhich month? January, February, March, April, May, or June?\n').strip().lower()

    try: 
        month = months.index(month_choice)+1
        valid_month = True
        return month, valid_month
    except ValueError:
        print('An invalid month was chosen. Check spelling and ensure you are choosing from the first six months of the year.')
        return get_month()

def get_day():
    """
    Prompts user for day and returns a valid value.

    Returns:
        (int) day - name of the day to filter by
        (bool) valid_day - A T/F bool whether a valid day was chosen
    """
    days = {'m': 'Monday', 'tu': 'Tuesday', 'w': 'Wednesday', 
            'th':'Thursday', 'f':'Friday', 'sa': 'Saturday', 'su': 'Sunday'}
    day_choice = input('\nWhich day? Please type a day M, Tu, W, Th, F, Sa, Su.\n').strip().lower()
    try: 
        day = days[day_choice]
        valid_day = True
        return day, valid_day
    except KeyError:
        print('An ivalid day choice was inputted. Check spelling and ensure you are typing the desired day in the proper format.')
        return get_day()

def get_city():
    """
    Prompts user for city and returns a valid value.

    Returns:
        (str) city - name of the city to draw data from
    """
    city_input = input('\nWould you like to see data for Chicago, New York City, or Washington?\n').strip().lower()
    if city_input not in CITY_DATA.keys():
        print('Invalid city choice. Check spelling and ensure you are selecting one of the three cities provided.')
        return get_city()
    else:
        print(f'Will filter data within the {city_input.title()} dataset.')
        return city_input

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    city = ''
    month = ''
    day = ''
    
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). 
    city = get_city()

    valid_input = False
    while not valid_input:
        # Determine how/if a user wants to filter on time
        time_filter = input('\nWould you like to filter the data by "month", "day", "both", or "none" for not time filter?\n').strip().lower()
        if time_filter == 'month':
            # get user input for month (all, january, february, ... , june)
            month, valid_input = get_month()
        elif time_filter == 'day':
            # get user input for day of week (all, monday, tuesday, ... sunday)
            day, valid_input = get_day()
        elif time_filter == 'both':
            # Change month and day vars to account for both filtering
            print('Filtering for both day and month')
            
            # Get month info first. Break out of while loop if an invalid month was chosen
            month, valid_input = get_month()

            # Get day info second. Break out of while loop if a valid day was chosen
            day, valid_input = get_day()
        elif time_filter == 'none':
            # Change month and day vars to not filter on either
            print('No filter will be applied. All available days and months will be considered.')
            month = 'all'
            day = 'all'
            valid_input = True
        else:
            print('Invalid choice. Try running the program again and ensure that you are selecting the proper filter by'\
                    ' choosing an input listed in quotation marks.')
            valid_input = False
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
    # load the data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # Convert the End Time column to datetime
    df['End Time'] = pd.to_datetime(df['End Time'])

    # Create a month and day_of_week column by extracting from converted Start Time column
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()

    # filter by month if applicable
    if month and month != 'all':
        df = df[df['month'] == month]
    
    # filter by day if applicable
    if day and day != 'all':
        df = df[df['day_of_week'] == day.title()]

    return df

def get_mode(df, *args):
    """
    Get the most common count of a provided attribute(s).

    If more than one arg is given, the combo value of the
    two column headers are returned. For example, if 
    'Start Station' and 'End Station' are passed, then 
    the most common trip's start and stop stations stations
    are returned with their count.

    Args:
        (pandas df) df - A Pandas dataframe pre-built based on filters
        (str) attribute(s) - The df column header to filter on 

    Returns:
        pop_attribute - The mode of the the attribute
        pop_attribute_cnt - The mode value (count) of the attribute
    """
    if len(args) > 1:
        pop_attribute_df = df[[args[0], args[1]]].value_counts()
        pop_attribute = pop_attribute_df.idxmax()
        pop_attribute_cnt = pop_attribute_df.max()
    else:
        pop_attribute = df[args[0]].mode().iloc[0]
        pop_attribute_cnt = (df[df[args[0]] == pop_attribute][args[0]]).size
    return pop_attribute, pop_attribute_cnt

def time_stats(df):
    """
    Retrieve and print statistics on the most frequent times of travel.
    
    Args:
        (pandas df) df - A Pandas dataframe pre-built based on filters
    """
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    pop_month, pop_month_cnt = get_mode(df, 'month')

    # display the most common day of week
    pop_day, pop_day_cnt = get_mode(df, 'day_of_week')

    # create an hour column 
    df['start_hour'] = df['Start Time'].dt.hour
    
    # display the most common start hour
    pop_hour, pop_hour_cnt = get_mode(df, 'start_hour')

    print(f'Most popular month: {pop_month} - count: {pop_month_cnt}')
    print(f'Most popular day: {pop_day} - count: {pop_day_cnt}')
    print(f'Most popular hour: {pop_hour} - count: {pop_hour_cnt}')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """
    Retrieve and print statistics on the most popular stations and trip.
    
    Args:
        (pandas df) df - A Pandas dataframe pre-built based on filters
    """

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    pop_start_station, pop_start_station_cnt = get_mode(df, 'Start Station')

    # display most commonly used end station
    pop_end_station, pop_end_station_cnt = get_mode(df, 'End Station')

    # display most frequent combination of start station and end station trip
    pop_start_end, pop_start_end_cnt = get_mode(df, 'Start Station', 'End Station')
    
    print(f'Most popular start station: {pop_start_station}; count: {pop_start_station_cnt}')
    print(f'Most popular end station: {pop_end_station}; count: {pop_end_station_cnt}')
    print(f'Most popular trip:\nStarts at "{pop_start_end[0]}" and ends at "{pop_start_end[1]}"; count: {pop_start_end_cnt}')
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """
    Retrieve and print statistics on the total and average trip duration.
    
    Args:
        (pandas df) df - A Pandas dataframe pre-built based on filters
    """

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()
    
    # display total travel time
    trips_duration_total = df['Trip Duration'].sum()
    print(f'Total duration of all trips: {timedelta(seconds=int(trips_duration_total))}; count: {df['Trip Duration'].size}')

    # display mean travel time
    avg_duration_in_min = df['Trip Duration'].mean() / 60
    print(f'Avg trip duration: {avg_duration_in_min:.2f} minutes')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """
    Retrieve and print statistics on bikeshare users.
    
    Args:
        (pandas df) df - A Pandas dataframe pre-built based on filters
    """

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    users = df['User Type'].value_counts()
    print('User types...')
    for user in users.index:
        print(f'{user}: {users[user]}')

    # Display counts of gender
    print('\nGender data breakdown...')
    try: 
        gender_df = df['Gender'].value_counts()
        print(f"Male: {gender_df['Male']}; Female: {gender_df['Female']}")
    except KeyError:
        print('No gender data to display.')

    # Display earliest, most recent, and most common year of birth
    print('\nBirth data breakdown...')
    try:
        birth_df = df['Birth Year']
        print(f"Earliest birth year: {int(birth_df.min())}")
        print(f"Most recent birth year: {int(birth_df.max())}")
        print(f"Most common birth year: {int(birth_df.mode().iloc[0])}")
    except KeyError:
        print('No birth data to display')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def get_raw_data(df, start_index):
    """
    Return a pandas dataframe as an iterator.

    The returned pandas dataframe only contains necessary columns
    that are pertinent to individaul trip data. This generator function
    indexes into the passed dataframe to return data a row at a time.

    Args:
        (pandas df) df - A Pandas dataframe pre-built based on filters
        (int) start_index - Beginning index within the passed df to query
    """
    beg_index = start_index 
    while beg_index < df.shape[0]:
        try:
            yield df.iloc[start_index][['Start Time', 'End Time', 'Trip Duration', 'Start Station', 
                        'End Station', 'Gender', 'Birth Year', 'User Type']]
        except KeyError:
            yield df.iloc[start_index][['Start Time', 'End Time', 'Trip Duration', 'Start Station', 
                        'End Station', 'User Type']]
        finally: 
            beg_index += 1

def get_restart():
    """
    Prompts user if they want to restart the program.

    Returns:
        (bool) - Whether or not user wants to restart the program
    """
    restart_choice = input('\nWould you like to restart? Enter "yes" or "no": ').strip().lower()
    if restart_choice == 'yes':
        return True
    elif restart_choice == 'no':
        return False
    else:
        print('An invalid input was provided. Try again.')
        return get_restart()

def main():
    """Run the program via the overall main function"""
    run_program = True
    while run_program:
        city, month, day = get_filters()
        if not month and not day:
            print(f'You are filtering by...\nCity: {city.title()}\nMonth: ALL (Jan=1, June=06)\nDay: ALL')
        elif not month:
            print(f'You are filtering by...\nCity: {city.title()}\nMonth: ALL (Jan=1, June=06)\nDay: {day}')
        elif not day:
            print(f'You are filtering by...\nCity: {city.title()}\nMonth: {month} (Jan=1, June=06)\nDay: ALL')
        else:
            print(f'You are filtering by...\nCity: {city.title()}\nMonth: {month} (Jan=1, June=06)\nDay: {day}')
        
        df = load_data(city, month, day)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        show_raw = True
        num_entries_to_show = 5
        start_index = 0
        while show_raw:
            # Solicit and show raw data
            see_raw = input('\nWould you like to see individual trip data? Type "yes" or "no": ').strip().lower()
            if see_raw == 'yes':
                for _ in range(num_entries_to_show):
                    entry_data = next(get_raw_data(df, start_index))
                    print(f'---\n{entry_data}')
                    start_index += 1
            elif see_raw == 'no':
                show_raw = False
            else:
                print('Invalid input!')

        restart = get_restart()
        if not restart:
            run_program = False

if __name__ == "__main__":
	main()
