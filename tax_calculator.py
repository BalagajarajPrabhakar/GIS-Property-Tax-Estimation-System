zone_rates = {
    "A":10,
    "B":7,
    "C":5
}

type_factor = {
    "residential":1,
    "commercial":1.5,
    "industrial":2
}

def calculate_tax(area,zone,ptype):

    rate = zone_rates.get(zone,5)
    factor = type_factor.get(ptype,1)

    tax = area * rate * factor

    return tax