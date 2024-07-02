from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
db = SQLAlchemy()

class Author(db.Model):
    __tablename__ = 'authors'
    
    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String, unique=True, nullable=False)
    phone_number = db.Column(db.String(10))
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())
    # Add validators 
    @validates('name')
    def validate_name(self,key,name):
        if not name :
            raise ValueError("Name must be a unique non-empty string!")
        elif Author.query.filter_by(name=name).first():
            raise ValueError("Name must be a unique string!")
        return name
    @validates('phone_number')
    def validate_phone_number(self,key,number):
        #isdigits() returns True if all characters are digits and False if otherwise
        if not number.isdigit() or len(number)!=10:
            raise ValueError("Author's phone number must consist of 10 numbers")
        return number
    def __repr__(self):
        return f'Author(id={self.id}, name={self.name})'
   

class Post(db.Model):
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String)
    category = db.Column(db.String)
    summary = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Add validators  
    @validates('content')
    def validate_content(self,key,content):
        if len(content)< 250:
            raise ValueError("A post's content should at least have 250 characters!")
        return content
    @validates('summary')
    def validate_summary(self,key,summary):
        if len(summary) > 250:
            raise ValueError("A post's summary should at least have 250 characters!")
        return summary
    @validates('category')
    def validate_category(self,key,category):
        if category!='Fiction' and category!='Non-Fiction' :
            raise ValueError("A post's category should be Fiction or Non-Fiction!")
        return category
    @validates('title')
    def validate_title(self,key,title):
        clickbait_phrases=["Won't Believe","Secret","Top","Guess"]
        if not any(phrase in title for phrase in clickbait_phrases):
            raise ValueError("Invalid Post Title!")
        return title

    def __repr__(self):
        return f'Post(id={self.id}, title={self.title} content={self.content}, summary={self.summary})'
