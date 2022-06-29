import hard_constrains as HC
import soft_constraints as SC
import random

def order_position(event, function, teacher_in_period, subject_in_period, timetable):
    penalty = 0
    
    empty_position = function
    
    best_position = []
    feasible_position = []
    
    for position in empty_position:
        if HC.HC_check(event, position, subject_in_period, teacher_in_period) and SC.first_last_position(event, position):
            best_position.append(position)
        
        elif HC.HC_check(event, position, subject_in_period, teacher_in_period):
            if not SC.first_last_position(event, position):
                penalty += 1
            
                feasible_position.append([position, penalty])
        
        penalty = 0
        
    random.shuffle(best_position)
    
    feasible_position.sort(key=lambda feasible_position: feasible_position[1])
    feasible_position = [position[0] for position in feasible_position]
    
    all_position = best_position + feasible_position

    return all_position

def order_position_GVCN(event, function, timetable, subject_in_period, teacher_in_period):
    GVCN_position = function
    
    best_position = []
    feasible_position = []
    
    penalty = 0
    for position in GVCN_position:
        if SC.check_block_len(event, position, timetable) and HC.HC_check(event, position, subject_in_period, teacher_in_period):
            best_position.append(position)
        
        elif not SC.check_block_len(event, position, timetable):
            if HC.HC_check(event, position, subject_in_period, teacher_in_period):
                penalty += 2
            
                feasible_position.append([position, penalty])
        
        penalty = 0
        
    random.shuffle(best_position)
    
    feasible_position.sort(key=lambda feasible: feasible[1])
    feasible_position = [position for (position, penalty) in feasible_position]
    
    all_position = best_position + feasible_position
    
    return all_position

def order_position_repair(event, function, teacher_in_period, subject_in_period, timetable):
    repair_position = function
    
    best_position = []
    for position in repair_position:
        if HC.HC_check(event, position, subject_in_period, teacher_in_period) and SC.first_last_position(event, position):
            best_position.append(position)
        
    random.shuffle(best_position)
    
    return best_position