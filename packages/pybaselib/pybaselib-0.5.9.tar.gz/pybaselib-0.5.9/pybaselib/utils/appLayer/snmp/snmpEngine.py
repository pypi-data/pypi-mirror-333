# -*- coding: utf-8 -*-
# @Author: maoyongfan
# @email: maoyongfan@163.com
# @Date: 2024/12/9 23:53
import asyncio
from pysnmp.hlapi.v3arch.asyncio import *
from pysnmp.smi import builder, view, compiler, rfc1902
from pybaselib.utils import BugException


class SNMPManager:
    def __init__(self, ipaddr, central_port=161, local_port=161, community="public", mib_name="NTCIP1203v03f-MIB"):
        # self.snmpEngine = SnmpEngine()
        self.ipaddr = ipaddr
        self.port = central_port
        self.community = community
        self.mib_name = mib_name
        self.local_port = local_port
        self.central_port = central_port

    def switch_to_local(self, local_port=None):
        if local_port is None:
            self.port = self.local_port
        else:
            self.port = local_port

    def switch_to_central(self):
        self.port = self.central_port

    def deal_value(self, oid, value, prettyPrint):
        # print(" = ".join([x.prettyPrint() for x in (oid, value)]))
        print(f"\n{oid.prettyPrint()} = {value.prettyPrint()}")
        print(f"类型为：{type(value).__name__}")

        expect_rule = value.subtypeSpec
        sub_expect_rule = expect_rule[-1]
        try:
            sub_expect_rule(value)
        except Exception as e:  # ValueConstraintError
            raise BugException(
                f"{oid.prettyPrint()}返回值不符合预期范围||{oid.prettyPrint()}返回值不符合预期范围|返回值的范围为{sub_expect_rule},实际却为{value.prettyPrint()}||P1")

        if prettyPrint:
            return value.prettyPrint()
        elif isinstance(value, Integer32) or isinstance(value, Counter32) \
                or isinstance(value, Counter64) or isinstance(value, Integer):
            return int(value)
        elif isinstance(value, OctetString):
            print('octet')
            print(str(value))
            return value.prettyPrint()
        else:
            print('else')
            return value.prettyPrint()

    def deal_error(self, errorIndication, errorStatus, errorIndex, varBinds):
        if errorIndication:
            raise Exception("snmp 响应发生错误:", errorIndication)
        elif errorStatus:
            # print(
            #     f"{errorStatus.prettyPrint()} at {varBinds[int(errorIndex) - 1][0] if errorIndex else '?'}"
            # )
            if varBinds:
                raise Exception("%s at %s" % (errorStatus.prettyPrint(),
                                              errorIndex and varBinds[int(errorIndex) - 1][0] or "?",))
            else:
                raise Exception("%s at %s" % (errorStatus.prettyPrint(), str(varBinds)))
        else:
            pass

    def deal_mib_name(self, mib_name):
        if self.mib_name is None:
            return mib_name
        else:
            return self.mib_name

    def deal_set_value(self, value, object_type, check_value, mib_name, index, second_index):
        if isinstance(value, int):
            value = Integer32(value)
        if isinstance(value, str):
            if object_type in ["dmsActivateMessage"]:
                value = OctetString(hexValue=value)
            else:
                value = OctetString(value)
        if check_value:
            from pysnmp.smi import builder, view, compiler
            mibBuilder = builder.MibBuilder()
            mibViewController = view.MibViewController(mibBuilder)
            compiler.add_mib_compiler(
                mibBuilder,
                sources=["file:///usr/share/snmp/mibs"],
            )
            mibBuilder.load_modules("NTCIP1203v03f-MIB")
            if second_index is None:
                mib_obj = ObjectType(ObjectIdentity(mib_name, object_type, index), value). \
                    resolve_with_mib(mibViewController)
            else:
                mib_obj = ObjectType(ObjectIdentity(mib_name, object_type, index, second_index), value). \
                    resolve_with_mib(mibViewController)

            expect_rule = mib_obj[1].subtypeSpec
            sub_expect_rule = expect_rule[-1]
            try:
                sub_expect_rule(mib_obj[1])
            except Exception as e:  # ValueConstraintError
                raise Exception(f"返回值的范围为{sub_expect_rule},实际却为{mib_obj[1]}")

        else:
            if second_index is None:
                mib_obj = ObjectType(ObjectIdentity(mib_name, object_type, index), value)
            else:
                mib_obj = ObjectType(ObjectIdentity(mib_name, object_type, index, second_index), value)

        return mib_obj

    async def get_cmd_single(self, oid, prettyPrint=False):
        errorIndication, errorStatus, errorIndex, varBinds = await get_cmd(
            SnmpEngine(),
            CommunityData(self.community, mpModel=0),
            await UdpTransportTarget.create((self.ipaddr, self.port)),
            ContextData(),
            ObjectType(ObjectIdentity(oid))
        )

        self.deal_error(errorIndication, errorStatus, errorIndex, varBinds)

        for oid, value in varBinds:
            result = self.deal_value(oid, value, prettyPrint)
            print(result)
            return result

    async def get_cmd_single_mib(self, object_type, index=0, second_index=None, mib_name="NTCIP1203v03f-MIB",
                                 prettyPrint=False):
        mib_name = self.deal_mib_name(mib_name)
        if second_index is None:
            objectType = ObjectType(ObjectIdentity(mib_name, object_type, index))
        else:
            objectType = ObjectType(ObjectIdentity(mib_name, object_type, index, second_index))
        errorIndication, errorStatus, errorIndex, varBinds = await get_cmd(
            SnmpEngine(),
            CommunityData(self.community, mpModel=0),
            await UdpTransportTarget.create((self.ipaddr, self.port)),
            ContextData(),
            objectType
        )

        self.deal_error(errorIndication, errorStatus, errorIndex, varBinds)

        for oid, value in varBinds:
            result = self.deal_value(oid, value, prettyPrint)
            # print(result)
            return result

    async def get_cmd_many(self, *varBinds, prettyPrint=False):
        # print(content)
        resultList = []
        iterator = get_cmd(
            SnmpEngine(),
            CommunityData(self.community, mpModel=0),
            await UdpTransportTarget.create((self.ipaddr, self.port)),
            ContextData(),
            *varBinds
        )

        errorIndication, errorStatus, errorIndex, varBinds = await iterator

        self.deal_error(errorIndication, errorStatus, errorIndex, varBinds)

        for oid, value in varBinds:
            if "fontStatus" in oid.prettyPrint():
                result = self.deal_value(oid, value, True)
            else:
                result = self.deal_value(oid, value, prettyPrint)
            resultList.append(result)
        print(resultList)
        return resultList

    async def get_cmd_many_mib(self, varBinds, mib_name="NTCIP1203v03f-MIB", prettyPrint=False):
        """
        多个oid为一组请求，按object_type方式
        :param varBinds:
        :param mib_name:
        :param prettyPrint:
        :return:
        """
        mib_name = self.deal_mib_name(mib_name)
        resultList = []
        iterator = get_cmd(
            SnmpEngine(),
            CommunityData(self.community, mpModel=0),
            await UdpTransportTarget.create((self.ipaddr, self.port)),
            ContextData(),
            *[ObjectType(ObjectIdentity(mib_name, object_type, index)) if second_index is None
              else ObjectType(ObjectIdentity(mib_name, object_type, index, second_index))
              for object_type, index, second_index in varBinds]
        )

        errorIndication, errorStatus, errorIndex, varBinds = await iterator

        self.deal_error(errorIndication, errorStatus, errorIndex, varBinds)

        for oid, value in varBinds:
            result = self.deal_value(oid, value, prettyPrint)
            resultList.append(result)
        print(resultList)
        return resultList

    async def get_cmd_many_oid(self, varBinds, mib_name="NTCIP1203v03f-MIB", prettyPrint=False):
        """
        多个oid为一组请求，按oid方式
        :param varBinds:
        :param mib_name:
        :param prettyPrint:
        :return:
        """
        resultList = []
        iterator = get_cmd(
            SnmpEngine(),
            CommunityData(self.community, mpModel=0),
            await UdpTransportTarget.create((self.ipaddr, self.port)),
            ContextData(),
            *[ObjectType(ObjectIdentity(oid)) for oid in varBinds]
        )

        errorIndication, errorStatus, errorIndex, varBinds = await iterator

        self.deal_error(errorIndication, errorStatus, errorIndex, varBinds)

        for oid, value in varBinds:
            result = self.deal_value(oid, value, prettyPrint)
            resultList.append(result)
        print(resultList)
        return resultList

    async def set_cmd(self, oid, value, prettyPrint=False):
        if isinstance(value, int):
            value = Integer32(value)
        if isinstance(value, str):
            value = OctetString(value)
        errorIndication, errorStatus, errorIndex, varBinds = await set_cmd(
            SnmpEngine(),
            CommunityData(self.community, mpModel=0),
            await UdpTransportTarget.create((self.ipaddr, self.port)),
            ContextData(),
            ObjectType(ObjectIdentity(oid), value)
        )
        self.deal_error(errorIndication, errorStatus, errorIndex, varBinds)

        for oid, value in varBinds:
            result = self.deal_value(oid, value, prettyPrint)
            print(result)
            return result

    async def set_cmd_many_mib(self, varBinds, mib_name="NTCIP1203v03f-MIB", prettyPrint=False, check_value=False):
        """
        多个oid为一组请求，按object_type方式
        :param check_value:
        :param varBinds: object_type, index, value
        :param mib_name:
        :param prettyPrint:
        :return:
        """
        resultList = []
        objectTypeList = []
        mib_name = self.deal_mib_name(mib_name)
        for object_type, index, second_index, value in varBinds:
            mib_obj = self.deal_set_value(value, object_type, check_value, mib_name, index, second_index)
            objectTypeList.append(mib_obj)

        iterator = set_cmd(
            SnmpEngine(),
            CommunityData(self.community, mpModel=0),
            await UdpTransportTarget.create((self.ipaddr, self.port)),
            ContextData(),
            *objectTypeList
        )

        errorIndication, errorStatus, errorIndex, varBinds = await iterator

        self.deal_error(errorIndication, errorStatus, errorIndex, varBinds)

        for oid, value in varBinds:
            result = self.deal_value(oid, value, prettyPrint)
            resultList.append(result)
        print(resultList)
        return resultList

    async def set_cmd_single_mib(self, object_type, value, index=0, second_index=None, mib_name="NTCIP1203v03f-MIB",
                                 prettyPrint=False,
                                 check_value=False):
        mib_name = self.deal_mib_name(mib_name)
        mib_obj = self.deal_set_value(value, object_type, check_value, mib_name, index, second_index)

        errorIndication, errorStatus, errorIndex, varBinds = await set_cmd(
            SnmpEngine(),
            CommunityData(self.community, mpModel=0),
            await UdpTransportTarget.create((self.ipaddr, self.port)),
            ContextData(),
            mib_obj
        )

        self.deal_error(errorIndication, errorStatus, errorIndex, varBinds)

        for oid, value in varBinds:
            result = self.deal_value(oid, value, prettyPrint)
            print(result)
            return result

    async def next_cmd_single_mib(self, object_type, index=0, mib_name="NTCIP1203v03f-MIB", prettyPrint=False):
        mib_name = self.deal_mib_name(mib_name)
        errorIndication, errorStatus, errorIndex, varBinds = await next_cmd(
            SnmpEngine(),
            CommunityData(self.community, mpModel=1),
            await UdpTransportTarget.create((self.ipaddr, self.port)),
            ContextData(),
            ObjectType(ObjectIdentity(mib_name, object_type, index)),
            # lexicographicMode=True,
        )

        self.deal_error(errorIndication, errorStatus, errorIndex, varBinds)

        for oid, value in varBinds:
            result = self.deal_value(oid, value, prettyPrint)
            print(result)
            # return result

    async def bulk_cmd(self, nonRepeaters, maxRepetitions, *varBinds, prettyPrint=False):
        resultList = []
        errorIndication, errorStatus, errorIndex, varBindTable = await bulk_cmd(
            SnmpEngine(),
            CommunityData(self.community, mpModel=1),
            await UdpTransportTarget.create((self.ipaddr, self.port)),
            ContextData(),
            nonRepeaters, maxRepetitions,
            *varBinds
        )

        self.deal_error(errorIndication, errorStatus, errorIndex, varBindTable)

        for oid, value in varBindTable:
            result = self.deal_value(oid, value, prettyPrint)
            resultList.append(result)

        print(resultList)
        return resultList


if __name__ == "__main__":
    snmpObject = SNMPManager("192.168.1.121")  # 192.168.1.105 192.168.1.120
    # asyncio.run(snmpObject.get_cmd_many([
    #     ObjectType(ObjectIdentity("1.3.6.1.4.1.1206.4.2.3.3.1.0")),
    #     ObjectType(ObjectIdentity("1.3.6.1.4.1.1206.4.2.3.6.8.0"))]))

    # a = [("dmsMaxChangeableMsg", 0), ("dmsFreeChangeableMemory", 0)]
    # result = asyncio.run(snmpObject.get_cmd_many_mib(a))

    asyncio.run(snmpObject.get_cmd_single_mib("dmsMessageStatus", 3, 1))
    # asyncio.run(snmpObject.get_cmd_single("1.3.6.1.4.1.1206.4.2.3.3.1.0"))
    # 字体名称
    # print("返回",asyncio.run(snmpObject.get_cmd_single("1.3.6.1.4.1.1206.4.2.3.3.2.1.3.3")))
    # asyncio.run(snmpObject.set_cmd("1.3.6.1.4.1.1206.4.2.3.6.1.0",4))
    # result = asyncio.run(snmpObject.get_cmd_single("1.3.6.1.4.1.1206.4.2.3.6.1.0"))
    # print("result: ", result)

    # from pysnmp.hlapi import *
    #
    # # SNMP请求的目标设备和社区字符串
    # target = '192.168.1.120'  # 目标设备的IP地址
    # community = 'public'  # 社区字符串
    # oids = ['1.3.6.1.4.1.1206.4.2.3.3.1.0', '1.3.6.1.4.1.1206.4.2.3.6.8.0']  # 你需要请求的OID列表
    # mib_name = "NTCIP1203v03f-MIB"
    #
    # async def snmp_get():
    #     # 创建UDP传输目标对象，并调用 .create() 进行初始化
    #
    #
    #     # 创建SNMP GET请求
    #     result = get_cmd(
    #         SnmpEngine(),
    #         CommunityData(community,mpModel=0),
    #         await UdpTransportTarget.create((target, 161)),  # 使用已创建的传输目标对象
    #         ContextData(),
    #         # *[ObjectType(ObjectIdentity(oid)) for oid in oids]  # 确保 ObjectType 完全初始化
    #         *(
    #         ObjectType(ObjectIdentity(mib_name, "dmsMaxChangeableMsg",0)),
    #         ObjectType(ObjectIdentity(mib_name, "dmsFreeChangeableMemory",0))
    #         )
    #     )
    #
    #     # 发送请求并处理响应
    #     errorIndication, errorStatus, errorIndex, varBinds = await result
    #
    #     if errorIndication:
    #         print(f"Error: {errorIndication}")
    #     else:
    #         if errorStatus:
    #             print(f"Error: {errorStatus.prettyPrint()}")
    #         else:
    #             for varBind in varBinds:
    #                 print(f'{varBind[0]} = {varBind[1]}')

    # # 启动异步事件循环
    # asyncio.run(snmp_get())
