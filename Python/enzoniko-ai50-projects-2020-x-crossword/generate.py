import sys

from crossword import *
import copy
import random


class CrosswordCreator():

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size,
             self.crossword.height * cell_size),
            "black"
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        w, h = draw.textsize(letters[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill="black", font=font
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency()
        self.ac3()
        return self.backtrack(dict())

    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """
        
        # For each variable in the crossword
        for variable in self.crossword.variables:

            # Create a list of words that should be removed from the variable's domain later
            node_inconsistent_words = [
                word
                for word in self.domains[variable]
                if len(word) != variable.length
            ]


            # For each word in the node_inconsistent_words list     
            for word in node_inconsistent_words:

                # Remove the word from the variable's domain
                self.domains[variable].remove(word)   

    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """

        # Get the overlap, if any, between x and y variables.
        overlap = self.crossword.overlaps[x, y]

        # Create a list of values that will be removed from x's domain
        arc_inconsistent_values = []

        if overlap is None:
            return False

        # For every value in x’s domain
        for x_value in self.domains[x]:

            overlap_possible = any(
                x_value != y_value and x_value[overlap[0]] == y_value[overlap[1]]
                for y_value in self.domains[y]
            )

            # If no overlap is possible
            if not overlap_possible:

                # Append the x value to the arc_inconsistent_values to be removed later
                arc_inconsistent_values.append(x_value)

        # For every arc inconsistent x value 
        for x_value in arc_inconsistent_values:

            # Remove the x value from the x's domain
            self.domains[x].remove(x_value)
            # print("removed: ", x_value, "from :", x)

        # Returns if we made changes or not
        return len(arc_inconsistent_values) > 0

    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """

        # If arcs are not specified
        if arcs is None:
            
            # Initial queue of all arcs in the problem
            queue = []

            # Loop through all variables
            for X in self.crossword.variables:

                # Loop through all neighbor variables of X
                queue.extend((X, Y) for Y in self.crossword.neighbors(X))
        else:

            # While arcs is not empty
            while len(arcs) > 0:

                # Pop an arc from the queue
                (X, Y) = arcs.pop(0)

                # Run the revise algorithm in this arc
                # If the arc was revised
                if self.revise(X, Y):

                    # If there is nothing in X's domain
                    if len(self.domains[X]) == 0:

                        # Returns false since the constraint satisfaction problem is unsolvable
                        return False

                    # If there is something in X's domain
                    # For all variables that are neighbors of X except Y
                    for Z in self.crossword.neighbors(X) - {Y}:

                        # Append a new arc to the queue with Z and X
                        arcs.append((Z, X))

        # If the queue is empty and each variable is arc consistent
        # Returns true
        return True

    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """

        # If the assignment has the same number o variables as the total number of variables in the crossword
        return len(assignment) == len(self.crossword.variables)
 
    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """
    
        # Return false if all the values are not distinct
        if len(set(list(assignment.values()))) != len(list(assignment.values())):
            return False

        # For each variable in the assignment
        for variable in assignment:

            # If the variable length is not equal to the value length
            if variable.length != len(assignment[variable]):

                # Return false if the value does not have the correct length
                return False
 
            # Get the neighbors for the variable we are checking 
            neighbors = self.crossword.neighbors(variable)

            # For each neighbor
            for neighbor in neighbors:

                # If the neighbor is in the assignment
                if neighbor in assignment:
                    
                    # Get where the variable value and the neighbor value we are checking overlap
                    overlap = self.crossword.overlaps[variable, neighbor]

                    # Make sure that they actually overlap at the characters provided
                    # If the characters provided of each variables value is not equal
                    if assignment[variable][overlap[0]] != assignment[neighbor][overlap[1]]:

                        # Return false, because they are conflicting
                        return False

        # Returns true after not finding inconsitencies
        return True
            
    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """

        # Dictionary where the keys are words and the values are the number of values they rule out of neighboring variables
        n = {}

        # For each value in the var's domain
        for value in self.domains[var]:

            # Create a key with the word and start the value as zero
            n[value] = 0

            # For each neighbor of the var except those in the assignment
            for neighbor in self.crossword.neighbors(var) - set(assignment.keys()):

                # For each value in the domain of the neighbor we are checking
                for neighbor_value in self.domains[neighbor]:

                    # If by assigning the value to the var the overlaped character in the neighbor value is not equal and the both values are not the same words
                    if value[self.crossword.overlaps[var, neighbor][0]] != neighbor_value[self.crossword.overlaps[var, neighbor][1]] and value != neighbor_value:

                        # Increase the number of words ruled out of neighboring variables for this value
                        n[value] += 1  

        # Returns a list of all of the values in the domain of the variable sorted by the number of values they rule out of neighboring variables           
        return sorted(n, key = n.get)

    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        # Unassigned variables list
        unassigned_variables = [
            variable
            for variable in self.crossword.variables
            if variable not in list(assignment.keys())
        ]


        # Sort the unassigned variables list by the fewest number of remaining values in each variable's domain in ascending order
        unassigned_variables.sort(key = lambda remaining_values: len(self.domains[remaining_values]))

        # Sort the new unassigned variables list by the number of neighbors in descending order
        unassigned_variables.sort(key = lambda remaining_values: len(self.crossword.neighbors(remaining_values)), reverse = True)

        # Return the first item of the unassigned variables list
        # The first item has the fewest number of remaining values in its domain and has the most neighbors
        return unassigned_variables[0]

    def inferences(self, variable, assignment):

        # Get a copy of the domains
        old_domains = copy.deepcopy(self.domains)

        arcs = [(Y, variable) for Y in self.crossword.neighbors(variable)]
        # Enforce arc-consistency in this arcs
        # If everything is arc consistent
        if self.ac3(arcs=arcs) and self.domains != old_domains:
                # Create an empty inferences dict
            inferences = {
                variable: next(iter(self.domains[variable]))
                for variable in self.domains
                if len(self.domains[variable]) == 1 and variable not in assignment
            }


                # If the inferences dict is empty
            return inferences or None
        # If the ac3 function is False, return None (failure)
        return None
        
    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """
        # Check if assignment is complete
        if self.assignment_complete(assignment):
            return assignment

        # Select a variable that does not have an assignment yet
        variable = self.select_unassigned_variable(assignment)

        # For each value in the variable's domain
        for value in self.order_domain_values(variable, assignment):

            # Assign a value to the variable
            assignment[variable] = value

            # Get the inferences that can be made
            inferences = self.inferences(variable, assignment) 

            # If the resulting assignment is consistent
            if self.consistent(assignment):

                # If inferences can be made
                if inferences is not None:
                    
                    # For each inference
                    for inference in inferences:

                        # Append the inference to the assignment
                        assignment[inference] = inferences[inference]

                        # print("Added: ", inference, inferences[inference], "to assignment")

                # Run backtrack in the resulting assignment
                result = self.backtrack(assignment)
                
                # If the result is not a failure
                if result is not None:

                    # Returns the result
                    return result

            # Pop the variable from the assignment if it was not a good choice
            assignment.pop(variable)
        
            # Pop all inferences from the assignment if it was not a good choice
            if inferences is not None:

                # For each inference
                for inference in inferences:
                    
                    # Pop it from the assignment
                    assignment.pop(inference)
                    
        # Otherwise returns none (failure)
        return None

def main():

    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main()
