from flask import Flask, render_template, request, redirect, url_for, session, flash 
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import timedelta
from functools import wraps
from flask_migrate import Migrate
import os
import requests


app = Flask(__name__, template_folder='assets', static_folder='assets', static_url_path='/assets')
app.secret_key = 'your_secret_key' 

app.permanent_session_lifetime = timedelta(minutes=30)

def send_log(message):
    try:
        requests.post('http://log:6000/log', json={'message': message})
    except:
        pass  

@app.before_request
def log_request():
    path_messages = {
        '/': '\nHome 페이지 접속\n',
        '/about-us': '\nAbout this portal 페이지 접속\n',
        '/services': '\nServices 페이지 접속\n',
        '/contact': '\nInformation 페이지 접속\n',
        '/login': '\nLogin 페이지 접속\n',
        '/register': '\nRegister 페이지 접속\n',
        '/survey': '\nSurvey 페이지 접속\n',
        '/result': '\nResult 페이지 접속\n',
    }
    message = path_messages.get(request.path)

    if message:
        send_log(message)
    else:
        send_log(f"접속: {request.path}")


instance_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'instance')
os.makedirs(instance_path, exist_ok=True)
app.instance_path = instance_path

db_path = os.path.join(app.instance_path, 'database.db')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

questions = [
    {
        'text': '하루에 일회용 플라스틱을 몇 개 사용하나요?',
        'options': ['0개', '1개', '2개', '3개', '4개 이상'],
        'weight': 5
    },
    {
        'text': '하루에 고기를 몇 끼 섭취하나요?',
        'options': ['0끼니', '1끼니', '2끼니', '3끼니', '4끼니 이상'],
        'weight': 4
    },
    {
        'text': '하루 평균 전기 사용량(kWh)은 얼마나 되나요?',
        'options': ['0-5kWh', '6-10kWh', '11-15kWh', '16-20kWh', '21kWh 이상'],
        'weight': 5
    },
    {
        'text': '일주일에 자동차로 몇 km 이동하나요?',
        'options': ['0km', '1-50km', '51-100km', '101-200km', '201km 이상'],
        'weight': 4
    },
    {
        'text': '하루에 물을 몇 리터 사용하나요?',
        'options': ['0-50L', '51-100L', '101-150L', '151-200L', '201L 이상'],
        'weight': 3
    },
    {
        'text': '일주일에 대중교통을 몇 회 이용하나요?',
        'options': ['7회 이상', '5-6회', '3-4회', '1-2회', '0회'],
        'weight': 3
    },
    {
        'text': '일주일에 재활용을 얼마나 자주 하나요?',
        'options': ['매일', '주 4-6회', '주 2-3회', '주 1회', '전혀 하지 않음'],
        'weight': 4
    },
    {
        'text': '한 달에 구매하는 의류 개수는 얼마인가요?',
        'options': ['0개', '1개', '2개', '3개', '4개 이상'],
        'weight': 3
    },
    {
        'text': '하루에 육류 외의 단백질을 몇 번 섭취하나요?',
        'options': ['4회 이상', '3회', '2회', '1회', '0회'],
        'weight': 2
    },
    {
        'text': '일주일에 외식을 몇 번 하나요?',
        'options': ['0회', '1회', '2회', '3회', '4회 이상'],
        'weight': 2
    },
    {
        'text': '하루에 종이 타월을 몇 장 사용하나요?',
        'options': ['0장', '1-2장', '3-4장', '5-6장', '7장 이상'],
        'weight': 2
    },
    {
        'text': '한 달에 항공편을 이용한 횟수는 얼마인가요?',
        'options': ['0회', '1회', '2회', '3회', '4회 이상'],
        'weight': 5
    },
    {
        'text': '하루 음식물 쓰레기량은 얼마나 되나요?',
        'options': ['0g', '1-100g', '101-200g', '201-300g', '301g 이상'],
        'weight': 4
    },
    {
        'text': '샤워를 평균적으로 얼마나 하나요?',
        'options': ['0-5분', '6-10분', '11-15분', '16-20분', '21분 이상'],
        'weight': 3
    },
    {
        'text': '하루에 전자 기기를 몇 시간 사용하나요?',
        'options': ['0-2시간', '3-4시간', '5-6시간', '7-8시간', '9시간 이상'],
        'weight': 3
    },
    {
        'text': '일주일에 자전거를 몇 회 이용하나요?',
        'options': ['7회 이상', '5-6회', '3-4회', '1-2회', '0회'],
        'weight': 2
    },
    {
        'text': '한 달에 지역 농산물을 몇 번 구매하나요?',
        'options': ['10회 이상', '7-9회', '4-6회', '1-3회', '0회'],
        'weight': 3
    },
    {
        'text': '하루에 커피 테이크아웃 컵을 몇 개 사용하나요?',
        'options': ['0개', '1개', '2개', '3개', '4개 이상'],
        'weight': 3
    },
    {
        'text': '일주일에 친환경 제품을 몇 번 구매하나요?',
        'options': ['7회 이상', '5-6회', '3-4회', '1-2회', '0회'],
        'weight': 2
    },
    {
        'text': '하루에 이메일을 몇 통 보내나요?',
        'options': ['0-10통', '11-20통', '21-30통', '31-40통', '41통 이상'],
        'weight': 1
    },
    {
        'text': '한 달에 온라인 쇼핑을 몇 회 하나요?',
        'options': ['0회', '1-2회', '3-4회', '5-6회', '7회 이상'],
        'weight': 3
    },
    {
        'text': '일주일에 조깅이나 걷기를 몇 회 하나요?',
        'options': ['7회 이상', '5-6회', '3-4회', '1-2회', '0회'],
        'weight': 2
    },
    {
        'text': '하루에 냉난방 기기를 몇 시간 사용하나요?',
        'options': ['0시간', '1-2시간', '3-4시간', '5-6시간', '7시간 이상'],
        'weight': 4
    },
    {
        'text': '한 달에 새 전자제품을 몇 번 구매하나요?',
        'options': ['0회', '1회', '2회', '3회', '4회 이상'],
        'weight': 4
    },
    {
        'text': '일주일에 종이 프린트를 몇 장 하나요?',
        'options': ['0장', '1-10장', '11-20장', '21-30장', '31장 이상'],
        'weight': 2
    },
    {
        'text': '일주일에 재사용 가능한 가방을 몇 회 사용하나요?',
        'options': ['7회 이상', '5-6회', '3-4회', '1-2회', '0회'],
        'weight': 3
    },
    {
        'text': '하루에 식수 이외의 음료를 몇 잔 섭취하나요?',
        'options': ['0잔', '1-2잔', '3-4잔', '5-6잔', '7잔 이상'],
        'weight': 1
    },
    {
        'text': '일주일에 사용하시는 세제의 양은 얼마나 되나요? (ml)',
        'options': ['0-50ml', '51-100ml', '101-150ml', '151-200ml', '201ml 이상'],
        'weight': 2
    },
    {
        'text': '일주일에 옷을 세탁하는 횟수는 몇 회인가요?',
        'options': ['0회', '1회', '2회', '3회', '4회 이상'],
        'weight': 2
    },
    {
        'text': '텔레비전 시청 시간은 하루에 몇 시간 인가요?',
        'options': ['0시간', '1-2시간', '3-4시간', '5-6시간', '7시간 이상'],
        'weight': 2
    },
]


custom_solutions = {
    0: {
        'solution': "일회용 플라스틱 사용을 줄이고 재사용 가능한 제품을 사용하세요.",
        'explanation': "플라스틱 폐기물은 해양 생태계를 위협하고, 분해에 수백 년이 걸립니다. 재사용 가능한 제품을 사용하면 폐기물 감소에 큰 도움이 됩니다."
    },
    1: {
        'solution': "고기 섭취를 줄이고 식물성 단백질을 섭취해보세요.",
        'explanation': "축산업은 전 세계 온실가스 배출의 약 14.5%를 차지합니다. 고기 소비를 줄이면 탄소 발자국을 크게 줄일 수 있습니다."
    },
    2: {
        'solution': "에너지 효율적인 가전제품을 사용하고 불필요한 전기 사용을 줄이세요.",
        'explanation': "전기 사용량을 줄이면 탄소 배출을 감소시키고 에너지 비용을 절약할 수 있습니다. LED 전구와 고효율 가전을 사용해보세요."
    },
    3: {
        'solution': "대중교통이나 자전거, 도보를 이용하여 이동 거리를 줄이세요.",
        'explanation': "교통수단은 전 세계 탄소 배출의 약 24%를 차지합니다. 친환경 교통수단을 이용하면 환경 보호에 큰 도움이 됩니다."
    },
    4: {
        'solution': "물을 절약하기 위해 샤워 시간을 줄이고 절수형 기기를 사용하세요.",
        'explanation': "물 부족은 심각한 글로벌 문제입니다. 물 사용량을 줄이면 수자원 보호에 기여할 수 있습니다."
    },
    5: {
        'solution': "대중교통 이용을 늘려 탄소 배출을 줄이세요.",
        'explanation': "대중교통은 개인 차량보다 탄소 배출이 적습니다. 일주일에 한 번만 더 이용해도 환경에 긍정적인 영향을 미칩니다."
    },
    6: {
        'solution': "재활용 분리수거를 철저히 하여 폐기물을 줄이세요.",
        'explanation': "재활용은 자원 절약과 에너지 소비 감소에 기여합니다. 올바른 재활용은 환경 보호에 중요합니다."
    },
    7: {
        'solution': "유행하는 옷 구매를 줄이고 품질 좋은 옷을 오래 입으세요.",
        'explanation': "패스트패션 산업은 환경 오염의 주요 원인 중 하나입니다. 지속 가능한 패션을 선택하세요."
    },
    8: {
        'solution': "식물성 단백질 섭취를 늘려보세요.",
        'explanation': "식물성 단백질은 탄소 발자국이 낮습니다. 건강에도 도움이 됩니다."
    },
    9: {
        'solution': "외식 횟수를 줄이고 집에서 식사를 준비하세요.",
        'explanation': "외식은 포장재와 음식물 쓰레기를 증가시킵니다. 집밥은 건강에도 좋습니다."
    },
    10: {
        'solution': "종이 타월 대신 천으로 된 행주를 사용하세요.",
        'explanation': "종이 사용을 줄이면 산림 보호에 기여합니다. 재사용 가능한 행주는 쓰레기를 줄입니다."
    },
    11: {
        'solution': "항공 여행을 줄이고 다른 교통수단을 고려하세요.",
        'explanation': "항공기는 탄소 배출량이 높습니다. 가능한 경우 기차나 버스를 이용하세요."
    },
    12: {
        'solution': "음식물 쓰레기를 줄이고 필요한 만큼만 소비하세요.",
        'explanation': "음식물 쓰레기는 메탄 가스를 배출합니다. 계획적인 식단은 낭비를 줄입니다."
    },
    13: {
        'solution': "샤워 시간을 줄이고 물 사용량을 관리하세요.",
        'explanation': "샤워 시간을 1분 줄이면 연간 수백 리터의 물을 절약할 수 있습니다."
    },
    14: {
        'solution': "전자 기기 사용 시간을 관리하고 에너지 절약 모드를 사용하세요.",
        'explanation': "전자 기기는 대기 전력도 소비합니다. 사용하지 않을 때는 전원을 꺼주세요."
    },
    15: {
        'solution': "자전거 이용을 늘려 건강과 환경을 모두 지키세요.",
        'explanation': "자전거는 탄소 배출이 없고 운동에도 좋습니다. 가까운 거리는 자전거를 이용하세요."
    },
    16: {
        'solution': "지역 농산물을 구매하여 탄소 발자국을 줄이세요.",
        'explanation': "장거리 운송은 탄소 배출을 증가시킵니다. 지역 제품은 신선하고 환경에도 좋습니다."
    },
    17: {
        'solution': "개인 컵을 사용하여 일회용 컵 사용을 줄이세요.",
        'explanation': "일회용 컵은 연간 수십 억 개가 버려집니다. 개인 컵 사용은 쓰레기를 줄입니다."
    },
    18: {
        'solution': "친환경 제품을 적극적으로 구매하세요.",
        'explanation': "친환경 제품은 환경에 덜 해롭습니다. 수요가 늘면 공급도 늘어납니다."
    },
    19: {
        'solution': "불필요한 이메일을 삭제하여 에너지 소비를 줄이세요.",
        'explanation': "데이터 저장은 전기를 소비합니다. 이메일 정리는 작은 실천입니다."
    },
    20: {
        'solution': "온라인 쇼핑 횟수를 줄이고 한 번에 구매하세요.",
        'explanation': "배송 횟수를 줄이면 탄소 배출을 감소시킵니다. 필요한 것을 한 번에 구매하세요."
    },
    21: {
        'solution': "걷기나 조깅을 늘려 건강과 환경을 지키세요.",
        'explanation': "운동은 건강에 좋고, 교통수단 이용을 줄여 환경에도 좋습니다."
    },
    22: {
        'solution': "냉난방 온도를 적정 수준으로 유지하세요.",
        'explanation': "1도만 낮춰도 에너지 소비를 크게 줄일 수 있습니다. 적정 온도를 유지하세요."
    },
    23: {
        'solution': "전자제품 구매를 자제하고 필요한 경우 중고품을 고려하세요.",
        'explanation': "전자 폐기물은 환경에 해롭습니다. 재사용을 통해 폐기물을 줄이세요."
    },
    24: {
        'solution': "디지털 문서를 활용하여 종이 사용을 줄이세요.",
        'explanation': "종이 생산은 많은 자원을 소모합니다. 전자 문서는 편리하고 친환경적입니다."
    },
    25: {
        'solution': "재사용 가능한 가방을 항상 휴대하여 사용하세요.",
        'explanation': "비닐봉투 사용을 줄이면 해양 오염을 감소시킬 수 있습니다."
    },
    26: {
        'solution': "음료 소비를 줄이고 물을 더 많이 마셔보세요.",
        'explanation': "음료 생산은 많은 자원을 소비합니다. 물은 건강에도 이롭습니다."
    },
    27: {
        'solution': "세제 사용량을 줄이고 친환경 세제를 사용하세요.",
        'explanation': "세제는 수질 오염의 원인입니다. 친환경 세제는 환경 영향을 줄입니다."
    },
    28: {
        'solution': "세탁 횟수를 주 2회 이하로 줄이고 세탁물을 모아서 하세요.",
        'explanation': "세탁은 물과 에너지를 많이 소비합니다. 효율적인 세탁은 자원 절약에 도움이 됩니다."
    },
    29: {
        'solution': "텔레비전 시청 시간을 하루에 몇 시간 이하로 줄였나요?",
        'explanation': "에너지 소비를 줄이고 더 많은 활동적인 시간을 보낼 수 있습니다."
    },
}

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    survey_completed = db.Column(db.Boolean, default=False)
    survey_response = db.relationship('SurveyResponse', backref='user', uselist=False)

class SurveyResponse(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    responses = db.Column(db.PickleType, nullable=False)
    score = db.Column(db.Float, nullable=False)  

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            flash('로그인이 필요합니다.', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.context_processor
def inject_user():
    if 'username' in session:
        user = User.query.filter_by(username=session['username']).first()
        return dict(current_user=user)
    return dict(current_user=None)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about-us')
def about_us():
    return render_template('about-us.html')

@app.route('/services')
def services():
    return render_template('services.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/gallery')
def gallery():
    return render_template('gallery.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            session.permanent = True 
            session['username'] = user.username
            flash('로그인에 성공했습니다.', 'success')
            return redirect(url_for('index')) 
        else:
            error = '잘못된 자격 증명입니다. 다시 시도해주세요.'
    return render_template('login.html', error=error)

@app.route('/register', methods=['GET', 'POST'])
def register():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if not username or not password:
            error = '사용자명과 비밀번호를 모두 입력해주세요.'
        elif User.query.filter_by(username=username).first():
            error = '이미 존재하는 사용자명입니다.'
        else:
            hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
            new_user = User(username=username, password=hashed_password)
            db.session.add(new_user)
            db.session.commit()
            session.permanent = True
            session['username'] = new_user.username
            flash('회원가입에 성공했습니다.', 'success')
            return redirect(url_for('index')) 
    return render_template('register.html', error=error)

@app.route('/survey', methods=['GET', 'POST'])
@login_required
def survey():
    user = User.query.filter_by(username=session['username']).first()
    if user.survey_completed:
        flash('이미 설문에 참여하셨습니다.', 'info')
        return redirect(url_for('result'))

    if request.method == 'POST':
        responses = {}
        total_score = 0
        max_score = 5 * len(questions)
        for idx in range(len(questions)):
            q_key = f'q{idx}'
            score = request.form.get(q_key)
            if score is None:
                flash('모든 질문에 답변해주세요.', 'warning')
                return redirect(url_for('survey'))
            try:
                score = int(score)
                if score < 1 or score > 5:
                    raise ValueError
            except ValueError:
                flash('유효한 값값를 선택해주세요.', 'warning')
                return redirect(url_for('survey'))
            responses[q_key] = score
            total_score += score

        environment_index = round((total_score / max_score) * 100, 2)

        survey_response = SurveyResponse(user_id=user.id, responses=responses, score=environment_index)
        user.survey_completed = True
        db.session.add(survey_response)
        db.session.commit()
        flash('설문 기록이 저장되었습니다.', 'success')
        return redirect(url_for('result'))

    enumerated_questions = list(enumerate(questions))
    return render_template('survey.html', questions=enumerated_questions)

def generate_solutions(responses):
    solutions = []
    for q_key, score in responses.items():
        idx = int(q_key[1:])
        if score > 3:
            solution_data = custom_solutions.get(idx)
            if solution_data:
                solutions.append({'question_index': idx, 'solution': solution_data})
    return solutions

@app.route('/result')
@login_required
def result():
    user = User.query.filter_by(username=session['username']).first()
    if not user.survey_completed:
        flash('먼저 설문에 참여해주세요.', 'info')
        return redirect(url_for('survey'))

    user_response = SurveyResponse.query.filter_by(user_id=user.id).first()
    all_responses = SurveyResponse.query.all()
    user_score = user_response.score

    scores = [response.score for response in all_responses if response.score is not None]
    higher_scores = len([score for score in scores if score > user_score])
    percentile = round((1 - (higher_scores / len(scores))) * 100, 2) if scores else 0

    solutions = generate_solutions(user_response.responses)

    all_responses_formatted = [
        {'username': response.user.username, 'score': response.score}
        for response in all_responses
    ]

    return render_template(
        'result.html',
        user_score=user_score,
        percentile=percentile,
        solutions=solutions,
        all_responses=all_responses_formatted,
        questions=questions,
        custom_solutions=custom_solutions  
    )

@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('로그아웃되었습니다.', 'success')
    return redirect(url_for('index'))

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def server_error(e):
    return render_template('500.html'), 500

@app.route('/reset_survey', methods=['POST'])
@login_required
def reset_survey():
    user = User.query.filter_by(username=session['username']).first()
    if user.survey_completed:
        survey_response = SurveyResponse.query.filter_by(user_id=user.id).first()
        if survey_response:
            db.session.delete(survey_response)
        user.survey_completed = False
        db.session.commit()
        flash('설문이 초기화되었습니다. 다시 설문에 참여할 수 있습니다.', 'success')
    else:
        flash('설문이 이미 초기화되었습니다.', 'info')
    return redirect(url_for('survey'))

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
