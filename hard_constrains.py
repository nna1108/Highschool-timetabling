import prepare_data

#position = (highschool_class, day, period) 
#event = [[subject, teacher], highschool_class]
#event = [[[subject, teacher], [subject, teacher]], highschool_class]

data = prepare_data.read_json('THPT_CG_input.json')

#HC3
def subject_unoverload(event, position, subject_in_period):
    subject = event[0][0][0]
    highschool_class = event[1]
    
    if len(event[0]) == 1:
        day = position[1]
        subject_in_period[highschool_class][day].append(subject)
        
        subject_count = subject_in_period[highschool_class][day].count(subject)
        
        subject_in_period[highschool_class][day].remove(subject)
    
    else:
        day = position[0][1]
        for pos in position:
            subject_in_period[pos[0]][pos[1]].append(subject)
        
        subject_count = subject_in_period[highschool_class][day].count(subject)
        
        for pos in position:
            subject_in_period[pos[0]][pos[1]].remove(subject)
            
    if subject_count <= max(data['Events']['blocks'][highschool_class][subject]):
        return True

#HC4
def teacher_available(event, position, teacher_in_period):
    teacher = event[0][0][1]
    
    if len(event[0]) == 1:
        period = position[2]
        if teacher not in teacher_in_period[period]:
            return True
    else:
        period_1 = position[0][2]
        period_2 = position[1][2]
        if teacher not in teacher_in_period[period_1] and teacher not in teacher_in_period[period_2]:
            return True

#kiem tra vi pham HC
def HC_check(event, position, subject_in_period, teacher_in_period):
    return subject_unoverload(event, position, subject_in_period) and teacher_available(event, position, teacher_in_period)