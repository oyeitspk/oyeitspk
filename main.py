import os, logging
from datetime import datetime
from app.content_commentary import *
from app.cloudvisionapi import read_using_cloud_vision
from app.global_config import config

#input_file = "OCR/AP_examples_orig_res/02_orig_res.json"#

log_file_name = 'app_logs/' + datetime.now().strftime('logs_%Y_%m_%d__%H_%M_%S') + '.log'

logging.basicConfig(filename=log_file_name, filemode='w', format='%(name)s - %(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

def main():
    source_folder = config['SOURCE_FOLDER']
    for root, subdirs, files in os.walk(source_folder):
        for file in files:
            if(file.endswith('.jpg') or file.endswith('.jpeg')):
                logger.info(f'Prcessing file: {file}')
                filePath = os.path.join(root, file).replace('\\','/')
                raw_json_file = read_using_cloud_vision(filePath)
                if(raw_json_file != None):
                    content, commentary = get_content_commentary(raw_json_file)
                    logger.info('Successfully extracted text and commntary')
                    save_output(filePath, content, commentary)
                    logger.info(f'Saved extracted data in file: {filePath}')

def save_output(filePath, content, commentary):
    con_folder = filePath[:filePath.rindex('/')]
    file_name = filePath[filePath.rindex('/') + 1:]
    output_folder = con_folder + '/Final Output'
    if(not os.path.exists(output_folder)):
        os.makedirs(output_folder)
    output_file = output_folder + '/' + file_name.replace('.jpg', '.json').replace('.jpeg', '.json')
    with open(output_file, "w") as outfile:
        outfile.write(json.dumps({
                "content" : content,
                "commentary" : commentary
        }))

# content, commentary = get_content_commentary(filePath)

# logger.info(content)
# logger.info('----------')
# logger.info(commentary)

main()
