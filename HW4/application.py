import psycopg2
from flask import Flask, request, make_response, render_template, url_for, redirect, flash
from werkzeug.exceptions import abort

app = Flask(__name__, template_folder="templates")


def connect_db():
	connection = psycopg2.connect(
		host='localhost',
		database='CRUD',
		user='postgres',
		password='BARSIKETOZLO'
	)
	return connection


def form_valid(form):
	"""
	Function for form validation
	Args:
		form (dict):
	Returns:
		bool: True if all is ok
	"""
	return all(map(len, form.values()))


def get_product(pid):
	con = connect_db()
	cur = con.cursor()
	cur.execute("SELECT * FROM products WHERE id = %s", (pid,))
	data = cur.fetchone()
	cur.close()
	con.close()
	if data is None:
		abort(404)
	return data


@app.route('/')
@app.route('/products')
def products():
	con = connect_db()
	cur = con.cursor()
	cur.execute("SELECT * FROM products")
	data = cur.fetchall()
	cur.close()
	con.close()
	return render_template("products.html", products=data)


@app.route('/product/create', methods=['GET', 'POST'])
def product_create():
	if request.method == 'POST':
		if form_valid(request.form):
			name = request.form.get('name')
			description = request.form.get('description')
			price = request.form.get('price')

			con = connect_db()
			cur = con.cursor()

			cur.execute("INSERT INTO products (name, description, price) VALUES (%s, %s, %s)", (
				name,
				description,
				price))

			con.commit()
			con.close()
			return redirect(url_for('products'))

	return render_template('product_create.html')


@app.route('/product/<int:pid>/edit', methods=['GET', 'POST'])
def product_edit(pid):
	product = get_product(pid)

	if request.method == 'POST':
		if form_valid(request.form):
			name = request.form.get('name')
			description = request.form.get('description')
			price = request.form.get('price')

			con = connect_db()
			cur = con.cursor()

			cur.execute("UPDATE products SET name = %s, description = %s, price = %s WHERE id = %s", (
				name,
				description,
				price,
				pid))

			con.commit()
			con.close()
			return redirect(url_for('products'))
	return render_template('product_edit.html', product=product)


@app.route('/product/<int:pid>/delete', methods=['GET', 'POST'])
def product_delete(pid):
	product = get_product(pid)
	if request.method == 'POST':
		if request.form.get('not_delete'):
			return redirect(url_for('products'))
		con = connect_db()
		cur = con.cursor()
		cur.execute('DELETE FROM products WHERE id = %s', (pid,))
		con.commit()
		cur.close()
		con.close()
		return redirect(url_for('products'))
	return render_template('product_delete.html')

# @app.route("/")
# def index():
# 	res = make_response()
#
# 	if "color" in request.cookies:
# 		color = request.cookies.get('color')
# 	else:
# 		color = "#ddd"
# 		res.set_cookie("color", color)
# 		print("set cookie")
#
# 	content = render_template("index.html", color=color)
# 	res.data = content
#
# 	return res
#
# def form_valid(form):
# 	"""
# 	Function for form validation
# 	Args:
# 		form (dict):
# 	Returns:
# 		bool: True if all is ok
# 	"""
# 	return all(map(len, form.values()))
#
# @app.route("/product", methods=['GET', 'POST'])
# def product_123():
# 	connection = sqlite3.connect('sqlite3.db')
# 	connection.row_factory = sqlite3.Row
#
# 	if request.method == "POST":
# 		if form_valid(request.form):
# 			cur = connection.cursor()
# 			sql_command = "insert into products (name, description, price) VALUES (?, ?, ?)"
#
# 			name = request.form.get('name')
# 			description = request.form.get('description')
# 			price = int(request.form.get('price'))
#
# 			data = (name, description, price)
# 			cur.execute(sql_command, data)
# 			connection.commit()
#
# 			response = redirect(url_for('product_123'))
# 			return response
#
# 	products = connection.execute('SELECT * FROM products').fetchall()
#
# 	connection.close()
#
# 	return render_template("create.html", products=products)


if __name__ == "__main__":
	app.run(host='127.0.0.1', port=5000, debug=True)
