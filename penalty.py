def total_check_hard(data, timetable, subject_in_period, teacher_in_period):
    count_HC1, count_HC3, count_HC4, count_SC = 0, 0, 0, 0
    not_violated_SC, violated_SC = [], []
    
    over_subject = {}
    for highschool_class in data['Classes']['Class_ID']:
        over_subject.update({highschool_class: {}})
        for day in list(data['Events']['timetable'][highschool_class].keys()):
            over_subject[highschool_class].update({day: []})
    
    over_teacher = {}
    for period in range(1, 57):
        over_teacher.update({period: []})
        
    for position in timetable:
        #check HC1
        if timetable[position] != None:
            count_HC1 += 0
            
            #check HC3
            subject_count = subject_in_period[position[0]][position[1]].count(timetable[position][0][0][0])
            if subject_count <= max(data['Events']['blocks'][position[0]][timetable[position][0][0][0]]):
                count_HC3 += 0
            else:
                if timetable[position][0][0][0] in over_subject[position[0]][position[1]]:
                    count_HC3 += 0
                else:
                    count_HC3 += 1
                    over_subject[position[0]][position[1]].append(timetable[position][0][0][0])
            
            #check HC4
            teacher_count = teacher_in_period[position[2]].count(timetable[position][0][0][1])
            if teacher_count == 1:
                count_HC4 += 0
                
            else:
                if timetable[position][0][0][1] in over_teacher[position[2]]:
                    count_HC4 += 0
                else:
                    count_HC4 += teacher_count - 1
                    over_teacher[position[2]].append(timetable[position][0][0][1])
                
            #check SC
            if position[2] not in [1, 28, 29, 56]:
                if position[1] == 'Thu_hai' or position[1] == 'Thu_bay':
                    if position[2] == data['Events']['timetable'][position[0]][position[1]][1]:
                        if timetable[position][0][0][1] == data['Classes']['GVCN_ID'][position[0]]:
                            count_SC += 0
                            not_violated_SC.append(position)
                            
                            if timetable[position][2] == 2:
                                if position[1] == 'Thu_hai':
                                    not_violated_SC.append((position[0], position[1], position[2] + 1))
                                
                                elif position[1] == 'Thu_bay':
                                    not_violated_SC.append((position[0], position[1], position[2] - 1)) 
                                                    
                        else:
                            count_SC += 0.25
                            violated_SC.append(position)
                            
                            if timetable[position][2] == 2:
                                if position[1] == 'Thu_hai':
                                    violated_SC.append((position[0], position[1], position[2] + 1))
                                    
                                elif position[1] == 'Thu_bay':
                                    violated_SC.append((position[0], position[1], position[2] - 1))      
                    
                    else:
                        count_SC += 0
                
                elif position[1] not in ['Thu_hai', 'Thu_bay']:
                    count_SC += 0 
        
        else:
            count_HC1 += 1
    
    over_subject.clear()
    over_teacher.clear()
    
    return count_HC1, count_HC3, count_HC4, count_SC, not_violated_SC, violated_SC

def total_check_soft(data, timetable, subject_in_period, teacher_in_period):
    count_HC1, count_HC3, count_HC4, count_SC = 0, 0, 0, 0
    not_violated_SC, violated_SC = [], []
    
    over_subject = {}
    for highschool_class in data['Classes']['Class_ID']:
        over_subject.update({highschool_class: {}})
        for day in list(data['Events']['timetable'][highschool_class].keys()):
            over_subject[highschool_class].update({day: []})
    
    over_teacher = {}
    for period in range(1, 57):
        over_teacher.update({period: []})
        
    violated_HC4 = {} 
    for teacher in data['Teachers']['Teacher_ID']:
        violated_HC4.update({teacher: []})
        
    for position in timetable:
        #check HC1
        if timetable[position] != None:
            count_HC1 += 0
            
            #check HC3
            subject_count = subject_in_period[position[0]][position[1]].count(timetable[position][0][0][0])
            if subject_count <= max(data['Events']['blocks'][position[0]][timetable[position][0][0][0]]):
                count_HC3 += 0
            else:
                if timetable[position][0][0][0] in over_subject[position[0]][position[1]]:
                    count_HC3 += 0
                else:
                    count_HC3 += 1
                    over_subject[position[0]][position[1]].append(timetable[position][0][0][0])
            
            #check HC4
            teacher_count = teacher_in_period[position[2]].count(timetable[position][0][0][1])
            if teacher_count == 1:
                count_HC4 += 0
                
            else:
                if timetable[position][0][0][1] in over_teacher[position[2]]:
                    count_HC4 += 0
                else:
                    count_HC4 += teacher_count - 1
                    over_teacher[position[2]].append(timetable[position][0][0][1])
                
                if timetable[position][0][0][1] != data['Classes']['GVCN_ID'][position[0]]:
                    violated_HC4[timetable[position][0][0][1]].append(position)
                else:
                    violated_HC4[timetable[position][0][0][1]].append((position[0], 'GVCN', position[2]))
                
            #check SC
            if position[2] not in [1, 28, 29, 56]:
                if position[1] == 'Thu_hai' or position[1] == 'Thu_bay':
                    if position[2] == data['Events']['timetable'][position[0]][position[1]][1]:
                        if timetable[position][0][0][1] == data['Classes']['GVCN_ID'][position[0]]:
                            count_SC += 0
                            not_violated_SC.append(position)
                            
                            if timetable[position][2] == 2:
                                if position[1] == 'Thu_hai':
                                    not_violated_SC.append((position[0], position[1], position[2] + 1))
                                
                                elif position[1] == 'Thu_bay':
                                    not_violated_SC.append((position[0], position[1], position[2] - 1)) 
                                                    
                        else:
                            count_SC += 0.25
                            violated_SC.append(position)
                            
                            if timetable[position][2] == 2:
                                if position[1] == 'Thu_hai':
                                    violated_SC.append((position[0], position[1], position[2] + 1))
                                    
                                elif position[1] == 'Thu_bay':
                                    violated_SC.append((position[0], position[1], position[2] - 1))      
                    
                    else:
                        count_SC += 0
                
                elif position[1] not in ['Thu_hai', 'Thu_bay']:
                    count_SC += 0 
        
        else:
            count_HC1 += 1
    
    over_subject.clear()
    over_teacher.clear()
    
    return count_HC1, count_HC3, count_HC4, count_SC, not_violated_SC, violated_SC, violated_HC4