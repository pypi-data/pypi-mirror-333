import unittest
from datetime import datetime
from dotenv import load_dotenv
from time import sleep
from msfabricpysdkcore.coreapi import FabricClientCore

load_dotenv()

class TestFabricClientCore(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(TestFabricClientCore, self).__init__(*args, **kwargs)
        #load_dotenv()
        self.fc = FabricClientCore()

    def test_data_pipelines(self):

        fc = self.fc
        workspace_id = '63aa9e13-4912-4abe-9156-8a56e565b7a3'
        datetime_str = datetime.now().strftime("%Y%m%d%H%M%S")
        pipeline_name = f"pipeline_{datetime_str}"

        dp = fc.create_data_pipeline(workspace_id, display_name=pipeline_name, description="asda")
        dp.update_definition(dp.definition)

        dps = fc.list_data_pipelines(workspace_id)
        dp_names = [dp.display_name for dp in dps]
        self.assertGreater(len(dps), 0)
        self.assertIn(pipeline_name, dp_names)

        self.assertEqual(dp.display_name, pipeline_name)
        pipeline_name2 = f"pipeline_{datetime_str}_2"
        dp2 = fc.update_data_pipeline(workspace_id, dp.id, display_name=pipeline_name2, return_item=True)

        dp = fc.get_data_pipeline(workspace_id, data_pipeline_id=dp.id)
        self.assertEqual(dp.display_name, pipeline_name2)
        self.assertEqual(dp.id, dp2.id)

        dp2 = fc.update_data_pipeline(workspace_id, dp.id, display_name=pipeline_name, return_item=True)

        dp = fc.get_data_pipeline(workspace_id, data_pipeline_id=dp.id)
        self.assertEqual(dp.display_name, pipeline_name)
        self.assertEqual(dp.id, dp2.id)
        status_code = fc.delete_data_pipeline(workspace_id, dp.id)
        self.assertEqual(status_code, 200)