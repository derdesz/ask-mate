from typing import List, Dict

from psycopg2 import sql
from psycopg2.extras import RealDictCursor

import database

"""
QUESTIONS
"""

@database.connection_handler
def get_all_question(cursor: RealDictCursor) -> list:
    cursor.execute("select * from question order by submission_time desc")
    return cursor.fetchall()

@database.connection_handler
def get_current_question(cursor: RealDictCursor, q_id) -> list:
    cursor.execute("select * from question where id = '%s' " % q_id)
    return cursor.fetchall()

@database.connection_handler
def add_question(cursor: RealDictCursor, q_id, submission_time, title, message) -> list:
    cursor.execute("insert into question values('%s', '%s', 0, 0, '%s', '%s') " % (q_id, submission_time, title, message))

@database.connection_handler
def edit_question(cursor: RealDictCursor, time, header, q_id, message) -> list:
    cursor.execute("update question set title = '%s', message = '%s', submission_time = '%s' where id = '%s' " % (header, message, time, q_id))

@database.connection_handler
def sort_questions(cursor: RealDictCursor, header, way) -> list:
    cursor.execute("select * from question order by {} {} ".format(header, way))
    return cursor.fetchall()

@database.connection_handler
def delete_question(cursor: RealDictCursor, q_id) -> list:
    cursor.execute("delete from question where id = '%s' " % q_id)
    cursor.execute("delete from answer where question_id = '%s' " % q_id)





"""
ANSWERS
"""


@database.connection_handler
def add_answer(cursor: RealDictCursor, q_id, a_id, submission_time, message) -> list:
    cursor.execute("insert into answer values('%s', '%s', 0, '%s', '%s') " % (a_id, submission_time, q_id, message))


@database.connection_handler
def get_all_answer(cursor: RealDictCursor, q_id) -> list:
    cursor.execute("select * from answer where question_id = '%s' " % q_id)
    return cursor.fetchall()


@database.connection_handler
def get_current_answer(cursor: RealDictCursor, a_id) -> list:
    cursor.execute("select * from answer where id = '%s' " % a_id)
    return cursor.fetchall()

@database.connection_handler
def delete_answer(cursor: RealDictCursor, a_id) -> list:
    cursor.execute("delete from comment where answer_id = '%s' " % a_id)
    cursor.execute("delete from answer where id = '%s' " % a_id)


@database.connection_handler
def edit_answer(cursor: RealDictCursor, a_id, message) -> list:
    cursor.execute("update answer set message = '%s' where id = '%s' " % (message, a_id))

@database.connection_handler
def questionID_by_answerID(cursor: RealDictCursor, a_id) -> list:
    cursor.execute("select * from answer where id = '%s'" % a_id)
    return cursor.fetchall()

"""
IMAGE
"""


@database.connection_handler
def add_image(cursor: RealDictCursor, header, filename, q_id, time) -> list:
    cursor.execute("update {} set image = '%s', submission_time = '%s' where id = '%s' ".format(header) % (filename, time, q_id))


"""
VOTE
"""

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



"""
COMMENT
"""
@database.connection_handler
def get_comment(cursor: RealDictCursor, id_type, id ) -> list:
    cursor.execute("select * from comment where {} = '%s' ".format(id_type) % id)
    return cursor.fetchall()

@database.connection_handler
def get_current_comment(cursor: RealDictCursor, id) -> list:
    cursor.execute("select * from comment where id = '%s' " % id)
    return cursor.fetchall()

@database.connection_handler
def get_all_comment(cursor: RealDictCursor) -> list:
    cursor.execute("select * from comment")
    return cursor.fetchall()

@database.connection_handler
def add_question_comment(cursor: RealDictCursor, own_id, question_id, message, time, ) -> list:
    cursor.execute("insert into comment values('%s', '%s', NULL, '%s', '%s',  0) " % (own_id, question_id, message, time))

@database.connection_handler
def add_answer_comment(cursor: RealDictCursor, own_id, answer_id, message, time, ) -> list:
    cursor.execute("insert into comment values('%s', NULL, '%s',  '%s', '%s',  0) " % (own_id, answer_id, message, time))

@database.connection_handler
def edit_comment(cursor: RealDictCursor, message, time, comment_id) -> list:
    cursor.execute("update comment set message = '%s', submission_time = '%s', edited_count = edited_count + 1 where id = '%s'" % (message, time, comment_id))


@database.connection_handler
def delete_comment(cursor: RealDictCursor, comment_id) -> list:
    cursor.execute("DELETE FROM comment WHERE id = '%s'" % comment_id)


"""
TAGS
"""
@database.connection_handler
def get_all_tags(cursor: RealDictCursor) -> list:
    cursor.execute("SELECT * FROM tag")
    return cursor.fetchall()


@database.connection_handler
def add_tag(cursor: RealDictCursor, tag_id, tag) -> list:
    cursor.execute("INSERT INTO tag VALUES ('%s', '%s')" % (tag_id, tag))


@database.connection_handler
def add_to_question_tag(cursor: RealDictCursor, q_id, tag_id) -> list:
    cursor.execute("INSERT INTO question_tag VALUES ('%s', '%s')" % (q_id, tag_id))

@database.connection_handler
def tagID_by_tagNAME(cursor: RealDictCursor, name) -> list:
    cursor.execute("SELECT id FROM tag WHERE name = '%s' " % name)
    return cursor.fetchall()


@database.connection_handler
def get_tag_for_question(cursor: RealDictCursor, q_id) -> list:
    cursor.execute("SELECT * FROM tag INNER JOIN question_tag ON tag.id = question_tag.tag_id WHERE question_id = '%s' " % q_id)
    return cursor.fetchall()


@database.connection_handler
def delete_question_tag(cursor: RealDictCursor, q_id, tag_id) -> list:
    cursor.execute("DELETE FROM question_tag WHERE tag_id = '%s' and question_id = '%s'" % (tag_id, q_id))

"""
SEARCH
"""

@database.connection_handler
def searched_phrase_q(cursor: RealDictCursor, search_phrase) -> list:
    cursor.execute("SELECT * FROM question WHERE message LIKE '%{}%' or title LIKE '%{}%' ".format(search_phrase, search_phrase))
    return cursor.fetchall()

@database.connection_handler
def searched_phrase_a(cursor: RealDictCursor, search_phrase) -> list:
    cursor.execute("SELECT * FROM answer WHERE message LIKE '%{}%' ".format(search_phrase))
    return cursor.fetchall()


@database.connection_handler
def get_last_5_questions(cursor: RealDictCursor) -> list:
    cursor.execute("select message, submission_time from question order by submission_time DESC limit 5")
    return cursor.fetchall()

"""
USER
"""

@database.connection_handler
def get_max_user_id(cursor: RealDictCursor) -> list:
    cursor.execute("select MAX(user_id) from user_datas")
    max_id = cursor.fetchall()[0]['max']
    return max_id


@database.connection_handler
def add_user(cursor: RealDictCursor, id, name, password, date) -> list:
    cursor.execute("INSERT INTO user_datas VALUES ('%s', '%s', '%s', '%s')" % (id, name, password, date))


@database.connection_handler
def get_usernames(cursor: RealDictCursor) -> list:
    cursor.execute("select username from user_datas")
    all_datas = cursor.fetchall()
    list_of_datas = [row['username'] for row in all_datas]
    return list_of_datas


@database.connection_handler
def get_hash_password(cursor: RealDictCursor, username) -> list:
    cursor.execute("select password from user_datas where username = '%s' " % username)
    pw = cursor.fetchall()[0]['password']
    return pw