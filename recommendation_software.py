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
    intro_image = """        ::::::::::::::.                 
        . . ::..:-. ..                  
        ....::..:::...                  
        .::::==::.                    
            ::.:-::-                     
    ......:=-=+==-.....                
    .=-------==++=========-              
    =---------==--========              
    =-----::::::::::=====-              
    ------  Welcome -====-              
    :-----:** to *: =====:              
    ::----  Zack's  -====:              
    ::---- Fragrance ====:              
    ::----  Finder  -====:              
    ::-----------========:              
    :-------------=======:              
    -:------------=======:              
    :------------=-======:              
    -------------========:              
    :::::.... .  ....:::-:              
    .::::::::::::::::::::.              
    ..:..... .  . ....:::.\n"""
    
    def __init__(self, filename):
        self.data_handler = DataHandler(filename)
        self.fragrance_sample = FragranceNode("", "", [], "")

    def get_filter_one(self):
        options = [key.title() for key in vars(self.fragrance_sample).keys() if key != 'next_node']
        while True:     
            try:   
                print("Type a filter you'd like to sort by: ")
                filter = input().title()
                if filter in options:
                    return filter
                else:
                    raise ValueError()
            except ValueError:
                print(f"Please select from: {options}")


        
class DataHandler:
    def __init__(self, filename):
        self.headers, self.data = self.load_data(filename)
        self.filter_chars = WordTree()
        self.hashmaps = {}

    def load_data(self, filename):
        with open(filename, mode='r', encoding='utf-8') as file:
            csv_reader = csv.reader(file)
            headers = next(csv_reader)
            data = list(csv_reader)

        return headers, data

    def create_hashmap(self, filter_category, size):
        headers = self.headers
        data = self.data
        hashmap = HashMap(size)
        self.hashmaps[f"{filter_category}"] = hashmap

        header_map = {
            "brand": headers.index("House"),
            "name": headers.index("Perfume"),
            "scent_categories": headers.index("Accords"),
            "cost": headers.index("Cost")
        }
        
        for row in data:

            brand = row[header_map["brand"]]
            name = row[header_map["name"]]
            scent_categories = row[header_map["scent_categories"]].split("; ")
            cost = row[header_map["cost"]]

            frag_node = FragranceNode(brand, name, scent_categories, cost)
            for key, value in frag_node.__dict__.items():
                if key == filter_category:
                    if isinstance(value, list):
                        for attribute in value:
                            self.filter_chars.insert_word(attribute)
                            hashmap.assign(attribute, frag_node)

                    else:
                        self.filter_chars.insert_word(value)
                        hashmap.assign(value, frag_node)

    def retrieve_data(self, main_category, filter):
        hashmap = self.hashmaps[f"{main_category}"]
        return hashmap[f"{filter}"]


class FragranceNode:
    def __init__(self, brand: str, name: str, scent_category:[str], cost: str):
        self.brand = brand
        self.name = name
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

    def insert_word(self, word: str, current_node: TreeNode=None, depth=0):
            if current_node is None:
                current_node = self.root
            
            if depth == len(word):
                return

            letter = word[depth]

            if letter in current_node.children:
                next_node = current_node.children[letter]
            else:
                next_node = TreeNode(letter)
                current_node.children[letter] = next_node

            self.insert_word(word, next_node, depth+1)

    def find_words(self, word: str, current_node: TreeNode = None, current_word="", list_of_words=None):
        if list_of_words is None:
            list_of_words = []
        
        if current_node is None:
            current_node = self.root

        for letter in word:
            if letter not in current_node.children:
                return [None]
            
            current_node = current_node.children[letter]

        current_word += word

        def dfs(node, word_so_far):
            if not node.children:
                list_of_words.append(word_so_far)
                return

            for letter, child in node.children.items():
                dfs(child, word_so_far + letter)

        dfs(current_node, current_word)
        return list_of_words
          

        
# main
def main():
    print(ProgramRunner.intro_image)
    frag_finder = ProgramRunner(FRAG_FILE)
    frag_finder.get_filter_one()



if __name__ == "__main__":
    main()