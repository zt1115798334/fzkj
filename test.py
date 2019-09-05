from fzkj_login import selenium_login


def main():
    cookies = selenium_login("175015218", "19980508")
    print(cookies)


if __name__ == '__main__':
    main()
