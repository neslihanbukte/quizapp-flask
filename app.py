from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///quiz.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
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

    return render_template("score.html", user=user, highest_score=get_highest_score(), highest_scorer=highest_scorer_name, footer_text="Neslihan Bükte tarafından geliştirildi. Tüm hakları saklıdır.")


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)



