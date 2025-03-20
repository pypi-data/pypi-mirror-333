import os
import numpy as np
import sympy as sp
from scipy.linalg import null_space
import libsbml
from .utils import extract_species, from_str_to_list, flatten_list, parse_string_to_reaction_list


def contains_all(list1, list2):
    return all(element in list1 for element in list2)


def proj_mat(xsub, xall):
    mask = np.isin(xall, xsub)
    return np.diag(mask.astype(int))


def proj_mat_comp(xsub, xall):
    I = np.identity(len(xall))
    return I - proj_mat(xsub, xall)


def dimker(mat):
    nullspace = null_space(np.array(mat))
    return nullspace.shape[1]


def dimcoker(mat):
    nullspace = null_space(np.array(mat).T)
    return nullspace.shape[1]


def random_nonzero_or_zero(element, range_vals=(1., 5.)):
    return np.random.uniform(*range_vals) if element != 0 else 0.


def randomize_nonzero_entries(matrix):
    nonzero_mask = matrix != 0
    random_numbers = np.random.uniform(1., 1.5, size=matrix.shape)
    return np.where(nonzero_mask, random_numbers, 0)


def make_hashable(obj):
    if isinstance(obj, (tuple, list)):
        return tuple((make_hashable(e) for e in obj))
    elif isinstance(obj, np.ndarray):
        return tuple(obj.tolist())
    else:
        return obj


def remove_duplicates(lst):
    seen = set()
    new_lst = []
    for item in lst:
        hashable_item = make_hashable(item)
        if hashable_item not in seen:
            seen.add(hashable_item)
            new_lst.append(item)
    return new_lst


def get_indices_of_element(the_list, element):
    return [index for index, item in enumerate(the_list) if item == element]


def from_lbs_to_bs(lbs):
    return [lbs[1], sorted(lbs[2] + lbs[3])]


def nonzero_with_error(arr, ep=1e-5):
    return np.where(np.abs(arr) > ep)[0]


def get_intersection(l1, l2):
    """
    Calculates the intersection of two lists of vectors.

    Args:
        l1 (list): The first list of vectors.
        l2 (list): The second list of vectors.

    Returns:
        numpy.ndarray: The intersection of the two lists of vectors.
    """
    n_l1, n_l2 = len(l1), len(l2)
    if n_l1 == 0 or n_l2 == 0:
        return np.array([])
    A = np.array(l1).transpose()
    B = np.array(l2).transpose()
    C = np.hstack((A,-B))
    U = null_space(C)
    return (A @ U[:n_l1]).transpose()


def get_intersection_symb(l1, l2):
    """
    Calculates the intersection of two symbolic matrices.

    Parameters:
    l1 (numpy.ndarray): The first symbolic matrix.
    l2 (numpy.ndarray): The second symbolic matrix.

    Returns:
    numpy.ndarray: The intersection of the two symbolic matrices.
    """
    n_l1, n_l2 = l1.shape[0], l2.shape[0]

    if n_l1 == 0 and n_l2 == 0:
        return sp.zeros(0,0)
    elif n_l1 == 0 or n_l1==0:
        return sp.zeros(0, l1.shape[1])

    A = sp.Matrix(l1).T
    B = sp.Matrix(l2).T
    C = A.row_join(-B)
    U = C.nullspace()
    if not U:
        return sp.zeros(0, l1.shape[1])

    U_matrix = sp.Matrix.hstack(*U)
    intersection = A * U_matrix[:n_l1, :]
    return intersection.T


def get_orthogonal_complement(l1):
    """
    Calculates the orthogonal complement of a given vectors.

    Parameters:
    l1 (list or numpy.ndarray): The input vectors

    Returns:
    numpy.ndarray: The orthogonal complement of the input vectors.
    """
    A = np.array(l1)
    if A.shape[0] == 0:
        return np.identity(A.shape[1])
    U = null_space(A)
    return U.transpose()


def get_orthogonal_complement_symb(l1):
    """
    Compute the orthogonal complement of a given list of vectors.

    Parameters:
    l1 (list or matrix): The input vectors.

    Returns:
    matrix: The orthogonal complement of the input vectors.
    """
    A = sp.Matrix(l1)
    if A.rows == 0:
        return sp.eye(A.cols)
    U = A.nullspace()
    if not U:
        return sp.zeros(0, A.cols)
    U_matrix = sp.Matrix.hstack(*U)
    return U_matrix.T


def sbml_to_reaction_list(sbml_file):
    reader = libsbml.SBMLReader()
    document = reader.readSBML(sbml_file)
    model = document.getModel()

    list_reactions = []

#    print("Number of reactions (SBML): ", model.getNumReactions())

    for i in range(model.getNumReactions()):
        reaction = model.getReaction(i)
        reactants = []
        products = []

        for reactant in reaction.getListOfReactants():
            species_id = reactant.getSpecies()
            stoichiometry = reactant.getStoichiometry()
            is_boundary = model.getSpecies(species_id).getBoundaryCondition()
            if not is_boundary:
                reactants.append([species_id, stoichiometry])

        for modifier in reaction.getListOfModifiers():
            species_id = modifier.getSpecies()
            stoichiometry = 1
            is_boundary = model.getSpecies(species_id).getBoundaryCondition()
            if not is_boundary:
                reactants.append([species_id, stoichiometry])

        if len(reactants) == 0:
            reactants.append(['', 1])

        for product in reaction.getListOfProducts():
            species_id = product.getSpecies()
            stoichiometry = product.getStoichiometry()
            is_boundary = model.getSpecies(species_id).getBoundaryCondition()
            if not is_boundary:
                products.append([species_id, stoichiometry])

        if len(reaction.getListOfProducts()) == 0:
            products.append(['', 1])

        list_reactions.append([reactants, products])

        if reaction.getReversible():
            list_reactions.append([products, reactants])
    
    return list_reactions


def transpose(matrix): # transpose a list of lists
    return list(map(list, zip(*matrix)))


def compute_nullspace(mat, mode='dense'):
    if mode == 'dense':
        return null_space(mat)
    # elif mode == 'sparse':
    #     return iterative_null_space(csr_matrix(mat))
    else:
        raise ValueError("Invalid mode. Choose either 'dense' or 'sparse'.")


def deep_compare(lst1, lst2):
    if type(lst1) != type(lst2):
        print("Type mismatch:", lst1, lst2)
        return False
    if isinstance(lst1, list) and isinstance(lst2, list):
        if len(lst1) != len(lst2):
            print("Length mismatch:", lst1, lst2)
            return False
        for i, (sub_lst1, sub_lst2) in enumerate(zip(lst1, lst2)):
            if not deep_compare(sub_lst1, sub_lst2):
                print(f"Mismatch found in list at index {i}: {sub_lst1} != {sub_lst2}")
                return False
        return True
    elif isinstance(lst1, np.ndarray) and isinstance(lst2, np.ndarray):
        if lst1.shape != lst2.shape:
            print("Shape mismatch:", lst1.shape, lst2.shape)
            return False
        comparison = np.array_equal(lst1, lst2)
        if not comparison:
            print("Array value mismatch")
        return comparison
    else:
        comparison = lst1 == lst2
        if isinstance(comparison, np.ndarray):
            if not comparison.all():
                print("Direct value mismatch in arrays:", lst1, lst2)
            return comparison.all()
        else:
            if not comparison:
                print("Direct value mismatch:", lst1, lst2)
            return comparison



class ReactionSystem:
    """
    Represents a reaction system. Implements functions for finding RPA properites of a reaction system.

    Attributes:
    - species (list): The list of species.
    - nr (int): The number of reactions.
    - ns (int): The number of species.
    - ind (dict): The dictionary mapping species to their indices.
    - rmat (numpy.ndarray): The reaction matrix.
    - pmat (numpy.ndarray): The product matrix.
    - smat (numpy.ndarray): The stoichiometric matrix.
    - cmat (numpy.ndarray): The nullspace matrix of smat.
    - dmat (numpy.ndarray): The nullspace matrix of smat transposed.

    Methods:
    - enumerate_labeled_buffering_structures: Enumerates labeled buffering structures.
    - enumerate_labeled_buffering_structures_by_name: Enumerates labeled buffering structures (pecies are indicated by names).
    - enumerate_affected_subnetworks: Enumerates subnetworks that are affected by the perturbation of each parameter.
    - compute_influence_index: Computes the influence index of a subnetwork.
    - is_output_complete: Checks if a given subnetwork is output-complete. 
    - find_reactions_to_add: For a given subnetwork, it finds reactions to be added to make the subnetwork output-complete.
    - write_species_to_file: Writes the species to a file.
    - get_S11: Returns the submatrix S11 of the stoichiometric matrix.
    - get_S12: Returns the submatrix S12 of the stoichiometric matrix.
    - get_S21: Returns the submatrix S21 of the stoichiometric matrix.
    - get_S22: Returns the submatrix S22 of the stoichiometric matrix.
    - get_S_tilde: Returns the augmented stoichiometric matrix.
    - get_emergent_cycles: Returns the emergent cycles of a subnetwork.
    - get_emergent_cycles_symb: Returns the emergent cycles of a subnetwork computed using sympy.
    - get_emergent_conserved_quantities: Returns the emergent conserved quantities of a subnetwork.
    - get_emergent_conserved_quantities_symb: Returns the emergent conserved quantities of a subnetwork computed using sympy.
    - get_lost_conserved_quantities: Returns the lost conserved quantities of a subnetwork.
    - get_lost_conserved_quantities_symb: Returns the lost conserved quantities of a subnetwork computed using sympy.
    - find_integrators_from_lbs: Returns the integrators corresponding to a labeled buffering structure.
    - find_integrators_from_bs: Returns the integrators for a buffering structure. 
    """

    def __init__(self, reactions_input, input_type='string', show_info=False):
        """
        Initializes a ReactionSystem object.

        Parameters:
        reactions_input (str or list): The list of reactions. If input_type is 'string', reactions_input should be 
        a string representing the reactions. If input_type is 'list', reactions_input should be a list of reactions.
        input_type (str): The type of input reactions. Default is 'string'.
        show_info (bool): Whether to display additional information during initialization. Default is False.

        """

        if type(reactions_input) == str and input_type == 'string':
            reactions = parse_string_to_reaction_list(reactions_input)
            self.nr = len(reactions)
            r_list_c = [ [from_str_to_list(reactions[i][j]) for i in range(self.nr) ] for j in range(2) ] 
        elif type(reactions_input) == list: 
            reactions = reactions_input
            self.nr = len(reactions)
            r_list_c = [ [from_str_to_list(reactions[i][j]) for i in range(self.nr) ] for j in range(2) ] 
        elif input_type == 'sbml':
            r_list_c = transpose(sbml_to_reaction_list(reactions_input))
            self.nr = len(r_list_c[0])
        else:
            raise NotImplementedError("unrecognized file format")

        if show_info:
            print('reactions\n', r_list_c)

        self.species = extract_species(flatten_list(r_list_c))
        self.ns = len(self.species)
        self.ind = { self.species[i] : i for i in range(len(self.species)) }

        if show_info:
            print("\n species list")
            print(self.ind)

        self.rmat = np.transpose(np.array([ self._complex_to_vec(r) for r in r_list_c[0]]))
        self.pmat = np.transpose(np.array([ self._complex_to_vec(r) for r in r_list_c[1]]))
        self.smat = self.pmat - self.rmat 
        self.cmat = compute_nullspace(self.smat).T
        self.dmat = compute_nullspace(self.smat.T).T
        # row vectors correspond to cycles and conserved quantities

        tolerance = 1e-10
        self.cmat[np.abs(self.cmat) < tolerance] = 0
        self.dmat[np.abs(self.dmat) < tolerance] = 0

        if show_info:
            print("\nnum. of reactioins:", self.nr)
            print("num. of species:", self.ns)
            print("dim ker S =", len(self.cmat))
            print("dim coker S =", len(self.dmat))
        
        return

    def write_species_to_file(self, filename):
            """
            Write the species to a file.

            Args:
                filename (str): The name of the file to write the species to.

            Returns:
                None
            """
            current_directory = os.getcwd()
            filename = os.path.join(current_directory, filename)
            with open(filename, 'w') as f:
                for s in self.species:
                    f.write(s + '\n')
            return

    def _complex_to_vec(self, c):
        # c = [["A",1],["B",2]], [["C",2], ["B",1]]        
        c = [cc for cc in c if cc[0]!=''] 
        nums = [ [self.ind[s[0]], s[1]] for s in c]
        vec = np.zeros(len(self.species), dtype='float64')
        for num in nums: 
            vec[num[0]] = num[1]
        return vec

    def compute_influence_index(self, subn, verbose=False):
        """
        Computes the influence index of a given subnetwork.

        Parameters:
        - subn: A tuple containing the subnetwork's species (xs) and reactions (rs).
        - verbose: A boolean indicating whether to print additional information.

        Returns:
        - int: The influence index of the subnetwork.
        """
        xs, rs = subn

        smat = self.smat        
        xall = list(range(self.ns))
        rall = list(range(self.nr))
        pr = proj_mat(rs, rall)
        pmbar = proj_mat_comp(xs, xall)

        if verbose:
            print('len(rall):', len(rall) )
            print('dimcoker(smat):', dimcoker(smat))
            print('dimker(np.dot(smat, pr)):', dimker(np.dot(smat, pr)))
            print('dimcoker(np.dot(pmbar, smat)):', dimcoker(np.dot(pmbar, smat)))
            print('xs:', xs)
            print('xall:', xall)
            print('rs:', rs)
            print('rall:', rall)
            print('pmbar\n', pmbar)
            print('pmbar @ smat:\n')
            print(pmbar @ smat)

        return len(rall) + dimcoker(smat) - dimker(smat @ pr) - dimcoker(pmbar @ smat)

    def is_output_complete(self, subn):
        """
        Check if a given subnetwork is output-complete.

        Parameters:
        subn (tuple): A tuple containing two lists: xs and rs.
                  xs (list): List of species indices.
                  rs (list): List of reaction indices.

        Returns:
        bool: True if the subnetwork is output-complete, False otherwise.
        """
        xs, rs = subn

        aa = np.array( [ self.rmat[i,:] for i in xs ] )
        r_indices = np.array(flatten_list([ np.nonzero(a)[0] for a in aa]))
        r_indices = np.unique(r_indices)

        return contains_all(rs, r_indices.tolist())

    def _compute_amat(self, verbose=False):
        drdx = randomize_nonzero_entries(self.rmat.T)

        cmat = self.cmat
        dmat = self.dmat
        
        ns, nr = self.ns, self.nr
        nc, nd = cmat.shape[0], dmat.shape[0] # indices are: c[alpha, A], d[alpha_bar, i]
        dim = ns + nc
        
        if verbose:
            print(f"nx,nr,nc,nd: {ns, nr, nc, nd}")
            print("drdx:\n", drdx)
            print("cmat:\n", cmat)
            print(cmat.shape)
            print("dmat:\n", dmat)

        assert ns + nc == nr + nd, "Fredholm's theorem violated"
    
        amat = np.zeros((dim, dim))
        for i in range(dim):
            for j in range(dim):
                if i < nr and j < ns:
                    amat[i, j] = drdx[i, j]
                elif i < nr and j >= ns:
                    amat[i, j] = cmat[j - ns, i]
                elif i >= nr and j < ns:
                    amat[i, j] = dmat[i - nr, j]
        
        return amat

    def _compute_response_mat(self, verbose=False):        
        ns = self.ns
        nc = self.cmat.shape[0]
        dim = ns + nc

        amat = self._compute_amat()

        # det = np.linalg.det(amat)
        # print("det A=", det)
        # if np.abs(det) < 1e-10:
        #     raise ValueError("Matrix is not invertible; determinant is close to zero: ", det)

        ainv = np.linalg.inv(amat)

        if verbose:
            print("amat\n", amat)
            print("ainv\n", ainv)
        
        s_resp = ainv[:ns, :]
        r_resp = self.cmat.T @ ainv[ns:dim, :]
        
        return s_resp, r_resp

    def find_reactions_to_add(self, xs, rs, verbose=False):
        """
        Finds the reactions to add to make the given subnetwork output-complete.

        Args:
            xs (list): List of input species.
            rs (list): List of output species.
            verbose (bool, optional): If True, prints additional information. Defaults to False.

        Returns:
            numpy.ndarray: Array of indices of reactions to be added. 
        """
        if verbose:
            print('inside find_reactions_to_add')
            print('xs:', xs)
            print('rs:', rs)
            print('is_output_complete([xs, rs]):', self.is_output_complete([xs, rs]))
              
        if self.is_output_complete([xs, rs]):
            return np.array([], dtype=int)
        
        rmat = self.rmat
        list_ = np.sum(rmat[np.array(xs)], axis=0)
        affected_rs = np.nonzero(list_ > 0)[0]

        if verbose:
            print('inside find_reactions_to_add')
            print('xs:', xs)
            print('rs:', rs)
            print('affected rs:',affected_rs)

        complement = list(set(affected_rs) - set(rs))

        if verbose:
            print('to be added:', complement)

        return sorted(complement)

    def enumerate_affected_subnetworks(self, verbose=False):
            """
            Enumerates the affected subnetworks by the perturbation of each reaction parameter.

            Parameters:
            - verbose (bool): If True, prints the responded species and reactions.

            Returns:
            - affected_subnetworks (list): A list of affected subnetworks, whose i-th subnetwork is represents subnetworks affected by the perturbation of the i-th reaction parameter.
            """

            ns, nr = self.ns, self.nr
            nc, nd = self.cmat.shape[0], self.dmat.shape[0]
            dim = ns + nc

            s_resp, r_resp = self._compute_response_mat()

            responded_species = []
            for j in range(dim):
                non_zero_indices = nonzero_with_error(s_resp[:, j])
                responded_species.append(non_zero_indices)

            if verbose:
                print(responded_species)

            responded_reactions = []

            for j in range(dim):
                non_zero_indices = nonzero_with_error(r_resp[:, j])
                responded_reactions.append(non_zero_indices)

            if verbose:
                print(responded_reactions)

            affected_subnetworks = []
            for i in range(dim):
                xs = responded_species[i]
                rs = responded_reactions[i]
                affected_subnetworks.append([xs, rs])
            
            return affected_subnetworks

    def enumerate_labeled_buffering_structures(self, ntrial=2, verbose=False):
        """
            Enumerates labeled buffering structures of a given reaction network.

            Parameters:
            - ntrial (int): The number of trials to perform for identifying affected subnetworks. Default is 2.
            - verbose (bool): Whether to print additional information during the enumeration process. Default is False.

            Returns:
            - lbs_list (list): A list of labeled buffering structures, where each structure is represented as a nested list.
        """

        lbs_would_be_list = [self.enumerate_affected_subnetworks() for i in range(ntrial)]

        def is_consistent(lbs_would_be_list):
            return all( [ deep_compare(lbs_would_be_list[0], el) for el in lbs_would_be_list[1:] ])

        if ntrial>1 and not is_consistent(lbs_would_be_list):
            raise ValueError("The identification of affected subnetworks is not consistent across trials.")

        lbs_would_be = make_hashable(lbs_would_be_list[0])

        if verbose:
            print('would be lbs')
            for l in lbs_would_be:
                print(l)
        
        if verbose:
            print('hashable form of would be lbs')
            print(make_hashable(lbs_would_be))

        lbs_duplicates_removed = remove_duplicates(lbs_would_be)

        added_reactions = []

        for i in range(len(lbs_duplicates_removed)):
            xs = lbs_duplicates_removed[i][0]
            rs = lbs_duplicates_removed[i][1]
            added_reactions.append(tuple(self.find_reactions_to_add(xs, rs)))

        lbs_duplicates_removed_2 = []
        for i in range(len(lbs_duplicates_removed)):
            lbs_duplicates_removed_2.append( lbs_duplicates_removed[i]  + (added_reactions[i],) )

        lbs = []

        for i in range(len(lbs_duplicates_removed)):
            reactions = tuple(get_indices_of_element(lbs_would_be, lbs_duplicates_removed[i]))
            lbs.append( (reactions,) + lbs_duplicates_removed_2[i] )

        lbs_list = [[[el for el in inner_tuple] for inner_tuple in outer_tuple] for outer_tuple in lbs]

        return lbs_list

    def enumerate_labeled_buffering_structures_by_name(self):
        """
        Enumerates the labeled buffering structures (species are indicated by names).

        Returns:
            A list labeled buffering structures, in which species are indicated by names.
        """
        lbs_list = self.enumerate_labeled_buffering_structures()
        return [self.lbs_to_name(l) for l in lbs_list]

    def enumerate_buffering_structures(self):
        """
        Enumerates the buffering structures of a given reaction network.

        Returns:
            list: A list of buffering structures.
        """
        lbs_list = self.enumerate_labeled_buffering_structures()
        bs_list = [from_lbs_to_bs(l) for l in lbs_list]
        return bs_list

    def lbs_to_name(self, lbs):
        name = {v: k for k, v in self.ind.items()}
        res = [ lbs[0], list(map(lambda x: name[x], lbs[1])), lbs[2], lbs[3] ]
        return res

    def bs_to_name(self, bs):
        name = {v: k for k, v in self.ind.items()}
        res = [ list(map(lambda x: name[x], bs[0])), bs[1] ]
        return res

    def get_S11(self, subn):
        return self.smat[np.ix_( *subn )]

    def get_S12(self, subn):
        xs, rs = subn
        smat = self.smat
        rs_comp = list(set(range(self.nr)) - set(rs))
        return smat[np.ix_(xs, rs_comp)]

    def get_S21(self, subn):
        xs, rs = subn
        smat = self.smat
        xs_comp = list(set(range(self.ns)) - set(xs))
        return smat[np.ix_(xs_comp, rs)]
    
    def get_S22(self, subn):
        xs, rs = subn
        smat = self.smat
        xs_comp = list(set(range(self.ns)) - set(xs))
        rs_comp = list(set(range(self.nr)) - set(rs))
        return smat[np.ix_(xs_comp, rs_comp)]

    def get_S_tilde(self, subn):
        #
        # S_tilde = (S11 S12 S11)
        #           (S21 S22  0 )
        #
        s11 = self.get_S11(subn)
        n_pad = self.ns - s11.shape[0]
        s11_padded = np.pad(s11, ((0, n_pad), (0, 0)))
        return np.hstack( (self.smat, s11_padded))

    def get_emergent_cycles(self, subn):
        """
        Computes the emergent cycles of a given subnetwork.

        Parameters:
        - subn: A subnetwrok represented as a tuple containing a list of species indices and a list of reaction indices.

        Returns:
        - emergent_cycles: An array containing the emergent cycles of the subnetwork.
        """
        s11 = self.get_S11(subn)
        s21 = self.get_S21(subn)

        if s11.shape[0] == 0:
            kerS11 = np.identity(s11.shape[1])
        else:
            kerS11 = null_space(s11).transpose()
        if kerS11.shape[0] == 0:
            return np.array([])

        if s21.shape[0] == 0:
            kerS21 = np.identity(s21.shape[1])
        else:
            kerS21 = null_space(s21).transpose()
        if kerS21.shape[0] == 0:
            return kerS11
        
        kerS21_orth = get_orthogonal_complement(kerS21)
        return get_intersection(kerS11, kerS21_orth)

    def get_emergent_cycles_symb(self, subn):
        """
        Computes the emergent cycles of a given subnetwork using sympy.

        Parameters:
        - subn: A subnetwrok represented as a tuple containing a list of species indices and a list of reaction indices.

        Returns:
        - emergent_cycles: An array containing the emergent cycles of the subnetwork.
        """
        s11 = sp.Matrix(self.get_S11(subn))
        s21 = sp.Matrix(self.get_S21(subn))

        if s11.rows == 0:
            kerS11 = sp.eye(s11.cols)
        else:
            kerS11 = s11.nullspace()
            kerS11 = sp.Matrix.hstack(*kerS11).transpose()
        if not kerS11:
            return sp.zeros(0, len(subn[1]))

        if s21.rows == 0:
            kerS21 = sp.eye(s21.cols)
        else:
            kerS21 = s21.nullspace()
            kerS21 = sp.Matrix.hstack(*kerS21).transpose()
        if not kerS21:
            return kerS11

        kerS21_orth = get_orthogonal_complement_symb(kerS21)

        return get_intersection_symb(kerS11, kerS21_orth)

    def get_emergent_conserved_quantities(self, subn):
        """
        Computes the emergent conserved quantities for a given subnetwork.

        Args:
        - subn: A subnetwrok represented as a tuple containing a list of species indices and a list of reaction indices.

        Returns:
        - emergent conserved quantities: An array containing the emergent conserved quantities of the subnetwork.
        """
        xs, rs = subn
        S11 = self.get_S11(subn)

        if S11.shape[1] == 0:
            coker_S11 = np.identity(len(xs))
        else:
            coker_S11 = null_space(self.get_S11(subn).T).T

        S_tilde = self.get_S_tilde(subn)
        coker_S_tilde = null_space(S_tilde.T).T
        d1 = coker_S_tilde[:, :len(xs)]

        return get_intersection(coker_S11, get_orthogonal_complement(d1))
    
    def get_emergent_conserved_quantities_symb(self, subn):
        """
        Computes the emergent conserved quantities for a given subnetwork using sympy.

        Args:
        - subn: A subnetwrok represented as a tuple containing a list of species indices and a list of reaction indices.

        Returns:
        - emergent conserved quantities: An array containing the emergent conserved quantities of the subnetwork.
        """
        xs, rs = subn

        S11_np = self.get_S11(subn)
        S11 = sp.Matrix(S11_np.astype(int))

        if S11.cols == 0:
            coker_S11 = sp.eye(len(xs))
        else:
            coker_S11 = S11.T.nullspace()
            coker_S11 = sp.Matrix.hstack(*coker_S11).transpose()
            if coker_S11.rows == 0:
                coker_S11 = sp.zeros(0, len(xs))

        S_tilde_np = self.get_S_tilde(subn)
        S_tilde = sp.Matrix(S_tilde_np)

        coker_S_tilde = S_tilde.T.nullspace()

        if len(coker_S_tilde) == 0:
            coker_S_tilde = sp.zeros(0, self.ns)
        else:
            coker_S_tilde = sp.Matrix.hstack(*coker_S_tilde).transpose()

        d1 = coker_S_tilde[:, :len(xs)]

        return get_intersection_symb(coker_S11, get_orthogonal_complement_symb(d1))

    def get_lost_conserved_quantities(self, subn):
        """
        Computes the lost conserved quantities for a given subnetwork.

        Args:
        - subn: A subnetwrok represented as a tuple containing a list of species indices and a list of reaction indices.

        Returns:
        - lost conserved quantities: An array containing the lost conserved quantities of the subnetwork.
        """
        # D_l = coker S \cap coker S_tilde
        coker_S = self.dmat
        S_tilde = self.get_S_tilde(subn)
        coker_S_tilde = null_space(S_tilde.T).T

        return get_intersection(coker_S, get_orthogonal_complement(coker_S_tilde))

    def get_lost_conserved_quantities_symb(self, subn):
        """
        Computes the lost conserved quantities for a given subnetwork using sympy.

        Args:
        - subn: A subnetwrok represented as a tuple containing a list of species indices and a list of reaction indices.

        Returns:
        - lost conserved quantities: An array containing the lost conserved quantities of the subnetwork.
        """
        S_mat = sp.Matrix(self.smat)
        coker_S = S_mat.T.nullspace()
        coker_S = sp.Matrix.hstack(*coker_S).transpose()

        S_tilde = sp.Matrix(self.get_S_tilde(subn))
        coker_S_tilde = S_tilde.T.nullspace()
        coker_S_tilde = sp.Matrix.hstack(*coker_S_tilde).transpose()

        if coker_S_tilde.rows == 0:
            coker_S_tilde = sp.zeros(0, coker_S.cols)

        return get_intersection_symb(coker_S, get_orthogonal_complement_symb(coker_S_tilde))

    def _compute_integrator_matrices(self, subn, pinv_mode='sympy'):

        s11 = sp.Matrix(self.get_S11(subn).astype(int))
        s21 = sp.Matrix(self.get_S21(subn).astype(int))
        s12 = sp.Matrix(self.get_S12(subn).astype(int))
        s22 = sp.Matrix(self.get_S22(subn).astype(int))

        if pinv_mode == 'sympy':
            s11_plus = s11.pinv()
            s21_plus = s21.pinv()
        elif pinv_mode == 'numpy':
            if s11.rows == 0 or s11.cols == 0:
                s11_plus = sp.zeros(s11.cols, s11.rows)
            else:
                s11_plus = sp.Matrix( np.linalg.pinv(np.array(s11.evalf().tolist(), dtype=np.float64)) )
            
            if s21.rows == 0 or s21.cols == 0:
                s21_plus = sp.zeros(s21.cols, s21.rows)
            else:
                s21_plus = sp.Matrix( np.linalg.pinv(np.array(s21.evalf().tolist(), dtype=np.float64)) )
        else:
            raise ValueError("Invalid pinv mode")

        s_p = s22 - s21 * s11_plus * s12   # Generalized Schur complement

        emergent_cycles = self.get_emergent_cycles_symb(subn)
        emergent_conserved_quantities = self.get_emergent_conserved_quantities_symb(subn)

        s21c11 = s21 * emergent_cycles.transpose()

        p_mat = sp.Matrix.hstack( *(s21c11.transpose().nullspace()) ).transpose()
        q_mat = sp.Matrix.hstack(- s21 * s11_plus, sp.eye(s22.rows))

        kerS11 = sp.Matrix.hstack(*s11.nullspace()).transpose() 
        if kerS11.shape[0] == 0:
            kerS11 = sp.zeros(0, s11.cols)

        kerS21 = sp.Matrix.hstack(*s21.nullspace()).transpose() 
        if kerS21.shape[0] == 0:
            kerS21 = sp.zeros(0, s21.cols)

        return [ p_mat * q_mat, 
                 p_mat * s_p, 
                 emergent_conserved_quantities, 
                 emergent_conserved_quantities * s12, 
                 s11_plus, 
                 s11_plus * s12, 
                 kerS11, 
                 s21_plus, 
                 kerS21, 
                 s22
                ]

    def _create_species_str(self, symbol_mode='subscript'):
        if symbol_mode == 'subscript':
            symbol_x_str = " ".join( map(lambda s: "x_{" + s + "}", self.species) )
        elif symbol_mode == 'name':
            symbol_x_str = " ".join( self.species )
        elif symbol_mode == 'index':
            symbol_x_str = " ".join( map(lambda s: "x_{" + str(s) + "}", range(self.ns)) )
        else:
            raise ValueError("Invalid symbol mode")
       
        return symbol_x_str

    def find_integrators_from_bs(self, subn, output_style='latex', symbol_mode='subscript', pinv_mode='sympy'):
        """
        Returns the integrators for a given buffering structure.

        Parameters:
        - subn: A buffering structure, which is a subnetwork with zero influence index.
        - output_style: The style of the output. Valid options are 'latex' and 'symbolic'.
        - symbol_mode: The mode for representing symbols. Valid options are 'subscript', 'name', and 'index'.
        - pinv_mode: The mode for computing the pseudo-inverse. Valid options are 'sympy' and 'numpy'.

        Returns:
        - list: A list of expressions representing the integrators. The style of the expressions depends on the output_style parameter.

        Warnings:
        - Using 'sympy' for the pseudo-inverse computation can be slow for large subnetworks. 
        For larger matrices or subnetworks, consider using 'numpy' to significantly reduce computation time.
        - When 'numpy' is selected for `pinv_mode`, the computation uses numerical methods, which 
        might introduce floating-point precision inaccuracies.
        """
        p_q, p_sp, d, c2, s11plus, s11p_s12, kerS11, s21plus, kerS21, s22= self._compute_integrator_matrices(subn, pinv_mode)
        x1, x2, r1, r2, r1_indices = self._prepare_variables(symbol_mode, subn)

        expressions1 = [ d * x1, c2 * r2, p_q * (x1.col_join(x2)), p_sp * r2 ] 

        if output_style == 'latex':
            data = [ (lambda x:sp.latex(sp.simplify(x)))(x) for x in expressions1]
        elif output_style == 'symbolic':
            data = [ sp.simplify(x) for x in expressions1]
        else:
            raise ValueError("Invalid output style")

        return data

    def find_integrators_from_lbs(self, lbs, output_style='latex', symbol_mode='subscript', pinv_mode='sympy'):
        """
        Returns the integrators for a given labeled buffering structure.

        Parameters:
        - lbs (list): A labeled buffering structure.
        - output_style (str, optional): The output style for the integrators. Default is 'latex' If 'symbol' is chosen, it returns sympy expressions.
        - symbol_mode (str, optional): The mode for representing symbols. Default is 'subscript'.
        - pinv_mode: The mode for computing the pseudo-inverse. Valid options are 'sympy' and 'numpy'.

        Returns:
        - list: A list of integrators based on the specified output style.

        Warnings:
        - Using 'sympy' for the pseudo-inverse computation can be slow for large subnetworks. 
        For larger matrices or subnetworks, consider using 'numpy' to significantly reduce computation time.
        - When 'numpy' is selected for `pinv_mode`, the computation uses numerical methods, which 
        might introduce floating-point precision inaccuracies.
        """
        subn = from_lbs_to_bs(lbs)
        p_q, p_sp, d, c2, s11plus, s11plus_s12, kerS11, s21plus, kerS21, s22 = self._compute_integrator_matrices(subn, pinv_mode)
        x1, x2, r1, r2, r1_indices = self._prepare_variables(symbol_mode, subn)
        
        expressions1 = [ d * x1, c2 * r2, p_q * (x1.col_join(x2)), p_sp * r2 ] 

        if output_style == 'latex':
            data1 = [ (lambda x:sp.latex(sp.simplify(x)))(x) for x in expressions1]
        elif output_style == 'symbolic':
            data1 = expressions1
        else:
            raise ValueError("Invalid output style")

        if len(lbs[3]) == 0:  # \mathcal E_\gamma is empty 
            data2 = [ sp.zeros(0, 1) for _ in range(4)]
            if output_style == 'latex':
                data2 = [ sp.latex(x) for x in data2 ]
                return data1 + data2
            elif output_style == 'symbolic':
                return data1 + data2
            else:
                raise ValueError("Invalid output style")

        # Make a projection matrix to \mathcal E_\gamma
        lbs3_indices = [ r1_indices.index(val) for val in lbs[3] ]
        proj_hat = sp.Matrix.hstack(*[sp.Matrix([0]*i + [1] + [0]*(len(subn[1])-i-1)) for i in lbs3_indices]).transpose()

        kerS11_perp = get_orthogonal_complement_symb(kerS11)
        kerS21_perp = get_orthogonal_complement_symb(kerS21)

        proj_hat_1 = get_intersection_symb(proj_hat, kerS11_perp)
        proj_hat_2 = get_intersection_symb(proj_hat, kerS21_perp)

        expressions2 = [ proj_hat_1 * (s11plus * x1), 
                        proj_hat_1 * (r1 + s11plus_s12 * r2), 
                        proj_hat_2 * (s21plus * x2), 
                        proj_hat_2 * (r1 + s21plus * s22 * r2)
                        ]

        data2 = [ sp.simplify(x) for x in expressions2]

        if output_style == 'latex':
            data2= [ sp.latex(x) for x in data2]
            return data1 + data2
        elif output_style == 'symbolic':
            return data1 + data2
        else:
            raise ValueError("Invalid output style")

    def _prepare_variables(self, symbol_mode, subn):
        symbol_x_str = self._create_species_str(symbol_mode)
        x = sp.Matrix( sp.symbols(symbol_x_str) )

        symbol_r_str = " ".join( map(lambda s: "r_{" + str(s+1) + "}", range(self.nr)) )
        r = sp.Matrix( sp.symbols(symbol_r_str) )

        x1 = sp.Matrix([x[i] for i in subn[0]])
        xs_comp = list(set(range(self.ns)) - set(subn[0]))
        x2 = sp.Matrix([x[i] for i in xs_comp])
        if x2.shape[0] == 0:
            x2 = sp.zeros(0, 1)

        r1 = sp.Matrix([r[i] for i in subn[1]])
        r1_indices = [i for i in range(self.nr) if i in subn[1]]

        rs_comp = list(set(range(self.nr)) - set(subn[1]))
        r2 = sp.Matrix([r[i] for i in rs_comp])
        if r2.shape[0] == 0:
            r2 = sp.zeros(0, 1)

        return x1, x2, r1, r2, r1_indices
