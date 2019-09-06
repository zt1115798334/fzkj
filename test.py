from fzkj_login import selenium_login


def main():
    cookies = selenium_login("19013122", "Wy17637987113.")
    print(cookies)


if __name__ == '__main__':
    main()
