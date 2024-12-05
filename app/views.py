from flask import render_template, flash, redirect, url_for, request, session
from flask_admin.contrib.sqla import ModelView
from flask_login import login_user, LoginManager, login_required, logout_user, current_user
from app import app, db, models, admin, bcrypt
from .forms import SignUpForm, LoginForm, CheckoutForm, EditForm, PasswordForm, SearchForm
from .models import Customer, Lego
import json

admin.add_view(ModelView(Customer, db.session))
admin.add_view(ModelView(Lego, db.session))

categories = ['Architecture', 'Art', 'BOOST', 'Batman', 
              'Brick Sketches', 'BrickHeadz', 'City', 'Classic', 
              'Creator 3-in-1', 'Creator Expert', 'DC', 'DIMENSIONS', 
              'DOTS', 'DUPLO', 'Disney', 'Elves', 'Fortnite', 'Friends', 
              'Frozen', 'Harry Potter', 'Home', 'Ideas', 'Jurassic World', 
              'LEGO Avatar', 'LEGO DREAMZzz', 'LEGO Education', 
              "LEGO Gabby's Dollhouse", 'LEGO Icons', 'LEGO Sonic the Hedgehog', 
              'LEGO Super Mario', 'LEGO Wednesday Sets', 'Lord of the Rings', 
              'Marvel', 'Minecraft', 'Minifigures', 'Minions', 'Monkie Kid', 
              'NEXO KNIGHTS', 'NINJAGO', 'Overwatch', 'Powered UP', 
              'Speed Champions', 'Spider-Man', 'Star Wars', 'THE LEGO BATMAN MOVIE', 
              'THE LEGO MOVIE 2', 'Technic', 'The Botanical Collection', 
              'VIDIYO ', 'Wicked', 'Other']

ages = ['1½+','2+','3+','4+','5+','6+', '7+', '8+', 
        '9+', '10+', '12+', '14+', '16+', '18+',]

app.app_context().push()

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(customer_id):
        return Customer.query.get(int(customer_id))

'''this code is repeated below in a function 
 however, to improve performance i have made the all lists outside of it 
 as this will not change, whereas if someone is shopping by category or age
 it will be different and for each one'''
names_list = []
main_urls = []
legos = models.Lego.query.all()
names = db.session.query(models.Lego.product_name).all()
urls = db.session.query(models.Lego.image_urls).all()
for i in range(len(urls)-1):
        url_list = urls[i][0].split(',')
        main_urls.append(url_list[0])

for i in range(len(names)-1):
        names_list.append(names[i][0])

def namesAndUrls(column, shopby):
        shopby_names_list = []
        shopby_main_urls = []
        if column == 'age':
                names = db.session.query(models.Lego.product_name).filter_by(age_range=shopby).all()
                urls = db.session.query(models.Lego.image_urls).filter_by(age_range=shopby).all()
        elif column == 'category':
                names = db.session.query(models.Lego.product_name).filter_by(category=shopby).all()
                urls = db.session.query(models.Lego.image_urls).filter_by(category=shopby).all()

        for i in range(len(urls)-1):
                url_list = urls[i][0].split(',')
                shopby_main_urls.append(url_list[0])

        for i in range(len(names)-1):
                shopby_names_list.append(names[i][0])

        return shopby_names_list, shopby_main_urls

@app.route('/', methods=['GET', 'POST'])
def All():
        return render_template('shop.html', title='Shop All', 
                           legos=legos, names_list=names_list, 
                           main_urls=main_urls, categories=categories,
                           ages=ages)

@app.route('/ShopBy/<string:shopby>', methods=['GET', 'POST'])
def ShopBy(shopby):
        if '+' in shopby:
                legos = models.Lego.query.filter_by(age_range=shopby).all()
                shopby_names_list, shopby_main_urls = namesAndUrls('age', shopby)
        else:
                legos = models.Lego.query.filter_by(category=shopby).all()
                shopby_names_list, shopby_main_urls = namesAndUrls('category', shopby)
        return render_template('shop.html', title=shopby, 
                              legos=legos, names_list=shopby_names_list, 
                                main_urls=shopby_main_urls, categories=categories,
                                ages=ages)

@app.route('/search', methods=['GET', 'POST'])
def Search():
        form = SearchForm()
        if form.validate_on_submit():
                search = "%{}%".format(form.search.data)
                
                legos = db.session.query(Lego).filter(Lego.product_name.like(search)).all()
                items = []
                for lego in legos:
                        items.append(lego.id)

                # make lists for displaying
                searched_names = []
                searched_urls = []

                for item in items:
                        product = models.Lego.query.get(item)
                        searched_names.append(product.product_name)
                        urls = product.image_urls.split(',')
                        searched_urls.append(urls[0])
                return render_template('search.html', title='Search', form=form, legos=legos, names_list=searched_names, 
                                main_urls=searched_urls)
        
        return render_template('search.html', form=form)

@app.route('/Details/<string:productId>', methods=['GET', 'POST'])
def Details(productId):
        product = models.Lego.query.get(productId)
        urls = product.image_urls
        images = urls.split(',')
        return render_template('details.html', product=product, bigImg=images[0], title=product.product_name, images=images, 
                               categories=categories, ages=ages)

@app.route('/sign_up', methods=['GET', 'POST'])
def Sign_up():
        form = SignUpForm()
        if form.validate_on_submit():
                hash = bcrypt.generate_password_hash(form.password.data)
                customers = db.session.query(models.Customer.email).filter_by(email=form.email.data).all()
                if not customers:
                        new_customer = Customer(firstname=form.firstname.data, surname=form.surname.data, email=form.email.data, password=hash)
                        db.session.add(new_customer)
                        db.session.commit()
                        flash("User successfully registered.")
                        return redirect(url_for('Login'))
                else:
                        flash("User with that email already exists!")
        return render_template('sign_up.html', title='Sign up', form=form)

@app.route('/login', methods=['GET', 'POST'])
def Login():
        form = LoginForm()
        if form.validate_on_submit():
                customer = Customer.query.filter_by(email=form.email.data).first()
                if customer:
                        if bcrypt.check_password_hash(customer.password, form.password.data):
                                login_user(customer)
                                return redirect(url_for('Account'))
                        else:
                                flash("Incorrect password")
        return render_template('login.html', title='Login', form=form)

@app.route('/account', methods=['GET', 'POST'])
@login_required
def Account():
        return render_template('account.html')

@app.route('/logout', methods=['GET', 'POST'])
@login_required
def Logout():
        logout_user()
        return redirect(url_for('Login'))

@app.route('/addtobasket', methods=['GET', 'POST'])
def AddToBasket():
        data = json.loads(request.data)
        product_id = int(data.get('product_id'))
        product = models.Lego.query.get(product_id)
        if product.stock_quantity > 1:
                # if this throws an error then basket is empty and session variable needs to be first created
                try:
                        if session['basket'] != "":
                                session['basket'] = session['basket'] + ',' + str(product_id)
                        else:
                                raise Exception("basket already created.")
                except:
                        session['basket'] = str(product_id)

        return json.dumps({'status': 'OK', 'added': product_id})

@app.route('/basket', methods=['GET', 'POST'])
def Basket():
        try:
                # sort basket into list
                string_items = session['basket'].split(',')
                items = []
                for item in string_items:
                        items.append(int(item))

                # make lists for displaying
                basket_names_list = []
                basket_main_urls = []

                for item in items:
                        product = models.Lego.query.get(item)
                        basket_names_list.append(product.product_name)
                        urls = product.image_urls.split(',')
                        basket_main_urls.append(urls[0])
                
                return render_template('basket.html', title='Basket', names=basket_names_list, urls=basket_main_urls, items=items)
        except:
                return render_template('basket.html', title='Basket Empty')

@app.route('/deletefrombasket/<int:productId>', methods=['GET', 'POST'])
def DeleteFromBasket(productId):
        string_items = session['basket'].split(',')
        items = []
        for item in string_items:
                items.append(int(item))

        items.remove(productId)

        session['basket'] = ""
        for item in items:
                if session['basket']:
                        session['basket'] = session['basket'] + ',' + str(item)
                else:
                        session['basket'] = str(item)
        
        return redirect(url_for('Basket'))

@app.route('/checkout', methods=['GET', 'POST'])
def Checkout():
        form = CheckoutForm()
        if form.validate_on_submit():
                string_items = session['basket'].split(',')
                items = []
                for item in string_items:
                        items.append(int(item))

                for item in items:
                        product = models.Lego.query.get(item)
                        if product.stock_quantity > 0:
                                product.stock_quantity -= 1
                                db.session.commit()
                        else:
                                flash("An item became out of stock.")
                                return render_template('checkout.html', title='Checkout', form=form)
                flash("Thank you for your order!")
                session['basket'] = ""
        return render_template('checkout.html', title='Checkout', form=form)

@app.route('/thankyou', methods=['GET', 'POST'])
def Thankyou():
        return render_template('thankyou.html', legos=legos, names_list=names_list, 
                                main_urls=main_urls, categories=categories,
                                ages=ages)

@app.route('/addtowishlist/<int:productId>/<int:customerId>', methods=['GET', 'POST'])
def AddToWishlist(productId, customerId):
        customer = models.Customer.query.get(customerId)
        product = models.Lego.query.get(productId)
        customer.legos.append(product)
        db.session.commit()

        urls = product.image_urls
        images = urls.split(',')
        return render_template('details.html', product=product, bigImg=images[0], title=product.product_name, images=images, 
                               categories=categories, ages=ages)

@app.route('/wishlist', methods=['GET', 'POST'])
@login_required
def Wishlist():
        if current_user.legos:
                items = []
                for lego in current_user.legos:
                        items.append(lego.id)

                # make lists for displaying
                wishlist_names = []
                wishlist_urls = []

                for item in items:
                        product = models.Lego.query.get(item)
                        wishlist_names.append(product.product_name)
                        urls = product.image_urls.split(',')
                        wishlist_urls.append(urls[0])
                return render_template('wishlist.html', title='Wishlist', names=wishlist_names, urls=wishlist_urls, items=items)
        else:
                return render_template('wishlist.html', title='Wishlist Empty')
        
@app.route('/editinfo', methods=['GET', 'POST'])
@login_required
def EditInfo():
        form = EditForm()
        customer = models.Customer.query.get(current_user.id)
        if form.validate_on_submit():
                customers = models.Customer.query.filter_by(email=form.email.data).all()
                customersList = []
                for email in customers:
                        customersList.append(email.email)
                if(len(customersList)) == 1:
                        customer.firstname = form.firstname.data
                        customer.surname = form.surname.data
                        customer.email = form.email.data
                        db.session.commit()
                        flash("Information changed")
                else:
                        flash("Customer with that email already exists!")
        return render_template('editinfo.html', title='Edit info', form=form)

@app.route('/changepassword', methods=['GET', 'POST'])
@login_required
def ChangePassword():
        form = PasswordForm()
        customer = models.Customer.query.get(current_user.id)
        if form.validate_on_submit():
                if bcrypt.check_password_hash(customer.password, form.old_password.data):
                        hash = bcrypt.generate_password_hash(form.new_password.data)
                        customer.password = hash
                        db.session.commit()
                else:
                        flash("Incorrect password")
        return render_template('password.html', title='Change Password', form=form)
