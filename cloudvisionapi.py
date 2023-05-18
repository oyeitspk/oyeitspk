from base64 import b64encode
from pylab import rcParams
import json, requests, os, logging
from app.global_config import config

url = config['CLOUD_VISION_API_URL']
api_key = config['API_KEY']
log = logging.getLogger(__name__)

def make_image_data(imgpath):
    img_req = None
    with open(imgpath, 'rb') as f:
        ctxt = b64encode(f.read()).decode()
        img_req = {
            'image': {
                'content': ctxt
            },
            'features': [{
                'type': 'DOCUMENT_TEXT_DETECTION',
                'maxResults': 1
            }]
        }
    return json.dumps({"requests": img_req}).encode()
     

def request_ocr(url, api_key, imgpath):
  imgdata = make_image_data(imgpath)
  response = requests.post(url, 
                           data = imgdata, 
                           params = {'key': api_key}, 
                           headers = {'Content-Type': 'application/json'})
  return response


def read_using_cloud_vision(img_loc):

    output_file = None
    try:
        con_folder = img_loc[:img_loc.rindex('/')]
        file_name = img_loc[img_loc.rindex('/') + 1:]
        output_folder = con_folder + '/Raw_ouptut'
        if(not os.path.exists(output_folder)):
            os.makedirs(output_folder)
        output_file = output_folder + '/' + file_name.replace('.jpg', '.json').replace('.jpeg', '.json')

        result = request_ocr(url, api_key, img_loc)
            
        if result.status_code != 200 or result.json().get('error'):
            log.error("Something went wrong! Please check API status and credentials.")
        else:
            result = result.json()['responses'][0]#['textAnnotations']
            with open(output_file, "w") as outfile:
                outfile.write(json.dumps(result))
            log.info(f'Raw JSON saved as: {output_file}')
    except Exception as e:
        log.info('Something went wrong while calling CloudVisionAPI')
        log.error(str(e))

    return output_file
