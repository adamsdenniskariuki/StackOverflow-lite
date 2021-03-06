"""
This module defines the questions model and associated functions
"""
from datetime import datetime, timedelta

# local imports
from .... import init_db
from .base_model import BaseModel

class QuestionModel(BaseModel):
    """This class encapsulates the functions of the question model"""
    def __init__(self, user_id=0, text="text", description="desc"):
        """initialize the question model"""
        self.user_id = user_id
        self.text = text
        self.description = description
        self.date_created = datetime.now()
        self.db = init_db()

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

    def get_all(self):
        """This function returns a list of all the questions"""
        dbconn = self.db
        curr = dbconn.cursor()
        curr.execute("""SELECT * FROM questions;""")
        data = curr.fetchall()
        self.close_db()
        resp = []
        
        for i, items in enumerate(data):
            question_id, user_id, text, description, date = items
            question = dict(
               question_id=int(question_id),
               user_id=int(user_id),
               text=text,
               description=description,
               date_created=date
            )
            resp.append(question)
        return resp
    