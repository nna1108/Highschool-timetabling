import prepare_data

#position = (highschool_class, day, period) 
#event = [[subject, teacher], highschool_class]
#event = [[[subject, teacher], [subject, teacher]], highschool_class]

data = prepare_data.read_json('THPT_CG_input.json')

#SC1 va SC2
def first_last_position(event, position):
    teacher = event[0][0][1]
    highschool_class = event[1]
    
    if len(event[0]) == 1:
        day = position[1]
        period = position[2]
    
        if day == 'Thu_hai' or day == 'Thu_bay':
            if period == data['Events']['timetable'][highschool_class][day][1]:
                if teacher == data['Classes']['GVCN_ID'][highschool_class]:
                    return True
            
            else:
                return True
        
        else:
            return True
    
    else:
        day = position[0][1]
        period_1 = position[0][2]
        period_2 = position[1][2]
        
        if day == 'Thu_hai':
            if period_1 == data['Events']['timetable'][highschool_class][day][1]:
                if teacher == data['Classes']['GVCN_ID'][highschool_class]:
                    return True
            
            else:
                return True
        
        elif day == 'Thu_bay':
            if period_2 == data['Events']['timetable'][highschool_class][day][1]:
                if teacher == data['Classes']['GVCN_ID'][highschool_class]:
                    return True
            
            else:
                return True
        
        else:
            return True
        
def check_block_len(event, position, timetable):
    if len(event[0]) == 1:
        if timetable[position][2] == 1:
            return True
        
        else:
            if position[1] == 'Thu_hai' and timetable[(position[0], position[1], position[2] + 2)][2] == 1:
                return True
    
    else:
        position_1 = position[0]
        position_2 = position[1]
        
        if timetable[position_1][2] == 1 and timetable[position_2][2] == 1:
            return True
        
        elif timetable[position_1][2] == 2:
            return True
        
        elif position_1[1] == 'Thu_hai' and timetable[position_1][2] == 1 and timetable[position_2][2] == 2:
            return True