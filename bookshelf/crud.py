# Copyright 2015 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from bookshelf import get_model
from flask import Blueprint, redirect, render_template, request, url_for
import pymysql

crud = Blueprint('crud', __name__)


# [START list]
@crud.route("/")
def list():
    token = request.args.get('page_token', None)
    if token:
        token = token.encode('utf-8')

    books, next_page_token = get_model().list(cursor=token)

    connect = pymysql.connect(host='localhost', user='root', password='passw0rd', db='bookshelf', charset='utf8mb4')
    cur = connect.cursor()
    query = "SELECT * FROM realtime ORDER BY realTimeID DESC"
    datas = cur.execute(query)
    connect.commit()
    datas = cur.fetchmany(size=1)

    return render_template(
        "list.html",
        books=books,
        next_page_token=next_page_token,
        realtime = datas)
# [END list]


@crud.route('/<id>')
def view(id):
    book = get_model().read(id)
    return render_template("view.html", book=book)


# [START add]
@crud.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        data = request.form.to_dict(flat=True)

        book = get_model().create(data)

        return redirect(url_for('.view', id=book['id']))

    return render_template("form.html", action="Add", book={})
# [END add]


@crud.route('/<id>/edit', methods=['GET', 'POST'])
def edit(id):
    book = get_model().read(id)

    if request.method == 'POST':
        data = request.form.to_dict(flat=True)

        book = get_model().update(data, id)

        return redirect(url_for('.view', id=book['id']))

    return render_template("form.html", action="Edit", book=book)


@crud.route('/<id>/delete')
def delete(id):
    get_model().delete(id)
    return redirect(url_for('.list'))

@crud.route('/titlesearch/')
def searchbytitle():
    title = request.args.get('title')
    token = request.args.get('page_token', None)
    if token:
        token = token.encode('utf-8')
    books, next_page_token = get_model().searchbytitle(title, cursor=token)
    return render_template("list.html", books=books, next_page_token=next_page_token)

@crud.route('/authorsearch/')
def searchbyauthor():
    author = request.args.get('author')
    token = request.args.get('page_token', None)
    if token:
        token = token.encode('utf-8')
    books, next_page_token = get_model().searchbyauthor(author, cursor=token)
    return render_template("list.html", books=books, next_page_token=next_page_token)
    