from collections import UserDict
from datetime import datetime
import pickle

class Field:
    def __init__(self, value):
        if not self.validate(value):
            raise ValueError
        self.__value = value

    def validate(self, value):
        return True
    
    @property
    def value(self):
        return self.__value
    
    @value.setter
    def value(self, new_value):
        if not self.validate(new_value):
            raise ValueError
        self.__value = new_value
    
    def __str__(self):
        return str(self.__value)

class Name(Field): 
    pass

class Phone(Field):
    def __init__(self, value):
        if self.validate(value): #_phone_valid
            self.__value = value
        else:
            raise ValueError("Incorrect number: phone must contain 10 digit!")
           
    @property
    def value(self):
        return self.__value
    
    @value.setter
    def value(self, new_value):
        if self.validate(new_value): #_phone_valid
            self.__value = new_value
        else:
            raise ValueError("Incorrect number: phone must contain 10 digit!")

    def validate(self, value):   # def _phone_valid
        return len(value) == 10 and value.isdigit()

class Birthday(Field):
    def __init__(self, value):
        if self.validate(value): # _bday_valid
            self.__value = value
        elif value is None:
            raise ValueError("No date of birth, should be YYYY-MM-DD")
        else:
            raise ValueError("Wrong format, date of birth should be YYYY-MM-DD")  
        
    @property
    def value(self):
        return self.__value
        
    @value.setter
    def value(self, new_value):
        if self.validate(new_value): # _bday_valid
            self.__value = new_value
        else:
            raise ValueError("Wrong format, date of birth should be YYYY-MM-DD")

    def validate(self, value):  # _bday_valid 
        try:
            datetime.strptime(value, '%Y-%m-%d')
            return True
        except ValueError:
            return False
    
    def days_to_birthday(self):
        today = datetime.now()
        bday_date = datetime.strptime(self.value, '%Y-%m-%d')
        bday_upgreat = datetime(today.year, bday_date.month, bday_date.day)
        if today > bday_upgreat:
            bday_upgreat = datetime(today.year + 1, bday_date.month, bday_date.day)
        days_to_next_bday = (bday_upgreat - today).days
        return days_to_next_bday

class Record:
    def __init__(self, name, birthday=None):
        self.name = Name(name)
        self.phones = []
        self.birthday = Birthday(birthday) if birthday else None

    def add_phone(self, phone_number):
        phone = Phone(phone_number)
        phone.validate(phone_number)    # _phone_valid              
        self.phones.append(phone)

    def remove_phone(self, phone_number):
        for element in self.phones:
            if element.value == phone_number:
                self.phones.remove(element)

    def edit_phone(self, old_phone, new_phone):
        for phone in self.phones:
            if phone.value == old_phone:
                new_phone_check = Phone(new_phone)
                new_phone_check.validate(new_phone)   # _phone_valid
                phone.value = new_phone
                return       
        raise ValueError(f'{old_phone} not exist')

    def find_phone(self, phone_number):
        for phone in self.phones:
            if phone.value == phone_number:
                return phone
        return None
    
    def days_to_birthday(self):
        if self.birthday:
            return self.birthday.days_to_birthday()
        return None

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(phone.value for phone in self.phones)}"

class AddressBook(UserDict):
    def iterator(self, N):
        records = list(self.data.values())
        for i in range(0, len(records), N):
            yield records[i:i+N]

    def save_to_file(self, some_file):
        with open(some_file, 'wb') as file:
            pickle.dump(self.data, file)

    def load_from_file(self, some_file):
        try:
            with open(some_file, 'rb') as file:
                self.data = pickle.load(file)
        except FileNotFoundError:
            print("File not exist. Should creat a new address book.")

    def searching(self, some_info):
        result = []
        for record in self.data.values():
            if some_info in record.name.value or any(some_info in phone.value for phone in record.phones):
                result.append(record)
        return result

    def add_record(self, record): 
        self.data[record.name.value] = record

    def find(self, name):
        result = self.data.get(name)
        return result
    
    def delete(self, name):
        if name in self.data:
            del self.data[name]

if __name__ == '__main__':
    book = AddressBook()
    book.save_to_file('address_book.txt')
    book.load_from_file('address_book.txt')
