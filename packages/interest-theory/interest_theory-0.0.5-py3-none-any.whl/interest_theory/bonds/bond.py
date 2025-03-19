from typing import List

from interest_theory.interest_rates.interest_rate import InterestRate


class Bond:
    def __init__(
        self,
        face_value: float,
        coupons_number: int,
        coupon_rate: InterestRate,
        yield_rate: InterestRate,
        redemption=None,
    ):
        self.face_value: float = face_value
        self.coupon_rate: InterestRate = coupon_rate
        self.coupons_number: int = coupons_number
        self.coupon: float = face_value * coupon_rate.value
        self.yield_rate: InterestRate = yield_rate
        self._convert_yield_rate()
        self.redemption: float = face_value if redemption is None else redemption
        self.price: float = 0.0
        self._compute_price()

    def _compute_price(self):
        present_value_coupons = self.yield_rate.present_value_annuity_immediate(self.coupons_number, self.coupon)
        present_value_redemption = self.yield_rate.present_value(self.coupons_number, self.redemption)
        self.price = present_value_coupons + present_value_redemption

    def _convert_yield_rate(self):
        if self.coupon_rate.convertibility != self.yield_rate.convertibility:
            self.yield_rate = self.yield_rate.convert(new_convertibility=self.coupon_rate.convertibility)

    def book_values(self):
        values: List[float] = [self.price]
        coupons_number = self.coupons_number
        for _ in range(1, self.coupons_number):
            self.coupons_number -= 1
            self._compute_price()
            values.append(self.price)
        values.append(self.redemption)
        self.coupons_number = coupons_number
        self._compute_price()
        return values

    def __repr__(self):
        return f""""
        ${self.price:.4f}, {self.coupons_number} coupons with value ${self.coupon},
        paid {self.coupon_rate.convertibility} times a year
        """
