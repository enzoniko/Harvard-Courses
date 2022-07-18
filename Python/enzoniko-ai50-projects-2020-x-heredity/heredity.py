import csv
import itertools
import sys
import math

PROBS = {

    # Unconditional probabilities for having gene
    "gene": {
        2: 0.01,
        1: 0.03,
        0: 0.96
    },

    "trait": {

        # Probability of trait given two copies of gene
        2: {
            True: 0.65,
            False: 0.35
        },

        # Probability of trait given one copy of gene
        1: {
            True: 0.56,
            False: 0.44
        },

        # Probability of trait given no gene
        0: {
            True: 0.01,
            False: 0.99
        }
    },

    # Mutation probability
    "mutation": 0.01
}

def main():

    # Check for proper usage
    if len(sys.argv) != 2:
        sys.exit("Usage: python heredity.py data.csv")
    people = load_data(sys.argv[1])

    # Keep track of gene and trait probabilities for each person
    probabilities = {
        person: {
            "gene": {
                2: 0,
                1: 0,
                0: 0
            },
            "trait": {
                True: 0,
                False: 0
            }
        }
        for person in people
    }

    # Loop over all sets of people who might have the trait
    names = set(people)
    for have_trait in powerset(names):

        # Check if current set of people violates known information
        fails_evidence = any(
            (people[person]["trait"] is not None and
             people[person]["trait"] != (person in have_trait))
            for person in names
        )
        if fails_evidence:
            continue

        # Loop over all sets of people who might have the gene
        for one_gene in powerset(names):
            for two_genes in powerset(names - one_gene):

                # Update probabilities with new joint probability
                p = joint_probability(people, one_gene, two_genes, have_trait)
                update(probabilities, one_gene, two_genes, have_trait, p)

    # Ensure probabilities sum to 1
    normalize(probabilities)

    # Print results
    for person in people:
        print(f"{person}:")
        for field in probabilities[person]:
            print(f"  {field.capitalize()}:")
            for value in probabilities[person][field]:
                p = probabilities[person][field][value]
                print(f"    {value}: {p:.4f}")

def load_data(filename):
    """
    Load gene and trait data from a file into a dictionary.
    File assumed to be a CSV containing fields name, mother, father, trait.
    mother, father must both be blank, or both be valid names in the CSV.
    trait should be 0 or 1 if trait is known, blank otherwise.
    """
    data = {}
    with open(filename) as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row["name"]
            data[name] = {
                "name": name,
                "mother": row["mother"] or None,
                "father": row["father"] or None,
                "trait": (True if row["trait"] == "1" else
                          False if row["trait"] == "0" else None)
            }
    return data

def powerset(s):
    """
    Return a list of all possible subsets of set s.
    """
    s = list(s)
    return [
        set(s) for s in itertools.chain.from_iterable(
            itertools.combinations(s, r) for r in range(len(s) + 1)
        )
    ]

def joint_probability(people, one_gene, two_genes, have_trait):
    """
    Compute and return a joint probability.

    The probability returned should be the probability that
        * everyone in set `one_gene` has one copy of the gene, and
        * everyone in set `two_genes` has two copies of the gene, and
        * everyone not in `one_gene` or `two_gene` does not have the gene, and
        * everyone in set `have_trait` has the trait, and
        * everyone not in set` have_trait` does not have the trait.
    """

    # List with all the probabilities
    each_person_probability = []

    # For each person in people, calculate the probability depending on the parents
    for person in list(people.values()):

        # If there are no parents registered for this person
        if person["mother"] is None and person["father"] is None:

            # Get the number of genes this person has
            gene = get_number_of_genes(person["name"], one_gene, two_genes)

            # Get the probability for trait
            no_parents_trait_probability = PROBS["trait"][gene][person["name"] in have_trait]

            # Get the probability for gene
            no_parents_gene_probability = PROBS["gene"][gene]

            # Get the total probability for this person and append it to the each_person_probability list
            each_person_probability.append(no_parents_gene_probability * no_parents_trait_probability)

        # If there are parents registered for this person
        if person["mother"] is not None and person["father"] is not None:

            # Get the number of genes this person has
            genes = get_number_of_genes(person["name"], one_gene, two_genes)

            # Get the probability that this person gets the gene from his mother
            mother_mutation_probability = get_mutation_probability(get_number_of_genes(person["mother"], one_gene, two_genes))

            # Get the probability that this person gets the gene from his father
            father_mutation_probability = get_mutation_probability(get_number_of_genes(person["father"], one_gene, two_genes))

            # Get the gene probability for the person
            gene_probability = get_child_gene_probability(genes, mother_mutation_probability, father_mutation_probability)
            
            # Get the trait probability for the person
            trait_probability = PROBS["trait"][genes][person["name"] in have_trait]

            # Get the total probability for this person and append it to the each_person_probability list
            each_person_probability.append(gene_probability * trait_probability)

    # Returns the joint probability of all of this events taking place
    # Therefore, the entire joint probability is just the result of multiplying all of the values from each person probability
    return math.prod(each_person_probability)   

def update(probabilities, one_gene, two_genes, have_trait, p):
    """
    Add to `probabilities` a new joint probability `p`.
    Each person should have their "gene" and "trait" distributions updated.
    Which value for each distribution is updated depends on whether
    the person is in `have_gene` and `have_trait`, respectively.
    """
    
    # For each person in the probabilities dictionary
    for person in probabilities:

        # Get the distribution for this person
        this_person_distribution = probabilities[person]
        
        # Update the gene probability for this person, the get_number_of_genes function gets the number of genes a person has
        this_person_distribution["gene"][get_number_of_genes(person, one_gene, two_genes)] += p

        # Update the trait probability for this person
        this_person_distribution["trait"][person in have_trait] += p

def normalize(probabilities):
    """
    Update `probabilities` such that each probability distribution
    is normalized (i.e., sums to 1, with relative proportions the same).
    """

    # For each person in the probabilities dictionary
    for person in probabilities:
    
        # Get the normalization factor for the trait distribution
        trait_normalization_factor = 1 / sum(list(probabilities[person]["trait"].values()))

        # Get the normalization factor for the gene distribution
        gene_normalization_factor = 1 / sum(list(probabilities[person]["gene"].values()))

        # Update each value in the trait distribution for this person 
        for trait in probabilities[person]["trait"]:

            # Multiply the value by the normalization factor
            probabilities[person]["trait"][trait] = probabilities[person]["trait"][trait] * trait_normalization_factor

        # Update each value in the gene distribution for this person
        for gene in probabilities[person]["gene"]:

            # Multiply the value by the normalization factor
            probabilities[person]["gene"][gene] = probabilities[person]["gene"][gene] * gene_normalization_factor

def get_number_of_genes(person, one_gene, two_genes):

    # Returns the number of genes this person has
    if person in one_gene:
        return 1
    return 2 if person in two_genes else 0

def get_mutation_probability(genes):

    # Returns the mutation probability this person has

    # If the person has 1 gene
    if genes == 1:

        # if a parent has one copy of the mutated gene, then the gene is passed on to the child with probability 0.5. 
        # After a gene is passed on, though, it has some probability of undergoing additional mutation: changing from a version of the gene that causes hearing impairment to a version that doesn’t, or vice versa.
        return (0.5 * (1 - PROBS["mutation"])) + (0.5 * PROBS["mutation"])
    
    # If the person has 2 genes
    if genes == 2:

        # If a parent has two copies of the mutated gene, then they will pass the mutated gene on to the child.
        # After a gene is passed on, though, it has some probability of undergoing additional mutation: changing from a version of the gene that causes hearing impairment to a version that doesn’t, or vice versa.
        return (1 - PROBS["mutation"])

    # If the person has 0 genes
    if genes == 0:

        # If a parent has no copies of the mutated gene, then they will not pass the mutated gene on to the child.
        # After a gene is passed on, though, it has some probability of undergoing additional mutation: changing from a version of the gene that causes hearing impairment to a version that doesn’t, or vice versa.
        return PROBS["mutation"]

def get_child_gene_probability(child_genes, mother_mutation_probability, father_mutation_probability):

    # If the child has 1 gene
    if child_genes == 1:

        # Return the total gene probability for the child
        # Either the child gets the gene from his mother and not his father, or he gets the gene from his father and not his mother
        return ((mother_mutation_probability * (1 - father_mutation_probability)) + (father_mutation_probability * (1 - mother_mutation_probability)))
    
    # If the child has 2 genes
    if child_genes == 2:

        # Return the total gene probability for the child
        # The child can only get two genes if both parents give one
        return (mother_mutation_probability * father_mutation_probability)

    # If the child has 0 genes
    if child_genes == 0:

        # Get the total gene probability for the child
        # The child can only get zero genes if both parents do not pass their genes
        return ((1 - mother_mutation_probability) * (1 - father_mutation_probability))

if __name__ == "__main__":
    main()
