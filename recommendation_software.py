"""
Game Name: Fragrance Recommender
Description: Type in a category of fragrance and we'll recommend some!
Author: Zachary Coe
Date: 2024-10-21
"""



import csv



FRAG_FILE = 'Zach\'s Tried Fragrance List - non-formatted.csv'
SCENT_SIZE = 45



class ProgramRunner:
    intro_image = """      ::::::::::::::.                 
            . . ::..:-. ..                  
            ....::..:::...                  
            .::::==::.                    
                ::.:-::-                     
        ......:=-=+==-.....                
        .=-------==++=========-              
        =---------==--========              
        =-----::::::::::=====-              
        ------   :=.:   -====-              
        :-----:**:=-.*: =====:              
        ::----   .::.   -====:              
        ::----          =====:              
        ::----          -====:              
        ::-----------========:              
        :-------------=======:              
        -:------------=======:              
        :------------=-======:              
        -------------========:              
        :::::.... .  ....:::-:              
        .::::::::::::::::::::.              
        ..:..... .  . ....:::."""
    
    instructions = ""
    
    def __init__(self):
        pass

    def __str__(self):
        
# TODO:
# Adjust create_hashmap with new Tree class
# to take input and return list of options
class DataHandler:
    def __init__(self, filename):
        self.data = self.load_data(filename)
        self.filter_chars = {}
        self.hashmaps = {}

    def load_data(self, filename):
        with open(filename, mode='r', encoding='utf-8') as file:
            csv_reader = csv.reader(file)
            header = next(csv_reader)

        return list(csv_reader)

    def create_hashmap(self, filter_category, size):
        data = self.data
        hashmap = HashMap(size)
        self.hashmaps[f"{filter_category}"] = hashmap
        
        for row in data:

            if len(row) < 4:
                continue

            frag_node = FragranceNode(row[1], row[0], row[2].split(";"), row[3])
            for key, value in frag_node.__dict__.items():
                if key == filter_category:
                    if isinstance(value, list):

                        for attribute in value:
                            first_letter = attribute[0].lower()
                            if first_letter not in self.filter_chars:
                                self.filter_chars[first_letter] = [attribute]
                            elif attribute not in self.filter_chars[first_letter]:
                                self.filter_chars[first_letter].append(attribute)

                            hashmap.assign(attribute, frag_node)
                    else:
                        first_letter = value[0].lower()
                        if first_letter not in self.filter_chars:
                            self.filter_chars[first_letter] = [value]
                        elif value not in self.filter_chars[first_letter]:
                            self.filter_chars[first_letter].append(value)

                        hashmap.assign(value, frag_node)

    def retrieve_data(self, main_category, filter):
        hashmap = self.hashmaps[f"{main_category}"]
        return hashmap[f"{filter}"]


class FragranceNode:
    def __init__(self, name: str, brand: str, scent_category:[str], cost: str):
        self.name = name
        self.brand = brand
        self.scent_category = scent_category
        self.cost = cost
        self.next_node = None

    def __str__(self):
        frag_string = f"""
------------------------------

Name: {self.name}
Brand: {self.brand}
Cost: {self.cost}"""
        
        return frag_string

    def set_next_node(self, next_node):
        self.next_node = next_node

class LinkedList:
    def __init__(self, node: FragranceNode):
        self.head_node = node

    def get_head_node(self):
        return self.head_node
    
    def insert_beginning(self, node: FragranceNode):
        new_node = node
        new_node.set_next_node(self.head_node)
        self.head_node = new_node

class HashMap:
    def __init__(self, array_size):
        self.array_size = array_size
        self.array = [None for item in range(array_size)]

    def hash(self, key, count_collisions=0):
        hash_code = hash(key)
        return hash_code + count_collisions

    def compressor(self, hash_code):
        return hash_code % self.array_size
    
    def assign(self, key, frag_node):
        number_collisions = 0
        
        while (True):
            hash_code = self.hash(key, number_collisions)
            array_index = self.compressor(hash_code)
            current_array_value = self.array[array_index]

            if (current_array_value is None):
                new_linked_list = LinkedList(frag_node)
                self.array[array_index] = [key, new_linked_list]
                return
            
            if (current_array_value[0] == key):
                existing_linked_list = current_array_value[1]
                if isinstance(existing_linked_list, LinkedList):
                    existing_linked_list.insert_beginning(frag_node)
                    return
            
            number_collisions += 1

class TreeNode:
    def __init__(self, letter: str):
        self.letter = letter
        self.children = {}

class WordTree:
    def __init__(self):
        self.root = TreeNode("")

    def insert_word(self, word: str, current_node: TreeNode, depth=0):
            if depth == len(word):
                return

            letter = word[depth]

            if letter in current_node.children:
                next_node = current_node.children[letter]
            else:
                next_node = TreeNode(letter)
                current_node.children[letter] = next_node

            self.insert_word(word, next_node, depth+1)

    # TODO:
    # Write find_word(s) function. Think iterative approach will
    # work best. Needs to return all words that start with input
    # from user.
    def find_word(self, word: str):
        current_node = self.root

        for n in range(len(word)):
            if word[n] not in self.root.children:
                return [None]
            
            current_node = current_node.children[word[n]]
    
        list_of_words = []
        num_of_words = 1
        while num_of_words > 0:
            if len(current_node.children.keys()) > 1:


        







# main
def main():
    return



if __name__ == "__main__":
    main()