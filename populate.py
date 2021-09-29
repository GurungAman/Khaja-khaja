import string
from random import randint, choices
from user.models import Customer
from restaurant.models import Restaurant,  Tags, Category, FoodItems
from django.contrib.auth import get_user_model
from faker import Faker
from cart.models import OrderItem

User = get_user_model()

f = Faker()
password = 'amangrg123'

print("Creating superuser.!")
user = User.objects.create_superuser(
    email='admin@admin.com',
    password=password
)
#  Create customer users
for i in range(10):
    base_user_customer = User.objects.create_user(
        email=f"test{i+1}@customer.com",
        password=password
    )
    name = f.name().split(' ')
    print(f"creating customer {name[0]}")
    customer = Customer.objects.create(
        customer=base_user_customer,
        first_name=name[0],
        last_name=name[1],
        address=f.address(),
    )
    base_user_restaurant = User.objects.create_user(
        email=f"test{i+1}@restaurant.com",
        password=password
    )
    r_name = f.name().split(' ')[0]
    print(f"Creating restaurant {r_name}")
    restaurant = Restaurant.objects.create(
        restaurant=base_user_restaurant,
        name=r_name,
        license_number=''.join(
            choices(string.ascii_uppercase + string.digits, k=7)),
        address=f.address(),
        bio=f.text()[:100]
    )

#  Create tags and categories
for i in range(10):
    tags = Tags.objects.create(
        name=f"tag {i+1}"
    )
    print(f'Tag {tags.name} created')
    category = Category.objects.create(
        name=f"category {i+1}"
    )
    print(f'Category {category.name} created')


restaurant = Restaurant.objects.all()
category = Category.objects.all()

for i in range(25):
    food_item = FoodItems.objects.create(
        restaurant=choices(restaurant)[0],
        category=choices(category)[0],
        name=f'food-item {i+1}',
        price=100,
        is_available=True,
    )
    print(f"Created food item {food_item.name}")

food_items = FoodItems.objects.all()
customer = Customer.objects.all()

for x in range(20):
    user = choices(customer)[0]
    food_item = choices(food_items)[0]
    print(f"Creating order for food item {food_item.name}")
    order_item = OrderItem.objects.create(
        user=user,
        food_item=food_item,
        quantity=randint(1, 9)
    )
