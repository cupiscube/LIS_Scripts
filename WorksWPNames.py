from Connect import DBConnect


def change_wp_name():
    wp_name = input("Введите название рабочего места: ")

    # Get work by WP
    select_wp = f"""
    select w."text" work_name,
           w.id,
           w.shorttext
    from lab.work as w,
         lab.workplace as wp
    where wp."text" = '{wp_name}'
        and w.workplace_id = wp.id
    """

    connection = DBConnect.connect
    cursor = connection.cursor()

    cursor.execute(select_wp)
    wp = cursor.fetchall()
    wp = [list(tuple_) for tuple_ in wp]
    # works = [w[0] for w in wp]

    # Fix WP names
    new_works_name = []
    for i in range(len(wp)):
        # work = work_[0]
        # find left brekits
        current_left_bracket = wp[i][0].find('[') + 1
        # current_left_bracket = 0
        # next_left_brekit = 0
        # left_brekits = []
        # print(work)
        # while next_left_brekit != -1:
        #     next_left_brekit = work[current_left_bracket+1::].find('[')
        #     if next_left_brekit != -1:
        #         current_left_bracket += next_left_brekit + 1
        #         left_brekits.append(current_left_bracket)
        # print(left_brekits)
        # find the last right brekit
        # current_right_brekit = work_[0][::].rfind(']')
        wp[i][0] = wp[i][0][:current_left_bracket:] + wp_name + ']'
        # new_works_name.append([new_work, work_[1]])

        current_left_bracket = wp[i][2].find('[') + 1
        wp[i][2] = wp[i][2][:current_left_bracket:] + wp_name + ']'


    # Update values
    cursor = connection.cursor()
    for n_work in wp:
        table_modification = f"""UPDATE lab.work as w SET text = '{str(n_work[0])}', shorttext = '{str(n_work[2])}' WHERE id = {n_work[1]};"""
        # print(table_modification)
        try:
            cursor.execute(table_modification)
            connection.commit()
        except:
            print('Except!')
            cursor.execute("ROLLBACK")
            connection.commit()

    cursor.close()
    connection.close()
    return "Успех!"


if __name__ == '__main__':
    change_wp_name()
    print('Скрипт закончил работу! \nВсе изменения применены, обратного пути нет!')
