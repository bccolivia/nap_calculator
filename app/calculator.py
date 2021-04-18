import pandas as pd
import numpy as np
import math
import datetime as dt
from itertools import product
from itertools import combinations
import operator
import time
import sys

def NapGenerator(
    wake_window_length_value_min,
    wake_window_length_value_max,
    wake_window_length_label,
    nap_length_value_min,
    nap_length_value_max,
    nap_length_label,
    earliest_bedtime,
    latest_bedtime,
    last_nap_start_time,
    last_nap_still_ongoing,
    possible_num_naps,
    round_times_by,
    last_nap_end_time = None,
    ):
    
    # Cleaning variables:
    min_wake_window = pd.Timedelta(str(wake_window_length_value_min)+wake_window_length_label)
    max_wake_window = pd.Timedelta(str(wake_window_length_value_max)+wake_window_length_label)
    min_nap_length = pd.Timedelta(str(nap_length_value_min)+nap_length_label)
    max_nap_length = pd.Timedelta(str(nap_length_value_max)+nap_length_label)
    
    earliest_bedtime = pd.Timestamp(
        tz='US/Pacific',
        year=pd.Timestamp.now(tz='US/Pacific').year, 
        month=pd.Timestamp.now(tz='US/Pacific').month, 
        day=pd.Timestamp.now(tz='US/Pacific').day, 
        hour=earliest_bedtime.hour,
        minute=earliest_bedtime.minute,
        )
    latest_bedtime = pd.Timestamp(
        tz='US/Pacific',
        year=pd.Timestamp.now(tz='US/Pacific').year, 
        month=pd.Timestamp.now(tz='US/Pacific').month, 
        day=pd.Timestamp.now(tz='US/Pacific').day, 
        hour=latest_bedtime.hour,
        minute=latest_bedtime.minute,
        )
    
    last_nap_start_time = pd.Timestamp(
        tz='US/Pacific',
        year=pd.Timestamp.now(tz='US/Pacific').year, 
        month=pd.Timestamp.now(tz='US/Pacific').month, 
        day=pd.Timestamp.now(tz='US/Pacific').day, 
        hour=last_nap_start_time.hour,
        minute=last_nap_start_time.minute,
        )
    if last_nap_end_time is not None:
        last_nap_end_time = pd.Timestamp(
            tz='US/Pacific',
            year=pd.Timestamp.now(tz='US/Pacific').year, 
            month=pd.Timestamp.now(tz='US/Pacific').month, 
            day=pd.Timestamp.now(tz='US/Pacific').day, 
            hour=last_nap_end_time.hour,
            minute=last_nap_end_time.minute,
            )
    
    possible_num_naps = list(range(possible_num_naps+1))
    print(round_times_by, file=sys.stderr)
    round_times_by_num = int(round_times_by.split()[0])
    now_time =  pd.Timestamp.now(tz='US/Pacific')
#    For testing at different now_times
#    now_time = pd.Timestamp(
#        tz='US/Pacific',
#        year=pd.Timestamp.now(tz='US/Pacific').year, 
#        month=pd.Timestamp.now(tz='US/Pacific').month, 
#        day=pd.Timestamp.now(tz='US/Pacific').day, 
#        hour=12,
#        minute=30,
#        )
    last_nap_still_ongoing = last_nap_still_ongoing == 'True'
    
    print('Variables cleaned. Moving on to generating naps.', file=sys.stderr)
    
    # Generating possible nap, wake window lengths, and when to wake wake from ongoing nap
    possible_nap_lengths = []
    i = min_nap_length
    print(round_times_by, file=sys.stderr)
    print(type(round_times_by), file=sys.stderr)
    while i <= max_nap_length:
        possible_nap_lengths.append(i)
        i += pd.Timedelta(round_times_by)

    if last_nap_still_ongoing == True:
        possible_ongoing_nap_length = []
        possible_nap_end = max(now_time, last_nap_start_time + min_nap_length)
        
        print('Current nap length: '+str(possible_nap_end))
        while possible_nap_end <= max(now_time, last_nap_start_time + max_nap_length):
            possible_ongoing_nap_length.append(((possible_nap_end-last_nap_start_time),))
            
            possible_nap_end += pd.Timedelta(round_times_by)
            
            print('New nap length: '+str(possible_nap_end))
            num_seconds = (possible_nap_end.minute*60)
            delta = math.floor(num_seconds / (round_times_by_num*60)) * (round_times_by_num*60) - num_seconds
            possible_nap_end = possible_nap_end + dt.timedelta(seconds=delta)

            print('Rounded nap length: '+str(possible_nap_end))
            
    possible_wake_window_lengths = []
    i = min_wake_window
    while i <= max_wake_window:
        possible_wake_window_lengths.append(i)
        i += pd.Timedelta(round_times_by)
    
    print('Nap and ww increments created. Now generating possibilities.', file=sys.stderr)
    
    ## Creating combos of naps and wake window lengths
    ## Number of naps here includes the ongoing nap
    nap_possibilities = pd.DataFrame()

    for num_nap in possible_num_naps:
        print('Checking for '+str(num_nap)+' naps', file=sys.stderr)
        nap_possibility = pd.DataFrame()

        print('Generating nap sequences and wake window sequences', file=sys.stderr)
        nap_combos = list(product(possible_nap_lengths,repeat=num_nap))
        ww_combos = list(product(possible_wake_window_lengths,repeat=num_nap+1))

        print('Generating nap+wake window sequences', file=sys.stderr)
        ## Nap sequence includes the ongoing nap
        if last_nap_still_ongoing == True:
            all_combos_tuple = list(product(possible_ongoing_nap_length, nap_combos, ww_combos))
            nap_sequence = [list(i[0])+ list(i[1]) for i in all_combos_tuple]
            ww_sequence = [list(i[2]) for i in all_combos_tuple]
        elif last_nap_still_ongoing == False:
            all_combos_tuple = list(product(nap_combos, ww_combos))
            nap_sequence = [list(i[0]) for i in all_combos_tuple]
            ww_sequence = [list(i[1]) for i in all_combos_tuple]

        print('Sequences created. Combining sequences together.', file=sys.stderr)
        all_combos = []
        for element in all_combos_tuple:
            combos_summed = [i for sub in element for i in sub]
            all_combos.append(combos_summed)

        print(str(len(all_combos))+' combinations created. Summing length of each combo.', file=sys.stderr)
        total_lengths = []
        for combo in all_combos:
            total_lengths.append(pd.Series(combo).sum())

        print('Creating dataframe', file=sys.stderr)
        nap_possibility['nap_sequence'] = nap_sequence
        nap_possibility['ww_sequence'] = ww_sequence
        nap_possibility['total_time'] = total_lengths
        nap_possibility['num_naps'] = num_nap

        nap_possibilities = nap_possibilities.append(nap_possibility)

    print('Done generating nap possibilities. Now filtering based on valid possibilities.', file=sys.stderr)
    
    # Filter possibilities based on bedtime
    valid_possibilities = nap_possibilities

    if last_nap_still_ongoing == True:
        valid_possibilities['bedtime'] = last_nap_start_time + valid_possibilities['total_time']
    elif last_nap_still_ongoing == False:
        valid_possibilities['bedtime'] = last_nap_end_time + valid_possibilities['total_time']

    valid_possibilities = valid_possibilities[valid_possibilities['bedtime'] >=  earliest_bedtime]
    valid_possibilities = valid_possibilities[valid_possibilities['bedtime'] <=  latest_bedtime]
    
    # Stop calculator if there are no valid possibilities
    if len(valid_possibilities) == 0:
        cleaned_possibilities = nap_possibilities.sort_values(by=['bedtime'],ascending=False).head(15)
        message = 'No nap and wake window combinations will achieve the desired bedtime. Try loosening some of the parameters. The table below shows a sample of some scenarios generated, but none achieve the desired bedtime.'
    elif len(valid_possibilities) > 0:

        # Add preference column based on min nap length
        if last_nap_still_ongoing == True:
            valid_possibilities['last_nap_length'] = [i[0] for i in valid_possibilities['nap_sequence']]
        elif last_nap_still_ongoing == False:
            valid_possibilities['last_nap_length'] = last_nap_end_time - last_nap_start_time 
        valid_possibilities['next_ww'] = [i[0] for i in valid_possibilities['ww_sequence']]
        valid_possibilities['start_next_nap_at'] = last_nap_start_time + valid_possibilities['last_nap_length'] + valid_possibilities['next_ww']

        min_nap_length_boolean = []
        if last_nap_still_ongoing == True:
            for nap_sequence in valid_possibilities['nap_sequence']:
                min_nap_length_boolean.append(all([nap == min_nap_length for nap in nap_sequence[1:]]))
        elif last_nap_still_ongoing == False:
            for nap_sequence in valid_possibilities['nap_sequence']:
                min_nap_length_boolean.append(all([nap == min_nap_length for nap in nap_sequence]))
        valid_possibilities['preferred'] = min_nap_length_boolean
        preferred_map = valid_possibilities[['start_next_nap_at','preferred']][valid_possibilities['preferred'] == True].drop_duplicates()

        valid_possibilities = valid_possibilities.drop(['preferred'], axis=1)
        valid_possibilities = valid_possibilities.merge(preferred_map, on='start_next_nap_at', how='left')
        valid_possibilities = valid_possibilities.fillna(False)

        print('Done validating possibilities. Now cleaning output.', file=sys.stderr)
        # Simplify the output
        ## Reformating the time columns to be more readable
        cleaned_possibilities = valid_possibilities
        cleaned_possibilities['bedtime'] = cleaned_possibilities['bedtime'].dt.strftime("%-I:%M%p")

        pretty_nap_sequence = []
        for row in cleaned_possibilities['nap_sequence']:
            pretty_nap_sequence.append([time.strftime("%H:%M", time.gmtime(s.seconds)) for s in row])
        cleaned_possibilities['length_of_naps'] = pretty_nap_sequence

        pretty_ww_sequence = []
        for row in cleaned_possibilities['ww_sequence']:
            pretty_ww_sequence.append([time.strftime("%H:%M", time.gmtime(s.seconds)) for s in row])
        cleaned_possibilities['length_of_wake_windows'] = pretty_ww_sequence
        ## Again, how_many_more_naps is how many additional more naps
        cleaned_possibilities['start_next_nap_at'] = cleaned_possibilities['start_next_nap_at'].dt.strftime("%-I:%M%p")
        cleaned_possibilities['how_many_more_naps'] = cleaned_possibilities['num_naps']
        cleaned_possibilities['works_even_if_all_remaining_naps_are_short'] = cleaned_possibilities['preferred']

        if last_nap_still_ongoing == True:
            cleaned_possibilities['cap_nap_at'] = last_nap_start_time + cleaned_possibilities['last_nap_length']
            cleaned_possibilities['cap_nap_at'] = cleaned_possibilities['cap_nap_at'].dt.strftime("%-I:%M%p")

            cleaned_possibilities = cleaned_possibilities[[
                'cap_nap_at',
                'how_many_more_naps',
                'start_next_nap_at',
                'bedtime',
                'length_of_naps',
                'length_of_wake_windows',
                'works_even_if_all_remaining_naps_are_short'
                ]]

            best_cleaned_possibilities = cleaned_possibilities[cleaned_possibilities['works_even_if_all_remaining_naps_are_short'] == True]
            if len(best_cleaned_possibilities) > 0:
                nap_cap = max(best_cleaned_possibilities['cap_nap_at'])
                best_cleaned_possibilities = best_cleaned_possibilities[best_cleaned_possibilities['cap_nap_at'] == nap_cap]
                next_nap_start = min(best_cleaned_possibilities['start_next_nap_at'])
                next_nap_end = max(best_cleaned_possibilities['start_next_nap_at'])
                bedtime_start = min(best_cleaned_possibilities['bedtime'])
                bedtime_end = max(best_cleaned_possibilities['bedtime'])

                if next_nap_start == next_nap_end:
                    message = 'I suggest capping the nap at '+nap_cap+' and starting the next nap at '+next_nap_start+' in order to achieve a bedtime of '+bedtime_start+'. Capping the nap at '+nap_cap+' will ensure that even if all the remaining naps are short, a desired bedtime will still be achieved.'
                elif next_nap_start != next_nap_end:
                    message = 'I suggest capping the nap at '+nap_cap+' and starting the next nap between '+next_nap_start+' and '+next_nap_end+' in order to achieve a bedtime of '+bedtime_start+'-'+bedtime_end+'. Capping the nap at '+nap_cap+' will ensure that even if all the remaining naps are short, a desired bedtime will still be achieved.'
            elif len(best_cleaned_possibilities) == 0:
                message = 'All nap and wake window combinations depend on the baby having longer naps.'
            
            cleaned_possibilities['length_of_naps'] = cleaned_possibilities['length_of_naps'].astype(str)
            cleaned_possibilities = cleaned_possibilities.sort_values(by=['works_even_if_all_remaining_naps_are_short','start_next_nap_at', 'length_of_naps'], ascending=False).reset_index(drop=True)
            cleaned_possibilities.columns = [
                'Cap current nap at',
                '# of remaining naps',
                'Start next nap at',
                'Bedtime',
                'Length of remaining naps (including current nap)',
                'Length of wake windows',
                'Works even if all remaining naps are short?'
                ]
                
        elif last_nap_still_ongoing == False:
            cleaned_possibilities = cleaned_possibilities[[
                'how_many_more_naps',
                'start_next_nap_at',
                'bedtime',
                'length_of_naps',
                'length_of_wake_windows',
                'works_even_if_all_remaining_naps_are_short'
                ]]
            
            best_cleaned_possibilities = cleaned_possibilities[cleaned_possibilities['works_even_if_all_remaining_naps_are_short'] == True]
            if len(best_cleaned_possibilities) > 0:
                next_nap_start = min(best_cleaned_possibilities['start_next_nap_at'])
                next_nap_end = max(best_cleaned_possibilities['start_next_nap_at'])
                bedtime_start = min(best_cleaned_possibilities['bedtime'])
                bedtime_end = max(best_cleaned_possibilities['bedtime'])
            
                if next_nap_start == next_nap_end:
                    message = 'I suggest starting the next nap between '+next_nap_start+' in order to achieve a bedtime of '+bedtime_start+'. Starting the next nap between '+next_nap_start+' will ensure that even if all the remaining naps are short, a desired bedtime will still be achieved.'
                elif next_nap_start != next_nap_end:
                    message = 'I suggest starting the next nap between '+next_nap_start+' and '+next_nap_end+' in order to achieve a bedtime of '+bedtime_start+'-'+bedtime_end+'. Starting the next nap between '+next_nap_start+' will ensure that even if all the remaining naps are short, a desired bedtime will still be achieved.'
            elif len(best_cleaned_possibilities) == 0:
                message = 'All nap and wake window combinations depend on the baby having longer naps.'
            
            cleaned_possibilities['length_of_naps'] = cleaned_possibilities['length_of_naps'].astype(str)
            cleaned_possibilities = cleaned_possibilities.sort_values(by=['works_even_if_all_remaining_naps_are_short','start_next_nap_at', 'length_of_naps'], ascending=False).reset_index(drop=True)
            cleaned_possibilities.columns = [
                '# of remaining naps',
                'Start next nap at',
                'Bedtime',
                'Length of remaining naps',
                'Length of wake windows',
                'Works even if all remaining naps are short?'
                ]

        message = message+' The table below shows all possible nap and wake window combinations that achieve the desired bedtime.'
    
    return cleaned_possibilities, message