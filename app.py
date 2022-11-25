from db import *

from flask import Flask, render_template, request, flash, redirect, url_for, abort, render_template_string

from flask_paginate import Pagination, get_page_args


app = Flask(__name__)
app.config['SECRET_KEY'] = "48xL(QDcN*t&GbB@"


length = 10

#login screen
@app.route("/admin", methods=['GET', 'POST'])
def home():
    return render_template("index.html")


#authentication
@app.route('/auth', methods=['GET', 'POST'])
def authentication():
    if request.method == 'POST':
        user = request.form.get('login')
        password = request.form.get('password')
        if user == 'admin' and password == 'admin':
            return redirect('panel')
        else:
            flash("Login ou Senha incorretos")
            return render_template("index.html")
            



#panel
@app.route('/panel', methods=['GET', 'POST'])
def get_panel(records = ''):
    if records == '':
        records = get_all_records()
    def get_records(offset=0, per_page=10):
        return records[offset: offset+per_page]
    page, per_page, offset = get_page_args(page_parameter="page", per_page_parameter="per_page")
    total = len(records)
    pagination_records = get_records(offset=offset, per_page=per_page)
    pagination = Pagination(page=page, per_page=per_page, total=total, css_framework='bootstrap4')
    return render_template("panel.html", records=pagination_records,
                                        page=page,
                                        per_page=per_page,
                                        pagination=pagination)

#add new product
@app.route('/add_product', methods=['POST', 'GET'])
def add_product():
    return render_template("product.html")

@app.route('/product_added', methods=['POST'])
def save_product():
    if request.method == 'POST':
        name = request.form.get('name_product')
        manufacture = request.form.get('manufacture')
        serial = request.form.get('serial')
        status = request.form.get('status')
        print(name, manufacture, serial, status)

        new_product(name=name, manufacturers_id=manufacture, serial=serial, states_id=status)

        flash(f"{name} adicionado com sucesso.")
        return redirect('add_product')


#page edit product
@app.route('/edit_product', methods=['POST', 'GET'])
def edit_product():
    if request.method == 'POST':
        id = request.form.get('id')
        print(id)

        product = get_product(id)
        return render_template("product_edit.html",
                                id = id,
                                name_product = product[0][2],
                                manufacture = product[0][15],
                                serial = product[0][9],
                                status = product[0][22])


@app.route('/product_edited', methods=['POST'])
def update_product():
    if request.method == 'POST':
        id = request.form.get('id')
        name = request.form.get('name_product')
        manufacture = request.form.get('manufacture')
        serial = request.form.get('serial')
        status = request.form.get('status')
        print(name, manufacture, serial, status)

        update_product_sql(id=id, name=name, manufacturers_id=manufacture, serial=serial, states_id=status)

        flash(f"{name} atualizado com sucesso.")
        return render_template('product_edit.html', name_product=name, manufacture=manufacture, serial=serial)

@app.route('/product_deleted', methods=['POST', 'GET'])
def del_product():
    if request.method == 'POST':
        id = request.form.get('id')
        product = get_product(id)
        delete_product(id)
        flash(f"{product[0][2]} Deletado com sucesso.")
        return render_template("product_edit.html",
                                id = id,
                                name_product = product[0][2],
                                manufacture = product[0][15],
                                serial = product[0][9],
                                status = product[0][22])


search = ''

@app.route('/search_product', methods=['GET', 'POST'])
def search_product():
    if request.method == 'POST':
        global search
        product = request.form.get('search')
        search = search_records(product)

    return get_panel(search)

        
if __name__ == "__main__":
    app.run(debug=True)
