import prepare_data
import rank_event
import rank_position
import penalty
import neighbor

import time
import copy

#position = (highschool_class, day, period) 
#event = [[[subject, teacher]], highschool_class]
#event = [[[subject, teacher], [subject, teacher]], highschool_class]

data = prepare_data.read_json('THPT_CG_input.json')

def construct_initial_timetable(class_assigned_teacher):
    t = time.process_time()

    timetable = prepare_data.generate_timetable(data)
    subject_in_period = prepare_data.generate_subject_in_period(data)
    teacher_in_period = prepare_data.generate_teacher_in_period()
    
    #event had no empty positions
    unplaced_event = []
    
    for highschool_class in data['Classes']['Class_ID']:
        GVCN = str(data['Classes']['GVCN_ID'][highschool_class])
        
        #assign "Chao_co" on Monday
        day = 'Thu_hai'
        period = data['Events']['timetable'][highschool_class][day][0]
        position = (highschool_class, day, period)
        event = [[['Chao_co', GVCN]], highschool_class]
        
        timetable[position] = event
        teacher_in_period[period].append(GVCN)
        subject_in_period[highschool_class][day].append('Chao_co')
        class_assigned_teacher.remove(event)
        
        #assign "Sinh hoat" on Saturday
        day = 'Thu_bay'
        period = data['Events']['timetable'][highschool_class][day][2]
        position = (highschool_class, day, period)
        event = [[['Sinh_hoat', GVCN]], highschool_class]
        
        timetable[position] = event
        teacher_in_period[period].append(GVCN)
        subject_in_period[highschool_class][day].append('Sinh_hoat')
        class_assigned_teacher.remove(event)
    
    #assign other events
    list_of_events = rank_event.order_event(class_assigned_teacher)
    
    for event in list_of_events:
        list_of_positions = rank_position.order_position(event, prepare_data.get_empty_position(event, timetable, data), teacher_in_period, subject_in_period, timetable)
        if len(list_of_positions) == 0:
            unplaced_event.append(event)
        else:
            position = list_of_positions[0]
        
            if len(event[0]) == 1:
                timetable[position] = [event[0], event[1], 1]
                subject_in_period[position[0]][position[1]].append(timetable[position][0][0][0])
                teacher_in_period[position[2]].append(timetable[position][0][0][1])
            
            else:
                for pos in position:
                    timetable[pos] = [[event[0][0]], event[1], 2]
                    subject_in_period[pos[0]][pos[1]].append(timetable[pos][0][0][0])
                    teacher_in_period[pos[2]].append(timetable[pos][0][0][1])
                 
        class_assigned_teacher.remove(event)
    
    total_1 = penalty.total_check_hard(data, timetable, subject_in_period, teacher_in_period)
    
    initial_time = time.process_time() - t
    #print(initial_time)
    
    return unplaced_event, total_1, initial_time, timetable, subject_in_period, teacher_in_period

def construct_feasible_timetable(unplaced_event, total_1, timetable, subject_in_period, teacher_in_period):
    t = time.process_time()
    
    iteration = 0
    while total_1[0] > 0 and iteration < 20:
        #generate a neighbor
        for event in unplaced_event:
            timetable_1, subject_in_period_1, teacher_in_period_1 = neighbor.mutation_hard(event, timetable, subject_in_period, teacher_in_period, data)
        
        total_2 = penalty.total_check_hard(data, timetable_1, subject_in_period_1, teacher_in_period_1)
        if total_2[0] < total_1[0]:
            timetable, subject_in_period, teacher_in_period = timetable_1, subject_in_period_1, teacher_in_period_1
        
        iteration += 1
        
    feasible_time = time.process_time() - t
    #print(feasible_time)
    
    return total_2, feasible_time, timetable, subject_in_period, teacher_in_period

def construct_optimize_timetable():
    population_size = 16
    generation = 100
    
    population = []
    while len(population) < population_size:
        class_assigned_teacher = prepare_data.assigned_to_teacher(data)[1]
        initial = construct_initial_timetable(class_assigned_teacher)
        feasible = construct_feasible_timetable(initial[0], initial[1], initial[3], initial[4], initial[5])
        
        if feasible[0][0] == 0:
            population.append([feasible[0], feasible[1], feasible[2], feasible[3], feasible[4], initial[1], initial[2], feasible[0]]) #initial[1] la diem khoi tao, initial[2] la thoi gian khoi tao
    
    population.sort(key=lambda population: population[0][3])
    best_timetable = copy.copy(population[0])
    initial_time = sum([chromosome[6] for chromosome in population])
    feasible_time = sum([chromosome[1] for chromosome in population])
    
    t = time.process_time()
    population_1 = copy.copy(population)
    for gen in range(generation):
        new_population = []
        
        while len(new_population) < population_size:
            parent_1, parent_2 = neighbor.selection_soft(population_1)
            child_1, child_2 = neighbor.crossover_soft(copy.copy(parent_1), copy.copy(parent_2), data)
            
            GVCN_event_1 = rank_event.order_event_GVCN(neighbor.find_event_GVCN(child_1[2], data, child_1[0][5], child_1[0][4]))
            for position, event in GVCN_event_1:
                mutate_child_1 = neighbor.mutation_soft(child_1[2], child_1[3], child_1[4], position, event, child_1[0][4], child_1[0][5], data)
            
            total_1 = penalty.total_check_soft(data, mutate_child_1[0], mutate_child_1[1], mutate_child_1[2])
            new_population.append([total_1, child_1[1], mutate_child_1[0], mutate_child_1[1], mutate_child_1[2], child_1[5], child_1[6], parent_1[7]])
            
            GVCN_event_2 = rank_event.order_event_GVCN(neighbor.find_event_GVCN(child_2[2], data, child_2[0][5], child_2[0][4]))
            for position, event in GVCN_event_2:
                mutate_child_2 = neighbor.mutation_soft(child_2[2], child_2[3], child_2[4], position, event, child_2[0][4], child_2[0][5], data)
            
            total_2 = penalty.total_check_soft(data, mutate_child_2[0], mutate_child_2[1], mutate_child_2[2])
            new_population.append([total_2, child_2[1], mutate_child_2[0], mutate_child_2[1], mutate_child_2[2], child_2[5], child_2[6], parent_2[7]])
         
        population = new_population
        population.sort(key=lambda chromosome: chromosome[0][3], reverse=False)
    
    best = population[0]
    for chromosome in population:
        violated_HC4 = neighbor.union_period(chromosome[0][6])
        
        iteration = 0
        while chromosome[0][2] > 0 and iteration < 20:
            repair = neighbor.repair_HC4(data, chromosome[2], chromosome[3], chromosome[4], violated_HC4, chromosome[0][4])
            
            total = penalty.total_check_soft(data, repair[0], repair[1], repair[2])
            if total[2] < chromosome[0][2]:
                chromosome[0], chromosome[2:5] = total, repair[:-1]
                violated_HC4 = repair[3]
                
                if chromosome[0][2] < best[0][2]:
                    best = chromosome
        
            iteration += 1
       
    optimize_time = time.process_time() - t
    
    if best[0][2] == 0:
        prepare_data.write_excel(data, 'THPT_CG_output_data1.xlsx', best[2], best[5], best[7], best[0], initial_time, feasible_time, optimize_time)
    
    else:
        prepare_data.write_excel(data, 'THPT_CG_output_data1.xlsx', best_timetable[2], best_timetable[5], best_timetable[0], best_timetable[0], initial_time, feasible_time, optimize_time)
        
    return best, optimize_time, population, population_1

a = construct_optimize_timetable()