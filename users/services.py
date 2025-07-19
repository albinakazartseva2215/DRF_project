import stripe
from config.settings import STRIPE_API_KEY

stripe.api_key = STRIPE_API_KEY


def create_stripe_price(amount, product_id, currency="rub"):
    """Создает цену в страйпе"""
    price = stripe.Price.create(
        currency=currency.lower(),
        unit_amount=int(amount * 100),
        product=product_id,
    )
    return price


def create_stripe_product(name):
    """Создает продукт в Stripe"""
    product = name.course_payment if name.course_payment else name.lesson_payment
    stripe_product = stripe.Product.create(name=product)
    return stripe_product.get("id")


def create_stripe_sessions(price):
    """Создание сессии на оплату в страйпе"""
    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        success_url="https://127.0.0.1:8000/success",
        line_items=[{"price": price.get("id"), "quantity": 1}],
        mode="payment",
    )
    return session.get("id"), session.get("url")
