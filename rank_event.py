import prepare_data

data = prepare_data.read_json('THPT_CG_input.json')
teacher_data = prepare_data.assigned_to_teacher(data)[0]

def is_len_2(event):
    if len(event[0]) == 2:
        return True

def is_GVCN(event):
    teacher = event[0][0][1]
    highschool_class = event[1]
    
    if teacher == data['Classes']['GVCN_ID'][highschool_class]:
        return True
    
def is_Mon_or_Sat(position, event):
    if len(event[0]) == 2:
        if position[0][1] == 'Thu_hai' or position[0][1] == 'Thu_bay':
            return True
    
    else:
        if position[1] == 'Thu_hai' or position[1] == 'Thu_bay':
            return True

def count_teacher_workload(event):
    teacher = event[0][0][1]
        
    return len(teacher_data[teacher])

def rank_event(event):
    len_event = len(event[0]) * 20
    
    teacher_workload = count_teacher_workload(event) * 0.2
    
    return len_event + teacher_workload

def order_event(class_assigned_teacher):
    rank_1 = []
    rank_2 = []
    rank_3 = []
    rank_4 = []
    
    for event in class_assigned_teacher:
        if is_len_2(event) and is_GVCN(event):
            rank_1.append([event, rank_event(event) + 20])
        
        elif is_len_2(event) == False and is_GVCN(event):
            rank_2.append([event, rank_event(event) + 5])
        
        elif is_len_2(event) and is_GVCN(event) == False:
            rank_3.append([event, rank_event(event)])
        
        else:
            rank_4.append([event, rank_event(event)])
    
    rank_1.sort(key=lambda rank_1: rank_1[1], reverse = True)
    rank_1 = [event[0] for event in rank_1]
    
    rank_2.sort(key=lambda rank_2: rank_2[1], reverse = True)
    rank_2 = [event[0] for event in rank_2]
    
    rank_3.sort(key=lambda rank_3: rank_3[1], reverse = True)
    rank_3 = [event[0] for event in rank_3]
    
    rank_4.sort(key=lambda rank_4: rank_4[1], reverse = True)
    rank_4 = [event[0] for event in rank_4]
    
    list_of_event = rank_1 + rank_2 + rank_3 + rank_4
    
    return list_of_event

def order_event_GVCN(GVCN_event):
    rank_1 = []
    rank_2 = []
    rank_3 = []
    rank_4 = []
    
    for position, event in GVCN_event:
        if is_len_2(event) and is_Mon_or_Sat(position, event):
            rank_1.append([position, event, rank_event(event) + 20])
        
        elif is_len_2(event) == False and is_Mon_or_Sat(position, event):
            rank_2.append([position, event, rank_event(event) + 5])
        
        elif is_len_2(event) and is_Mon_or_Sat(position, event) == False:
            rank_3.append([position, event, rank_event(event) + 10])
            
        else:
            rank_4.append([position, event, rank_event(event)])
            
    rank_1.sort(key=lambda rank_1: rank_1[2], reverse = True)
    rank_1 = [[event[0], event[1]] for event in rank_1]
    
    rank_2.sort(key=lambda rank_2: rank_2[2], reverse = True)
    rank_2 = [[event[0], event[1]] for event in rank_2]
    
    rank_3.sort(key=lambda rank_3: rank_3[2], reverse = True)
    rank_3 = [[event[0], event[1]] for event in rank_3]
    
    rank_4.sort(key=lambda rank_4: rank_4[2], reverse = True)
    rank_4 = [[event[0], event[1]] for event in rank_4]
    
    list_of_event = rank_1 + rank_2 + rank_3 + rank_4
    
    return list_of_event