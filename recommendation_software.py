"""
Game Name: Fragrance Recommender
Description: Type in a category of fragrance and we'll recommend some!
Author: Zachary Coe
Date: 2024-10-21
"""



import argparse
import csv



FRAG_FILE = "csv_folder/recommendation_list.csv"
SCENT_SIZE = 80
COST_SIZE = 6



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
    
    def __init__(self):
        self.fragrance_sample = FragranceNode("", "", [], "")
        self.data_handler = DataHandler()

    def get_filter_one(self):
        ignore_list = ["next_node", "name"]
        options = [key.replace("_"," ").title() for key in vars(self.fragrance_sample).keys() if key not in ignore_list]
        while True:     
            try:   
                print("Type a filter you'd like to sort by: ")
                filter = input().title()
                if filter in options:
                    filter = filter.replace(" ", "_").lower()
                    return filter
                else:
                    raise ValueError()
            except ValueError:
                print(f"Please select from: {options}")

    def get_cost_filter(self):
        options = self.data_handler.hashmaps["cost"]
        if isinstance(options, HashMap):
            dollar_sign_options = [item[0] for item in options.array if item[0]]
        while True:
            try:
                dollar_signs = input(f"Type between 1 and 4 '$': ")
                if dollar_signs in dollar_sign_options:
                    return dollar_signs
                else:
                    raise ValueError()
            except ValueError:
                print(f"Invalid input. Type {options}")

    def get_next_filter(self, first_filter):
        filtered_first_filter = first_filter.replace("_", " ").title()
        while True:
            print(f"Type the beginning letters of the {filtered_first_filter} and see if it's available: ")
            
            user_input = input().lower()
            options = self.data_handler.filter_chars.find_words(user_input)      
            
            if options == [None]:
                print("Sorry we didn't find anything!")
                continue

            if len(options) > 1:
                print(f"With those beginning letters your choices are {options}")
                continue

            if len(options) == 1:
                while True:
                    print(f"The only option with those beginning letters is {options[0].title()}. Do you\nwant to look at the {options[0].title()} perfumes?")
                    response = input().strip().lower()
                    
                    if response in {"y", "ye", "yes"}:
                        return options[0].lower()
                    elif response in {"n", "no"}:
                        break
                    else:
                        print("Invalid input. Please type 'yes' or 'no'.")
    
    # Combines get_first and get_next and adds control flow
    def get_all_filters(self):
        first_filter = self.get_filter_one()
        if first_filter == "cost":
            if "cost" not in self.data_handler.hashmaps:
                self.data_handler.create_hashmap(first_filter, COST_SIZE)
            return first_filter, self.get_cost_filter()
        else:
            if first_filter not in self.data_handler.hashmaps:
                self.data_handler.create_hashmap(first_filter, SCENT_SIZE)
            return first_filter, self.get_next_filter(first_filter)
        
    def print_filtered_content(self, first_filter, second_filter):
        list_of_data = self.data_handler.retrieve_data(first_filter, second_filter)
        current_node = list_of_data.get_head_node()
        while current_node:
            print(current_node)
            current_node = current_node.next_node
        print("\n------------------------------\n")

    def again(self):
        while True:
            print("Would you like to find more fragrances?")
            
            response = input()
            if response in {"y", "ye", "yes"}:
                return True
            elif response in {"n", "no"}:
                return False
            else:
                print("Invalid input. Please type 'yes' or 'no'.")
        
class DataHandler:
    def __init__(self):
        self.filename = self.parse_args()
        self.headers, self.data = self.load_data(self.filename)
        self.hashmaps = {}

    def parse_args(self):
        parser = argparse.ArgumentParser()
        parser.add_argument("--file", type=str, default=FRAG_FILE, help="Input a file to be read")
        args = parser.parse_args()
        return args.file

    def load_data(self, filename):
        with open(filename, mode='r', encoding='utf-8') as file:
            csv_reader = csv.reader(file)
            headers = next(csv_reader)
            data = list(csv_reader)

        return headers, data

    def create_hashmap(self, filter_category, size):
        # Creates new wordtree and assigns new hashmap to corresponding dict key
        self.filter_chars = WordTree()
        headers = self.headers
        data = self.data
        hashmap = HashMap(size)
        self.hashmaps[f"{filter_category}"] = hashmap

        # Used to set the filters for each node
        header_map = {
            "Brand": headers.index("House"),
            "Name": headers.index("Perfume"),
            "Scent Categories": headers.index("Accords"),
            "Cost": headers.index("Cost")
        }
        
        for row in data:

            brand = row[header_map["Brand"]]
            name = row[header_map["Name"]]
            scent_categories = row[header_map["Scent Categories"]].split("; ")
            cost = row[header_map["Cost"]]

            frag_node = FragranceNode(brand, name, scent_categories, cost)
            for key, value in frag_node.__dict__.items():
                if key == filter_category:
                    # If attribute of node has more than one value (e.g. scent_category)
                    if isinstance(value, list):
                        for attribute in value:
                            # Assigns to hashmap/adds word to wordtree
                            self.filter_chars.insert_word(attribute)
                            hashmap.assign(attribute, FragranceNode(brand, name, scent_categories, cost))

                    else:
                        # Assigns to hashmap/adds word to wordtree
                        self.filter_chars.insert_word(value)
                        hashmap.assign(value, FragranceNode(brand, name, scent_categories, cost))

    def retrieve_data(self, main_category, filter):
        hashmap = self.hashmaps[f"{main_category}"]
        return hashmap.retrieve(filter)

class FragranceNode:
    def __init__(self, brand: str, name: str, scent_category:[str], cost: str):
        self.brand = brand
        self.name = name
        self.scent_category = scent_category
        self.cost = cost
        self.next_node = None

    def __str__(self):
        accords = f"{self.scent_category[0].title()}"
        for n in range(1, len(self.scent_category)):
            accords = accords + f", {self.scent_category[n].title()}"

        frag_string = f"""
------------------------------

Name: {self.name}
Brand: {self.brand}
Accords: {accords}
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
        self.array = [None for _ in range(array_size)]

    def hash(self, key, count_collisions=0):
        hash_code = hash(key)
        return hash_code + count_collisions

    def compressor(self, hash_code):
        return hash_code % self.array_size
    
    def assign(self, key, frag_node):
        key = key.lower()

        number_collisions = 0
        
        while True:
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

    def retrieve(self, key):
        key = key.lower()
        retrieval_collisions = 0
       
        while retrieval_collisions < self.array_size:

            hash_code = self.hash(key, retrieval_collisions)
            array_index = self.compressor(hash_code)

            possible_return_value = self.array[array_index]

            if possible_return_value is None:
                return None
            if possible_return_value[0] == key:
                return possible_return_value[1]
            
            retrieval_collisions += 1

        return None

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

            letter = word[depth].lower()

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
        list_of_words = [word.title() for word in list_of_words]
        return list_of_words
          

        
def main():
    print(ProgramRunner.intro_image)
    frag_finder = ProgramRunner()
    while True:
        first_filter, next_filter = frag_finder.get_all_filters()
        frag_finder.print_filtered_content(first_filter, next_filter)
        if not frag_finder.again():
            break
    

if __name__ == "__main__":
    main()