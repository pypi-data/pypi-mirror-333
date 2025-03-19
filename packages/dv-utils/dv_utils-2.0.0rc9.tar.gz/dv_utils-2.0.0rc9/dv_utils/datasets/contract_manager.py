"""
This module checks the quality of a dataset in a data source for checks defined by the data contract.
"""
from ..settings import settings as default_settings
from ..log_utils import log, LogLevel
from ..client import Client
from .contract import Contract


class ContractManager:
    NAMING_CONVENTION_MODEL="{{model}}"

    def __init__(self):
        self.client= Client()
        self.contract=Contract()
        self.data_connector_config_location=default_settings.data_connector_config_location
    
    def get_contract_for_data_descriptor(self, data_descriptor_id: str, data_descriptor:str):
        if data_descriptor != None:
            data_source_type=data_descriptor["settings"]["connector"] 
            contract=Contract()
            contract.create_contract(data_descriptor_id,data_source_type,data_descriptor)
            return contract
        else:
            log(f"Not able to create contract, data descriptor available: data_descriptor_id:{data_descriptor_id}", LogLevel.ERROR)

    def get_contracts_for_collaboration_space(self, collaboration_space_id: str,participants_role:str=Client.DATA_PROVIDER_COLLABORATOR_ROLE_VALUE):
        data_contracts=[]
        log(f"Get list of data providers for:{collaboration_space_id}", LogLevel.DEBUG)
        list_participants=self.client.get_list_of_participants(collaboration_space_id,participants_role)
        if list_participants != None and len(list_participants)>0:
            for participant in list_participants:
                client_id=participant["clientId"]
                data_descriptors=participant.get("dataDescriptors")
                if len(data_descriptors) > 0:
                    for data_descriptor in data_descriptors:
                        data_contracts.append(self.get_contract_for_data_descriptor(data_descriptor["id"],data_descriptor))
                else:
                    log(f"No data descriptor available for participant: {client_id}", LogLevel.ERROR)
            return data_contracts
        else:
            log(f"No participant as data provider available for collaboration_space_id: {collaboration_space_id}", LogLevel.ERROR)
            return None 

    def check_contract_for_data_descriptor(self, data_descriptor_id: str, data_descriptor:str):
        log(f"Check data contract for data_descriptor: {data_descriptor['id']}")
        contract=self.get_contract_for_data_descriptor(data_descriptor_id,data_descriptor)
        return contract.check_contract()
    
    def check_contracts_for_collaboration_space(self, collaboration_space_id: str):
        log(f"Check data contract for collaboration space {collaboration_space_id}")
        scan_results={}
        data_contracts=self.get_contracts_for_collaboration_space(collaboration_space_id)
        if data_contracts != None and len(data_contracts)>0:
            for data_contract in data_contracts:
                data_descriptor_id=data_contract.data_descriptor_id
                log(f"Check data contract for data descriptor: {data_descriptor_id}")
                scan_results[data_descriptor_id]=data_contract.check_contract()
        else:
            log(f"Error verifying data contracts for collaboration space {collaboration_space_id}. No data contract available.",LogLevel.ERROR)
            raise Exception(f"Unable to check data contracts for collaboration space {collaboration_space_id}")
        return scan_results
    
    