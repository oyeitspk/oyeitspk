import json
import statistics
import numpy as np

print('*********** hello from main app ***********')

def main():
    with open('file/9037_0255.json') as json_file:
        data = json.load(json_file)

    blocks = data["textAnnotations"][1:]
    #print(data)

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
        #print(y_cords_sorted)

        x_cords = [c['x'] for c in vertices]
        x_cords_sorted = sorted(x_cords)
        #print(x_cords_sorted)

        word = (block['description'], x_cords_sorted, y_cords_sorted, x_cords, y_cords)
        #print(word)

        word_pushed = False

        #if len(lines) == 0:
        #    lines.append([word])
        #else:
        for line in lines:
            line_y_cords = [w[2][0] for w in line]
            avg_y = np.percentile(line_y_cords, 50)
            # avg_y = statistics.mean(line_y_cords)
            if abs(word[2][0]-avg_y) < 25:
                line.append(word)
                word_pushed = True
                break

        if not word_pushed:
            lines.append([word])

    print('--- no. of lines ---')
    print(len(lines))
    print('-'*30)

    #for line in lines:
    #    line_txt = ' '.join(w[0] for w in line)
    #    print('~' + line_txt)


    print('-'*50)

    sorted_lines = sorted(lines, key = lambda x:x[0][2][0])

    last_x_cords = []
    first_x_cords = []

    for line in sorted_lines:
        line_txt = ' '.join(w[0] for w in line)
        avg_line_ht = statistics.mean([w[4][3]-w[4][0] for w in line[:2]])
        avg_line_ht2 = np.percentile([w[4][3]-w[4][0] for w in line[:2]], 100)
        #print('~ ' + str(avg_line_ht) + ' ~ ' + line_txt)
        print(line_txt)
        print(str(round(avg_line_ht, 1)))
        print(str(round(avg_line_ht2, 1)))
        print('--')

        char_ht_lst = [round(w[4][3]-w[4][0],1) for w in line]
        temp = ' '.join(str(char_ht_lst))
        #print(temp)

        #sort words based on position1
        sorted_line = sorted(line, key = lambda x:x[1][0])
        sorted_line_txt = ' '.join(w[0] for w in sorted_line)

        #print(line_txt)
        #print(sorted_line_txt)

        last_x_cords.append(sorted_line[-1][1][3])
        first_x_cords.append(sorted_line[0][1][0])

    #print(last_x_cords)
    #print(max(last_x_cords))

    min_x_cord = min(first_x_cords)
    max_x_cord = max(last_x_cords)

    col1_lines = []
    col2_lines = []

    copy_sorted_lines = sorted_lines.copy()

    # checking based on line-spacing
    prev_bottom_y_cord = 0
    prev_bottom_y_cord_2 = 0

    for line in sorted_lines:
        top_left_y_cord_of_first_word = line[0][4][0]
        bottom_left_y_cord_of_first_word = line[0][4][3]
        avg_top_y_cord_2 = np.percentile([w[4][0] for w in line], 50)
        avg_bottom_y_cord_2 = np.percentile([w[4][3] for w in line], 50)
        avg_top_y_cord = statistics.mean([w[4][0] for w in line])
        avg_bottom_y_cord = statistics.mean([w[4][3] for w in line])
        # print(avg_top_y_cord - prev_bottom_y_cord)
        # print(avg_top_y_cord_2 - prev_bottom_y_cord_2)
        prev_bottom_y_cord = avg_bottom_y_cord
        prev_bottom_y_cord_2 = avg_bottom_y_cord_2
        # print(avg_top_y_cord)
        # print(avg_bottom_y_cord)


    print('-'*50)
    #for i in range(len(sorted_lines)-1, -1, -1):
    for i in range(0, len(copy_sorted_lines) -1):
        x_nums = [*range(min_x_cord, max_x_cord)]
        line = copy_sorted_lines[i]
        sorted_line = sorted(line, key = lambda x:x[1][0])
        sorted_line_txt = ' '.join(w[0] for w in sorted_line)
        #print(sorted_line_txt)

        for word in sorted_line:
            for j in range(word[3][0], word[3][1]): #check indices
                if j in x_nums:
                    x_nums.remove(j)

        middle_x_cord = (min_x_cord + max_x_cord) / 2

        col1_line = []
        col2_line = []

        if(middle_x_cord in x_nums):
            for word in sorted_line:
                if (word[3][1] < middle_x_cord and word[3][2] < middle_x_cord):
                    col1_line.append(word)
                if(word[3][0] > middle_x_cord and word[3][3] > middle_x_cord):
                    col2_line.append(word)
            #sorted_lines.remove(line)
            col1_lines.append(col1_line)
            col2_lines.append(col2_line)


    for line in sorted_lines:
        for word in line:
            pass
            # print(f'{word[4][0]}\t\t\t{word[4][1]}')
            # print(f'\t{word[0]}')
            # print(f'{word[4][3]}\t\t\t{word[4][2]}')
        a1 = ' '.join([str(word[4][0]) for word in line])
        b1 = ' '.join([str(word[4][3]) for word in line])
        c1 = ' '.join([word[0] for word in line])
        # print(a1)
        # print(c1)
        # print(b1)
        print('-----------')

    # print('')
    # print('..content..')
    # for line in sorted_lines:
    #     line_txt = ' '.join(w[0] for w in line)
    #     print(line_txt)

    # print('')
    # print('..commentary col 1..')
    # for line in col1_lines:
    #     line_txt = ' '.join(w[0] for w in line)
    #     print(line_txt)

    # print('')
    # print('..commentary col 2..')
    # for line in col2_lines:
    #     line_txt = ' '.join(w[0] for w in line)
    #     print(line_txt)


    # print(x_nums)
    # print(min(first_x_cords), max(last_x_cords))
    # print((min(first_x_cords)+max(last_x_cords))/2)


#arr = [30,31,29,30]
#print(np.percentile(arr, 90))
#print(np.mean(arr)

#main()
#print([*range(0, 90)])

def main2():
    with open('file/9037_0255.json') as json_file:
        data = json.load(json_file)

    blocks = data["fullTextAnnotation"]['pages'][0]['blocks']

    for block in blocks:
        print('~~block~~')
        paras = block['paragraphs']
        for para in paras:
            #print('~~~para~~~')
            para_txt = ''
            words = para['words']
            for word in words:
                word_txt = ''.join([s['text'] for s in word['symbols']])
                para_txt += ' ' + word_txt
            print(para_txt)

main2()











