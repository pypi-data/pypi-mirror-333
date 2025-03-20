# -*- coding: utf-8 -*-
"""
Created on Sun Feb 23 2025

@author: Cord Hockemeyer
"""
from kstpy.helpers import kstFrozenset
from kstpy.helpers import domain

def constr(structure):
    """ Compute the smallest knowledge space containing a famly of kstFrozensets

    Parameters
    ----------
    structure: set
        Family of kstFrozensets

    Returns
    -------
    Knowledge space

    Examples
    --------
    >>> from kstpy.data import xpl_basis
    >>> constr(xpl_basis)
    """
        
    space = set({kstFrozenset({}), kstFrozenset(domain(structure))})
    space.union(structure)
    for state in structure:
        new_states = set({})
        for s in space:
            if not ((set({state | s})) <= space):
                new_states.add((state | s))
        space = space | new_states
    return space

def basis(structure):
    """ Determine the basis of a knolwdge space/structure
    
    Parameters
    ----------
    structure: set
        Family of kstFrozensets
    
    Returns
    -------
    Basis

    Examples
    --------
    >>> from kstpy.data import xpl_basis
    >>> s = constr(xpl_basis)
    >>> basis(s)
    """
    b = set({})
    for state in structure:
        h = set(state)
        for i in structure:
            if set(i) < set(state):
                h = h - set(i)
            if h == set({}):
                break
        if len(h) > 0:
            b.add(kstFrozenset(state))
    return b

def surmiserelation(structure):
    """Compute the surmise relation for a knowledge structure
    
    Parameters
    ----------

    structure: set
        Family of kstFrozensets
    
    Returns
    -------

    Corresponding surmise relation
    """
    d = domain(structure)
    sr = set({})
    b = basis(structure)

    for i in d:
        for j in d:
            sr.add((i,j))
    for s in b:
        for i in d:
            for j in d:
                if i in s and not j in s:
                    sr.discard((j,i))
                if j in s and not i in s:
                    sr.discard((i,j))
    return(sr)
