from flask import Blueprint, request, abort, current_app
import git
import hmac
import hashlib
import json

gitUpdate = Blueprint('gitUpdate', __name__)


def is_valid_signature(x_hub_signature, data, private_key):
    # x_hub_signature and data are from the webhook payload
    # private key is your webhook secret
    hash_algorithm, github_signature = x_hub_signature.split('=', 1)
    algorithm = hashlib.__dict__.get(hash_algorithm)
    encoded_key = bytes(private_key, 'latin-1')
    mac = hmac.new(encoded_key, msg=data, digestmod=algorithm)
    return hmac.compare_digest(mac.hexdigest(), github_signature)



def checkHeaders(headers, abort_code):
    # Do initial validations on required headers
    if 'X-Github-Event' not in headers:
        abort(abort_code)
    if 'X-Github-Delivery' not in headers:
        abort(abort_code)
    if 'X-Hub-Signature' not in headers:
        abort(abort_code)
    if 'User-Agent' not in headers:
        abort(abort_code)
    ua = request.headers.get('User-Agent')
    if not ua.startswith('GitHub-Hookshot/'):
        abort(abort_code)
    return


def checks(request, abort_code):
    # Do initial validations on required headers
    checkHeaders(request.headers, abort_code)
    if not request.is_json:
        abort(abort_code)

    event = request.headers.get('X-GitHub-Event')
    if event == "ping":
        return False, json.dumps({'msg': 'Hi!'})
    if event != "push":
        return False, json.dumps({'msg': "Wrong event type"})

    x_hub_signature = request.headers.get('X-Hub-Signature')
    # webhook content type should be application/json for request.data to have the payload
    # request.data is empty in case of x-www-form-urlencoded
    if not is_valid_signature(
            x_hub_signature,
            request.data,
            current_app.config['W_SECRET']):
        print('Deploy signature failed: {sig}'.format(sig=x_hub_signature))
        abort(abort_code)

    return True


def update(request, abort_code):
    payload = request.get_json()
    if payload is None:
        print('Deploy payload is empty: {payload}'.format(
            payload=payload))
        abort(abort_code)

    if payload['ref'] != 'refs/heads/production':
        return json.dumps({'msg': 'Not production; ignoring'})

    import sys
    project_home = '/home/Jacrac04/PythonDataStore/PythonDataStoreServer'
    if project_home not in sys.path:
        sys.path = [project_home] + sys.path
    repo = git.Repo(project_home)

    origin = repo.remotes.origin

    pull_info = origin.pull()

    if len(pull_info) == 0:
        return json.dumps(
            {'msg': "Didn't pull any information from remote!"})
    if pull_info[0].flags > 128:
        return json.dumps(
            {'msg': "Didn't pull any information from remote!"})

    commit_hash = pull_info[0].commit.hexsha
    build_commit = f'build_commit = "{commit_hash}"'
    print(f'{build_commit}')
    return 'Updated PythonAnywhere server to commit {commit}'.format(
        commit=commit_hash) + '\n' + build_commit


@gitUpdate.route('/update_source', methods=['GET', 'POST'])
def webhook():
    if request.method != 'POST':
        return 'OK'
    else:
        abort_code = 418
        # Do initial validations on required headers
        # checkHeaders(request.headers, abort_code)

        success, msg = checks(request, abort_code)
        if not success:
            return msg

    return update(request, abort_code)
