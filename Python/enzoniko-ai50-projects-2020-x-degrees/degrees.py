import csv
import sys

from util import Node, StackFrontier, QueueFrontier

# Maps names to a set of corresponding person_ids
names = {}

# Maps person_ids to a dictionary of: name, birth, movies (a set of movie_ids)
people = {}

# Maps movie_ids to a dictionary of: title, year, stars (a set of person_ids)
movies = {}


def load_data(directory):
    """
    Load data from CSV files into memory.
    """
    # Load people
    with open(f"{directory}/people.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            people[row["id"]] = {
                "name": row["name"],
                "birth": row["birth"],
                "movies": set()
            }
            if row["name"].lower() not in names:
                names[row["name"].lower()] = {row["id"]}
            else:
                names[row["name"].lower()].add(row["id"])

    # Load movies
    with open(f"{directory}/movies.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            movies[row["id"]] = {
                "title": row["title"],
                "year": row["year"],
                "stars": set()
            }

    # Load stars
    with open(f"{directory}/stars.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                people[row["person_id"]]["movies"].add(row["movie_id"])
                movies[row["movie_id"]]["stars"].add(row["person_id"])
            except KeyError:
                pass


def main():
    if len(sys.argv) > 2:
        sys.exit("Usage: python degrees.py [directory]")
    directory = sys.argv[1] if len(sys.argv) == 2 else "large"

    # Load data from files into memory
    print("Loading data...")
    load_data(directory)
    print("Data loaded.")

    source = person_id_for_name(input("Name: "))
    if source is None:
        sys.exit("Person not found.")
    target = person_id_for_name(input("Name: "))
    if target is None:
        sys.exit("Person not found.")
    if source == target:
        sys.exit("Same person.")

    path = shortest_path(source, target)

    if path is None:
        print("Not connected.")
    else:
        degrees = len(path)
        print(f"{degrees} degrees of separation.")
        path = [(None, source)] + path
        for i in range(degrees):
            person1 = people[path[i][1]]["name"]
            person2 = people[path[i + 1][1]]["name"]
            movie = movies[path[i + 1][0]]["title"]
            print(f"{i + 1}: {person1} and {person2} starred in {movie}")


def shortest_path(source, target):
    """
    Returns the shortest list of (movie_id, person_id) pairs
    that connect the source to the target.
    If no possible path, returns None.
    1. Start with an empty Queue-Frontier
    2. Add initial state to the frontier
    3. Start with an empty explored set
    4 Loop
    4.1 if the frontier is empty, return none
    4.2 remove a node from the frontier
    4.3 Add the node to the explored set
    4.4 Expand the node by getting neighbours (neighbours_for_person)
    4.5 if neighbor contains goal state, return solution
    4.6 Add neighbor nodes to the frontier if they aren't already in the there or in the explored set
    """
    # Initialize frontier that uses breadth-first search to find the shortest path
    start = Node(state = source, parent = None, action=None)
    frontier = QueueFrontier()
    frontier.add(start)

    explored = set()

    # Keep looping until solution found
    while True:

        # If frontier is empty, return None
        if frontier.empty():
            return None
        
        # Remove a node from the frontier
        node = frontier.remove()

        # Add the node to the explored set
        explored.add(node.state)

        # Expand the node by getting neighbours
        for movie, actor in neighbors_for_person(node.state):

            # If they aren't already in the frontier or in the explored set
            if not frontier.contains_state(actor) and actor not in explored:

                # Store them in a node called child
                child = Node(state = actor, parent = node, action = movie)

                # If child contains the goal state, return the solution
                if child.state == target:
                    path = []

                    # While the child has a parent node, do Backtracking
                    while child.parent is not None:
                        # Append a touple of movie_id and Person_id to the path
                        path.append((child.action, child.state))

                        # Set the parent as the current child
                        child = child.parent
                    
                    # Reverse the path so it is in the right order
                    path.reverse()

                    # Return the solution
                    return path

                # If child doesn't contain the goal state
                else:

                    # Add the child to the frontier
                    frontier.add(child)
        



def person_id_for_name(name):
    """
    Returns the IMDB id for a person's name,
    resolving ambiguities as needed.
    """
    person_ids = list(names.get(name.lower(), set()))
    if not person_ids:
        return None
    elif len(person_ids) > 1:
        print(f"Which '{name}'?")
        for person_id in person_ids:
            person = people[person_id]
            name = person["name"]
            birth = person["birth"]
            print(f"ID: {person_id}, Name: {name}, Birth: {birth}")
        try:
            person_id = input("Intended Person ID: ")
            if person_id in person_ids:
                return person_id
        except ValueError:
            pass
        return None
    else:
        return person_ids[0]


def neighbors_for_person(person_id):
    """
    Returns (movie_id, person_id) pairs for people
    who starred with a given person.
    """
    movie_ids = people[person_id]["movies"]
    neighbors = set()
    for movie_id in movie_ids:
        for person_id in movies[movie_id]["stars"]:
            neighbors.add((movie_id, person_id))
    return neighbors


if __name__ == "__main__":
    main()
