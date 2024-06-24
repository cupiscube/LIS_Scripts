# import WorksWPNames
# import ResultFormulas
# import Norms


print("""Script by Danil Batrakov""")


def main_menu():
    while True:
        print("""
        *** Главное меню ***
        
        1 - Изменение названия рабочего места в [] в работах по названию РМ
        2 - Починка формул в результатах по наименованию рабочего места
        3 - Скопировать нормы с одного РМ на другое
        
        0 - Выход из приложения
        
        """)
        doing = input("Выберете неоходимый пункт меню: ")
        try:
            doing_ = int(doing)
            if doing_ == 1:
                import WorksWPNames
                print(WorksWPNames.change_wp_name())
            elif doing_ == 2:
                import ResultFormulas
                print(ResultFormulas.fix_formulas())
            elif doing_ == 3:
                import Norms
                print(Norms.copy_norms())
            elif doing_ == 0:
                break

            else:
                print("Выберете значение из списка!")

        except:
            print("Выберете значение из списка!")


if __name__ == '__main__':
    main_menu()


