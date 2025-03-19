# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

from aliyunsdkcore.request import RpcRequest
from aliyunsdkoceanbasepro.endpoint import endpoint_data

class ModifyInstanceSpecRequest(RpcRequest):

	def __init__(self):
		RpcRequest.__init__(self, 'OceanBasePro', '2019-09-01', 'ModifyInstanceSpec','oceanbase')
		self.set_method('POST')

		if hasattr(self, "endpoint_map"):
			setattr(self, "endpoint_map", endpoint_data.getEndpointMap())
		if hasattr(self, "endpoint_regional"):
			setattr(self, "endpoint_regional", endpoint_data.getEndpointRegional())

	def get_InstanceClass(self): # String
		return self.get_body_params().get('InstanceClass')

	def set_InstanceClass(self, InstanceClass):  # String
		self.add_body_params('InstanceClass', InstanceClass)
	def get_DryRun(self): # Boolean
		return self.get_body_params().get('DryRun')

	def set_DryRun(self, DryRun):  # Boolean
		self.add_body_params('DryRun', DryRun)
	def get_DiskSize(self): # Long
		return self.get_body_params().get('DiskSize')

	def set_DiskSize(self, DiskSize):  # Long
		self.add_body_params('DiskSize', DiskSize)
	def get_DiskType(self): # String
		return self.get_body_params().get('DiskType')

	def set_DiskType(self, DiskType):  # String
		self.add_body_params('DiskType', DiskType)
	def get_InstanceId(self): # String
		return self.get_body_params().get('InstanceId')

	def set_InstanceId(self, InstanceId):  # String
		self.add_body_params('InstanceId', InstanceId)
	def get_UpgradeSpecNative(self): # Boolean
		return self.get_body_params().get('UpgradeSpecNative')

	def set_UpgradeSpecNative(self, UpgradeSpecNative):  # Boolean
		self.add_body_params('UpgradeSpecNative', UpgradeSpecNative)
