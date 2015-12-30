from __future__ import print_function, division

import pypsa

import datetime
import pandas as pd

import networkx as nx

import numpy as np

from itertools import chain

import os



import numpy as np

from itertools import chain

import os


from distutils.spawn import find_executable



def test_opf():


    csv_folder_name = "../examples/opf-storage-hvdc/opf-storage-data"

    network = pypsa.Network(csv_folder_name=csv_folder_name)

    solver_search_order = ["glpk","gurobi"]

    solver_executable = {"glpk" : "glpsol", "gurobi" : "gurobi_cl"}

    solver_name = None

    for s in solver_search_order:
        if find_executable(solver_executable[s]) is not None:
            solver_name = s
            break

    if solver_name is None:
        print("No known solver found, quitting.")
        sys.exit()

    print("Using solver:",solver_name)

    snapshots = network.snapshots
    network.lopf(snapshots=snapshots,solver_name=solver_name)


    results_folder_name = "results"


    network.export_to_csv_folder(results_folder_name,time_series={"generators" : {"p" : None},
                                                               "storage_units" : {"p" : None}})

    good_results_filename =  os.path.join(csv_folder_name,"results","generators-p.csv")

    good_arr = pd.read_csv(good_results_filename,index_col=0).values

    print(good_arr)

    results_filename = os.path.join(results_folder_name,"generators-p.csv")


    arr = pd.read_csv(results_filename,index_col=0).values


    print(arr)


    np.testing.assert_array_almost_equal(arr,good_arr)



if __name__ == "__main__":
    test_opf()
