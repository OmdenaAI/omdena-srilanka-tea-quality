'''
Client script to test the flask api by sending request to the server.
Example:
  python3 client.py -i {img file path} -e {environment | default=production}
'''
from argparse import ArgumentParser
from requests import post
from os.path import exists, basename


def get_base_url(env='development'):
    if env == 'development':
        return 'http://localhost:5000/api'
    raise Exception(f'Env:{env} not implemented yet.')


def inference_api(base_url, filepath):
    # Prepare url for inferences endpoint
    url = base_url + '/inferences'
    # prepare files dict to include the image file
    files = {
        'file': (basename(filepath), open(filepath, 'rb'))
    }
    # Send the request to the server
    response = post(url, files=files)
    # Read the json content from response object
    if response.status_code == 200:
        res_json = response.json()
        # print(res_json)
        # Display the json content
        print('Response msg    :', res_json['msg'])
        print('Response status :', res_json['status'])
    else:
        print('Something went wrong')
        print('---Response---')
        print(response.status_code)
        print(response.text)


if __name__ == "__main__":
    # Parse the CLI arguments 'env', 'img'
    ap = ArgumentParser()
    ap.add_argument('--img', '-i', required=True,
                    type=str, help="Image file path")
    ap.add_argument('--env', '-e', required=False,
                    default='production', type=str,
                    choices=['development', 'staging', 'production'],
                    help="Client's Environment")
    vars = ap.parse_args()

    # Check if img path exists and has access to the path
    if not exists(vars.img):
        raise Exception(
            f"{vars.img} not exists or doesn't have access to the path.")

    # Get the base url based on environment
    base_url = get_base_url(vars.env)
    # Call the inferences endpoint method.
    inference_api(base_url, vars.img)
