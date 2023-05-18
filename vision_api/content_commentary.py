import json
import numpy as np

def get_content_commentary(input_file):

    lines_list = list()
    curr_line = list()
    prev_x_coord = None
    prev_y_coord = None


    # Opening JSON file
    with open(input_file) as json_file:
        data = json.load(json_file)

    fullTextAnnotation = data["fullTextAnnotation"]

    # Parsing one page json at a time
    page = fullTextAnnotation["pages"][0]

    blocks = page["blocks"]

    for block in blocks:
        if block["blockType"] == "TEXT":

            paragraphs = block["paragraphs"]
            for paragraph in paragraphs:

                words = paragraph["words"]
                for word in words:

                    symbols = word["symbols"]
                    word_text = "".join([symbol["text"] for symbol in symbols])
                    #print(word_text)

                    word_bounding_box = word["boundingBox"]
                    vertices = word_bounding_box["vertices"]

                    y_coords = [coord["y"] for coord in vertices]
                    y_coords_sorted = sorted(y_coords)
                    #print("y")
                    curr_word_size_y = y_coords_sorted[3] - y_coords_sorted[1]
                    #print(curr_word_size_y)
                    #print(y_coords_sorted)

                    x_coords = [coord["x"] for coord in vertices]
                    x_coords_sorted = sorted(x_coords)
                    #print("x")
                    #print(x_coords_sorted)
                    curr_word_size_x = x_coords_sorted[3] - x_coords_sorted[1]
                    #print(curr_word_size_x)


                    if (prev_x_coord is not None) and (prev_x_coord > x_coords_sorted[0]) and (prev_y_coord is not None) and (y_coords_sorted[0] - prev_y_coord > 25):
                        #print("New line detected")
                        #print(word_text)
                        #print("\n")
                        lines_list.append(curr_line)
                        curr_line = list()

                    curr_line.append((word_text, x_coords_sorted, y_coords_sorted))
                    prev_x_coord = x_coords_sorted[0]
                    prev_y_coord = y_coords_sorted[0]


    line_sizes = list()


    for line in lines_list[1:]:
        lowest_x = line[0][1][0]
        line_sizes.append(lowest_x)


    min_line_size = np.percentile(line_sizes, 15)
    max_line_size = np.percentile(line_sizes, 95)
    #print(min_line_size, max_line_size)



    commentary = ""
    content = ""

    for line in lines_list[1:]:
        line_joined = " ".join([l[0] for l in line])
        #print(line_joined)
        lowest_x = line[0][1][0]
        #print(lowest_x)

        dist_from_content = abs(lowest_x-max_line_size)
        #print("dist_from_content")
        #print(dist_from_content)

        dist_from_commentary = abs(lowest_x-min_line_size)
        #print("dist_from_commentary")
        #print(dist_from_commentary)

        if dist_from_content > dist_from_commentary:
            #print("Commentary")
            commentary = commentary + "\n" + line_joined
        else:
            #print("Content")
            content = content + "\n" + line_joined

        #print("\n")
        
    return content, commentary


