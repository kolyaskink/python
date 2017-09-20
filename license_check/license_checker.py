import requests


def get_config():
    """ Parse config file
        and save data as a dictionary
    """

    with open('config.txt') as f:
        settings={}
        for line in f:
            line = line.strip()
            settings[(line.split('=')[0])]=(line.split('=')[1])
        return settings


def web_call(get_config):
    """ Get response from URL
        and save if for future interaction
    """

    if get_config['ssl']=='yes':
        protocol='https'
    elif get_config['ssl']=='no':
        protocol='http'
    else:
        print("SSL value could be only 'yes' or 'no'")
        return "ERROR"

    url=protocol + "://" + get_config['hostname'] + "/" + get_config['url']

    response_code = requests.get(url, auth=(get_config['user'], get_config['pass'])).status_code
    return (response_code)

def main():
    """ Check status of Zuora endpoint
        This function checks GH API, which communicates with Zuora website to check
        if it's working properly
    """

    print(web_call(get_config()))

main()