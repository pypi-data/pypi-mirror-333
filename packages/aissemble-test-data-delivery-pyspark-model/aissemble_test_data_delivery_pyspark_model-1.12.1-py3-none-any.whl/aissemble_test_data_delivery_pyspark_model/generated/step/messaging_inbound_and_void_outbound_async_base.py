###
# #%L
# aiSSEMBLE::Test::MDA::Data Delivery Pyspark
# %%
# Copyright (C) 2021 Booz Allen
# %%
# This software package is licensed under the Booz Allen Public License. All Rights Reserved.
# #L%
###
from ...generated.step.abstract_pipeline_step import AbstractPipelineStep
from krausening.logging import LogManager
from abc import abstractmethod
from time import time_ns
from ..pipeline.pipeline_base import PipelineBase
from aissemble_core_metadata.hive_metadata_api_service import HiveMetadataAPIService
from kafka import KafkaConsumer
import asyncio
import threading
from aissemble_core_config import MessagingConfig
from pathlib import Path
from policy_manager.configuration import PolicyConfiguration
from aissemble_encrypt_policy import DataEncryptionPolicy, DataEncryptionPolicyManager
from typing import List
import os
from pyspark.sql.functions import udf, col, lit, when
from pyspark.sql.types import StringType
from aissemble_encrypt.vault_key_util import VaultKeyUtil
from aissemble_encrypt.aes_cbc_encryption_strategy import AesCbcEncryptionStrategy
from aissemble_encrypt.aes_gcm_96_encryption_strategy import AesGcm96EncryptionStrategy
from aissemble_encrypt.vault_remote_encryption_strategy import VaultRemoteEncryptionStrategy
from aissemble_encrypt.vault_local_encryption_strategy import VaultLocalEncryptionStrategy
from uuid import uuid4
from datetime import datetime

def aissemble_encrypt_simple_aes(plain_text):
    '''
    Pyspark User Defined Function for running encryption on columns.
    Note: must be registered with the spark session.
    return The cipher text
    '''
    # TODO: Due to issues with defining the udf inside the class we are defining them outside.  It would be good to revisit this issue in future releases.
    if (plain_text is not None):
        if not os.environ.get('KRAUSENING_BASE'):
            MessagingInboundAndVoidOutboundAsyncBase.logger.warn('KRAUSENING_BASE environment variable was not set.  Using default path -> ./krausening/base')
            os.environ['KRAUSENING_BASE'] = 'krausening/base/'

        encryption_strategy = AesCbcEncryptionStrategy()

        encrypted_column_value = encryption_strategy.encrypt(plain_text)

        # Depending on the encryption algorithm the return value may be bytes or bytesarray which requires decoding
        try:
            encrypted_column_value = encrypted_column_value.decode('utf-8')
        except (UnicodeDecodeError, AttributeError):
            pass

        return encrypted_column_value
    else:
        return ''


def aissemble_encrypt_with_vault_key(key, plain_text):
    '''
    Pyspark User Defined Function for running encryption on columns.
    Vault supplies an AES GCM 96 encryption key which will be used here.
    Note: must be registered with the spark session.
    return The cipher text
    '''
    if (plain_text is not None):
        if not os.environ.get('KRAUSENING_BASE'):
            MessagingInboundAndVoidOutboundAsyncBase.logger.warn('KRAUSENING_BASE environment variable was not set.  Using default path -> ./config')
            os.environ['KRAUSENING_BASE'] = 'krausening/base/'

        encryption_strategy = AesGcm96EncryptionStrategy(key)

        encrypted_column_value = encryption_strategy.encrypt(plain_text)

        # Depending on the encryption algorithm the return value may be bytes or bytesarray which requires decoding
        try:
            encrypted_column_value = encrypted_column_value.decode('utf-8')
        except (UnicodeDecodeError, AttributeError):
            pass

        return encrypted_column_value
    else:
        return ''


class MessagingInboundAndVoidOutboundAsyncBase(AbstractPipelineStep):
    """
    Performs scaffolding asynchronous processing for MessagingInboundAndVoidOutboundAsync. Business logic is delegated to the subclass.

    GENERATED CODE - DO NOT MODIFY (add your customizations in MessagingInboundAndVoidOutboundAsync).

    Generated from: templates/data-delivery-pyspark/asynchronous.processor.base.py.vm
    """

    logger = LogManager.get_instance().get_logger('MessagingInboundAndVoidOutboundAsyncBase')
    step_phase = 'MessagingInboundAndVoidOutboundAsync'
    bomIdentifier = "Unspecified MessagingInboundAndVoidOutboundAsync BOM identifier"

    consumer: KafkaConsumer | None


    def __init__(self, data_action_type, descriptive_label):
        super().__init__(data_action_type, descriptive_label)

        self.set_metadata_api_service(HiveMetadataAPIService())
        self.messaging_config = MessagingConfig()
        self.consumer = None


    def get_consumer_configs(self) -> dict:
        """
        Returns the configurations for the kafka consumer. Override this method to specify your own configurations.
        """
        return {
            'api_version': (2, 0, 2),
            'bootstrap_servers': [self.messaging_config.server()],
            'group_id': 'MessagingInboundAndVoidOutboundAsync',
            'auto_offset_reset': 'earliest'
        }


    async def execute_step(self) -> None:
        """
        Executes this step.
        """
        execute_step = threading.Thread(target=asyncio.run, args=(self.consume_from_kafka(),))
        execute_step.start()


    async def consume_from_kafka(self) -> None:
        self.consumer = KafkaConsumer("inboundChannel", **self.get_consumer_configs())

        for message in self.consumer:
            start = time_ns()
            MessagingInboundAndVoidOutboundAsyncBase.logger.info('START: step execution...')

            message_value = message.value.decode('utf-8')
            inbound = self.check_and_apply_encryption_policy(message_value)

            run_id = uuid4()
            job_name = self.get_job_name()
            default_namespace = self.get_default_namespace()
            parent_run_facet = PipelineBase().get_pipeline_run_as_parent_run_facet()
            # pylint: disable-next=assignment-from-none
            event_data = self.create_base_lineage_event_data()
            start_time = datetime.utcnow()
            self.record_lineage(self.create_lineage_start_event(run_id=run_id,job_name=job_name,default_namespace=default_namespace,parent_run_facet=parent_run_facet,event_data=event_data,start_time=start_time))
            try:
                await self.execute_step_impl(inbound)
                end_time = datetime.utcnow()
                self.record_lineage(self.create_lineage_complete_event(run_id=run_id,job_name=job_name,default_namespace=default_namespace,parent_run_facet=parent_run_facet,event_data=event_data,start_time=start_time,end_time=end_time))
            except Exception as error:
                self.logger.exception(
                    "An exception occurred while executing "
                    + self.descriptive_label
                )
                self.record_lineage(self.create_lineage_fail_event(run_id=run_id,job_name=job_name,default_namespace=default_namespace,parent_run_facet=parent_run_facet,event_data=event_data,start_time=start_time,end_time=datetime.utcnow(),error=error))
                PipelineBase().record_pipeline_lineage_fail_event()
                raise Exception(error)

            self.record_provenance()


            self.consumer.commit()

            stop = time_ns()
            MessagingInboundAndVoidOutboundAsyncBase.logger.info('COMPLETE: step execution completed in %sms' % ((stop - start) / 1000000))

        self.consumer.close()


    @abstractmethod
    async def execute_step_impl(self, inbound: str) -> None:
        """
        This method performs the business logic of this step,
        and should be implemented in MessagingInboundAndVoidOutboundAsync.
        """
        pass




    def check_and_apply_encryption_policy(self, inbound: str) -> None:
        """
        Checks for encryption policies and applies encryption to the designated fields.
        If no policies are found then the original data is returned.
        """

        MessagingInboundAndVoidOutboundAsyncBase.logger.warn('Encryption is not yet supported for messaging without specifying an inbound record type!')
        MessagingInboundAndVoidOutboundAsyncBase.logger.warn('If desired, please add encryption manually by overriding check_and_apply_encryption_policy()!')
        return inbound


    def aissemble_encrypt_aes_udf(self):
        return udf(lambda text: aissemble_encrypt_simple_aes(text))


    def aissemble_encrypt_vault_udf(self, key):
        return udf(lambda text: aissemble_encrypt_with_vault_key(key, text))


    def apply_encryption_to_dataset(self, inbound: str, fields_to_update: List[str], algorithm: str) -> str:
        '''
            This method applies encryption to the given fields
        '''
        MessagingInboundAndVoidOutboundAsyncBase.logger.info('applying encryption')


        # some other text
        return_payload = []
        for encrypt_field in fields_to_update:
            if(algorithm == 'VAULT_ENCRYPT'):
                # Because of the restrictive nature of PySpark UDF's we have to retrieve the Vault key outside of
                # the udf call to avoid threading errors
                vault_key_util = VaultKeyUtil.get_instance()
                vault_key = vault_key_util.get_vault_key_encoded()
                return_payload = inbound.withColumn(encrypt_field, self.aissemble_encrypt_vault_udf(vault_key)(col(encrypt_field)))
            else:
                return_payload = inbound.withColumn(encrypt_field, self.aissemble_encrypt_aes_udf()(col(encrypt_field)))

            return_payload.show()

        return return_payload


    def get_fields_list(self, inbound: str) -> List[str]:
        '''
            This method gets the field names from the given data type
        '''
        # Get the column names
        return inbound.columns

    def get_logger(self):
        return self.logger
    
    def get_step_phase(self):
        return self.step_phase
