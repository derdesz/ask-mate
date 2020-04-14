from typing import List, Dict

from psycopg2 import sql
from psycopg2.extras import RealDictCursor

import database



@database.connection_handler
def get_all_question(cursor: RealDictCursor) -> list:
    cursor.execute("select * from question order by submission_time desc")
    return cursor.fetchall()


@database.connection_handler
def get_current_question(cursor: RealDictCursor, q_id) -> list:
    cursor.execute("select * from question where id = '%s' " % q_id)
    return cursor.fetchall()

@database.connection_handler
def get_current_answer(cursor: RealDictCursor, q_id) -> list:
    cursor.execute("select * from answer where question_id = '%s' " % q_id)
    return cursor.fetchall()

@database.connection_handler
def add_question(cursor: RealDictCursor, q_id, submission_time, title, message) -> list:
    cursor.execute("insert into question values('%s', '%s', 0, 0, '%s', '%s') " % (q_id, submission_time, title, message))


@database.connection_handler
def add_image(cursor: RealDictCursor, header, filename, q_id, time) -> list:
    cursor.execute("update {} set image = '%s', submission_time = '%s' where id = '%s' ".format(header) % (filename, time, q_id))

@database.connection_handler
def edit_question(cursor: RealDictCursor, header, q_id, message) -> list:
    cursor.execute("update question set title = '%s', message = '%s' where id = '%s' " % (header, message, q_id))


@database.connection_handler
def add_answer(cursor: RealDictCursor, q_id, a_id, submission_time, message) -> list:
    cursor.execute("insert into answer values('%s', '%s', 0, '%s', '%s') " % (a_id, submission_time, q_id, message))



@database.connection_handler
def sort_questions(cursor: RealDictCursor, header, way) -> list:
    cursor.execute("select * from question order by {} {} ".format(header, way))
    return cursor.fetchall()


@database.connection_handler
def delete_question(cursor: RealDictCursor, q_id) -> list:
    cursor.execute("delete from question where id = '%s' " % q_id)
    cursor.execute("delete from answer where question_id = '%s' " % q_id)

@database.connection_handler
def delete_answer(cursor: RealDictCursor, a_id) -> list:
    cursor.execute("delete from answer where id = '%s' " % a_id)

@database.connection_handler
def vote_question_up(cursor: RealDictCursor, q_id) -> list:
    cursor.execute("update question set vote_number = vote_number + 1 where id = '%s' " % q_id)

@database.connection_handler
def vote_question_down(cursor: RealDictCursor, q_id) -> list:
    cursor.execute("update question set vote_number = vote_number - 1 where id = '%s' " % q_id)


@database.connection_handler
def vote_answer_up(cursor: RealDictCursor, a_id) -> list:
    cursor.execute("update answer set vote_number = vote_number + 1 where id = '%s' " % a_id)

@database.connection_handler
def vote_answer_down(cursor: RealDictCursor, a_id) -> list:
    cursor.execute("update answer set vote_number = vote_number - 1 where id = '%s' " % a_id)