from Connect import DBConnect
from decimal import Decimal


def copy_norms():
    work_place_current = input('Введите название ИСХОДНОГО рабочего места С которого копируем нормы: ')
    work_place_target = input('Введите название ЦЕЛЕВОГО рабочего места НА которое копируем нормы: ')
    work = input("Введите название работы на исходном РМ (если пропустить то сопоставятся все нормы): ")

    select_wp_c = f"""
    select w."text" work_name
    from lab.work as w,
    	 lab.workplace as wp
    where wp."text" = '{work_place_current}'
        and w.workplace_id = wp.id
        {f"and w.text = '{work}'" if work != '' else ''}
    """
    connection = DBConnect.connect
    cursor = connection.cursor()

    cursor.execute(select_wp_c)
    wp_c = cursor.fetchall()
    cursor.close()
    # Get works name without [{wp name}]
    works_c = [w[0][:w[0].find('[') - 1] for w in wp_c]

    for work_c in works_c:
        select_norm_c = f"""
        select wr.text wresul_name,
               wrv.text,
        	   n.*
        from lab.work as w,
        	 lab.workplace as wp,
        	 lab.workresult as wr,
        	 lab.workresult_value as wrv,
        	 lab.norm as n
        where wp."text" = '{work_place_current}'
            and w.workplace_id = wp.id
            {f"and w.text = '{work}'" if work != '' else ''}
            and w.text like '{work_c}%'
        	and wr.work_id = w.id
        	and wrv.workresult_id = wr.id
        	and n.workresult_value_id = wrv.id
        """
        cursor = connection.cursor()
        cursor.execute(select_norm_c)
        work_c_results = cursor.fetchall()
        cursor.close()
        # Get works name without [{wp name}]
        results_c = [list(w) for w in work_c_results]

        for result in results_c:
            # fix data types
            for i in range(len(result)):
                if result[i] is None:
                    result[i] = 'null'
                elif isinstance(result[i], Decimal):
                    result[i] == float(result[i])

            select_wrv_id_t = f"""
            select wrv.id
            from lab.work as w,
            	 lab.workplace as wp,
            	 lab.workresult as wr,
            	 lab.workresult_value as wrv
            where wp."text" = '{work_place_target}'
                and w.workplace_id = wp.id
            	and w.text like '{work_c}%'
            	and wr.text = '{result[0]}'
            	and wrv.text = '{result[1]}'
            	and wr.work_id = w.id
            	and wrv.workresult_id = wr.id
            """
            cursor = connection.cursor()
            cursor.execute(select_wrv_id_t)
            result_t_id = cursor.fetchall()
            cursor.close()

            # Insert correct new workresult_value_id
            try:
                result[-3] = int(result_t_id[0][0])
                # Delete all norms on target result
                delete_select = f"""
                            delete
                            from lab.norm as n
                            using (select wrv.id
                            		from lab.work as w,
                            			 lab.workplace as wp,
                            			 lab.workresult as wr,
                            			 lab.workresult_value as wrv
                            		where wp."text" = '{work_place_target}'
                            			and w.workplace_id = wp.id
                            			and w.text like '{work_c}%'
                            			and wr.text = '{result[0]}'
                            			and wrv.text = '{result[1]}'
                            			and wr.work_id = w.id
                            			and wrv.workresult_id = wr.id) as wrv 
                            where n.workresult_value_id = wrv.id
                            """
                cursor = connection.cursor()
                cursor.execute(delete_select)
                # updated_row_count = cursor.rowcount
                # test_select = f'select * from lab.norm where id = {result[0]}'

                connection.commit()
                # result_t_id = cursor.fetchall()
                cursor.close()

                # Add norms from current WP
                insert_select = f"""
                            insert into lab.norm
                                        (
                                	id,
                                	createby,
                                	createdate,
                                	updateby,
                                	updatedate,
                                	code_sets_id,
                                	norm_group_id,
                                	norm,
                                	norm_low,
                                	norm_high,
                                	pathologic,
                                	pathologic_low,
                                	pathologic_high,
                                	critical,
                                	critical_low,
                                	critical_high,
                                	workresult_value_id,
                                	note,
                                	norm_text
                                			  )
                        	   values ((select max(id) + 1 from lab.norm),
                        			  {result[3]},
                        			  current_timestamp,
                        			  {result[5]},
                        			  current_timestamp,
                        			  {result[7]},
                        			  {result[8]},
                        			  {result[9]},
                        			  {result[10]},
                        			  {result[11]},
                        			  {result[12]},
                        			  {result[13]},
                        			  {result[14]},
                        			  {result[15]},
                        			  {result[16]},
                        			  {result[17]},
                        			  {result[18]},
                        			  {result[19]},
                        			  '{result[20]}')
                            """
                cursor = connection.cursor()
                cursor.execute(insert_select)
                # updated_row_count = cursor.rowcount
                connection.commit()
                cursor.close()
            except IndexError:
                result[-3] = 'null'
                print(f'Внимание! Необновлены нормы в {result[0]}, {result[1]}')
                cursor.close()


    cursor.close()
    connection.close()
    return "Успех!"


if __name__ == '__main__':
    copy_norms()
    print('Скрипт закончил работу! \nВсе изменения применены, обратного пути нет!')
