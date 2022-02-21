from flask import Flask, render_template, redirect, request, url_for
app = Flask(__name__)
import datas
import random

@app.route('/')
def make_choice():
    dic = datas.count

    return render_template('main.html', dic = dic)


@app.route('/result')
def render_result():
    return render_template('result.html')

@app.route('/test')
def render_test():
    dic = datas.count

    return render_template('test.html', dic = dic)

if __name__ == '__main__':
    app.run(debug=True)