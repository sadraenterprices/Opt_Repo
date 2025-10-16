import math

class BlackScholes:
    def __init__(self, S, K, T, r, sigma):
        self.S = S  # Current stock price
        self.K = K  # Option strike price
        self.T = T  # Time to expiration in years
        self.r = r  # Risk-free interest rate
        self.sigma = sigma  # Volatility of the underlying asset

    def d1(self):
        return (math.log(self.S / self.K) + (self.r + 0.5 * self.sigma ** 2) * self.T) / (self.sigma * math.sqrt(self.T))

    def d2(self):
        return self.d1() - self.sigma * math.sqrt(self.T)

    def call_price(self):
        from scipy.stats import norm
        return (self.S * norm.cdf(self.d1()) - self.K * math.exp(-self.r * self.T) * norm.cdf(self.d2()))

    def put_price(self):
        from scipy.stats import norm
        return (self.K * math.exp(-self.r * self.T) * norm.cdf(-self.d2()) - self.S * norm.cdf(-self.d1()))

    def delta_call(self):
        from scipy.stats import norm
        return norm.cdf(self.d1())

    def delta_put(self):
        return norm.cdf(self.d1()) - 1

    def gamma(self):
        from scipy.stats import norm
        return norm.pdf(self.d1()) / (self.S * self.sigma * math.sqrt(self.T))

    def vega(self):
        from scipy.stats import norm
        return self.S * norm.pdf(self.d1()) * math.sqrt(self.T)

    def theta_call(self):
        from scipy.stats import norm
        return (-self.S * norm.pdf(self.d1()) * self.sigma / (2 * math.sqrt(self.T)) - self.r * self.K * math.exp(-self.r * self.T) * norm.cdf(self.d2()))

    def theta_put(self):
        from scipy.stats import norm
        return (-self.S * norm.pdf(self.d1()) * self.sigma / (2 * math.sqrt(self.T)) + self.r * self.K * math.exp(-self.r * self.T) * norm.cdf(-self.d2()))

    def rho_call(self):
        from scipy.stats import norm
        return self.K * self.T * math.exp(-self.r * self.T) * norm.cdf(self.d2())

    def rho_put(self):
        from scipy.stats import norm
        return -self.K * self.T * math.exp(-self.r * self.T) * norm.cdf(-self.d2())

# Example usage:
# bs = BlackScholes(S=100, K=100, T=1, r=0.05, sigma=0.2)
# print(bs.call_price())
# print(bs.put_price())
