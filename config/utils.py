import decimal
from decimal import Decimal


def get_transaction_fee(total_amount):
    '''
    Calculates transaction fee given Stripe formula.

    math.round($x.xx * 0.029 + 0.3)

      - https://stripe.com/pricing
      - https://support.stripe.com/questions/rounding-rules-for-stripe-fees
    '''
    return ((total_amount) * Decimal('0.029') + Decimal('0.3')).quantize(Decimal('0.01'), rounding=decimal.ROUND_HALF_UP)


def get_checkout_total(musician_amount, website_donation, transaction_covered):
    '''
    Inputs

      - musician_amount: initial amount pledge.
      - website_donation: opt in to donating to the Musician Tips Dividend.
      - transaction_covered: opt in to covering the transaction fees.

    Outputs
      - total_amount: the final total bill.
      - musician_amount: musician amount after readjustment.
      - transaction_fee: how much goes to Stripe.
      - website_amount: how much goes to the Musician Tips Dividend.
    '''
    if website_donation:
        website_amount = Decimal('0.25')
    else:
        website_amount = Decimal('0.00')


    musician_amount = Decimal(musician_amount) / Decimal('100')

    if transaction_covered:
        total_amount = musician_amount + website_amount
        proposed_total = total_amount
        while True:
            proposed_total += Decimal('0.01')
            proposed_transaction_fee = proposed_total - total_amount
            actual_transaction_fee = get_transaction_fee(proposed_total)
            if actual_transaction_fee <= proposed_transaction_fee:
                break
        transaction_fee = get_transaction_fee(proposed_total)
        musician_amount = proposed_total - website_amount - transaction_fee

    else:
        transaction_fee = get_transaction_fee(musician_amount + website_amount)
        musician_amount -= transaction_fee

    total_amount = musician_amount + website_amount + transaction_fee

    return total_amount, musician_amount, transaction_fee, website_amount
