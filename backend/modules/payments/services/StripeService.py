import stripe
import environ

env = environ.Env()


class StripeService:
    stripe.api_key = env.str("STRIPE_SECRET_KEY", "sk_test_xxxxxxxxxxx")

    @classmethod
    def create_payment_intent_sheet(cls, cus_id, cents, payment_method=''):
        ephemeralKey = stripe.EphemeralKey.create(
            customer=cus_id,
            stripe_version=env.str("STRIPE_VERSION", '2020-08-27'),
        )
        if payment_method:
            paymentIntent = stripe.PaymentIntent.create(
                amount=cents,
                currency=env.str("STRIPE_CURRENCY", 'usd'),
                customer=cus_id,
                payment_method=payment_method,
            )
        else:
            paymentIntent = stripe.PaymentIntent.create(
                amount=cents,
                currency=env.str("STRIPE_CURRENCY", 'usd'),
                customer=cus_id
            )

        return {
            "id": paymentIntent.id,
            "paymentIntent": paymentIntent.client_secret,
            "ephemeralKey": ephemeralKey.secret,
            "customer": cus_id,
            "payment_method": payment_method
        }

    @classmethod
    def attach_payment_method(cls, cus_id):
        ephemeralKey = stripe.EphemeralKey.create(
            customer=cus_id,
            stripe_version=env.str("STRIPE_VERSION", '2020-08-27'),
        )
        setupIntent = stripe.SetupIntent.create(
            customer=cus_id,
        )
        return {
            "id": setupIntent.id,
            "setupIntent": setupIntent.client_secret,
            "ephemeralKey": ephemeralKey.secret,
            "customer": cus_id,
        }

    @classmethod
    def get_payments_history(cls, cus_id, limit=100, offset=0):
        return stripe.PaymentIntent.list(
            customer=cus_id, limit=limit, offset=offset,
        ).get('data', [])

    @classmethod
    def get_payments_methods(cls, cus_id, type='card', limit=100, offset=0):
        return stripe.PaymentMethod.list(customer=cus_id, type=type, limit=limit, offset=offset).get('data', [])

    @classmethod
    def detach_payment_method(cls, payment_method_id):
        return stripe.PaymentMethod.detach(payment_method_id)

    @classmethod
    def create_payment_intent_sheet_for_user(cls, user, cents, payment_method):
        user = user
        stripe_profile = user.stripe_profile
        if not stripe_profile.stripe_cus_id:
            customer = stripe.Customer.create(email=user.email)
            stripe_cus_id = customer['id']
            stripe_profile.stripe_cus_id = stripe_cus_id
            stripe_profile.save()
        else:
            stripe_cus_id = stripe_profile.stripe_cus_id
        response = StripeService.create_payment_intent_sheet(stripe_cus_id, cents, payment_method)
        return response

    @classmethod
    def initiate_refund(cls, payment_intent_id):
        return stripe.Refund.create(payment_intent=payment_intent_id, )
