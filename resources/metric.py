import re
c = {
    "in": 2.54, #cm
    "ft": 0.3048, #m
    "yd": 0.9144, #m
    "mi": 1.6093, #km
    "floz": 28.41, #mL
    "pt": 0.568, #L
    "gal": 4.546, #L
    "oz": 28.35, #g
    "lb": 0.4536, #kg
    "st": 6.3503 #kg
}

def to_c(f):
    return (f - 32) * (5/9)

def metric(text):
    converted = []
    current = []
    for unit in c:
        if unit in text:
            try:
                current = re.findall(fr"(\d+)\s*{unit}", text)
                for number in current:
                    converted.append(float(number)*c[unit])
            except ValueError:
                pass
    return converted

print(metric("It's like 2 in of rain outside and another 2 in of snow, oh and shes 5ft tall"))