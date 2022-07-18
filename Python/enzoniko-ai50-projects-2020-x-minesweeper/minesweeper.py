import itertools
import random


class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=15, width=15, mines=30):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for _ in range(self.height):
            row = [False for _ in range(self.width)]
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i, j in itertools.product(range(cell[0] - 1, cell[0] + 2), range(cell[1] - 1, cell[1] + 2)):
            # Ignore the cell itself
            if (i, j) == cell:
                continue

                # Update count if cell in bounds and is mine
            if 0 <= i < self.height and 0 <= j < self.width and self.board[i][j]:
                count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count
    
    # For removing duplicates later
    # Commented for the assignment
    # def __hash__(self):
        #return self.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """

        # If the number of cells in the sentence is equal to the count of mines, then all the cells are mines, returns them
        return self.cells if len(self.cells) == self.count else None

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """

        # If the count of mines is zero, then all the cells are safe, returns them
        return self.cells if len(self.cells) > 0 and self.count == 0 else None
        

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """

        # If the cell is in the sentence
        if cell in self.cells:
            # Remove it from the sentence since the cell is a mine
            self.cells.remove(cell)
            # Reduce the count number since one of the mines was discovered
            self.count -= 1
            return 1
        return 0

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """

        # If the cell is in the sentence
        if cell in self.cells:
            # Remove it from the sentence since the cell is safe
            self.cells.remove(cell)
            return 1
        return 0


class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=15, width=15):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """

        # Mark the cell as a move that has been made
        self.moves_made.add(cell)

        # Mark the cell as a safe cell, and update all sentences
        self.mark_safe(cell)

        # Empty neighbours list
        neighbours = []

        # Loop over all cells within one row and column
        for i, j in itertools.product(range(cell[0] - 1, cell[0] + 2), range(cell[1] - 1, cell[1] + 2)):
            # Ignore the cell itself
            if (i, j) == cell:
                continue

                # Update count if cell in bounds and cell is not a move made
            if (
                0 <= i < self.height
                and 0 <= j < self.width
                and (i, j) not in self.moves_made
            ):
                neighbours.append((i, j))

        # Add new sentence to the knowledge base, this sentence contains the neighbours of the provided cell and the count of mines
        self.knowledge.append(Sentence(neighbours, count))

        # Debug:
        # print("Moves Made:")
        # print(self.moves_made)
        # print("Safes:")
        # print(self.safes)
        # print("Mines:")
        # print(self.mines)
        # print("Sentences:")

        # Clean up the knowledge
        garbage = [sentence for sentence in self.knowledge if len(sentence.cells) == 0]

        # Remove possible duplicates from the knowledge
        # Using hash function in the Sentence class
        # I commented it for the assignment
        # self.knowledge = list(set(self.knowledge))

        # For each sentence is the garbage, remove it from the knowledge
        for sentence in garbage:
            if sentence in self.knowledge:
                self.knowledge.remove(sentence)

        # Temporary copy of the knowledge
        temp_knowledge = self.knowledge.copy()

        # Update values
        self.update()

        # While the temporary copy is different than the knowledge after the update
        while self.knowledge != temp_knowledge:

            # Re-assign the temporary knowledge and update again
            temp_knowledge = self.knowledge.copy()
            self.update()
        return

    # Update function
    def update(self):

        # If there are mines in self.mines
        if len(self.mines) != 0:

            # Mark each mine as a mine in the knowledge
            for mine in self.mines:
                self.mark_mine(mine)

        # If there are safes in self.safes
        if len(self.safes) != 0:

            # Mark each safe as a safe in the knowledge
            for safe in self.safes:
                self.mark_safe(safe)

        # If there are knowledge in self.knowledge
        if len(self.knowledge) != 0:

            # For each sentence in the knowledge
            for sentence in self.knowledge:

                # If there are safes in the sentence
                if sentence.known_safes() is not None:

                    # Update self.safes with the known safes from the sentence
                    self.safes = self.safes.union(sentence.known_safes())

                # If there are mines in the sentence
                if sentence.known_mines() is not None:

                    # Update self.mines with the known mines from the sentence
                    self.mines = self.mines.union(sentence.known_mines())

        # If there are more than 1 sentence in the knowledge
        if len(self.knowledge) > 1:

            # Empty list for temporary knowledge
            temp_knowledge = []

            # For each sentence in the knowledge base
            for super_sentence in self.knowledge:

                # Loops through all the sentences in the knowledge base again
                temp_knowledge.extend(
                    Sentence(
                        super_sentence.cells.difference(sub_sentence.cells),
                        super_sentence.count - sub_sentence.count,
                    )
                    for sub_sentence in self.knowledge
                    if sub_sentence.cells.issubset(super_sentence.cells)
                    and super_sentence != sub_sentence
                )

            # For each sentence in the temporary knowledge list
            for temp_sentence in temp_knowledge:

                # If the sentence is not already in the knowledge base
                if temp_sentence not in self.knowledge:

                    # Append the sentence
                    self.knowledge.append(temp_sentence)

        return 1

    """
    # First try, not completed...
        safes = []
        # For each sentence in the knowledge base
        for sentence in self.knowledge:

            # If there are known safes in the sentence
            if sentence.known_safes() is not None:

                # Mark each safe as a safe
                for safe in sentence.known_safes():
                    safes.append(safe)
                for safe in safes:
                    self.mark_safe(safe)
                safes.clear()

        mines = []
        # For each sentence in the knowledge base
        for sentence in self.knowledge:
            
            # If there are known mines in the sentence
            if sentence.known_mines() is not None:

                # Mark each mine as a mine
                for mine in sentence.known_mines():
                    mines.append(mine)
                for mine in mines:
                    self.mark_mine(mine)
                mines.clear()

        # For each sentence in the knowledge base
        for sentence in self.knowledge:

            # Loops through all the sentences in the knowledge base again
            for other_sentence in self.knowledge:

                # If a sentence is subset of another sentence
                if other_sentence.cells.issubset(sentence.cells) and sentence != other_sentence:

                    # Add to the knowledge base a new sentence using the subset method described in the background
                    self.knowledge.append(Sentence(sentence.cells.difference(other_sentence.cells), sentence.count - other_sentence.count))
    """
    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """

        if safes := [safe for safe in self.safes if safe not in self.moves_made]:
            return random.choice(safes)

        # Else returns None
        return None


    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        
        if available_moves := [
            (i, j)
            for i, j in itertools.product(range(self.height), range(self.width))
            if (i, j) not in self.moves_made and (i, j) not in self.mines
        ]:
            return random.choice(available_moves)

        # Else returns None
        return None
    
