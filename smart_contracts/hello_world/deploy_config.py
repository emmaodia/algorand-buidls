import typing as t
import logging
from algopy import Box, arc4, ARC4Contract, String
from algosdk.v2client.algod import AlgodClient
from algosdk.v2client.indexer import IndexerClient
import algokit_utils

logger = logging.getLogger(__name__)

class MyContract(ARC4Contract):
    def __init__(self) -> None:
        self.box_b = Box(arc4.String, key=b"BOX_B")

    @arc4.abimethod
    def hello(self, name: String) -> bool:
        self.box_b.value = arc4.String("Hello, " + name)
        return True

    @arc4.abimethod
    def read_name(self) -> arc4.String:
        return self.box_b.value


# Deployment function based on the reference example
def deploy(algod_client: AlgodClient, indexer_client: IndexerClient, app_spec: algokit_utils.ApplicationSpecification, deployer: algokit_utils.Account) -> None:
    from smart_contracts.artifacts.my_contract.my_contract_client import MyContractClient

    # Initialize MyContractClient
    app_client = MyContractClient(
        algod_client=algod_client,
        creator=deployer,
        indexer_client=indexer_client,
    )

    # Deploy the contract, including box allocation
    app_client.deploy(
        on_schema_break=algokit_utils.OnSchemaBreak.AppendApp,
        on_update=algokit_utils.OnUpdate.AppendApp,
        boxes=1 
    )

    # Call the contract's 'hello' method with a string argument
    name = "world"
    response = app_client.hello(name=name)
    
    # Log the response from the contract call
    logger.info(
        f"Called hello on {app_spec.contract.name} ({app_client.app_id}) "
        f"with name={name}, received: {response.return_value}"
    )
