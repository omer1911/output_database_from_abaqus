from odbAccess import openOdb
from abaqus import mdb, session
import numpy as np

def find_nodes(setName):
    model = mdb.models['Original']
    assembly = model.rootAssembly
    my_set = assembly.sets[setName]
    nodes_in_set = my_set.nodes
    node_labels = np.array([node.label for node in nodes_in_set])
    return node_labels

def write_to_file(output_file, data,header):
    np.savetxt(output_file, data, fmt='%s',header=header,comments="")
def main(MyodbPath,stepName,setName):
    nodes = find_nodes(setName) 
    odb = openOdb(MyodbPath)
    num_frames = len(odb.steps[stepName].frames)
    output_data = []

    for i in range(num_frames):
        currentFrame = odb.steps[stepName].frames[i]
        displacement = currentFrame.fieldOutputs['U']

        for node_label in nodes:
            Node = odb.rootAssembly.instances['PREFORM-1'].getNodeFromLabel(node_label)
            centerDisplacement = displacement.getSubset(region=Node)

            for v in centerDisplacement.values:
                output_data.append([v.nodeLabel, v.dataDouble[0], v.dataDouble[1]])
    output_data = np.array(output_data)
    output_file_path = 'youroutputpath/result_deformation.txt'
    header = "Node Label, X Displacement, Y Displacement"
    write_to_file(output_file_path, output_data, header)
    

MyodbPath = 'yourodbpath/yourodbname.odb'
stepName='yourstepname'
setName='yoursetname'
main(MyodbPath,stepName,setName)