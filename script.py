import string, random
from user.models import Customer
from restaurant.models import Restaurant, Menu, Tags, Category, FoodItems
from django.contrib.auth import  get_user_model
from  faker import Faker

User = get_user_model()

f = Faker()
password = 'amangrg123'


#  Create customer users
for i in range(5):
    base_user = User.objects.create_user(
        email =  f"test{i+1}@customer.com",
        password = password
    )
    name = f.name().split(' ')
    print(f"creating customer {name[0]}")
    customer = Customer.objects.create(
        customer = base_user,
        first_name = name[0],
        last_name = name[1],
        address = f.address(),
    )

# Create restaurants and Menu
for i in range(5):
    base_user = User.objects.create_user(
        email=f"test{i+1}@restaurant.com",
        password=password
    )
    restaurant = Restaurant.objects.create(
        restaurant = base_user,
        name = f.name(),
        license_number = ''.join(random.choices(
            string.ascii_uppercase + string.digits, k=7)),
        address =f.address(),
        bio = f.text()[:30]
    )
    print(f"creating restaurant {restaurant.name}")
    menu = Menu.objects.create(
        name = f"menu {i+1}",
        restaurant = restaurant
    )

#  Create tags and categories
for i in range(7):
    tags = Tags.objects.create(
        name = f"tag {i+1}" 
        )
    category = Category.objects.create(
        name = f"category {i+1}"
    )
