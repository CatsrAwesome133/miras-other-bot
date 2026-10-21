import re
# to get the dictionary of conversions properly
import sys
from pathlib import Path

parent_dir = Path(__file__).resolve().parent.parent
sys.path.append(str(parent_dir))

from constants import c, c_full


def to_c(f):
    return (f - 32) * (5/9)


def metric(text, pronoun="they"):
    converted = []
    current = []
    long = False

    # shortened units
    for unit in c:
        if unit in text:
            try:
                current = re.findall(fr"(\d+)\s*{unit}", text)
                for number in current:
                    converted.append(str(float(number)*c[unit][0])+f" {c[unit][1]}")
            except ValueError:
                pass
    # full units (except singular feet)
    for unit in c_full:
            if unit in text:
                try:
                    current = re.findall(fr"(\d+)\s*{unit}", text)
                    for number in current:
                        converted.append(str(float(number)*c_full[unit][0])+f" {c_full[unit][1]}")
                except ValueError:
                    pass
    # farenheit
    if "f" in text.lower():
        # removing other units
        for unit in c:
            text = text.replace(unit, "")
        for unit in c_full:
                    text = text.replace(unit, "")
        
        try:
            current = re.findall(r"(\d+)\s*f", text.lower())
            for number in current:
                converted.append(str(int(to_c(float(number))//1))+f" celcius")
        except ValueError:
            pass
    out = f"{pronoun.capitalize()} have said:\n"
    for n in converted:
        out += (f"- {n}\n")
    out += "Figure out the order yourself. The creator is tired."
    if len(converted) >= 3:
         out += f"\nSiren would like to ask why {pronoun} used that many units."
         long = True
    return out, long

print(metric("It's like 2 in of rain outside, 80f outside, also 2 pounds because, and another 2 in of snow, oh and shes 5ft tall, and again its 80f outside bruh"))