import sys
from classes import AddressBook, Record
import pickle

book = AddressBook()

def save_to_file(some_file):
        try:
            with open(some_file, 'wb') as file:
                pickle.dump(book.data, file)
        except IOError:
            print('Error, data not saved')

def load_from_file(some_file):
        try:
            with open(some_file, 'rb') as file:
                book.data = pickle.load(file)
            print('Loading was successful')
        except FileNotFoundError:
            print("File not exist. Should creat a new address book.")

def input_error(func):
    def exception_handling(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError:
            return "Please, enter a name"
        except ValueError:
            return "Please, enter name and phone number"
        except IndexError:
            return "Incorrect command"
    return exception_handling

@input_error
def notation(name, phone):   # запис телефону в словникa
    record = Record(name)
    record.add_phone(phone)
    book.add_record(record)
    return f'You have added a contact'
        
@input_error
def changes(name, old_phone, new_phone):  # зміна номеру мобільного для вказаного імені
    record = book.data.get(name)
    if not record:
        raise KeyError(f'No contact {name} in the notebook')
    for phone in record.phones:
        if phone.value == old_phone:
            phone.value = new_phone
            return f'You have changed the {name} contact phone number'
    return f'No {old_phone} in the notebook'

@input_error
def show_phone(name): # вивід номеру телефону по запиту
    record = book.data.get(name)
    if record:
        phones = [phone.value for phone in record.phones]
        return phones
    return 'No contact in the notebook'

@input_error
def show_all():  # вивід всього змісту записника
    if not book.data:
        print('The notebook is empty')
        return 'The notebook is empty'
    result = ''
    for name, record in book.data.items():
        phones = [phone.value for phone in record.phones] 
        phones_to_str = ', '.join(phones)
        result += f'{name}: {phones_to_str}\n'
    return result 

@input_error
def searching(some_info): # пошук по імені або телефону
    contacts = []
    for record in book.data.values():
        name = record.name.value
        phone_numbers = [phone.value for phone in record.phones]
        if some_info in name or any(some_info in num for num in phone_numbers):
            contacts.append(record)
    if len(contacts) == 0:
        return 'Nothing found'
    result = ''
    for record in contacts:
        name = record.name.value
        phones = ', '.join(phone.value for phone in record.phones)
        result += f'Name: {name}\nPhone: {phones}\n\n'
    return result

@input_error
def closing(): # закриття програми
    print('Good bye!')
    sys.exit()

def bot_commander(command):
    command_lower = command.lower()
    block = command_lower.split()
    if block[0] == 'hello':
        print('How can I help you?')
    elif block[0] == 'add':
        if len(block) < 3:
            print('Name and phone number are missing') 
        else:
            name = block[1]
            phone = block[2]
            result = notation(name, phone)
            #print(result)
            return result
    elif block[0] =='change':
        if len(block) < 4:
            print('Name or phone number are missing')
        else:
            name = block[1]
            old_phone = block[2]
            new_phone = block[3]
            result = changes(name, old_phone, new_phone)
            #print(result)
            return result
    elif block[0] == 'phone':
        if len(block) < 2:
            print('Name is missing')
        else:
            name = block[1]
            result = show_phone(name)
            #print(result)
            return result
    elif block[0] == 'search':
        if len(block) < 2:
            print('Name or phone number are missing')
            return 'Name or phone number are missing'  
        else:
            some_info = ''.join(block[1:])
            result = searching(some_info)
            #print(result)
            return result
    elif block[0] == 'show' and block[1] == 'all':
        result = show_all()
        #print(result)
        return result
    elif block[0] in ['good', 'bye', 'close', 'exit']:
        closing()
    else:
        print("Don't understand the command. Please, try again!")

def main(): # зберігання/завантаження даних по результатам взаємодії з ботом
    print('Welcome!') 
    load_from_file('adress_book.txt') 
    while True:
        command = input("Enter a command [add/change/phone/show all/search] and info for the notebook: ")
        result = bot_commander(command)
        print(result)
        save_to_file('adress_book.txt')

if __name__ == "__main__":
    main()
