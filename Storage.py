
import re
HEADER = r"""
  _________ __                                      
 /   _____//  |_  ________________     ____   ____  
 \_____  \\   __\/  _ \_  __ \__  \   / ___\_/ __ \ 
 /        \|  | (  <_> )  | \// __ \_/ /_/  >  ___/ 
/_________/|__|  \____/|__|  (______/\___  / \____>
                                    /_____/      
if you want to see help, type 'help'
<-------------------------------------------------->
"""


# command: add/remove/get/show/clear/exit/help/autoshow
# item: contain only latters
# amont: contains only digits

# $command $item $amount


def reg_check(command, item, amount):
    text = " ".join([command, item, amount]) 
    pattern = r'^(add|remove) [a-zA-Z]+ \d+$'
    return True if re.match(pattern, text) else False


def classic_check(command, item, amount):
    if command != 'add' and command != 'remove':
        return False
    
    if not item.isalpha():
        return False
    
    if not amount.isdigit():
        return False
    
    return True


def parse_input(sequence, check_callback):
    tokens = sequence.split(' ') # -> ['$command', '$item', '$amount']
    
    if len(tokens) != 3:
        return None

    res = check_callback(*tokens)
    if not res:
        return None
    
    return tokens


def add(storage, item, amount):
    # print(f'Add to storage: {item} - {amount}')
    storage_item = storage.get(item)
    if storage_item is None:
        storage[item] = amount
    else:
        storage[item] += amount


def remove(storage, item, amount):
    # print(f'Remove from storage: {item} - {amount}')
    storage_item = storage.get(item)
    if storage_item is None:
        print(f'\nNo such item: {item}')
    else:
        if storage_item > amount:
            storage[item] -= amount
        else:
            storage.pop(item)


def get(storage, item):
    storage_item = storage.get(item)
    if storage_item is None:
        print(f'\nNo such item: {item}')
    else:
        print(f'\n{item} - {storage[item]}')


def show(storage):
    print(f'\n{"Storage state":-^23}')
    for k, v in storage.items():
        print(f'|{k:<10}|{v:-^10}|')
    print(f'{"":-<23}')


def clear(storage):
    storage.clear()
    print('\nStorage cleared!')


def help():
    print(f'\n{"Help":-^78}')
    com = {'add [item] [amount]':'add amount of item to storage',
            'remove [item] [amount]':'remove amount of item from storage',
            'get [item]':'show amount of item in storage',
            'show':'show storage state',
            'autoshow':'auto show storage state after each command on/off',
            'clear':'clear storage',
            'exit':'exit from program',
            'help':'show command list',
            'command format':'$command $item $amount'
            }
    for k, v in com.items():
        print(f'|{k:<25}|{v:<50}|')
    print(f'{"":-<78}')


def storage():
    print(HEADER)

    storage = {}
    autoshow = False

    while True:
        sequence = input('\nEnter command: ')

        if sequence == 'help':
            help()
            continue

        if sequence == 'clear':
            clear(storage)
            continue

        if sequence == 'show':
            show(storage)
            continue
        
        if sequence == 'autoshow':
            autoshow = not autoshow
            continue

        if sequence.startswith('get'):
            item = sequence.split(' ')[1]
            get(storage, item)
            continue

        if sequence == 'exit':
            print('Bye!')
            break

        parsing_res = parse_input(sequence, reg_check)
        if parsing_res is None:
            print('\nWrong command format')
            continue
        
        command, item, amount = parsing_res

        commands = {
            'add': add,
            'remove': remove
        }
        commands[command](storage, item, int(amount))
        # globals()[command](storage, item, int(amount))
        
        if autoshow:
            print(f'\n{"Storage state":-^23}')
            for k, v in storage.items():
                print(f'|{k:<10}|{v:-^10}|')
            print(f'{"":-<23}')

if __name__ == '__main__':
    storage()