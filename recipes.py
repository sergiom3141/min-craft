import re
import pickle
import sys
from math import ceil


class recipe:

	def __init__(self,name,recipeyield,componentlist):
		self.name = name
		self.recipeyield = recipeyield
		self.componentlist = componentlist

	def printRecipe(self):
		finalString = str(self.recipeyield)
		finalString += ' '
		finalString += self.name
		finalString += ' = '
		finalString += str(self.componentlist)
		return(finalString)

	def calc_num_required(recipe,n):

		'''
		Takes recipe and the number of that item required.
		Produces dictionary of all the ingredients and the number of
		those ingredients required.
		'''
		
		if recipe not in recipeBook:
			return n

		component_list = recipeBook[recipe].componentlist
		recipe_yield = recipeBook[recipe].recipeyield
		num_recipes_needed = ceil(n / recipe_yield)
		num_components_required = {}

		for component in component_list:
			num_components_required[component] = num_recipes_needed * component_list[component]

		return num_components_required

	def DFS(recipeGraph,currentRecipe,postorderlist,visited):

		'''
		Produces a postorder list of recipes for a recipe called
		currentRecipe in the recipeGraph of all recipes
		'''
		
		if currentRecipe not in recipeGraph:
			postorderlist.append(currentRecipe)
			return

		for ingredient in recipeGraph[currentRecipe]:
			if ingredient not in visited or visited[ingredient] == False:
				recipe.DFS(recipeGraph,ingredient,postorderlist,visited)

		visited[currentRecipe] = True
		postorderlist.append(currentRecipe)
		return

	def reverse_postorder(postorderlist):

		'''
		Takes postorderlist and reverses it.
		Produces an index dictionary that gives an index for each item
		in the reverse postorder list.

		Returns reverse postorder list and list of indices into reverse
		postorder list.
		'''
		
		index = {}
		reversepostorderlist = postorderlist[::-1]
		for i in range(len(reversepostorderlist)):
			currentItem = reversepostorderlist[i]
			index[currentItem] = i
		return (reversepostorderlist,index)


	def relax_comp_req(reversepostorderlist,index,n):

		'''
		Takes reverse postorder list, dictionary of indices of items
		in the list, and the number n required for the first item

		Returns the relaxed requirements for each component and
		the reverse topological ordering, which is in the order
		of dependencies of the recipes. Max dependencies first.
		'''
		
		postreqs = [0 for i in range(len(reversepostorderlist))]
		postreqs[0] = n
		reverse_topo_order = []
		componentList = reversepostorderlist

		for i in range(len(reversepostorderlist)-1):
			currentItem = reversepostorderlist[i]
			
			if currentItem in recipeBook:
				requiredComponents = recipe.calc_num_required(currentItem,n)
				reverse_topo_order.append({currentItem:requiredComponents})
				
				for comp in requiredComponents:
					currentIndex = index[comp]
					itemToRelax = reversepostorderlist[currentIndex]
					postreqs[currentIndex] += requiredComponents[comp]

		return postreqs,reverse_topo_order
		
	def base_resources(postreqs,reversepostorderlist):
		baseresources = {}
		
		for i in range(len(reversepostorderlist)):
			item = reversepostorderlist[i]
			
			if item not in recipeBook:
				baseresources[item] = postreqs[i]
				
		return baseresources

	def calc_crafted_items(craftedItem, ingredient, numIngredient):
		currentRecipe = recipeBook[craftedItem]
		numberCraftedPerRecipe = currentRecipe.recipeyield
		numIngredientInRecipe = currentRecipe.componentList[ingredient]
		return numIngredient * numberCraftedPerRecipe // numIngredientInRecipe

	def print_topo_order(topologicalorder, relaxedrequirements):
		
		for i in range(len(topologicalorder)-1,-1,-1):
			currentCraft = topologicalorder[i]
			numIngredient = relaxedrequirements[i]
			currentRecipeString = ''
			
			for ingredientname in currentCraft.keys():
				currentRecipeString += str(ingredientname) + " = " + str(currentCraft[ingredientname])
				print(currentRecipeString)



recipeBook = {}
with open('/home/sergio/Dropbox (MIT)/scripts/projects/minCraft/recipeData','rb') as data:
	recipeBook = pickle.load(data)
with open('/home/sergio/Dropbox (MIT)/scripts/projects/minCraft/recipeGraph','rb') as data:
	recipeGraph = pickle.load(data)

