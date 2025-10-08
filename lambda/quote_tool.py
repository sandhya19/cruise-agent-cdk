import random

def generate_quote(destination, nights, adults, children):
    base_price = random.randint(1200, 2000)
    cruise_cost = base_price * (adults + children * 0.5)
    hotel_cost = nights * 150 * (adults + children * 0.5)
    total = cruise_cost + hotel_cost
    return {
        "destination": destination,
        "nights": nights,
        "adults": adults,
        "children": children,
        "estimated_price": f"£{int(total)}"
    }
