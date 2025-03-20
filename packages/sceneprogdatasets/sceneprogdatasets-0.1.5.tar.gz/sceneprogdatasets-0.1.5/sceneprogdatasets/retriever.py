from .HSSD.hssd import AssetRetrieverHSSD
from .future.future import AssetRetrieverFuture
from .objaverse.objaverse import AssetRetrieverObjaverse

class SceneProgAssetRetriever:
    def __init__(self):
       
        import os
        from pathlib import Path
        path = Path(__file__).parent
        
        if os.getenv('FUTURE_PATH') is None or os.getenv('HSSD_PATH') is None or os.getenv('OBJAVERSE_PATH') is None:
            msg = f"""
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
You need to set the FUTURE_PATH and HSSD_PATH environment variables first!

Run the following commands to set the environment variables:
export FUTURE_PATH=<path_to_future_assets>
export HSSD_PATH=<path_to_hssd_assets>
export OBJAVERSE_PATH=<path_to_objaverse_assets>

!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
"""
            raise Exception(msg)
        
            
        if not os.path.exists(os.path.join(path,'HSSD/assets/model2description.json')) or not os.path.exists(os.path.join(path,'future/assets/model2description.json')) or not os.path.exists(os.path.join(path,'objaverse/assets/compiled.json')):
            msg = f"""
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
You need to download the assets first!

Run the following commands to download the assets:

aws s3 cp s3://sceneprog-nautilus/sceneprogdatasets/future/ {os.path.join(path,'future/assets')} --recursive
aws s3 cp s3://sceneprog-nautilus/sceneprogdatasets/hssd/ {os.path.join(path,'HSSD/assets')} --recursive
aws s3 cp s3://sceneprog-nautilus/sceneprogdatasets/objaverse/ {os.path.join(path,'objaverse/assets')} --recursive
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
"""
            raise Exception(msg)
       
        self.hssd = AssetRetrieverHSSD()
        self.future = AssetRetrieverFuture()
        self.objaverse = AssetRetrieverObjaverse()
    
    def __call__(self, description, random=True):
        ## first search in Future
        future_results = self.future(description, random=random)
        if not future_results == 'No models found':
            return ("FUTURE",future_results)
        
        ## then search in HSSD
        hssd_results = self.hssd(description, random=random)
        if not hssd_results == 'No models found':
            return ("HSSD",hssd_results)
        
        ## then search in OBJAVERSE
        objaverse_results = self.objaverse(description)
        if not objaverse_results == 'No models found':
            return ("OBJAVERSE",objaverse_results)
        
        return "No models found"