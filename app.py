from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///quiz.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    last_score = db.Column(db.Integer, default=0)
    highest_score = db.Column(db.Integer, default=0)

questions = [
    {"question": " Question 1: Bir Gün Kaç Saniyedir?", "options": ["86000", "88600", "86400", "84800"], "answer": "86400"},
    {"question": "Question 2: 'Sinekli Bakkal' Romanının Yazarı Kimdir?", "options": ["Reşat Nuri Güntekin", "Halide Edip Adıvar", "Ziya Gökalp", "Ömer Seyfettin"], "answer": "Halide Edip Adıvar"},
    {"question": "Question 3: Altının kimyasal sembolü nedir?", "options": ["Au", "He", "Li", "Be"], "answer": "Au"},
    {"question": "Question 4: 'Yıldızlı Gece' adlı sanat başyapıtını hangi sanatçı çizmiştir?", "options": ["Vincent van Gogh", "Claude Monet", "Salvador Dali", "Frida Kahlo"], "answer": "Vincent van Gogh"},
    {"question": "Questin 5: 2003 yılında Eurovision Şarkı Yarışması'nda Türkiye'yi temsil eden ve birinci olan sanatçımız kimdir?", "options": ["Grup Athena", "Sertap Erener", "Şebnem Paker", "Ajda Pekkan"], "answer": "Sertap Erener"}
]

def get_highest_score():
    highest = db.session.query(db.func.max(User.highest_score)).scalar()
    return highest if highest else 0

@app.route("/")
@app.route("/quiz")
def quiz():
    user = User.query.first()
    if not user:
        user = User()
        db.session.add(user)
        db.session.commit()
    return render_template("quiz.html", questions=enumerate(questions), user=user, highest_score=get_highest_score(), footer_text="Neslihan Bükte tarafından geliştirildi. Tüm hakları saklıdır.")

@app.route("/submit", methods=["POST"])
def submit():
    user = User.query.first()
    if not user:
        user = User()
        db.session.add(user)
    
    score = 0
    for i, q in enumerate(questions):
        selected_answer = request.form.get(f"question_{i}")
        if selected_answer == q["answer"]:
            score += 1
    
    user.last_score = score
    if score > user.highest_score:
        user.highest_score = score
    db.session.commit()
    
    return render_template("score.html", user=user, highest_score=get_highest_score(), footer_text="Neslihan Bükte tarafından geliştirildi. Tüm hakları saklıdır.")

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)



