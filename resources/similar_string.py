def similar(one, two):
    if len(one) > len(two):
        one = one[:len(two)]
    if len(one) < len(two):
            two = two[:len(one)]

    if not one:
         return False

    matching = sum(1 for c1,c2 in zip(one,two) if c1==c2)

    return matching > len(one)/2

if __name__ == '__main__':
    print(similar("Apply","Applica"))
    print(similar("applesaregood","appled"))