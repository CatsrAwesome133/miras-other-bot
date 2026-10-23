# for bot
ANGLER = 1504819900957589555
FRIEDFISH = '<:friedfish:1561070704844341410>'
HAIKU = '📃'
HELLOS = [
    'Welcome.',
    'Hello!',
    'Greetings.',
    '...and how may I help you this fine new loop?'
]
HELLO_WEIGHTS = [
     3,
     2,
     2,
     0.1
]
COINS = ['1','0']
GUILD = 1504795388417150976
FUN = [
    "How's life?",
    "Hmm, someone in this conversation needs to sleep.",
    "Anyone care to brief the silly butterfly on our current situation?",
    "Ah! Words!"
]

# for tools
c = {
    "in ": [2.54, "centimetres"], #cm
    "ft ": [0.3048, "metres"], #m
    "yd ": [0.9144, "metres"], #m
    "mi ": [1.6093, "kilometres"], #km
    "fl oz ": [28.41, "mililitres"], #mL
    "pt ": [0.568, "litres"], #L
    "gal ": [4.546, "liters"], #L
    "oz ": [28.35, "grams"], #g
    "lb ": [0.4536, "kilograms"], #kg
    "st ": [6.3503, "kilograms"] #kg
}
c_full = {
    "inch": [2.54, "centimetres"], #cm
    "feet": [0.3048, "metres"], #m - unfortunatley, english
    "yard": [0.9144, "metres"], #m
    "mile": [1.6093, "kilometres"], #km
    "fluid ounce": [28.41, "mililitres"], #mL
    "pint": [0.568, "litres"], #L
    "gallon": [4.546, "liters"], #L
    "ounce": [28.35, "grams"], #g
    "pound": [0.4536, "kilograms"], #kg
    "stone": [6.3503, "kilograms"] #kg
}
c_all = [c, c_full]

# other stuff
def give_msg_back(user):
    options = [f"Now, now. Give {user} their message back.",
               f"Not the time to be mean and kidnap {user}'s message, dear.",
               f"Oh no, did you really copy and delete a message from {user}? That's not very nice, is it?"]
    return options