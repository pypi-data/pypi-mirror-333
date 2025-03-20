import os
import json
import bentoml
import trimesh
import numpy as np
from scipy.spatial.transform import Rotation as R

class AssetRetrieverObjaverse:
    def __init__(self):
        self.img2rot = {
            "0.png": 0,
            "1.png": 30,
            "2.png": 60,
            "3.png": 90,
            "4.png": 120,
            "5.png": 150,
            "6.png": -180,
            "7.png": -150,
            "8.png": -120,
            "9.png": -90,
            "10.png": -60,
            "11.png": -30,
        }
        from pathlib import Path
        BASE = str(Path(__file__).parent)
        self.correction_data  = os.path.join(BASE, 'assets/compiled.json')
        with open(self.correction_data, 'r') as f:
            self.correction_data = json.load(f)
        
        self.OBJAVERSE_PATH = os.getenv('OBJAVERSE_PATH')

    def rotate_vertices_around_point(self, vertices, rot, point):
        x,y,z = point
        vertices -= np.array([[x,y,z]])
        r = R.from_euler('y', rot, degrees=True).as_matrix()
        vertices = (r@vertices.T).T
        vertices += np.array([[x,y,z]])
        return vertices

    def apply_objaverse_fix_init(self, mesh):
        vertices = mesh.vertices
        vertices -= vertices.mean(axis=0)
        vertices = self.rotate_vertices_around_point(vertices, 180, vertices.mean(axis=0))
        mesh.vertices = vertices
        return mesh

    def apply_objaverse_fix(self, mesh, rot):
        vertices = mesh.vertices
        vertices = self.rotate_vertices_around_point(vertices, rot, vertices.mean(axis=0))
        mesh.vertices = vertices
        return mesh

    def get_objaverse_local(self, obj):
        path = os.path.join(self.OBJAVERSE_PATH,f'{obj}.glb')
        mesh = trimesh.load(path, force='mesh', process=False)
        mesh = self.apply_objaverse_fix_init(mesh)
        return mesh
    
    def get_id(self, desc):
        with bentoml.SyncHTTPClient('http://chetak.ucsd.edu:3001') as client:
            result: str = client.retrieve([desc])[0]

        if result == '**':
            return "No models found"
        assetID, bbox = result.split('|')

        return assetID

    def __call__(self, desc):
        id = self.get_id(desc)

        if id == "No models found":
            return None
        
        mesh = self.get_objaverse_local(id)
        if id in self.correction_data:
            mesh = self.apply_objaverse_fix(mesh, self.img2rot[self.correction_data[id]])
        
        return mesh

