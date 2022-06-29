import random
import bisect
import numpy as np

import prepare_data
import rank_position
import rank_event
import penalty
import hard_constrains as HC

def find_block(timetable, position, event):
    first_period = [p for p in range(6, 31, 5)] + [2, 30] + [p for p in range(34, 59, 5)]
    last_period = [p for p in range(5, 30, 5)] + [27, 55] + [p for p in range(33, 58, 5)]
    
    if position[2] in first_period:
        next_pos = (position[0], position[1], position[2] + 1)
        return [event, position, timetable[next_pos], next_pos]
    
    elif position[2] in last_period:
        pre_pos = (position[0], position[1], position[2] - 1)
        return [timetable[pre_pos], pre_pos, event, position]
    
    else:
        pre_pos = (position[0], position[1], position[2] - 1)
        next_pos = (position[0], position[1], position[2] + 1)
    
        if timetable[pre_pos] == event:
            return [timetable[pre_pos], pre_pos, event, position]
        
        elif timetable[next_pos] == event:
            return [event, position, timetable[next_pos], next_pos]
        
def find_all_event(position, timetable, data, not_violated_SC):
    highschool_class = position[0]
    day = position[1]
    
    list_of_pos = []
    for day in data['Events']['timetable'][highschool_class]:
        for period in data['Events']['timetable'][highschool_class][day]:
            position_1 = (highschool_class, day, period)
            
            if position_1 not in not_violated_SC and timetable[position_1][0][0][0] not in ['Chao_co', 'Sinh_hoat'] and timetable[position_1][0][0][1] == timetable[position][0][0][1]:
                list_of_pos.append(position_1)
            
    return list_of_pos

def find_event_GVCN(timetable, data, violated_SC, not_violated_SC):
    over_class = []
    
    GVCN_event = []
    for position in violated_SC:
        if position[0] not in over_class:
            GVCN_event += find_all_event((position[0], 'Thu_hai', data['Events']['timetable'][position[0]]['Thu_hai'][0]), timetable, data, not_violated_SC)
            over_class.append(position[0])
    
    GVCN_event_1 = []
    over_position = []
    for position in GVCN_event:
        idx = GVCN_event.index(position)
        
        if position not in over_position and idx < len(GVCN_event) - 1:
            if GVCN_event[idx + 1] == (position[0], position[1], position[2] + 1):
                new_pos = [position, GVCN_event[idx + 1]]
                new_event = [[timetable[position][0][0], timetable[position][0][0]], position[0], 2]
                GVCN_event_1 += [[new_pos, new_event]]
                over_position += [position, GVCN_event[idx + 1]]
            
            else:
                GVCN_event_1 += [[position, timetable[position]]]
                over_position += [position]
    
    over_class.clear()
    GVCN_event.clear()
    
    return GVCN_event_1
    
def mutation_hard(event, timetable, subject_in_period, teacher_in_period, data):
    #find position
    position_1 = rank_position.order_position(event, prepare_data.get_position(event, timetable, data), teacher_in_period, subject_in_period, timetable)
    if len(position_1) != 0:
        pos_1 = position_1[0]
        
        if len(event[0]) == 1:
            #timetable[pos_1][2] == 1
            if timetable[pos_1][2] == 1:
                position_2 = rank_position.order_position(timetable[pos_1], prepare_data.get_empty_position(timetable[pos_1], timetable, data), teacher_in_period, subject_in_period, timetable)
                if len(position_2) != 0:
                    pos_2 = position_2[0]
                    
                    subject_in_period[pos_1[0]][pos_1[1]].remove(timetable[pos_1][0][0][0])
                    teacher_in_period[pos_1[2]].remove(timetable[pos_1][0][0][1])
                    
                    timetable[pos_2] = timetable[pos_1]
                    timetable[pos_1] = None
                    timetable[pos_1] = [event[0], event[1], 1]
                    
                    for pos in [pos_1, pos_2]:
                       subject_in_period[pos[0]][pos[1]].append(timetable[pos][0][0][0])
                       teacher_in_period[pos[2]].append(timetable[pos][0][0][1])
               
            #timetable[pos_1][2] == 2
            else:
                #tim event con lai cua timetable[pos_1]
                #event_2 = timetable[pos_1]
                event_2a, pos_1a, event_2b, pos_1b = find_block(timetable, pos_1, timetable[pos_1])
                event_2 = [[event_2a[0][0], event_2b[0][0]], event_2a[1], 2]
                position_2 = rank_position.order_position(event_2, prepare_data.get_empty_position(event_2, timetable, data), teacher_in_period, subject_in_period, timetable)
                if len(position_2) != 0:
                    pos_2 = position_2[0]
                    
                    for pos in [pos_1a, pos_1b]:
                        subject_in_period[pos[0]][pos[1]].remove(timetable[pos][0][0][0])
                        teacher_in_period[pos[2]].remove(timetable[pos][0][0][1])
                    
                    timetable[pos_2[0]] = timetable[pos_1a]
                    timetable[pos_2[1]] = timetable[pos_1b]
                    
                    timetable[pos_1a] = None
                    timetable[pos_1b] = None
                    
                    timetable[pos_1] = [event[0], event[1], 1]
                    
                    for pos in [pos_1, pos_2[0], pos_2[1]]:
                        subject_in_period[pos[0]][pos[1]].append(timetable[pos][0][0][0])
                        teacher_in_period[pos[2]].append(timetable[pos][0][0][1])
                
        else:
            #pos_1 is a complete block
            if timetable[pos_1[0]] == timetable[pos_1[1]]:
                event_2 = [[timetable[pos_1[0]][0][0], timetable[pos_1[1]][0][0]], pos_1[0][0], 2]
                position_2 = rank_position.order_position(event_2, prepare_data.get_empty_position(event_2, timetable, data), teacher_in_period, subject_in_period, timetable)
                if len(position_2) != 0:
                    pos_2 = position_2[0]
                    
                    for pos in pos_1:
                        subject_in_period[pos[0]][pos[1]].remove(timetable[pos][0][0][0])
                        teacher_in_period[pos[2]].remove(timetable[pos][0][0][1])
                    
                    timetable[pos_2[0]] = timetable[pos_1[0]]
                    timetable[pos_2[1]] = timetable[pos_1[1]]
                    
                    timetable[pos_1[0]] = None
                    timetable[pos_1[0]] = [[event[0][0]], event[1], 2]
                    
                    timetable[pos_1[1]] = None
                    timetable[pos_1[1]] = [[event[0][1]], event[1], 2]
                        
                    for pos in [pos_1[0], pos_1[1], pos_2[0], pos_2[1]]:
                        subject_in_period[pos[0]][pos[1]].append(timetable[pos][0][0][0])
                        teacher_in_period[pos[2]].append(timetable[pos][0][0][1])
                        
            elif timetable[pos_1[0]][2] == 1 and timetable[pos_1[1]][2] == 2:
                #find empty position for timetable[pos_1[0]]
                position_2a = rank_position.order_position(timetable[pos_1[0]], prepare_data.get_empty_position(timetable[pos_1[0]], timetable, data), teacher_in_period, subject_in_period, timetable)
                
                #find remaining block of timetable[pos_1[1]] and empty position for double block
                event_2b, pos_1b, event_2c, pos_1c = find_block(timetable, pos_1[1], timetable[pos_1[1]])
                event_2 = [[event_2b[0][0], event_2c[0][0]], pos_1b[0], 2]
                position_2b = rank_position.order_position(event_2, prepare_data.get_empty_position(event_2, timetable, data), teacher_in_period, subject_in_period, timetable)
                
                if len(position_2a) != 0 and len(position_2b) != 0:
                    pos_2a = position_2a[0]
                    pos_2b = position_2b[0]
                    
                    if pos_2a not in pos_2b:
                        for pos in [pos_1[0], pos_1b, pos_1c]:
                            subject_in_period[pos[0]][pos[1]].remove(timetable[pos][0][0][0])
                            teacher_in_period[pos[2]].remove(timetable[pos][0][0][1])
                        
                        #put block into new position
                        timetable[pos_2a] = timetable[pos_1[0]]
                        timetable[pos_2b[0]] = timetable[pos_1b]
                        timetable[pos_2b[1]] = timetable[pos_1c]
                        
                        #remove occupied event
                        for pos in [pos_1[0], pos_1b, pos_1c]:
                            timetable[pos] = None
                        
                        #put event into chosen position
                        timetable[pos_1[0]] = [[event[0][0]], event[1], 2]
                        timetable[pos_1[1]] = [[event[0][0]], event[1], 2]
                        
                        #update data
                        for pos in [pos_2a, pos_1[0], pos_1[1], pos_2b[0], pos_2b[1]]:
                            subject_in_period[pos[0]][pos[1]].append(timetable[pos][0][0][0])
                            teacher_in_period[pos[2]].append(timetable[pos][0][0][1])
                        
            elif timetable[pos_1[0]][2] == 2 and timetable[pos_1[1]][2] == 1:
                #find remaining block of timetable[pos_1[0]] and empty position for double block
                event_2a, pos_1a, event_2b, pos_1b = find_block(timetable, pos_1[0], timetable[pos_1[0]])
                event_2 = [[event_2a[0][0], event_2b[0][0]], pos_1a[0], 2]
                position_2a = rank_position.order_position(event_2, prepare_data.get_empty_position(event_2, timetable, data), teacher_in_period, subject_in_period, timetable)
                
                #find empty position for timetable[pos_1[1]]
                position_2b = rank_position.order_position(timetable[pos_1[1]], prepare_data.get_empty_position(timetable[pos_1[1]], timetable, data), teacher_in_period, subject_in_period, timetable)
                
                if len(position_2a) != 0 and len(position_2b) != 0:
                    pos_2a = position_2a[0]
                    pos_2b = position_2b[0]
                    
                    if pos_2b not in pos_2a:
                        for pos in [pos_1[1], pos_1a, pos_1b]:
                            subject_in_period[pos[0]][pos[1]].remove(timetable[pos][0][0][0])
                            teacher_in_period[pos[2]].remove(timetable[pos][0][0][1])
                        
                        #put block into new position
                        timetable[pos_2a[0]] = timetable[pos_1a]
                        timetable[pos_2a[1]] = timetable[pos_1b]
                        timetable[pos_2b] = timetable[pos_1[1]]
                        
                        #remove occupied event
                        for pos in [pos_1[1], pos_1a, pos_1b]:
                            timetable[pos] = None
                        
                        #put event into chosen position
                        timetable[pos_1[0]] = [[event[0][0]], event[1], 2]
                        timetable[pos_1[1]] = [[event[0][0]], event[1], 2]
                        
                        #update data
                        for pos in [pos_1[0], pos_1[1], pos_2a[0], pos_2a[1], pos_2b]:
                            subject_in_period[pos[0]][pos[1]].append(timetable[pos][0][0][0])
                            teacher_in_period[pos[2]].append(timetable[pos][0][0][1])
                      
            elif timetable[pos_1[0]][2] == 2 and timetable[pos_1[1]][2] == 2 and timetable[pos_1[0]] != timetable[pos_1[1]]:
                event_2a, pos_1a, event_2b, pos_1b = find_block(timetable, pos_1[0], timetable[pos_1[0]])
                event_2c, pos_1c, event_2d, pos_1d = find_block(timetable, pos_1[1], timetable[pos_1[1]])
                
                event_21 = [[event_2a[0][0], event_2b[0][0]], pos_1a[0], 2]
                event_22 = [[event_2c[0][0], event_2d[0][0]], pos_1c[0], 2]
                
                position_21 = rank_position.order_position(event_21, prepare_data.get_empty_position(event_21, timetable, data), teacher_in_period, subject_in_period, timetable)
                position_22 = rank_position.order_position(event_22, prepare_data.get_empty_position(event_22, timetable, data), teacher_in_period, subject_in_period, timetable)
                
                if len(position_21) != 0 and len(position_22) != 0:
                    pos_21 = position_21[0]
                    pos_22 = position_22[0]
                    
                    count = 0
                    for pos in pos_21:
                        if pos not in pos_22:
                            count += 1
                    
                    if count == len(pos_21):
                        for pos in [pos_1a, pos_1b, pos_1c, pos_1d]:
                            subject_in_period[pos[0]][pos[1]].remove(timetable[pos][0][0][0])
                            teacher_in_period[pos[2]].remove(timetable[pos][0][0][1])
                        
                        timetable[pos_21[0]] = timetable[pos_1a]
                        timetable[pos_21[1]] = timetable[pos_1b]
                        
                        timetable[pos_22[0]] = timetable[pos_1c]
                        timetable[pos_22[1]] = timetable[pos_1d]
                        
                        for pos in [pos_1a, pos_1b, pos_1c, pos_1d]:
                            timetable[pos] = None
                            
                        timetable[pos_1[0]] = [[event[0][0]], event[1], 2]
                        timetable[pos_1[1]] = [[event[0][0]], event[1], 2]
                        
                        for pos in [pos_1[0], pos_1[1], pos_21[0], pos_21[1], pos_22[0], pos_22[1]]:
                            subject_in_period[pos[0]][pos[1]].append(timetable[pos][0][0][0])
                            teacher_in_period[pos[2]].append(timetable[pos][0][0][1])
                        
    return timetable, subject_in_period, teacher_in_period

def mutation_soft(timetable, subject_in_period, teacher_in_period, position, event, not_violated_SC, violated_SC, data):
    #for position, event in GVCN_event:
        if len(event[0]) == 1:
            if position[1] == 'Thu_hai':
                if timetable[(position[0], position[1], data['Events']['timetable'][position[0]][position[1]][1])][2] == 1:
                    if (HC.HC_check(event, (position[0], position[1], data['Events']['timetable'][position[0]][position[1]][1]), subject_in_period, teacher_in_period) and HC.HC_check(timetable[(position[0], position[1], data['Events']['timetable'][position[0]][position[1]][1])], position, subject_in_period, teacher_in_period)) or (HC.subject_unoverload(event, (position[0], position[1], data['Events']['timetable'][position[0]][position[1]][1]), subject_in_period) and HC.subject_unoverload(timetable[(position[0], position[1], data['Events']['timetable'][position[0]][position[1]][1])], position, subject_in_period)):
                        for pos in [position, (position[0], position[1], data['Events']['timetable'][position[0]][position[1]][1])]:
                            subject_in_period[pos[0]][pos[1]].remove(timetable[pos][0][0][0])
                            teacher_in_period[pos[2]].remove(timetable[pos][0][0][1])
                        
                        timetable[position], timetable[(position[0], position[1], data['Events']['timetable'][position[0]][position[1]][1])] = timetable[(position[0], position[1], data['Events']['timetable'][position[0]][position[1]][1])], timetable[position]
                        
                        for pos in [position, (position[0], position[1], data['Events']['timetable'][position[0]][position[1]][1])]:
                            subject_in_period[pos[0]][pos[1]].append(timetable[pos][0][0][0])
                            teacher_in_period[pos[2]].append(timetable[pos][0][0][1])
                        
                        not_violated_SC.append((position[0], position[1], data['Events']['timetable'][position[0]][position[1]][1]))
                        
                else:
                    if position[2] in [4, 32]:
                        if (HC.HC_check(event, (position[0], position[1], data['Events']['timetable'][position[0]][position[1]][1]), subject_in_period, teacher_in_period) and HC.HC_check(timetable[(position[0], position[1], data['Events']['timetable'][position[0]][position[1]][1])], position, subject_in_period, teacher_in_period)) or (HC.subject_unoverload(event, (position[0], position[1], data['Events']['timetable'][position[0]][position[1]][1]), subject_in_period) and HC.subject_unoverload(timetable[(position[0], position[1], data['Events']['timetable'][position[0]][position[1]][1])], position, subject_in_period)):
                            for pos in [position, (position[0], position[1], data['Events']['timetable'][position[0]][position[1]][1])]:
                                subject_in_period[pos[0]][pos[1]].remove(timetable[pos][0][0][0])
                                teacher_in_period[pos[2]].remove(timetable[pos][0][0][1])
                            
                            timetable[position], timetable[(position[0], position[1], data['Events']['timetable'][position[0]][position[1]][1])] = timetable[(position[0], position[1], data['Events']['timetable'][position[0]][position[1]][1])], timetable[position]
                            
                            for pos in [position, (position[0], position[1], data['Events']['timetable'][position[0]][position[1]][1])]:
                                subject_in_period[pos[0]][pos[1]].append(timetable[pos][0][0][0])
                                teacher_in_period[pos[2]].append(timetable[pos][0][0][1])
                            
                            not_violated_SC.append((position[0], position[1], data['Events']['timetable'][position[0]][position[1]][1]))
                            
                    elif position[2] in [5, 33]:
                        if (HC.HC_check(timetable[(position[0], position[1], position[2] - 1)], (position[0], position[1], data['Events']['timetable'][position[0]][position[1]][1]), subject_in_period, teacher_in_period) and HC.HC_check(timetable[(position[0], position[1], data['Events']['timetable'][position[0]][position[1]][1])], (position[0], position[1], position[2] - 1), subject_in_period, teacher_in_period)) or (HC.subject_unoverload(timetable[(position[0], position[1], position[2] - 1)], (position[0], position[1], data['Events']['timetable'][position[0]][position[1]][1]), subject_in_period) and HC.subject_unoverload(timetable[(position[0], position[1], data['Events']['timetable'][position[0]][position[1]][1])], (position[0], position[1], position[2] - 1), subject_in_period)):
                            for pos in [(position[0], position[1], position[2] - 1), (position[0], position[1], data['Events']['timetable'][position[0]][position[1]][1])]:
                                subject_in_period[pos[0]][pos[1]].remove(timetable[pos][0][0][0])
                                teacher_in_period[pos[2]].remove(timetable[pos][0][0][1])
                            
                            timetable[(position[0], position[1], position[2] - 1)], timetable[(position[0], position[1], data['Events']['timetable'][position[0]][position[1]][1])] = timetable[(position[0], position[1], data['Events']['timetable'][position[0]][position[1]][1])], timetable[(position[0], position[1], position[2] - 1)]
                            
                            for pos in [(position[0], position[1], position[2] - 1), (position[0], position[1], data['Events']['timetable'][position[0]][position[1]][1])]:
                                subject_in_period[pos[0]][pos[1]].append(timetable[pos][0][0][0])
                                teacher_in_period[pos[2]].append(timetable[pos][0][0][1])
                                
                            if (HC.HC_check(event, (position[0], position[1], data['Events']['timetable'][position[0]][position[1]][1]), subject_in_period, teacher_in_period) and HC.HC_check(timetable[(position[0], position[1], data['Events']['timetable'][position[0]][position[1]][1])], position, subject_in_period, teacher_in_period)) or (HC.subject_unoverload(event, (position[0], position[1], data['Events']['timetable'][position[0]][position[1]][1]), subject_in_period) and HC.subject_unoverload(timetable[(position[0], position[1], data['Events']['timetable'][position[0]][position[1]][1])], position, subject_in_period)):
                                for pos in [position, (position[0], position[1], data['Events']['timetable'][position[0]][position[1]][1])]:
                                    subject_in_period[pos[0]][pos[1]].remove(timetable[pos][0][0][0])
                                    teacher_in_period[pos[2]].remove(timetable[pos][0][0][1])
                                
                                timetable[position], timetable[(position[0], position[1], data['Events']['timetable'][position[0]][position[1]][1])] = timetable[(position[0], position[1], data['Events']['timetable'][position[0]][position[1]][1])], timetable[position]
                                
                                for pos in [position, (position[0], position[1], data['Events']['timetable'][position[0]][position[1]][1])]:
                                    subject_in_period[pos[0]][pos[1]].append(timetable[pos][0][0][0])
                                    teacher_in_period[pos[2]].append(timetable[pos][0][0][1])
                                
                                not_violated_SC.append((position[0], position[1], data['Events']['timetable'][position[0]][position[1]][1]))
                                
            elif position[1] == 'Thu_bay':
                pos = (position[0], position[1], position[2] + 1)
                if (HC.HC_check(event, pos, subject_in_period, teacher_in_period) and HC.HC_check(timetable[pos], position, subject_in_period, teacher_in_period)): #or (HC.subject_unoverload(event, pos, subject_in_period) and HC.subject_unoverload(timetable[pos], position, subject_in_period)):
                    for p in [position, pos]:
                        subject_in_period[p[0]][p[1]].remove(timetable[p][0][0][0])
                        teacher_in_period[p[2]].remove(timetable[p][0][0][1])
                    
                    timetable[pos], timetable[position] = timetable[position], timetable[pos]
                    
                    for p in [position, pos]:
                        subject_in_period[p[0]][p[1]].append(timetable[p][0][0][0])
                        teacher_in_period[p[2]].append(timetable[p][0][0][1])
                    
                    not_violated_SC.append(pos)
                    
            elif position[1] not in ['Thu_hai', 'Thu_bay']:
                list_of_pos = rank_position.order_position_GVCN(event, prepare_data.get_position_soft(event, timetable, data, not_violated_SC), timetable, subject_in_period, teacher_in_period)
                
                if len(list_of_pos) != 0:
                    new_pos = list_of_pos[0]
                    
                    if timetable[new_pos][2] == 1:
                        if HC.HC_check(timetable[new_pos], position, subject_in_period, teacher_in_period) or HC.subject_unoverload(timetable[new_pos], position, subject_in_period):
                            for pos in [position, new_pos]:
                                subject_in_period[pos[0]][pos[1]].remove(timetable[pos][0][0][0])
                                teacher_in_period[pos[2]].remove(timetable[pos][0][0][1])
                            
                            timetable[position], timetable[new_pos] = timetable[new_pos], timetable[position]
                            
                            for pos in [position, new_pos]:
                                subject_in_period[pos[0]][pos[1]].append(timetable[pos][0][0][0])
                                teacher_in_period[pos[2]].append(timetable[pos][0][0][1])
                            
                            not_violated_SC.append(new_pos)
                            
                    elif new_pos[1] == 'Thu_hai' and timetable[new_pos][2] == 2 and timetable[(new_pos[0], new_pos[1], new_pos[2] + 2)][2] == 1:
                        pos_3 = (new_pos[0], new_pos[1], new_pos[2] + 2)
                        
                        if (HC.HC_check(timetable[new_pos], pos_3, subject_in_period, teacher_in_period) and HC.HC_check(timetable[pos_3], new_pos, subject_in_period, teacher_in_period)) or (HC.subject_unoverload(timetable[new_pos], pos_3, subject_in_period) and HC.subject_unoverload(timetable[pos_3], new_pos, subject_in_period)):
                            for pos in [new_pos, pos_3]:
                                subject_in_period[pos[0]][pos[1]].remove(timetable[pos][0][0][0])
                                teacher_in_period[pos[2]].remove(timetable[pos][0][0][1])
                            
                            timetable[new_pos], timetable[pos_3] = timetable[pos_3], timetable[new_pos]
                            
                            for pos in [new_pos, pos_3]:
                                subject_in_period[pos[0]][pos[1]].append(timetable[pos][0][0][0])
                                teacher_in_period[pos[2]].append(timetable[pos][0][0][1])
                            
                            if HC.HC_check(timetable[new_pos], position, subject_in_period, teacher_in_period) or HC.subject_unoverload(timetable[new_pos], position, subject_in_period):
                                for pos in [position, new_pos]:
                                    subject_in_period[pos[0]][pos[1]].remove(timetable[pos][0][0][0])
                                    teacher_in_period[pos[2]].remove(timetable[pos][0][0][1])
                                
                                timetable[position], timetable[new_pos] = timetable[new_pos], timetable[position]
                                
                                for pos in [position, new_pos]:
                                    subject_in_period[pos[0]][pos[1]].append(timetable[pos][0][0][0])
                                    teacher_in_period[pos[2]].append(timetable[pos][0][0][1])
                                
                                not_violated_SC.append(new_pos)
                                
        else:
            if position[0][1] == 'Thu_hai':
                if timetable[(position[0][0], position[0][1], data['Events']['timetable'][position[0][0]][position[0][1]][1])][2] == 1 and position[0][2] in [3, 31]:
                    if (HC.HC_check(timetable[position[1]], (position[0][0], position[0][1], data['Events']['timetable'][position[0][0]][position[0][1]][1]), subject_in_period, teacher_in_period) and HC.HC_check(timetable[(position[0][0], position[0][1], data['Events']['timetable'][position[0][0]][position[0][1]][1])], position[1], subject_in_period, teacher_in_period)) or (HC.subject_unoverload(timetable[position[1]], (position[0][0], position[0][1], data['Events']['timetable'][position[0][0]][position[0][1]][1]), subject_in_period) and HC.subject_unoverload(timetable[(position[0][0], position[0][1], data['Events']['timetable'][position[0][0]][position[0][1]][1])], position[1], subject_in_period)):
                        for pos in [(position[0][0], position[0][1], data['Events']['timetable'][position[0][0]][position[0][1]][1]), position[1]]:
                            subject_in_period[pos[0]][pos[1]].remove(timetable[pos][0][0][0])
                            teacher_in_period[pos[2]].remove(timetable[pos][0][0][1])
                        
                        timetable[position[1]], timetable[(position[0][0], position[0][1], data['Events']['timetable'][position[0][0]][position[0][1]][1])] = timetable[(position[0][0], position[0][1], data['Events']['timetable'][position[0][0]][position[0][1]][1])], timetable[position[1]]
                        
                        for pos in [(position[0][0], position[0][1], data['Events']['timetable'][position[0][0]][position[0][1]][1]), position[1]]:
                            subject_in_period[pos[0]][pos[1]].append(timetable[pos][0][0][0])
                            teacher_in_period[pos[2]].append(timetable[pos][0][0][1])
                        
                        not_violated_SC.append((position[0][0], position[0][1], data['Events']['timetable'][position[0][0]][position[0][1]][1]))
                        not_violated_SC.append((position[0][0], position[0][1], data['Events']['timetable'][position[0][0]][position[0][1]][2]))
                       
                elif timetable[(position[0][0], position[0][1], data['Events']['timetable'][position[0][0]][position[0][1]][1])][2] == 1 and position[0][2] in [4, 32]:
                    pos_1 = (position[0][0], position[0][1], data['Events']['timetable'][position[0][0]][position[0][1]][1])
                    pos_2 = (position[0][0], position[0][1], data['Events']['timetable'][position[0][0]][position[0][1]][2])
                    
                    if (HC.HC_check(timetable[pos_2], position[1], subject_in_period, teacher_in_period) and HC.HC_check(timetable[position[1]], pos_2, subject_in_period, teacher_in_period)) or (HC.subject_unoverload(timetable[pos_2], position[1], subject_in_period) and HC.subject_unoverload(timetable[position[1]], pos_2, subject_in_period)):
                        for pos in [pos_2, position[1]]:
                            subject_in_period[pos[0]][pos[1]].remove(timetable[pos][0][0][0])
                            teacher_in_period[pos[2]].remove(timetable[pos][0][0][1])
                        
                        timetable[pos_2], timetable[position[1]] = timetable[position[1]], timetable[pos_2]
                        
                        for pos in [pos_2, position[1]]:
                            subject_in_period[pos[0]][pos[1]].append(timetable[pos][0][0][0])
                            teacher_in_period[pos[2]].append(timetable[pos][0][0][1])
                        
                        if (HC.HC_check(timetable[pos_1], position[0], subject_in_period, teacher_in_period) and HC.HC_check(timetable[position[0]], pos_1, subject_in_period, teacher_in_period)) or (HC.subject_unoverload(timetable[pos_1], position[0], subject_in_period) and HC.subject_unoverload(timetable[position[0]], pos_1, subject_in_period)):
                            for pos in [pos_1, position[0]]:
                                subject_in_period[pos[0]][pos[1]].remove(timetable[pos][0][0][0])
                                teacher_in_period[pos[2]].remove(timetable[pos][0][0][1])
                            
                            timetable[pos_1], timetable[position[0]] = timetable[position[0]], timetable[pos_1]
                            
                            for pos in [pos_1, position[0]]:
                                subject_in_period[pos[0]][pos[1]].append(timetable[pos][0][0][0])
                                teacher_in_period[pos[2]].append(timetable[pos][0][0][1])
                            
                            not_violated_SC.append(position[0])
                            not_violated_SC.append(position[1])
                    
                elif timetable[(position[0][0], position[0][1], data['Events']['timetable'][position[0][0]][position[0][1]][1])][2] == 2:
                    pos_1 = (position[0][0], position[0][1], data['Events']['timetable'][position[0][0]][position[0][1]][1])
                    pos_2 = (position[0][0], position[0][1], data['Events']['timetable'][position[0][0]][position[0][1]][2])
                    pos = [pos_1, pos_2]
                    new_event = [[timetable[pos_1][0][0], timetable[pos_2][0][0]], pos_1[0], 2]
                    
                    if (HC.HC_check(new_event, position, subject_in_period, teacher_in_period) and HC.HC_check(event, pos, subject_in_period, teacher_in_period)) or (HC.subject_unoverload(new_event, position, subject_in_period) and HC.subject_unoverload(event, pos, subject_in_period)):
                        for pos in [pos_1, pos_2, position[0], position[1]]:
                            subject_in_period[pos[0]][pos[1]].remove(timetable[pos][0][0][0])
                            teacher_in_period[pos[2]].remove(timetable[pos][0][0][1])
                        
                        timetable[position[0]], timetable[pos_1] = timetable[pos_1], timetable[position[0]]
                        timetable[position[1]], timetable[pos_2] = timetable[pos_2], timetable[position[1]]
                        
                        for pos in [pos_1, pos_2, position[0], position[1]]:
                            subject_in_period[pos[0]][pos[1]].append(timetable[pos][0][0][0])
                            teacher_in_period[pos[2]].append(timetable[pos][0][0][1])
                        
                        not_violated_SC.append((position[0][0], position[0][1], data['Events']['timetable'][position[0][0]][position[0][1]][1]))
                        not_violated_SC.append((position[0][0], position[0][1], data['Events']['timetable'][position[0][0]][position[0][1]][2]))
                        
            elif position[0][1] not in ['Thu_hai', 'Thu_bay']:
                list_of_pos = rank_position.order_position_GVCN(event, prepare_data.get_position_soft(event, timetable, data, not_violated_SC), timetable, subject_in_period, teacher_in_period)
                
                if len(list_of_pos) != 0:
                    new_pos = list_of_pos[0]
                    
                    if timetable[new_pos[0]] == timetable[new_pos[1]]:
                        new_event = [[timetable[new_pos[0]][0][0], timetable[new_pos[1]][0][0]], new_pos[0][0], 2]
                        
                        if HC.HC_check(new_event, position, subject_in_period, teacher_in_period) or HC.subject_unoverload(new_event, position, subject_in_period):
                            for pos in [new_pos[0], new_pos[1], position[0], position[1]]:
                                subject_in_period[pos[0]][pos[1]].remove(timetable[pos][0][0][0])
                                teacher_in_period[pos[2]].remove(timetable[pos][0][0][1])
                            
                            timetable[new_pos[0]], timetable[position[0]] = timetable[position[0]], timetable[new_pos[0]]
                            timetable[new_pos[1]], timetable[position[1]] = timetable[position[1]], timetable[new_pos[1]]
                            
                            for pos in [new_pos[0], new_pos[1], position[0], position[1]]:
                                subject_in_period[pos[0]][pos[1]].append(timetable[pos][0][0][0])
                                teacher_in_period[pos[2]].append(timetable[pos][0][0][1])
                            
                            for pos in new_pos:
                                not_violated_SC.append(pos)
                        
                    elif timetable[new_pos[0]][2] == 1 and timetable[new_pos[1]][2] == 1:
                        if (HC.HC_check(timetable[new_pos[0]], position[0], subject_in_period, teacher_in_period) and HC.HC_check(timetable[new_pos[1]], position[1], subject_in_period, teacher_in_period)) or (HC.subject_unoverload(timetable[new_pos[0]], position[0], subject_in_period) and HC.subject_unoverload(timetable[new_pos[1]], position[1], subject_in_period)):
                            for pos in [new_pos[0], new_pos[1], position[0], position[1]]:
                                subject_in_period[pos[0]][pos[1]].remove(timetable[pos][0][0][0])
                                teacher_in_period[pos[2]].remove(timetable[pos][0][0][1])
                            
                            timetable[new_pos[0]], timetable[position[0]] = timetable[position[0]], timetable[new_pos[0]]
                            timetable[new_pos[1]], timetable[position[1]] = timetable[position[1]], timetable[new_pos[1]]
                            
                            for pos in [new_pos[0], new_pos[1], position[0], position[1]]:
                                subject_in_period[pos[0]][pos[1]].append(timetable[pos][0][0][0])
                                teacher_in_period[pos[2]].append(timetable[pos][0][0][1])
                            
                            for pos in new_pos:
                                not_violated_SC.append(pos)
                        
                        elif (HC.HC_check(timetable[new_pos[0]], position[1], subject_in_period, teacher_in_period) and HC.HC_check(timetable[new_pos[1]], position[0], subject_in_period, teacher_in_period)) or (HC.subject_unoverload(timetable[new_pos[0]], position[1], subject_in_period) and HC.subject_unoverload(timetable[new_pos[1]], position[0], subject_in_period)):
                            for pos in [new_pos[0], new_pos[1], position[0], position[1]]:
                                subject_in_period[pos[0]][pos[1]].remove(timetable[pos][0][0][0])
                                teacher_in_period[pos[2]].remove(timetable[pos][0][0][1])
                            
                            timetable[new_pos[0]], timetable[position[1]] = timetable[position[1]], timetable[new_pos[0]]
                            timetable[new_pos[1]], timetable[position[0]] = timetable[position[0]], timetable[new_pos[1]]
                            
                            for pos in [new_pos[0], new_pos[1], position[0], position[1]]:
                                subject_in_period[pos[0]][pos[1]].append(timetable[pos][0][0][0])
                                teacher_in_period[pos[2]].append(timetable[pos][0][0][1])
                            
                            for pos in new_pos:
                                not_violated_SC.append(pos)
                    
                    elif new_pos[0][1] == 'Thu_hai' and timetable[new_pos[0]][2] == 1 and timetable[new_pos[1]][2] == 2:
                        if (HC.HC_check(timetable[new_pos[0]], (new_pos[0][0], new_pos[0][1], new_pos[0][2] + 2), subject_in_period, teacher_in_period) and HC.HC_check(timetable[(new_pos[0][0], new_pos[0][1], new_pos[0][2] + 2)], new_pos[0], subject_in_period, teacher_in_period)) or (HC.subject_unoverload(timetable[new_pos[0]], (new_pos[0][0], new_pos[0][1], new_pos[0][2] + 2), subject_in_period) and HC.subject_unoverload(timetable[(new_pos[0][0], new_pos[0][1], new_pos[0][2] + 2)], new_pos[0], subject_in_period)):
                            for pos in [new_pos[0], (new_pos[0][0], new_pos[0][1], new_pos[0][2] + 2)]:
                                subject_in_period[pos[0]][pos[1]].remove(timetable[pos][0][0][0])
                                teacher_in_period[pos[2]].remove(timetable[pos][0][0][1])
                            
                            timetable[new_pos[0]], timetable[(new_pos[0][0], new_pos[0][1], new_pos[0][2] + 2)] = timetable[(new_pos[0][0], new_pos[0][1], new_pos[0][2] + 2)], timetable[new_pos[0]]
                            
                            for pos in [new_pos[0], (new_pos[0][0], new_pos[0][1], new_pos[0][2] + 2)]:
                                subject_in_period[pos[0]][pos[1]].append(timetable[pos][0][0][0])
                                teacher_in_period[pos[2]].append(timetable[pos][0][0][1])
                            
                            new_event = [[timetable[new_pos[0]][0][0], timetable[new_pos[1]][0][0]], new_pos[0][0], 2]
                            
                            if HC.HC_check(new_event, position, subject_in_period, teacher_in_period) or HC.subject_unoverload(new_event, position, subject_in_period):
                                for pos in [new_pos[0], new_pos[1], position[0], position[1]]:
                                    subject_in_period[pos[0]][pos[1]].remove(timetable[pos][0][0][0])
                                    teacher_in_period[pos[2]].remove(timetable[pos][0][0][1])
                                
                                timetable[new_pos[0]], timetable[position[0]] = timetable[position[0]], timetable[new_pos[0]]
                                timetable[new_pos[1]], timetable[position[1]] = timetable[position[1]], timetable[new_pos[1]]
                                
                                for pos in [new_pos[0], new_pos[1], position[0], position[1]]:
                                    subject_in_period[pos[0]][pos[1]].remove(timetable[pos][0][0][0])
                                    teacher_in_period[pos[2]].remove(timetable[pos][0][0][1])
                                
                                for pos in new_pos:
                                    not_violated_SC.append(pos)
                            
        return timetable, subject_in_period, teacher_in_period

def union_period(violated_HC4):
    over_position = []
    
    new_violated_HC4 = {}
    for teacher in violated_HC4:
        if len(violated_HC4[teacher]) > 0:
            sorted(violated_HC4)
            new_violated_HC4.update({teacher: []})
        
            for item in violated_HC4[teacher]:
                if item not in over_position:
                    same_period = np.where(np.array(violated_HC4[teacher], dtype=object) == item[2])[0]
                    new_violated_HC4[teacher].append([violated_HC4[teacher][i] for i in same_period])
                    over_position += [violated_HC4[teacher][i] for i in same_period]
                      
    over_position.clear()  
    
    return new_violated_HC4

def change_position(pos, data, timetable, subject_in_period, teacher_in_period, not_violated_SC):
    status = False
    
    if timetable[pos][2] == 1:
        list_new_pos = rank_position.order_position_repair(timetable[pos], prepare_data.get_position_repair(data, timetable, pos), teacher_in_period, subject_in_period, timetable)
        if len(list_new_pos) != 0:
            new_pos = list_new_pos[0]
            
            if HC.HC_check(timetable[new_pos], pos, subject_in_period, teacher_in_period):
                for position in [pos, new_pos]:
                    subject_in_period[position[0]][position[1]].remove(timetable[position][0][0][0])
                    teacher_in_period[position[2]].remove(timetable[position][0][0][1])
                
                timetable[pos], timetable[new_pos] = timetable[new_pos], timetable[pos]
                
                for position in [pos, new_pos]:
                    subject_in_period[position[0]][position[1]].append(timetable[position][0][0][0])
                    teacher_in_period[position[2]].append(timetable[position][0][0][1])
                
                status = True
                
    else:
        event_a, pos_a, event_b, pos_b = find_block(timetable, pos, timetable[pos])
        event = [[event_a[0][0], event_b[0][0]], pos_a[0], 2]
        full_pos = [pos_a, pos_b]
        
        list_new_pos = rank_position.order_position_repair(event, prepare_data.get_position_repair(data, timetable, pos), teacher_in_period, subject_in_period, timetable)
        if len(list_new_pos) != 0:
            new_pos = list_new_pos[0]
            
            if timetable[new_pos[0]] == timetable[new_pos[1]]:
                event_1 = [[timetable[new_pos[0]][0][0], timetable[new_pos[0]][0][0]], new_pos[0][0], 2]
                if HC.HC_check(event_1, full_pos, subject_in_period, teacher_in_period):
                    for position in [pos_a, pos_b, new_pos[0], new_pos[1]]:
                        subject_in_period[position[0]][position[1]].remove(timetable[position][0][0][0])
                        teacher_in_period[position[2]].remove(timetable[position][0][0][1])
                    
                    timetable[pos_a], timetable[new_pos[0]] = timetable[new_pos[0]], timetable[pos_a]
                    timetable[pos_b], timetable[new_pos[1]] = timetable[new_pos[1]], timetable[pos_b]
                    
                    for position in [pos_a, pos_b, new_pos[0], new_pos[1]]:
                        subject_in_period[position[0]][position[1]].append(timetable[position][0][0][0])
                        teacher_in_period[position[2]].append(timetable[position][0][0][1])
                    
                    status = True
                    
            else:
                if HC.HC_check(timetable[new_pos[0]], pos_a, subject_in_period, teacher_in_period) and HC.HC_check(timetable[new_pos[1]], pos_b, subject_in_period, teacher_in_period):
                    for position in [pos_a, pos_b, new_pos[0], new_pos[1]]:
                        subject_in_period[position[0]][position[1]].remove(timetable[position][0][0][0])
                        teacher_in_period[position[2]].remove(timetable[position][0][0][1])
                    
                    timetable[pos_a], timetable[new_pos[0]] = timetable[new_pos[0]], timetable[pos_a]
                    timetable[pos_b], timetable[new_pos[1]] = timetable[new_pos[1]], timetable[pos_b]
                    
                    for position in [pos_a, pos_b, new_pos[0], new_pos[1]]:
                        subject_in_period[position[0]][position[1]].append(timetable[position][0][0][0])
                        teacher_in_period[position[2]].append(timetable[position][0][0][1])
                    
                    status = True
                    
                elif (HC.HC_check(timetable[new_pos[0]], pos_b, subject_in_period, teacher_in_period) and HC.HC_check(timetable[new_pos[1]], pos_a, subject_in_period, teacher_in_period)):
                    for position in [pos_a, pos_b, new_pos[0], new_pos[1]]:
                        subject_in_period[position[0]][position[1]].remove(timetable[position][0][0][0])
                        teacher_in_period[position[2]].remove(timetable[position][0][0][1])
                    
                    timetable[pos_a], timetable[new_pos[1]] = timetable[new_pos[1]], timetable[pos_a]
                    timetable[pos_b], timetable[new_pos[0]] = timetable[new_pos[0]], timetable[pos_b]
                    
                    for position in [pos_a, pos_b, new_pos[0], new_pos[1]]:
                        subject_in_period[position[0]][position[1]].append(timetable[position][0][0][0])
                        teacher_in_period[position[2]].append(timetable[position][0][0][1])
                    
                    status = True
                                    
    return timetable, subject_in_period, teacher_in_period, status

def change_teacher(pos, data, timetable, subject_in_period, teacher_in_period, not_violated_SC):
    status = False
    
    teacher_1 = random.choice(data['Teachers']['Majors'][timetable[pos][0][0][0]])

    if teacher_1 != timetable[pos][0][0][1]:
        all_pos = find_all_event(pos, timetable, data, not_violated_SC)
        
        count = 0
        for position in all_pos:
            if teacher_1 not in teacher_in_period[position[2]]:
                count += 1
            
        if count == len(all_pos):
            for position in all_pos:
                teacher_in_period[position[2]].remove(timetable[position][0][0][1])
            
            for position in all_pos:
                timetable[position][0][0][1] = teacher_1
            
            for position in all_pos:
                teacher_in_period[position[2]].append(teacher_1)
            
            status = True
    
        count = 0
    
    return timetable, subject_in_period, teacher_in_period, status

function = random.choices([change_teacher, change_position], weights = [50, 50], k = 1)[0]

def repair_HC4(data, timetable, subject_in_period, teacher_in_period, violated_HC4, not_violated_SC):
    for teacher in violated_HC4:
        if len(violated_HC4[teacher]) > 0:
            for item in violated_HC4[teacher]:
                if len(item) > 0:
                    if len(item) >= 2:
                        idx = np.where(np.array(item, dtype=object) == 'GVCN')[0]
                        if len(idx) == 0:
                            list_of_pos = random.sample(item, len(item) - 1)
                        
                        else:
                            list_of_pos = [i for i in item if 'GVCN' not in i]
                            
                    elif len(item) == 1:
                        list_of_pos = item
                    
                    for pos in list_of_pos:
                        repair = change_teacher(pos, data, timetable, subject_in_period, teacher_in_period, not_violated_SC)
                        timetable, subject_in_period, teacher_in_period = repair[0], repair[1], repair[2]
                        
                        if repair[3] == False:
                            repair = change_position(pos, data, timetable, subject_in_period, teacher_in_period, not_violated_SC)
                            timetable, subject_in_period, teacher_in_period = repair[0], repair[1], repair[2]
                            
                            if repair[3] == True:
                                item.clear()
                        
                        else:
                            item.clear()
    
    for teacher in violated_HC4:
        count = 0
        for item in violated_HC4[teacher]:
            if len(item) == 0:
                count += 1
        
        if count == len(violated_HC4):
            violated_HC4[teacher].clear()
        
        count = 0
                    
    return timetable, subject_in_period, teacher_in_period, violated_HC4
      
def selection_soft(population):
    parent_1 = population[0]
    
    total_penalty_SC = sum([chromosome[0][3] for chromosome in population[1:]])
    
    prob_list = [chromosome[0][3]/total_penalty_SC for chromosome in population[1:]]
    
    #population[1:].sort(key=lambda chromosome: total_penalty_SC - chromosome[0][3], reverse=False)
    sorted(prob_list, reverse=False)
    
    n = random.uniform(0, 1)
    if n < prob_list[0] or n > prob_list[-1]:
        parent_2 = random.choice(population[1:])
    
    else:
        choose_value = bisect.bisect_left(prob_list, n)
        parent_2 = population[1:][choose_value]
    
    return parent_1, parent_2
    
def crossover_soft(parent_1, parent_2, data):
    class_violated_SC_1 = [position[0] for position in parent_1[0][5]]
    
    GVCN_event_1 = rank_event.order_event_GVCN(find_event_GVCN(parent_1[2], data, parent_1[0][5], parent_1[0][4]))
    event_in_Mon_Sat_1 = [position[0] for position, event in GVCN_event_1 if position[1] in ['Thu_hai', 'Thu_bay']]
    
    GVCN_event_2 = rank_event.order_event_GVCN(find_event_GVCN(parent_2[2], data, parent_2[0][5], parent_2[0][4]))
    event_in_Mon_Sat_2 = [position[0] for position, event in GVCN_event_2 if position[1] in ['Thu_hai', 'Thu_bay']]
    
    for highschool_class in class_violated_SC_1:
        if highschool_class not in event_in_Mon_Sat_1 and highschool_class in event_in_Mon_Sat_2:
            for day in data['Events']['timetable'][highschool_class]:
                for period in data['Events']['timetable'][highschool_class][day]:
                    position = (highschool_class, day, period)
                    
                    for chromosome in [parent_1, parent_2]:
                        chromosome[3][position[0]][position[1]].remove(chromosome[2][position][0][0][0])
                        chromosome[4][position[2]].remove(chromosome[2][position][0][0][1])
                        
                    parent_1[2][position], parent_2[2][position] = parent_2[2][position], parent_1[2][position]
                    
                    for chromosome in [parent_1, parent_2]:
                        chromosome[3][position[0]][position[1]].append(chromosome[2][position][0][0][0])
                        chromosome[4][position[2]].append(chromosome[2][position][0][0][1])
    
    for chromosome in [parent_1, parent_2]:
        chromosome[0] = penalty.total_check_soft(data, chromosome[2], chromosome[3], chromosome[4])
            
    return parent_1, parent_2