import pytest
from unittest.mock import MagicMock
from hiero_sdk_python.consensus.topic_id import TopicId
from hiero_sdk_python.consensus.topic_message_submit_transaction import TopicMessageSubmitTransaction
from hiero_sdk_python.transaction.transaction_id import TransactionId
from hiero_sdk_python.transaction.transaction_receipt import TransactionReceipt
from hiero_sdk_python.account.account_id import AccountId
from hiero_sdk_python.crypto.private_key import PrivateKey
from hiero_sdk_python.client.client import Client
from hiero_sdk_python.response_code import ResponseCode
from hiero_sdk_python.hapi.services import (
    response_pb2,
    transaction_receipt_pb2,
    timestamp_pb2 as hapi_timestamp_pb2
)

def test_execute_topic_submit_message():
    """
    Test executing the TopicMessageSubmitTransaction with a mock Client.
    When calling tx.execute(client), freeze_with() checks client.node_account_id if tx.node_account_id is None.
    """
    topic_id = TopicId(0, 0, 1234)
    message = "Hello from topic submit!"
    tx = TopicMessageSubmitTransaction(topic_id, message)

    tx.operator_account_id = AccountId(0, 0, 2)

    client = MagicMock(spec=Client)
    client.operator_private_key = PrivateKey.generate()
    client.operator_account_id = AccountId(0, 0, 2)
    client.node_account_id = AccountId(0, 0, 3) 

    real_tx_id = TransactionId(
        account_id=AccountId(0, 0, 2),
        valid_start=hapi_timestamp_pb2.Timestamp(seconds=12345, nanos=6789)
    )
    client.generate_transaction_id.return_value = real_tx_id

    client.topic_stub = MagicMock()

    mock_response = MagicMock()
    mock_response.nodeTransactionPrecheckCode = ResponseCode.OK
    client.topic_stub.submitMessage.return_value = mock_response

    real_receipt_proto = transaction_receipt_pb2.TransactionReceipt(
        status=ResponseCode.OK
    )
    real_receipt = TransactionReceipt.from_proto(real_receipt_proto)

    client.get_transaction_receipt.return_value = real_receipt

    try:
        receipt = tx.execute(client)  
    except Exception as e:
        pytest.fail(f"TopicMessageSubmitTransaction execution failed with: {e}")

    client.topic_stub.submitMessage.assert_called_once()
    assert receipt is not None
    assert receipt.status == ResponseCode.OK  
    print("Test passed: TopicMessageSubmitTransaction executed successfully.")
