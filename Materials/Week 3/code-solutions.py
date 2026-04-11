
friend_list = ["John", "Jane", "Jack"]

# function code goes here
def greet_friends(friends):
    for friend in friends:
        print(f"Hello {friend}!")

greet_friends(friend_list)


def calculate_tax(income, tax_rate):
    return income * tax_rate

print(calculate_tax(50000, 0.2))


def compound_interest(principal, interest_rate, duration):
    if interest_rate < 0 or interest_rate > 1:
        print("Please enter a decimal number between 0 and 1")
        return None
    if duration < 0:
        print("Please enter a positive number of years")
        return None
    for i in range(1, duration + 1):
        investment_value = principal * (1 + interest_rate) ** i
        print(f"The total amount of money earned by the investment is {int(investment_value)} £")
    return int(investment_value)

print(compound_interest(1000, 0.03, 5))

