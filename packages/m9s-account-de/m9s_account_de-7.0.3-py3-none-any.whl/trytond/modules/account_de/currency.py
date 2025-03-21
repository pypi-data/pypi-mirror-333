# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
from decimal import ROUND_HALF_UP

from trytond.pool import PoolMeta

# Note:
# Another widely used rounding function is
# round_price in product/product.py, using by default ROUND_HALF_EVEN.
# This function lacks extensibility, because it is directly imported from
# module product all over the place and therefore must be hard patched directly
# in the code.


class Currency(metaclass=PoolMeta):
    __name__ = 'currency.currency'

    def round(self, amount, rounding=ROUND_HALF_UP, opposite=False):
        return super().round(
            amount, rounding=rounding, opposite=opposite)
