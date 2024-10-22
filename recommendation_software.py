"""
Game Name: Fragrance Recommender
Description: Type in a category of fragrance and we'll recommend some!
Author: Zachary Coe
Date: 2024-10-21
"""



# imports
import csv


# constants



# classes
class FragranceNode:
    def __init__(self, name: str, brand: str, cost: str, scent_category:[str]):
        self.name = name
        self.brand = brand
        self.cost = cost
        self.scent_category = scent_category
        self.next_node = None

    def set_next_node(self, next_node):
        self.next_node = next_node

class LinkedList:
    def __init__(self, name: str, brand: str, cost: str, scent_category: str):
        self.head_node = FragranceNode(name, brand, cost, scent_category)

    def get_head_node(self):
        return self.head_node
    
    def insert_beginning(self, name: str, brand: str, cost: str, scent_category: str):
        new_node = FragranceNode(name, brand, cost, scent_category)
        new_node.set_next_node(self.head_node)
        self.head_node = new_node

class CategoryHashMap:
    pass

# main
def main():
    return


if __name__ == "__main__":
    main()