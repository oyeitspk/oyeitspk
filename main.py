import json
import statistics
import numpy as np

print('*********** hello from main app ***********')


def main():
    with open('file/rm2.json') as json_file:
        data = json.load(json_file)

    blocks = data["textAnnotations"][1:]
    # print(data)

    lines = []
    words = []
    prev_y = None

    for block in blocks:

        vertices = block['boundingPoly']['vertices']
        # print(f'({vertices[0]["x"]}, {vertices[0]["y"]}) \t ({vertices[1]["x"]}, {vertices[1]["y"]})')
        # print('\t' + block['description'])
        # print(f'({vertices[3]["x"]}, {vertices[3]["y"]}) \t ({vertices[2]["x"]}, {vertices[2]["y"]})')
        # print('\n')

        y_cords = [c['y'] for c in vertices]
        y_cords_sorted = sorted(y_cords)
        # print(y_cords_sorted)

        x_cords = [c['x'] for c in vertices]
        x_cords_sorted = sorted(x_cords)
        # print(x_cords_sorted)

        word = (block['description'], x_cords_sorted,
                y_cords_sorted, x_cords, y_cords)
        # print(word)

        word_pushed = False

        # if len(lines) == 0:
        #    lines.append([word])
        # else:
        for line in lines:
            line_y_cords = [w[2][0] for w in line]
            avg_y = statistics.mean(line_y_cords)
            if abs(word[2][0]-avg_y) < 15:
                line.append(word)
                word_pushed = True
                break

        if not word_pushed:
            lines.append([word])

    print(len(lines))

    # for line in lines:
    #    line_txt = ' '.join(w[0] for w in line)
    #    print('~' + line_txt)

    print('-'*50)

    sorted_lines = sorted(lines, key=lambda x: x[0][2][0])

    last_x_cords = []
    first_x_cords = []

    for line in sorted_lines:
        line_txt = ' '.join(w[0] for w in line)
        avg_line_ht = statistics.mean([w[4][3]-w[4][0] for w in line])
        # print('~ ' + str(avg_line_ht) + ' ~ ' + line_txt)
        # print(str(round(avg_line_ht, 1)))

        char_ht_lst = [round(w[4][3]-w[4][0], 1) for w in line]
        temp = ' '.join(str(char_ht_lst))
        # print(temp)

        # sort words based on position1
        sorted_line = sorted(line, key=lambda x: x[1][0])
        line = sorted_line

        print_line(line)
        print_line(sorted_line)

        # print(line_txt)
        # print(sorted_line_txt)

        last_x_cords.append(sorted_line[-1][1][3])
        first_x_cords.append(sorted_line[0][1][0])

    # printing line and last x cords of each line
    for line in sorted_lines:
        print(str(line[0][1][0]) + ' ' + str(line[-1][1][1])) 

    min_x_cord = min(first_x_cords)
    max_x_cord = max(last_x_cords)

    copy_sorted_lines = sorted_lines.copy()

    # checking based on line-spacing
    #prev_bottom_y_cord = 0
    #for line in sorted_lines:
    #    top_left_y_cord_of_first_word = line[0][4][0]
    #    bottom_left_y_cord_of_first_word = line[0][4][3]
    #    avg_top_y_cord = statistics.mean([w[4][0] for w in line])
    #    avg_bottom_y_cord = statistics.mean([w[4][3] for w in line])
    #    # print(avg_top_y_cord - prev_bottom_y_cord)
    #    prev_bottom_y_cord = avg_bottom_y_cord
    #    #print(avg_top_y_cord)
    #    #print(avg_bottom_y_cord)
    #    #print('\n')


    len(sorted_lines)
    print('+'*50)

    sorted_lines, col1_lines, col2_lines = separte_by_columns_new(sorted_lines)
    # sorted_lines, col1_lines, col2_lines = separte_by_columns_old(sorted_lines, min_x_cord, max_x_cord)

    print('##### Content....... ')
    print_lines(sorted_lines)

    print('##### Commentary (col 1)....... ')
    print_lines(col1_lines)

    print('##### Commentary (col 2)....... ')
    print_lines(col2_lines)


def print_lines(lines):
    [print_line(line) for line in lines]

def print_line(line):
    line_txt = ' '.join(word[0] for word in line)
    print(line_txt)

def separte_by_columns_old(sorted_lines, min_x_cord, max_x_cord):
    copy_sorted_lines = sorted_lines
    col1_lines = []
    col2_lines = []
    for i in range(len(sorted_lines)-1, -1, -1):
        # for i in range(0, len(copy_sorted_lines) -1):
        x_nums = [*range(min_x_cord, max_x_cord)]
        line = copy_sorted_lines[i]
        sorted_line = sorted(line, key=lambda x: x[1][0])
        #sorted_line_txt = ' '.join(w[0] for w in sorted_line)
        # print(sorted_line_txt)

        for word in sorted_line:
            for j in range(word[3][0], word[3][1]):  # check indices
                if j in x_nums:
                    x_nums.remove(j)

        middle_x_cord = int((min_x_cord + max_x_cord) / 2)

        # top left x cord of first word of current line
        line_min_x_cord = sorted_line[0][3][0]
        # top right x cord of last word of current line
        line_max_x_cord = sorted_line[-1][3][1]
        line_middle_x_cord = int((line_min_x_cord + line_max_x_cord) / 2)

        middle_word_1 = None
        middle_word_2 = None
        for word in sorted_line:
            if word[3][0] < middle_x_cord and word[3][1] > middle_x_cord:
                middle_word_1 = word[0]
            if word[3][0] < line_middle_x_cord and word[3][1] > line_middle_x_cord:
                middle_word_2 = word[0]

        #print_line(sorted_line)
        #print(x_nums)
        #print(middle_x_cord)
        #print(line_middle_x_cord)

        col1_line = []
        col2_line = []

        if middle_word_1 is not None:
            print('~~~' + middle_word_1)
        if middle_word_2 is not None:
            print('~~~' + middle_word_2)
            
        if (middle_x_cord not in x_nums and middle_word_1 is not None and middle_word_1 != '|'):
            if (line_middle_x_cord not in x_nums  and middle_word_2 is not None and middle_word_2 != '|'):
                print('..loop will break...')
                break
            else:
                for word in sorted_line:
                    if (word[3][1] < line_middle_x_cord and word[3][2] < line_middle_x_cord):
                        col1_line.append(word)
                    if (word[3][0] > line_middle_x_cord and word[3][3] > line_middle_x_cord):
                        col2_line.append(word)
                sorted_lines.remove(line)
                col1_lines.append(col1_line)
                col2_lines.append(col2_line)
        else:
            for word in sorted_line:
                if (word[3][1] < middle_x_cord and word[3][2] < middle_x_cord):
                    col1_line.append(word)
                if (word[3][0] > middle_x_cord and word[3][3] > middle_x_cord):
                    col2_line.append(word)
            sorted_lines.remove(line)
            col1_lines.append(col1_line)
            col2_lines.append(col2_line)

        # if(line_middle_x_cord in x_nums):
        #    for word in sorted_line:
        #        if (word[3][1] < line_middle_x_cord and word[3][2] < line_middle_x_cord):
        #            col1_line.append(word)
        #        if(word[3][0] > line_middle_x_cord and word[3][3] > line_middle_x_cord):
        #            col2_line.append(word)
        #    sorted_lines.remove(line)
        #    col1_lines.append(col1_line)
        #    col2_lines.append(col2_line)

    col1_lines.reverse()
    col2_lines.reverse()

    return sorted_lines, col1_lines, col2_lines

def separte_by_columns_new(sorted_lines):
    copy_sorted_lines = sorted_lines
    col1_lines = []
    col2_lines = []

    # checking based on starting position of the line
    upper_starting_x_cord_of_line = np.percentile([line[0][1][0] for line in sorted_lines[1:6]], 50)
    bottom_starting_x_cord_of_line = np.percentile([line[0][1][0] for line in sorted_lines[-6:-1]], 50)
    print('upper_starting_x_cord_of_line')
    print(upper_starting_x_cord_of_line)
    print('bottom_starting_x_cord_of_line')
    print(bottom_starting_x_cord_of_line)

    content_lines = []
    commeantary_lines = []

    for i in range(len(sorted_lines)-1, 0, -1):
        line = copy_sorted_lines[i]
        if abs(line[0][1][0] - bottom_starting_x_cord_of_line) < 20:
            commeantary_lines.append(line)
        else:
            content_lines.append(line)

    min_x_cord = min([line[0][3][0] for line in commeantary_lines])
    max_x_cord = max([line[-1][3][1] for line in commeantary_lines])

    print(min_x_cord)
    print(max_x_cord)

    print_lines(content_lines)

    x_nums = [*range(min_x_cord, max_x_cord)]
    
    for line in commeantary_lines:
        for word in line:
            for j in range(word[3][0], word[3][1]):  # check indices
                if j in x_nums:
                    x_nums.remove(j)
    
    print (x_nums)

    parition_middle_cord = statistics.mean(longest_subsequence(x_nums))

    for line in commeantary_lines:
        col1_line = []
        col2_line = []

        for word in line:
            if (word[3][1] < parition_middle_cord and word[3][2] < parition_middle_cord):
                col1_line.append(word)
            if (word[3][0] > parition_middle_cord and word[3][3] > parition_middle_cord):
                col2_line.append(word)

        col1_lines.append(col1_line)
        col2_lines.append(col2_line)

    col1_lines.reverse()
    col2_lines.reverse()

    return content_lines, col1_lines, col2_lines


# arr = [30,31,29,30]
# print(np.percentile(arr, 90))
# print(np.mean(arr)

def longest_subsequence(arr):
    sseq = []
    for n in arr:
        if len(sseq) == 0:
            sseq.append(n)
        else:
            if sseq[-1] + 1 == n:
                sseq.append(n)
            else:
                sseq = [n]
    if len(sseq) == 1:
        sseq = []
    print(sseq)
    return sseq

main()
# print([*range(0, 90)])


def main2():
    with open('file/9037.json') as json_file:
        data = json.load(json_file)

    blocks = data["fullTextAnnotation"]['pages'][0]['blocks']

    for block in blocks:
        print('~~block~~')
        paras = block['paragraphs']
        for para in paras:
            # print('~~~para~~~')
            para_txt = ''
            words = para['words']
            for word in words:
                word_txt = ''.join([s['text'] for s in word['symbols']])
                para_txt += ' ' + word_txt
            print(para_txt)

# main2()
