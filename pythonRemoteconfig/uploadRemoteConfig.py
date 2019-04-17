import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import argparse
import sys
import requests
import io


def createURL(project_id):
    # we will need to create our remote config url
    base_url = 'https://firebaseremoteconfig.googleapis.com'
    remote_config_endpoint = 'v1/projects/' + project_id + '/remoteConfig'
    remote_config_url = base_url + '/' + remote_config_endpoint
    return remote_config_url


def _get_access_token():
    # Find and apply application default credentials
    cred = credentials.ApplicationDefault()
    access_token_info = cred.get_access_token()
    return access_token_info.access_token


def _get(remote_config_url):
    # Retrieve the current Firebase Remote Config template from server and store the json
    headers = {
        'Authorization': 'Bearer ' + _get_access_token()
    }

    # get response, success if code 200
    resp = requests.get(remote_config_url, headers=headers)

    if resp.status_code == 200:
        with io.open('config.json', 'wb') as f:
            f.write(resp.text.encode('utf-8'))

        # log to console
        print('Retrieved template has been written to config.json')
        print('ETag from server: {}'.format(resp.headers['ETag']))

    else:
        print('Unable to get template')
        print(resp.text)


def _publish(etag, remote_config_url):
    # Publish the local template to the firebase server
    # - etag: id that helps us avoid race conditions when the template updates
    with open('config.json', 'r', encoding='utf-8') as f:
        content = f.read()

    # prepare header
    headers = {
        'Authorization': 'Bearer ' + _get_access_token(),
        'Content-Type': 'application/json; UTF-8',
        'If-Match': etag
    }

    # send out the header to the remote config url
    resp = requests.put(remote_config_url,
                        data=content.encode('utf-8'), headers=headers)

    if resp.status_code == 200:
        print('We have published our template!')
        print('Etag form the server: {}'.format(resp.headers['ETag']))
    else:
        print('publish failed')
        print(resp.text)


def _invalid_entry():
    # Log out the help message
    print('''\nplease define your project with:\n
\t--projectid=<YOUR GCP PROJECT ID>\n
And please use one of the additional flags:\n
\t--action=get
\t--action=publish --etag=<LATEST_ETAG>''')

    # stop the program
    sys.exit(0)


def main():
    # add argument for setting project
    parser = argparse.ArgumentParser()
    parser.add_argument('--projectid')
    parser.add_argument('--action')
    parser.add_argument('--etag')
    args = parser.parse_args()

    # check if a projectid has been entered or not
    if args.projectid is None:
        # no flag found
        _invalid_entry()
    else:
        # create the remote config url with the project
        remote_config_url = createURL(args.projectid)

        if args.action and args.action == 'get':
            _get(remote_config_url)

        elif args.action and args.action == 'publish' and args.etag:
            _publish(args.etag, remote_config_url)

        else:
            # no flag found
            _invalid_entry()


if __name__ == '__main__':
    main()
