from selenium import webdriver
from time import sleep
import argparse
from argparse import RawTextHelpFormatter
from write_data import perform


def update_dashboard():
    print('updating dashboard scripts')
    perform()
    print('done with the dashboard')


def main(latest_only:bool, N: int):

    till = ''
    if latest_only:
        with open('data.csv', 'r') as f:
            till = f.readlines()[0]
            N = 1

    print(till)

    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--ignore-ssl-errors')
    options.add_argument('headless')

    driver = webdriver.Chrome('./chromedriver', options=options)

    driver.get('https://selfcare.actcorp.in/group/blr/myaccount')
    print('url opened')
    sleep(5)

    driver.find_element_by_xpath('//*[@id="_ACTMyAccount_WAR_ACTMyAccountportlet_:j_idt35:j_idt43"]/span[2]').click()
    print('going to usage section...')

    sleep(10)

    open_btn = driver.find_element_by_xpath('//*[@id="_ACTMyAccount_WAR_ACTMyAccountportlet_:j_idt310:j_idt319"]')
    select_box = driver.find_element_by_xpath('//*[@id="_ACTMyAccount_WAR_ACTMyAccountportlet_:j_idt310:month"]')

    done = False

    with open('data.csv', 'w') as f:
        count = 0
        for option in select_box.find_elements_by_css_selector('option')[::-1][N - 3:-1]:
            if option.text == 'Select Month':
                continue
            option.click()
            open_btn.click()
            print(f'selected option {option.text}')
            sleep(5)
            table = driver.find_element_by_xpath('//*[@id="_ACTMyAccount_WAR_ACTMyAccountportlet_:j_idt310:j_idt328"]')
            print('table located...')

            for row in table.find_elements_by_css_selector('tr.rf-dt-r'):
                data_string = ''
                for col in row.find_elements_by_css_selector('td'):
                    data_string += col.text + ","
                if data_string[:-1] == till:
                    done = True
                    break
                f.write(data_string[:-1] + '\n')
                count += 1

            if done:
                break

            print(f'{count} rows written')
    f.close()

    driver.close()
    driver.quit()

    update_dashboard()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Analyze your internet usage", epilog=" ", formatter_class=RawTextHelpFormatter)
    parser.add_argument('--update-only', action="store_true", help="Upate only latest entries.", default=False)
    parser.add_argument('N', help="the last N months of data needed.\nCan be 1, 2 or 3.(Default 3)\nNote: This value will not affect the program if --update-only is used", nargs='?', default=3)
    
    args = parser.parse_args()
    
    main(args.update_only, int(args.N))
    