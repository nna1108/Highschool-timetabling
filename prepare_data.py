import random
import json
import xlsxwriter

def read_json(filename):
    with open(filename, 'r') as json_file:
        data = json.load(json_file)

    data = data['all_data']

    return data

def write_excel(data, filename, timetable, penalty_1, penalty_2, penalty_3, time_1, time_2, time_3):
    wb = xlsxwriter.Workbook(filename)
    
    sheet_result = wb.add_worksheet('Ket qua')
    sheet_AM = wb.add_worksheet('Buoi sang')
    sheet_PM = wb.add_worksheet('Buoi chieu')
    
    days = ['Thu_hai', 'Thu_ba', 'Thu_tu', 'Thu_nam', 'Thu_sau', 'Thu_bay']
    period_AM = [period for period in range(1, 29)]
    period_PM = [period for period in range(29, 57)]
    
    merge_format = wb.add_format({'align': 'center', 'valign': 'vcenter', 'border': 1})
    
    sheet_result.merge_range('A1:B1', 'Điều kiện', merge_format)
    sheet_result.merge_range('C1:E1', 'Khởi tạo', merge_format)
    sheet_result.merge_range('F1:H1', 'Cải thiện ràng buộc mềm', merge_format)
    
    sheet_result.merge_range('A2:B2', 'HC1', merge_format)
    sheet_result.merge_range('C2:E2', 0, merge_format)
    sheet_result.merge_range('F2:H2', 0, merge_format)
    
    sheet_result.merge_range('A3:B3', 'HC2', merge_format)
    sheet_result.merge_range('C3:E3', 0, merge_format)
    sheet_result.merge_range('F3:H3', 0, merge_format)
    
    sheet_result.merge_range('A4:B4', 'HC3', merge_format)
    sheet_result.merge_range('C4:E4', 0, merge_format)
    sheet_result.merge_range('F4:H4', 0, merge_format)
    
    sheet_result.merge_range('A5:B5', 'HC4', merge_format)
    sheet_result.merge_range('C5:E5', 0, merge_format)
    sheet_result.merge_range('F5:H5', 0, merge_format)
    
    sheet_result.merge_range('A6:B6', 'HC5', merge_format)
    sheet_result.merge_range('C6:E6', 0, merge_format)
    sheet_result.merge_range('F6:H6', 0, merge_format)
    
    sheet_result.merge_range('A7:B7', 'HC6', merge_format)
    sheet_result.merge_range('C7:E7', 0, merge_format)
    sheet_result.merge_range('F7:H7', 0, merge_format)
    
    sheet_result.merge_range('A8:B8', 'SC1 + SC2', merge_format)
    sheet_result.merge_range('C8:E8', penalty_2[3], merge_format)
    sheet_result.merge_range('F8:H8', penalty_3[3], merge_format)
    
    sheet_result.merge_range('A9:B9', 'Thời gian (giây)', merge_format)
    sheet_result.merge_range('C9:E9', time_1 + time_2, merge_format)
    sheet_result.merge_range('F9:H9', time_3, merge_format)

    for sheet in [sheet_AM, sheet_PM]:
        sheet.write(0, 0, 'Ngay', wb.add_format({'align': 'center'}))
        sheet.write(0, 1, 'Tiet', wb.add_format({'align': 'center'}))
    
    row = 0
    for day in days:
        sheet_AM.write(row + 1, 0, day, wb.add_format({'align': 'center'}))
        row += 10
    
    row = 0
    col = 0
    for period in period_AM:
        sheet_AM.write(row + 1, col + 1, period, wb.add_format({'align': 'center'}))
        row += 2
        
    col = 0
    for highschool_class in data['Classes']['Mode']['AM']:
        sheet_AM.write(0, col + 2, highschool_class, wb.add_format({'align': 'center'}))
        col += 1
    
    row = 0
    for day in days:
        sheet_PM.write(row + 1, 0, day, wb.add_format({'align': 'center'}))
        row += 10
    
    row = 0
    col = 0
    for period in period_PM:
        sheet_PM.write(row + 1, col + 1, period, wb.add_format({'align': 'center'}))
        row += 2
    
    col = 0
    for highschool_class in data['Classes']['Mode']['PM']:
        sheet_PM.write(0, col + 2, highschool_class, wb.add_format({'align': 'center'}))
        col += 1
        
    
    row = 0
    col = 0
    for highschool_class in data['Classes']['Mode']['AM']:
        for day in days:
            for period in data['Events']['timetable'][highschool_class][day]:
                position = (highschool_class, day, period)
                if timetable[position] != None:
                    sheet_AM.write(row + 1, col + 2, timetable[position][0][0][0])
                else:
                    sheet_AM.write(row + 1, col + 2, 'None')
                row += 2
        col += 1
        row = 0
    
    row = 0
    col = 0
    for highschool_class in data['Classes']['Mode']['AM']:
        for day in days:
            for period in data['Events']['timetable'][highschool_class][day]:
                position = (highschool_class, day, period)
                if timetable[position] != None:
                    sheet_AM.write(row + 2, col + 2, int(timetable[position][0][0][1]), wb.add_format({'align': 'right'}))
                else:
                    sheet_AM.write(row + 2, col + 2, 'None', wb.add_format({'align': 'right'}))
                row += 2
        col += 1
        row = 0
        
    row = 0
    col = 0
    for highschool_class in data['Classes']['Mode']['PM']:
        for day in days:
            for period in data['Events']['timetable'][highschool_class][day]:
                position = (highschool_class, day, period)
                if timetable[position] != None:
                    sheet_PM.write(row + 1, col + 2, timetable[position][0][0][0])
                else:
                    sheet_PM.write(row + 1, col + 2, 'None')
                row += 2
        col += 1
        row = 0
        
    row = 0
    col = 0
    for highschool_class in data['Classes']['Mode']['PM']:
        for day in days:
            for period in data['Events']['timetable'][highschool_class][day]:
                position = (highschool_class, day, period)
                if timetable[position] != None:
                    sheet_PM.write(row + 2, col + 2, int(timetable[position][0][0][1]), wb.add_format({'align': 'right'}))
                else:
                    sheet_PM.write(row + 2, col + 2, 'None', wb.add_format({'align': 'right'}))
                row += 2
        col += 1
        row = 0
        
    wb.close()

def assigned_to_room(data):
    room_assigned = {}
    
    for highschool_class in data['Classes']['Class_ID']:
        mode = data['Classes']['Mode'][highschool_class]
        room = random.choice(data['Rooms'][mode])
        room_assigned.update({highschool_class: room})
        data['Rooms'][mode].remove(room)
    
    return room_assigned

def assigned_to_teacher(data):
    #luu cac event ma giao vien duoc phan cong
    teacher_data = {}
    for teacher in data['Teachers']['Teacher_ID']:
        teacher_data.update({teacher: []})
    
    #TKB tam thoi
    class_assigned_teacher = []
    
    #luu giao vien da duoc phan cong cho lop
    subject_teacher_assigned = {}
    
    #phan cong giao vien
    for highschool_class in data['Classes']['Class_ID']:
        for subject in data['Events']['blocks'][highschool_class]:
            for block in data['Events']['blocks'][highschool_class][subject]:
                if subject == data['Classes']['GVCN_major'][highschool_class] or subject == 'Chao_co' or subject == 'Sinh_hoat':
                    teacher = data['Classes']['GVCN_ID'][highschool_class]
                    
                elif subject in subject_teacher_assigned:
                    teacher = subject_teacher_assigned[subject]
                
                elif subject not in subject_teacher_assigned:
                    teacher = random.choice(data['Teachers']['Majors'][subject])
            
                if block == 2:
                    class_assigned_teacher.append([[[subject, teacher]] * 2, highschool_class])
                    teacher_data[teacher].append([[[subject, teacher]] * 2, highschool_class])
                
                else:
                    class_assigned_teacher.append([[[subject, teacher]], highschool_class])
                    teacher_data[teacher].append([[[subject, teacher]], highschool_class])
            
                subject_teacher_assigned.update({subject: teacher})
        
        subject_teacher_assigned.clear()
       
    return teacher_data, class_assigned_teacher

#assigned_to_teacher(read_json('THPT_CG_input.json'))

#khoi tao thoi khoa bieu trong
def generate_timetable(data):
    timetable = {}
    
    #khoi tao thoi khoa bieu
    for highschool_class in data['Classes']['Class_ID']:
        for day in data['Events']['timetable'][highschool_class]:
            for period in data['Events']['timetable'][highschool_class][day]:
                position = (highschool_class, day, period)
                timetable[position] = None
    
    return timetable

#store information for teachers teach in that period
def generate_teacher_in_period():
    teacher_in_period = {}
    for period in range(1, 57):
        teacher_in_period.update({period: []})
    
    return teacher_in_period

#store information for subjects that are taught in that period
def generate_subject_in_period(data):
    subject_in_period = {}
    for highschool_class in data['Classes']['Class_ID']:
        subject_in_period.update({highschool_class: {}})
        for day in list(data['Events']['timetable'][highschool_class].keys()):
            subject_in_period[highschool_class].update({day: []})
    
    return subject_in_period

def get_position(event, timetable, data):
    list_of_pos = []
    
    if len(event[0]) == 1:
        #unallow_period = [1, 28, 29, 56]
        
        for day in data['Events']['timetable'][event[1]]:
            if day == 'Thu_hai':
                for period in data['Events']['timetable'][event[1]][day][1:]:
                    if timetable[(event[1], day, period)] != None:
                        list_of_pos.append((event[1], day, period))
            
            elif day == 'Thu_bay':
                for period in data['Events']['timetable'][event[1]][day][:-1]:
                    if timetable[(event[1], day, period)] != None:
                        list_of_pos.append((event[1], day, period))
            
            else:
                for period in data['Events']['timetable'][event[1]][day]:
                    if timetable[(event[1], day, period)] != None:
                        list_of_pos.append((event[1], day, period))
    
    else:
        #unallow_period = [p for p in range(5, 30, 5)] + [1, 27, 28, 29, 55, 56] + [p for p in range(33, 58, 5)]
        
        for day in data['Events']['timetable'][event[1]]:
            if day == 'Thu_hai':
                for period in data['Events']['timetable'][event[1]][day][1:4]:
                    if timetable[(event[1], day, period)] != None and timetable[(event[1], day, period + 1)] != None:
                        list_of_pos.append([(event[1], day, period), (event[1], day, period + 1)])
            
            elif day == 'Thu_bay':
                period = data['Events']['timetable'][event[1]][day][0]
                if timetable[(event[1], day, period)] != None and timetable[(event[1], day, period + 1)] != None:
                    list_of_pos.append([(event[1], day, period), (event[1], day, period + 1)])
            
            else:
                for period in data['Events']['timetable'][event[1]][day][:-1]:
                    if timetable[(event[1], day, period)] != None and timetable[(event[1], day, period + 1)] != None:
                        list_of_pos.append([(event[1], day, period), (event[1], day, period + 1)])
    
    return list_of_pos

def get_empty_position(event, timetable, data):
    empty_position = []
    
    if len(event[0]) == 1:
        #unallow_period = [1, 28, 29, 56]
        
        #vi tri cho lop: highschool_class = event[1]
        for day in data['Events']['timetable'][event[1]]:
            if day == 'Thu_hai':
                for period in data['Events']['timetable'][event[1]][day][1:]:
                    if timetable[(event[1], day, period)] == None:
                        empty_position.append((event[1], day, period))
            
            elif day == 'Thu_bay':
                for period in data['Events']['timetable'][event[1]][day][:-1]:
                    if timetable[(event[1], day, period)] == None:
                        empty_position.append((event[1], day, period))
            
            else:
                for period in data['Events']['timetable'][event[1]][day]:
                    if timetable[(event[1], day, period)] == None:
                        empty_position.append((event[1], day, period))
    
    else:
        #unallow_period = [p for p in range(5, 30, 5)] + [1, 28, 29, 56] + [p for p in range(33, 58, 5)]
        
        #vi tri cho lop: highschool_class = event[1]
        for day in data['Events']['timetable'][event[1]]:
            if day == 'Thu_hai':
                for period in data['Events']['timetable'][event[1]][day][1:4]:
                    if timetable[(event[1], day, period)] == None and timetable[(event[1], day, period + 1)] == None:
                        empty_position.append([(event[1], day, period), (event[1], day, period + 1)])
            
            elif day == 'Thu_bay':
                period = data['Events']['timetable'][event[1]][day][0]
                if timetable[(event[1], day, period)] == None and timetable[(event[1], day, period + 1)] == None:
                    empty_position.append([(event[1], day, period), (event[1], day, period + 1)])
            
            else:
                for period in data['Events']['timetable'][event[1]][day][:-1]:
                    if timetable[(event[1], day, period)] == None and timetable[(event[1], day, period + 1)] == None:
                        empty_position.append([(event[1], day, period), (event[1], day, period + 1)])
    
    return empty_position

def get_position_soft(event, timetable, data, not_violated_SC):
    list_of_pos_1 = [(event[1], 'Thu_hai', data['Events']['timetable'][event[1]]['Thu_hai'][1]), (event[1], 'Thu_bay', data['Events']['timetable'][event[1]]['Thu_bay'][1])]
    list_of_pos_2 = [[(event[1], 'Thu_hai', data['Events']['timetable'][event[1]]['Thu_hai'][1]), (event[1], 'Thu_hai', data['Events']['timetable'][event[1]]['Thu_hai'][2])], [(event[1], 'Thu_bay', data['Events']['timetable'][event[1]]['Thu_bay'][0]), (event[1], 'Thu_bay', data['Events']['timetable'][event[1]]['Thu_bay'][1])]]
    
    list_of_pos = []
    if len(event[0]) == 1:
        for pos in list_of_pos_1:
            if pos not in not_violated_SC:
                list_of_pos.append(pos)
    
    else:
        for pos in list_of_pos_2:
            if pos[0] not in not_violated_SC and pos[1] not in not_violated_SC:
                list_of_pos.append(pos)
    
    return list_of_pos

def get_position_repair(data, timetable, position):
    list_of_pos = []
    
    #unallow_period = [1, 2, 27, 28, 29, 30, 55, 56]
    
    if timetable[position][2] == 1:
        for day in data['Events']['timetable'][position[0]]:
            if day == 'Thu_hai':
                for period in data['Events']['timetable'][position[0]][day][2:]:
                    pos = (position[0], day, period)
                    
                    if pos != position and timetable[pos][2] == timetable[position][2]:
                        list_of_pos.append(pos)
            
            elif day == 'Thu_bay':
                pos = (position[0], day, data['Events']['timetable'][position[0]][day][0])
                
                if pos != position and timetable[pos][2] == timetable[position][2]:
                    list_of_pos.append(pos)
            
            else:
                for period in data['Events']['timetable'][position[0]][day]:
                    if pos != position and timetable[pos][2] == timetable[position][2]:
                        list_of_pos.append(pos)
    
    else:
        for day in data['Events']['timetable'][position[0]]:
            if day == 'Thu_hai':
                if timetable[(position[0], day, data['Events']['timetable'][position[0]][day][1])][2] == 2:
                    if position not in [(position[0], day, data['Events']['timetable'][position[0]][day][3]), (position[0], day, data['Events']['timetable'][position[0]][day][4])]:
                        list_of_pos.append([(position[0], day, data['Events']['timetable'][position[0]][day][3]), (position[0], day, data['Events']['timetable'][position[0]][day][4])])
                
                else:
                    if timetable[(position[0], day, data['Events']['timetable'][position[0]][day][2])][2] == 1 and timetable[(position[0], day, data['Events']['timetable'][position[0]][day][3])][2] == 2:
                        if position not in [(position[0], day, data['Events']['timetable'][position[0]][day][3]), (position[0], day, data['Events']['timetable'][position[0]][day][4])]:
                            list_of_pos.append([(position[0], day, data['Events']['timetable'][position[0]][day][3]), (position[0], day, data['Events']['timetable'][position[0]][day][4])])
                    
                    elif timetable[(position[0], day, data['Events']['timetable'][position[0]][day][2])][2] == 1 and timetable[(position[0], day, data['Events']['timetable'][position[0]][day][3])][2] == 1:
                        if position not in [(position[0], day, data['Events']['timetable'][position[0]][day][2]), (position[0], day, data['Events']['timetable'][position[0]][day][3]), (position[0], day, data['Events']['timetable'][position[0]][day][4])]:
                            list_of_pos.append([(position[0], day, data['Events']['timetable'][position[0]][day][2]), (position[0], day, data['Events']['timetable'][position[0]][day][3])])
                            list_of_pos.append([(position[0], day, data['Events']['timetable'][position[0]][day][3]), (position[0], day, data['Events']['timetable'][position[0]][day][4])])
            
            elif day not in ['Thu_hai', 'Thu_bay']:
                for period in data['Events']['timetable'][position[0]][day][:-1]:
                    pos = (position[0], day, period)
                    
                    if pos != position and timetable[pos][2] == 1 and timetable[(position[0], day, period + 1)][2] == 1:
                        list_of_pos.append([pos, (position[0], day, period + 1)])
                    
                    elif pos != position and timetable[pos][2] == 2 and timetable[(position[0], day, period + 1)][0][0] == timetable[pos][0][0]:
                        list_of_pos.append([pos, (position[0], day, period + 1)])
            
    return list_of_pos