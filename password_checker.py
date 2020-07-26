import hashlib
import sys
import requests


def check_response(res, tail):
    hash_res = res.text.splitlines()
    hash = (lines.split(':') for lines in hash_res)
    for h, count in hash:
        if h == tail:
            return count
    return 0


def check_api_for_pwnedpassword(head, tail):
    url = 'https://api.pwnedpasswords.com/range/' + head
    res = requests.get(url)
    if res.status_code != 200:
        raise RuntimeError(
            f'Error fetching: {res.status_code}, check the api and try again')
    else:
        count = check_response(res, tail)
        return count


def main(password):
    sha1 = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    head = sha1[:5]
    tail = sha1[5:]
    count = check_api_for_pwnedpassword(head, tail)
    if count:
        print(
            f'the password {password} was found {count} times.. Please change it..')
    else:
        print(f'the password {password} was not found..')


if __name__ == '__main__':
    password = input('Enter the password you want to check \n')
    main(password)
