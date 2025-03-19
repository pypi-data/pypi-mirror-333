class InterestRate:
    def __init__(self, value, convertibility=1, nominal=False):
        self.value = value
        if nominal:
            self.value /= convertibility
        self.convertibility = convertibility
        self.nominal_value = self.value * self.convertibility
        self.accumulation_factor = 1 + self.value
        self.discount_factor = 1 / self.accumulation_factor

    def accumulate(self, periods, amount=1):
        return amount * self.accumulation_factor**periods

    def present_value(self, periods, amount=1):
        return amount * self.discount_factor**periods

    def convert(self, new_convertibility):
        new_value = (1 + self.value) ** (self.convertibility / new_convertibility) - 1
        return InterestRate(new_value, new_convertibility)

    def present_value_annuity_immediate(self, periods, amount=1):
        return amount * (1 - self.present_value(periods)) / self.value

    def cumulative_value_annuity_immediate(self, periods):
        return (self.accumulate(periods) - 1) / self.value

    def __repr__(self):
        return f"{self.value:.6%}, convertibility {self.convertibility}"

    def __str__(self):
        return f"Effective {self.value:.6%}, nominal {self.nominal_value:.6%}, convertibility {self.convertibility}"
