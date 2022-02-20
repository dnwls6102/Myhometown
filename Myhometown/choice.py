from flask import Flask, render_template, redirect, request, url_for
app = Flask(__name__)
import datas
import random

def showresult(x,y):
    if x > y:
        return "정답!"
    else:
        return "오답"

def pick_another_one(x,y):
    while True:
        a = random.choice(list(datas.count.keys()))
        if a == x or a == y:
            continue
        return a

def getvalue(x):
    return datas.count.get(x)

def pickone():
    return random.sample(list(datas.count.keys()), 2)

#temp = []
@app.route('/')
def make_choice():
    #global temp
    temp = datas.pickone()
    FirstOneValue = datas.count[temp[0]]
    SecondOneValue = datas.count[temp[1]]
    Fresult = showresult(FirstOneValue, SecondOneValue)
    Sresult = showresult(SecondOneValue, FirstOneValue)
    dic = datas.count

    return render_template('main.html', First = temp[0], Second = temp[1],
                           Fresult = Fresult, Sresult = Sresult,
                           FOV = FirstOneValue, SOV = SecondOneValue,
                           pickAnotherOne = pick_another_one, getValue = getvalue,
                           showResult = showresult, dic = dic)


@app.route('/result')
def render_result():
    return render_template('result.html')

@app.route('/test')
def render_test():
    dic = datas.count

    return render_template('test.html', dic = dic)

if __name__ == '__main__':
    app.run(debug=True)