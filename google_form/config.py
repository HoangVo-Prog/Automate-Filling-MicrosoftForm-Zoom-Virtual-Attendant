import random


def get_items(n):
    # Part 1
    if n == 1:
        return ["Có", "Không"]
    
    elif n == 2:
        return ["Dưới 1 năm", "Từ 1 năm đến 5 năm", "Từ 6 năm đến 10 năm", "Trên 10 năm"]
    
    # Part 2
    elif n in range(3, 39):
        return ["1", "2", "3", "4", "5"]
    
    # Part 3:
    elif n == 39:
        return ["Nam", "Nữ"]

    elif n == 40:
        return [
            "Dưới 21 tuổi",
            "Từ 21 tuổi đến 30 tuổi",
            "Từ 31 tuổi đến 40 tuổi",
            "Từ 41 tuổi đến 50 tuổi",
            "Trên 50 tuổi"
        ]    
    
    elif n == 41:
        return ["Bosch"]
    
    elif n == 42:
        return ["Logistics Inbond"]

def get_weights(n):
    if n == 1:
        return [1.0, 0.0]
    
    elif n == 2:
        return [0.0, 0.3, 0.3, 0.4]
    
    elif n in range(3, 39):
        return [0.1, 0.1, 0.1, 0.2, 0.5]
    
    elif n == 39:
        return [0.7, 0.3]
    
    elif n == 40:
        return [0.2, 0.4, 0.2, 0.1, 0.1]
    
    elif n == 41:
        return [1]
    
    elif n == 42:
        return [1]
    
    
def get_answers(n):
    return random.choices(get_items(n), weights=get_weights(n), k=1)[0]

def get_all_answers(num_questions=42):
    answers = []
    for i in range(1, num_questions + 1):
        answer = get_answers(i)
        answers.append(answer)
    if answers[0] == "Không":
        answers[1] = None  
    if answers[1] == "Dưới 1 năm":
        answers[2] = None
    return answers
        
def get_all_questions(src):
    pass

    
