def exceptions(number1, number2, operator):
    #only digits verification
    try:
        int(number1)
    except:
        return "Error: Numbers must only contain digits."
    try:
        int(number2)
    except:
        return "Error: Numbers must only contain digits."
    #testing limit of 4 digits
    try:
        if len(number1) > 4 or len(number2) > 4:
            raise BaseException
    except:
        return "Error: Numbers cannot be more than four digits."
    # Operator must be + | - exception.
    try:
        if operator != '+' and operator != '-':
            raise BaseException
    except:
        return "Error: Operator must be '+' or '-'."
    return ""

def arithmetic_arranger(problems, ShouldShowOps=False):

    start = True
    spaceInSides = "    "
    line1 = line2 = line3 = line4 = ""
    
    for prob in problems:
        #splitting problems and storing them into new varibables
        splitted_problem = prob.split()
        number = splitted_problem[0]
        operator = splitted_problem[1]
        number2 = splitted_problem[2]

        exception = exceptions(number, number2, operator)
        if exception != "":
            return exception
            
        number_adjusted = int(number)
        number2_adjusted = int(number2)
        # space contains the max number os spaces required.
        space = max(len(number), len(number2))
        #start of arithmetic arrangement
        if start:
            line1 += number.rjust(space + 2)
            line2 += operator + ' ' + number2.rjust(space)
            line3 += '-' * (space + 2)

            if ShouldShowOps == True:
                if operator == '+':
                    line4 += str(number_adjusted + number2_adjusted).rjust(space + 2)
                else:
                    line4 += str(number_adjusted - number2_adjusted).rjust(space + 2)
            start = False

        #other than first arithmetic arragement
        else:
            line1 += number.rjust(space + 6)
            line2 += operator.rjust(5) + ' ' + number2.rjust(space)
            line3 += spaceInSides + '-' * (space + 2)

            if ShouldShowOps == True:
                if operator == '+':
                    line4 += spaceInSides + str(number_adjusted + number2_adjusted).rjust(space + 2)
                else:
                    line4 += spaceInSides + str(number_adjusted - number2_adjusted).rjust(space + 2)

    #ShouldShowOps is True, the line4 will be printed
    if ShouldShowOps == True:
        return line1 + '\n' + line2 + '\n' + line3 + '\n' + line4
    return line1 + '\n' + line2 + '\n' + line3

#ops list and ShouldShowOps setted like True
print(arithmetic_arranger(["32 + 698", "3801 - 2", "45 + 43", "123 + 49"], True))