#
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
#
from abc import ABC
from datetime import datetime

import grakn_protocol.common.concept_pb2 as concept_proto

from grakn.api.concept.thing.attribute import Attribute, RemoteAttribute, BooleanAttribute, RemoteBooleanAttribute, \
    LongAttribute, RemoteLongAttribute, DoubleAttribute, RemoteDoubleAttribute, StringAttribute, RemoteStringAttribute, \
    DateTimeAttribute, RemoteDateTimeAttribute
from grakn.api.concept.type.attribute_type import BooleanAttributeType, LongAttributeType, DoubleAttributeType, \
    StringAttributeType, DateTimeAttributeType
from grakn.api.concept.type.thing_type import ThingType
from grakn.common.rpc.request_builder import attribute_get_owners_req
from grakn.concept.proto import concept_proto_builder, concept_proto_reader
from grakn.concept.thing.thing import _Thing, _RemoteThing


class _Attribute(Attribute, _Thing, ABC):
    pass


class _RemoteAttribute(RemoteAttribute, _RemoteThing, ABC):

    def get_owners(self, owner_type: ThingType = None):
        return (concept_proto_reader.thing(t) for rp in self.stream(attribute_get_owners_req(self.get_iid(), concept_proto_builder.thing_type(owner_type)))
                for t in rp.attribute_get_owners_res_part.things)


class _BooleanAttribute(BooleanAttribute, _Attribute):

    def __init__(self, iid: str, type_: BooleanAttributeType, value: bool):
        super(_BooleanAttribute, self).__init__(iid)
        self._type = type_
        self._value = value

    @staticmethod
    def of(thing_proto: concept_proto.Thing):
        return _BooleanAttribute(concept_proto_reader.iid(thing_proto.iid), concept_proto_reader.attribute_type(thing_proto.type), thing_proto.value.boolean)

    def get_type(self) -> "BooleanAttributeType":
        return self._type

    def get_value(self):
        return self._value

    def as_remote(self, transaction):
        return _RemoteBooleanAttribute(transaction, self.get_iid(), self.get_type(), self.get_value())


class _RemoteBooleanAttribute(RemoteBooleanAttribute, _RemoteAttribute):

    def __init__(self, transaction, iid: str, type_, value: bool):
        super(_RemoteBooleanAttribute, self).__init__(transaction, iid)
        self._type = type_
        self._value = value

    def get_type(self) -> "BooleanAttributeType":
        return self._type

    def get_value(self):
        return self._value

    def as_remote(self, transaction):
        return _RemoteBooleanAttribute(transaction, self.get_iid(), self.get_type(), self.get_value())


class _LongAttribute(LongAttribute, _Attribute):

    def __init__(self, iid: str, type_: LongAttributeType, value: int):
        super(_LongAttribute, self).__init__(iid)
        self._type = type_
        self._value = value

    @staticmethod
    def of(thing_proto: concept_proto.Thing):
        return _LongAttribute(concept_proto_reader.iid(thing_proto.iid), concept_proto_reader.attribute_type(thing_proto.type), thing_proto.value.long)

    def get_type(self) -> "LongAttributeType":
        return self._type

    def get_value(self):
        return self._value

    def as_remote(self, transaction):
        return _RemoteLongAttribute(transaction, self.get_iid(), self.get_type(), self.get_value())


class _RemoteLongAttribute(RemoteLongAttribute, _RemoteAttribute):

    def __init__(self, transaction, iid: str, type_, value: int):
        super(_RemoteLongAttribute, self).__init__(transaction, iid)
        self._type = type_
        self._value = value

    def get_type(self) -> "LongAttributeType":
        return self._type

    def get_value(self):
        return self._value

    def as_remote(self, transaction):
        return _RemoteLongAttribute(transaction, self.get_iid(), self.get_type(), self.get_value())


class _DoubleAttribute(DoubleAttribute, _Attribute):

    def __init__(self, iid: str, type_: DoubleAttributeType, value: float):
        super(_DoubleAttribute, self).__init__(iid)
        self._type = type_
        self._value = value

    @staticmethod
    def of(thing_proto: concept_proto.Thing):
        return _DoubleAttribute(concept_proto_reader.iid(thing_proto.iid), concept_proto_reader.attribute_type(thing_proto.type), thing_proto.value.double)

    def get_type(self) -> "DoubleAttributeType":
        return self._type

    def get_value(self):
        return self._value

    def as_remote(self, transaction):
        return _RemoteDoubleAttribute(transaction, self.get_iid(), self.get_type(), self.get_value())


class _RemoteDoubleAttribute(RemoteDoubleAttribute, _RemoteAttribute):

    def __init__(self, transaction, iid: str, type_: DoubleAttributeType, value: float):
        super(_RemoteDoubleAttribute, self).__init__(transaction, iid)
        self._type = type_
        self._value = value

    def get_type(self) -> "DoubleAttributeType":
        return self._type

    def get_value(self):
        return self._value

    def as_remote(self, transaction):
        return _RemoteDoubleAttribute(transaction, self.get_iid(), self.get_type(), self.get_value())


class _StringAttribute(StringAttribute, _Attribute):

    def __init__(self, iid: str, type_: StringAttributeType, value: str):
        super(_StringAttribute, self).__init__(iid)
        self._type = type_
        self._value = value

    @staticmethod
    def of(thing_proto: concept_proto.Thing):
        return _StringAttribute(concept_proto_reader.iid(thing_proto.iid), concept_proto_reader.attribute_type(thing_proto.type), thing_proto.value.string)

    def get_type(self) -> "StringAttributeType":
        return self._type

    def get_value(self):
        return self._value

    def as_remote(self, transaction):
        return _RemoteStringAttribute(transaction, self.get_iid(), self.get_type(), self.get_value())


class _RemoteStringAttribute(RemoteStringAttribute, _RemoteAttribute):

    def __init__(self, transaction, iid: str, type_: StringAttributeType, value: str):
        super(_RemoteStringAttribute, self).__init__(transaction, iid)
        self._type = type_
        self._value = value

    def get_type(self) -> "StringAttributeType":
        return self._type

    def get_value(self):
        return self._value

    def as_remote(self, transaction):
        return _RemoteStringAttribute(transaction, self.get_iid(), self.get_type(), self.get_value())


class _DateTimeAttribute(DateTimeAttribute, _Attribute):

    def __init__(self, iid: str, type_: DateTimeAttributeType, value: datetime):
        super(_DateTimeAttribute, self).__init__(iid)
        self._type = type_
        self._value = value

    @staticmethod
    def of(thing_proto: concept_proto.Thing):
        return _DateTimeAttribute(concept_proto_reader.iid(thing_proto.iid), concept_proto_reader.attribute_type(thing_proto.type), datetime.fromtimestamp(float(thing_proto.value.date_time) / 1000.0))

    def get_type(self) -> "DateTimeAttributeType":
        return self._type

    def get_value(self):
        return self._value

    def as_remote(self, transaction):
        return _RemoteDateTimeAttribute(transaction, self.get_iid(), self.get_type(), self.get_value())


class _RemoteDateTimeAttribute(RemoteDateTimeAttribute, _RemoteAttribute):

    def __init__(self, transaction, iid: str, type_: DateTimeAttributeType, value: datetime):
        super(_RemoteDateTimeAttribute, self).__init__(transaction, iid)
        self._type = type_
        self._value = value

    def get_type(self) -> "DateTimeAttributeType":
        return self._type

    def get_value(self):
        return self._value

    def as_remote(self, transaction):
        return _RemoteDateTimeAttribute(transaction, self.get_iid(), self.get_type(), self.get_value())