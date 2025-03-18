from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////home/esraarslan/quizapp-flask/quiz.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    last_score = db.Column(db.Integer, default=0)
    highest_score = db.Column(db.Integer, default=0)

questions = [
    {"question": "Question 1: discord.py kütüphanesinde bir botun mesajlara yanıt vermesi için hangi olay (event) kullanılır?", "options": ["on_message()", "on_reaction_add()", "on_ready()", "on_member_join()"], "answer": "on_message()"},
    {"question": "Question 2: Flask uygulamasında, kullanıcının gönderdiği form verilerini almak için hangi metot kullanılır?", "options": ["request.get_data()", "request.input_data()", "request.form.get()", "request.retrieve_form()"], "answer": "request.form.get()"},
    {"question": "Question 3: TensorFlow ve PyTorch gibi kütüphaneler en çok hangi amaç için kullanılır?", "options": ["Web Geliştirme", "Makine Öğrenimi ve Derin Öğrenme", "Veri Tabanı Yönetimi", "Kriptografi"], "answer": "Makine Öğrenimi ve Derin Öğrenme"},
    {"question": "Question 4: OpenCV kütüphanesinde bir görüntüyü gri tonlamalı hale getirmek için hangi fonksiyon kullanılır?", "options": ["cv2.imread()", "cv2.cvtColor()", "cv2.threshold()", "cv2.resize()"], "answer": "cv2.cvtColor()"},
    {"question": "Question 5: NLTK kütüphanesinde kelime köklerini bulmak için kullanılan algoritma hangisidir?", "options": ["Lemmatization", "Tokenization", "Stemming", "POS tagging"], "answer": "Stemming"}
]

def get_highest_score():
    highest = db.session.query(db.func.max(User.highest_score)).scalar()
    return highest if highest else 0

@app.route("/")
@app.route("/quiz")
def quiz():
    user = User.query.first()
    if not user:
        user = User(name="Anonim", last_score=0, highest_score=0)
        db.session.add(user)
        db.session.commit()
    
    return render_template(
        "quiz.html", 
        questions=enumerate(questions), 
        user=user, 
        highest_score=get_highest_score(), 
        footer_text="Neslihan Bükte tarafından geliştirildi. Tüm hakları saklıdır."
    )

@app.route("/submit", methods=["POST"])
def submit():
    username = request.form.get("username")
    if not username:
        return redirect(url_for("quiz"))

    user = User.query.filter_by(name=username).first()
    
    if not user:
        user = User(name=username, last_score=0, highest_score=0)
        db.session.add(user)

    score = sum(1 for i, q in enumerate(questions) if request.form.get(f"question_{i}") == q["answer"])

    user.last_score = score
    if score > user.highest_score:
        user.highest_score = score
    
    db.session.commit()
    
    highest_scorer = User.query.order_by(User.highest_score.desc()).first()
    highest_scorer_name = highest_scorer.name if highest_scorer else "Bilinmiyor"

    return render_template(
        "score.html", 
        user=user, 
        highest_score=get_highest_score(), 
        highest_scorer=highest_scorer_name, 
        footer_text="Neslihan Bükte tarafından geliştirildi. Tüm hakları saklıdır."
    )

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
