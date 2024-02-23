from flask import Flask, render_template, request
import stripe

app = Flask(__name__, static_folder='static')

stripe.api_key = "your_stripe_secret_key"


@app.route("/")
def index():
  return render_template('index.html')


@app.route('/checkout', methods=['POST'])
def checkout():
  # Handle payment processing here
  token = request.form['stripeToken']
  amount = 1000  # Amount in cents

  try:
    charge = stripe.Charge.create(
        amount=amount,
        currency='usd',
        description='Example charge',
        source=token,
    )
    # Payment successful
    return render_template('checkout_success.html')
  except stripe.error.CardError as e:
    # Payment declined
    error_message = e.error.message
    return render_template('checkout_error.html', error_message=error_message)


if __name__ == "__main__":
  app.run(host='0.0.0.0', port=8080, debug=True)
