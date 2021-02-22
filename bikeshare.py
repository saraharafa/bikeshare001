import pandas as pd
import time

# Declared global Dictionaries for city, month, day and filter type
citydict = {0: 'chicago.csv',
            1: 'new_york_city.csv',
            2: 'washington.csv'}

mdict = {1: 'January', 2: 'February',
         3: 'March', 4: 'April',
         5: 'May', 6: 'June'}

ddict = {1: 'Monday', 2: 'Tuesday',
         3: 'Wednesday', 4: 'Thursday',
         5: 'Friday', 6: 'Saturday', 7: 'Sunday'}
filterType = {0: 'day', 1: 'month', 2: 'both', 3: 'none'}


def show_raw_data(df):

    """Displays raw Data for users 5 rows by 5 rows"""

    #Checks if df rows aren't empty, or removes the empty rows.
    df.dropna(axis=0)
    #User enters a yes if they want to see 5 lines of raw data
    show_Data01 = input(
        '\nWould you like to see raw data? Enter yes or any other key for a no.\n')
    #length is used afterwards to check the end of the df
    length = len(df)
    #counter is used to count 5rows in each iteration
    counter = 0
    # print(df.iloc[0].to_string(header=False))
    #flag states the end of data.
    flag = False  # a flag to know if we reached end of df
    while True:
        if show_Data01.lower() != 'yes':
            break
        else:
            for i in range(counter*5, (counter*5)+5):
                if i != length-1:
                    print(df.iloc[i].to_string()+'\n' +
                          '-------------------------'+'\n')
                else:
                    flag = True
                    break

            print('\n', counter)
            counter += 1
            if flag:
                print('This is the end of data.')
                break
            show_Data01 = input(
                '\nWould you like to see more raw data? Enter yes or any other key for a no.\n')
            if show_Data01.lower() != 'yes':
                break
            else:
                continue


def user_input_statistics(df, cityType):

    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print(user_types)
    # Display counts of gender and handles cities that doesn't include this clmn of gender
    if cityType != 2:  # NYC and Chicago only
        gender_types = df['Gender'].value_counts()
        print(gender_types)
        # Display earliest, most recent, and most common year of birth
        print("Most comon year of birth: ", df['Birth Year'].mode()[0])
        minValue = df['Birth Year'].min()
        print("Earliest year of birth is:", minValue)
        maxValue = df['Birth Year'].max()
        print('Most recent year of birth is:', maxValue)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_statistics(df):
    
    """Displays statistics on bikeshare trip duration."""

    #Add a duration column to the df 
    df['Duration'] = (df['End Time'] - df['Start Time'])
    # print(df['Duration'].astype('timedelta64[s]'))
    # Display total, and average time travel
    print("Total travel time is:", (df['Duration']).sum(), '\n')
    print("Average time is:", (df['Duration']).mean(), '\n')


def trip_statistics(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_st_station = df['Start Station'].mode()[0]
    print('Most Popular Start Station:', popular_st_station)

    # display most commonly used end station
    popular_end_station = df['End Station'].mode()[0]
    print('Most Popular End Station:', popular_end_station)

    # display most frequent combination of start station and end station trip
    Xgrouped = (df.groupby(['Start Station', 'End Station']
                           ).size().sort_values(ascending=False))
    stSt, endSt = Xgrouped[Xgrouped == Xgrouped.iloc[0]].index[0]

    print('Most Popular combined Start station :{} and End Stations: {}'.format(
        stSt, endSt))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def time_statistics(df):

    """Displays statistics on Start Time and End Time of the trips."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    popular_month = df['sMonth'].mode()[0]
    print('Most Popular Start Month:', popular_month)

    # display the most common day of week
    popular_day = df['sDay'].mode()[0]
    print('Most Popular Start Day:', popular_day)

    # display the most common start hour
    popular_hour = df['sHour'].mode()[0]
    print('Most Popular Start Hour:', popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def get_ui():
    """
    Asks user to specify a city, month, and day to analyze, and which filter do they need

    Returns:
        (int) city - number of the city to analyze; used dictionary
        (int) month - numberof the month to filter by, or "all" to apply no month filter
        (int) day - number of the day of week to filter by, or "all" to apply no day filter
        (int)filterType - filter type number; used dictionary
    """
    # get user input for city (chicago, new york city, washington).
    citymsg = "Type the city number you'd like to see the Data for:\n'0': Chicago,'1': New York,'2': Washington."
    while True:
        try:
            cityui = int(input(citymsg))
            if cityui in citydict:
                break
            else:
                print("You've entered a wrong number.Please try again.")
                continue
        except Exception:
            print('You\'ve entered an exception: {}, please try again.'.format(Exception))
            continue

    # get user input for filter type (Day, Month, Both, None)
    fmsg = "Type the filter number you'd like to do: 0->By Day, 1->By Month, 2->Both, 3->No Filter"
    while True:
        try:
            filterui = int(input(fmsg))
            if filterui in filterType:
                #filter 3 is the no filter type which returns the city only as is to read
                if filterui == 3:
                    return cityui, False, False, filterui
                else:
                    break
            else:
                print("You've entered a wrong number.Please try again.")
                continue
        except Exception:
            print('You\'ve entered an exception: {}, please try again.'.format(Exception))
            continue
    mmsg = """Type the month number:\n '1': January,'2': February,'3': March,'4': April,'5': May,'6': June"""
    # get user input for month (all, january, february, ... , june)

    if filterui == 1 or filterui == 2:  # if filter is both or month
        while True:
            try:
                monthui = int(input(mmsg))
                if monthui in mdict:
                    if filterui == 2:
                        break
                    else:
                        return cityui, monthui, False, filterui
                else:
                    print("You've entered a wrong number.Please try again.")
                    continue
            except Exception:
                print(
                    'You\'ve entered an exception: {}, please try again.'.format(Exception))
                continue

        # get user input for day of week (all, monday, tuesday, ... sunday)
    dmsg = """Please type the day's number:\n1 : 'Monday', 2 : 'Tuesday', 3 : 'Wednesday', 4 : 'Thursday',5 : 'Friday', 6 : 'Saturday',7 : 'Sunday'."""

    while True:
        try:
            dayui = int(input(dmsg))
            if dayui in ddict:
                if filterui == 0:
                    #print(cityui, 'False', dayui, filterui)
                    return cityui, False, dayui, filterui
                else:
                    return cityui, monthui, dayui, filterui
            else:
                print("You've entered a wrong number.Please try again.")
                continue
        except Exception:
            print('You\'ve entered an exception: {}, please try again.'.format(Exception))
            continue


def read_csv_city(citynum, monthnum, daynum, filternum):

    """Reads csv file for given city, month, day, acctording to given filter number"""

    cityfile = citydict[citynum]
    data00 = pd.read_csv(cityfile,
                         parse_dates=['Start Time', 'End Time'], na_values=['no info', '.', '??'],
                         dtype={"Trip duration": float, "Birth Year": float, "Start Station":
                                str, "End Station": str, "User Type": str})
    # extract month and day of week from Start Time to create new columns
    data00['sDay'], data00['sMonth'], data00['sHour'] = data00['Start Time'].dt.day_name(
    ), data00['Start Time'].dt.month, data00['Start Time'].dt.hour

    while True:
        if filternum == 3:  # no filter
            print(data00.head())
            return data00
        elif filternum == 2 or filternum == 0:
            data00 = data00[data00["sDay"] == ddict.get(daynum)]
            if filternum == 0:
                print(data00.head())
                return data00
            else:
                data00 = data00[data00["sMonth"] == monthnum]
                print(data00.head())
                return data00
        else:
            data00 = data00[data00["sMonth"] == monthnum]
            print(data00.head())
            return data00


def main():

    """This is the main function that runs bikeshare.py"""

    print('Hello! Let\'s explore some US bikeshare data!\n')
    while True:
        #Get user filter type needed using get_ui() function
        city, month, day, filterS = get_ui()
        #enter city, month, day, filtertype into read_csv_city to read the file, and filter it
        filteredData = read_csv_city(city, month, day, filterS)
        #the dataframe filtered if it contains data, if empty it returns back to the while loop to refilter the data
        if filteredData.empty:
            print('\nPlease choose another filters as this one has empty data\n')
            break
        time_statistics(filteredData)
        trip_statistics(filteredData)
        trip_duration_statistics(filteredData)
        user_input_statistics(filteredData, city)
        show_raw_data(filteredData)
        restart = input(
            '\nWould you like to restart? Enter yes or any other key to exit.\n')
        if restart.lower() != 'yes':
            print("Thanks for using Bikeshare data analysis")
            break
        else:
            continue


if __name__ == "__main__":
    main()
