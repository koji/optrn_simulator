from pydantic import BaseModel
from opentrons.simulate import simulate, format_runlog, get_protocol_api
import os
import io
import subprocess

class Simulator:
    def __init__(self):
        self.folder_path = 'storage'
        self.file_names = []

    # Define the Protocol class inside the ApiServer class
    class Protocol(BaseModel):
        name: str
        content: str

    def get_file_names(self):
        if not os.path.exists(self.folder_path):
            os.makedirs(self.folder_path)
            return []

        for root, dirs, files in os.walk(self.folder_path):
            for file in files:
                self.file_names.append(file)
        return self.file_names

    async def root(self):
        return {"message": "this is a test api server"}

    def upload_protocol(self, protocol: Protocol):
        file_path = 'storage/' + protocol.name
        save_result = self.save_text_as_file(protocol.content, file_path)

        if type(save_result) == str:
            response = self.call_opentrons_simulate(file_path)
            if response["status"] == "success":
                return {"protocol_name": protocol.name, "run_status": "success", "run_log": response['run_log']}
            else:
                return {"protocol_name": protocol.name, "run_status": "failure", "error_message": response['error_message']}
        else:
            return {"error_message": "something wrong while saving a protocol"}

    def call_opentrons_simulate(self, protocol_path: str):
        command = f"opentrons_simulate {protocol_path}"
        result = subprocess.run(command, shell=True, capture_output=True, text=True)

        if result.returncode == 0:
            return {"status": "success", "run_log": result.stdout}
        else:
            return {"status": "error", "error_message": result.stderr}

    def save_text_as_file(self, text, file_path):
        base = os.path.splitext(file_path)[0]
        ext = os.path.splitext(file_path)[1]
        counter = 1

        while os.path.exists(file_path):
            file_path = base + "_" + str(counter) + ext
            counter += 1

        try:
            with open(file_path, 'w') as file:
                file.write(text)
            return file_path
        except Exception as e:
            return False
