from faker import Faker
fake = Faker()

def generate_product_data():
    fake_product_data  = {
        "code": fake.aba(),
        "title": 
    }
    return {
        "name": fake.name(),
        "description": fake.text(),
        "price": fake.random_int(min=1, max=1000),
        "category": fake.word(),
        "image": fake.image_url()
    }