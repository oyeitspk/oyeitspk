import json
import statistics
#import numpy as np

print('*********** hello from main app ***********')

def main():
    with open('file\9037.json') as json_file:
        data = json.load(json_file)
        
    blocks = data["textAnnotations"][1:]
    #print(data)

    lines = []
    words = []
    prev_y = None

    for block in blocks:
        
        vertices = block['boundingPoly']['vertices']
        #print(f'({vertices[0]["x"]}, {vertices[0]["y"]}) \t ({vertices[1]["x"]}, {vertices[1]["y"]})')
        #print('\t' + block['description'])
        #print(f'({vertices[3]["x"]}, {vertices[3]["y"]}) \t ({vertices[2]["x"]}, {vertices[2]["y"]})')
        #print('\n')

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
            avg_y = statistics.mean(line_y_cords)
            if abs(word[2][0]-avg_y) < 15:
                line.append(word)
                word_pushed = True
                break

        if not word_pushed:
            lines.append([word])

    print(len(lines))

    for line in lines:
        line_txt = ' '.join(w[0] for w in line)
        print('~' + line_txt)
    print('-'*50)
    sorted_lines = sorted(lines, key = lambda x:x[0][2][0])

    for line in sorted_lines:
        line_txt = ' '.join(w[0] for w in line)
        avg_line_ht = statistics.mean([w[4][3]-w[4][0] for w in line])
        #print('~ ' + str(avg_line_ht) + ' ~ ' + line_txt)
        print(str(round(avg_line_ht, 1)))

        char_ht_lst = [round(w[4][3]-w[4][0],1) for w in line] 
        temp = ' '.join(str(char_ht_lst))
        print(temp)

#arr = [30,31,29,30]
#print(np.percentile(arr, 90))
#print(np.mean(arr))

main()
    
    


    
    
