from datetime import datetime, UTC

# Arbitraty year conversion:
# Take current year, convert to base 28, take last 2 digits

# Parts of this algorithm (the to_28 function) were written by AI. Specifically the latter half.
# This doesn't handle negative numbers because I sure hope we aren't in the BCs
def to_28(n):
    """Returns a tuple; first value indicates wether conversion was successful, second returns the number (or an error comment)"""
    if n == 0:
        return True, "0"
    
    digits = "0123456789ABCDEFGHIJKLMNOPQR"
    if n < 0:
        return False, "I sure hope you've only set your device time weirdly."
    
    n = abs(n)
    result = []
    
    while n > 0:
        n, remainder = divmod(n, 28)
        result.append(digits[remainder])
        
    return True, "".join(reversed(result))


def now_ph():
    irl = datetime.now(UTC) # I guess Pharloom arbitrarily is in the UTC timezone or something ;-;

    ph = {
        'Toll': to_28(int(float(irl.hour)*(28/24))),
        'Cycle': to_28(irl.year),
        'Others': to_28(irl.timetuple().tm_yday + irl.year*365) # can you see how arbitrary this is. tbf the worldbuilding wasn't made to handle more than hours-in-a-day conversion but.
    }
    
    for key in ph:
        if ph[key][0]:
            ph[key] = ph[key][1]
            if key == 'Cycle':
                ph[key] = ph[key][:2]
            if key == 'Others':
                ph[key] = ph[key][-3:]

    return f'{ph["Cycle"]}:{ph["Others"]}{ph["Toll"]}', ph


if __name__ == '__main__':
    now_ph()