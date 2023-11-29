import psycopg2
import psycopg2.extras
from dotenv import load_dotenv
import os

load_dotenv()

conn = None

try:
    with psycopg2.connect(
        host=os.getenv('host'),
        database=os.getenv('database'),
        user=os.getenv('user'),
        password=os.getenv('password'),
        port=os.getenv('port') ) as conn:

        with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:

            cur.execute('DROP TABLE IF EXISTS employee')

            create_table = ''' CREATE TABLE IF NOT EXISTS employee (
                                    id int PRIMARY KEY,
                                    name varchar(40) NOT NULL,
                                    salary int,
                                    dept_id varchar(255) )'''

            cur.execute(create_table)

            insert_script = 'INSERT INTO employee (id, name, salary, dept_id) VALUES (%s, %s, %s, %s)'

            insert_values = [(1, 'Prem', 50000, 'AI'), (2, 'Radhe', 60000, 'ML'), (3, 'Kabir', 70000, 'DL')]

            for record in insert_values:
                cur.execute(insert_script, record)

            update_script = '''UPDATE employee 
                            SET salary = salary+(salary*0.05)
                            WHERE salary <= 55000''' 
            
            cur.execute(update_script)

            delete_script = 'DELETE FROM employee WHERE name= %s'

            cur.execute(delete_script, ('Kabir', ))

            cur.execute('SELECT * FROM employee')
            records = cur.fetchall()
            for record in records:
                print(record)
                print(record['name'], record['salary'])

except Exception as error:
    print(error)

finally:
    if conn is not None:
        conn.close()
