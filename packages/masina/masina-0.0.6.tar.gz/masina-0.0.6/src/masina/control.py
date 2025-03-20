from datetime import date
import os
import auto

compName = os.getenv('COMPUTERNAME')

def get_auto_vals(ini_file, selectedStartDate, selectedEndDate):
    car = auto.Masina(ini_file)
    alimentari = car.get_alimentari_for_interval_type(selectedStartDate, selectedEndDate, None)
    for i in alimentari:
        print(i)
    print(car.table_totals)


def main():
    selectedStartDate = date(2021, 12, 30)
    selectedEndDate = date(2024, 1, 29)

    # masina_ini = r"C:\_Development\Diverse\pypi\cfgm.ini"
    # # masina_ini = r"C:\_Development\Diverse\pypi\cfgmRN.ini"
    if compName == 'DESKTOP-5HHINGF':
        ini_file = r"D:\Python\MySQL\cheltuieli.ini"
    else:
        ini_file = r"C:\_Development\Diverse\pypi\cfgm.ini"


    user = auto.Users(None, ini_file)
    # # print(users.all_users)
    # user = auto.Users('radu', ini_file)
    # print('user.masini', user.masini)
    # user.add_car('hyundai', 'ioniq', 'aa')
    # print('user.masini', user.export_profile())
    # src_file = r"C:\_Development\Diverse\pypi\radu\masina\bkp_profile\2024_07_26__14_14_23_radu.zip"
    # print(user.import_profile_with_files(src_file))

    # car = auto.Masina(masina_ini)
    user.erase_traces()

    # get_auto_vals(masina_ini, selectedStartDate, selectedEndDate)
    # car = auto.Masina(masina_ini)
    # print(car.electric_providers)


if __name__ == '__main__':
    main()
