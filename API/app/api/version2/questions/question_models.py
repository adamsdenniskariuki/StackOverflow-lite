"""
This module defines the questions model and associated functions
"""
from datetime import datetime, timedelta

from .... import init_db, create_app

class QuestionModel(object):

    def __init__(self, user_id=0, text="text", description="desc"):
        """initialize the question model"""
        self.user_id = user_id
        self.text = text
        self.description = description
        self.date_created = datetime.now()
        self.db = init_db()

    def get_questions_by_user_id(self, user_id=0):
        """return a list of all the questions with the id given"""
        if not user_id:
            user_id = self.user_id
        database = self.db
        curr = database.cursor()
        curr.execute(
            """SELECT * FROM questions WHERE user_id = %d;""" % (user_id))
        data = curr.fetchall()
        curr.close()
        # return a list of tuples
        return data

    def save_question(self):
        """Add question details to the database"""
        question = {
            "user_id": self.user_id,
            "text": self.text,
            "description": self.description
        }
        database = self.db
        curr = database.cursor()
        query = """INSERT INTO questions VALUES (nextval('increment_pkey'), %(user_id)s, %(text)s,\
                %(description)s, ('now')) RETURNING question_id;"""
        curr.execute(query, question)
        question_id = curr.fetchone()[0]
        database.commit()
        curr.close()
        return int(question_id)
  
    def delete_question(self, question_id):
        """This function takes in a question id and removes it from the database"""
        try:
            dbconn = self.db
            curr = dbconn.cursor()
            query = "DELETE FROM questions WHERE question_id = %d;" % (int(question_id))
            curr.execute(query)
            curr.close()
            dbconn.commit()
        except Exception as e:
            return "Not Found"
        pass

    def close_db(self):
        """This function closes the database"""
        self.db.close()
        pass