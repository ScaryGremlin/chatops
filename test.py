import smbclient
from smb.SMBConnection import SMBConnection
from smb import security_descriptors

import smb.security_descriptors

from smbprotocol.file_info import (
    InfoType,
)

from smbprotocol.open import (
    DirectoryAccessMask,
    FilePipePrinterAccessMask,
    SMB2QueryInfoRequest,
    SMB2QueryInfoResponse,
    SMB2SetInfoRequest
)

from smbprotocol.security_descriptor import (
    SMB2CreateSDBuffer,
)

# Not needed when using Kerberos auth, can also be set as kwargs when calling open_file.
smbclient.ClientConfig(username=r"CO\Administrator", password='RP21-kmn6root')


class SecurityInfo:
    Owner = 0x00000001
    Group = 0x00000002
    Dacl = 0x00000004
    Sacl = 0x00000008
    Label = 0x00000010
    Attribute = 0x00000020
    Scope = 0x00000040
    Backup = 0x00010000




def get_sd(fd, info):
    """ Get the Security Descriptor for the opened file. """
    query_req = SMB2QueryInfoRequest()
    permissions = SMB2SetInfoRequest()

    query_req['info_type'] = InfoType.SMB2_0_INFO_SECURITY
    query_req['output_buffer_length'] = 65535
    query_req['additional_information'] = info
    query_req['file_id'] = fd.file_id

    req = fd.connection.send(query_req, sid=fd.tree_connect.session.session_id, tid=fd.tree_connect.tree_connect_id)
    resp = fd.connection.receive(req)
    query_resp = SMB2QueryInfoResponse()
    query_resp.unpack(resp['data'].get_value())

    security_descriptor = SMB2CreateSDBuffer()
    security_descriptor.unpack(query_resp['buffer'].get_value())

    return security_descriptor


# # File example
# with smbclient.open_file(r'\\192.168.213.238\exchange\temp\file.txt', mode='rb', buffering=0,
#                          desired_access=FilePipePrinterAccessMask.READ_CONTROL) as fd:
#     sd = get_sd(fd.fd, SecurityInfo.Owner | SecurityInfo.Dacl)
#     print(str(sd.get_owner()))
#     print(str(sd.get_dacl()['aces']))



connection = SMBConnection(username="Administrator",
                                          password="",
                                          my_name="python_script",
                                          remote_name="dc-exchange.mfcmgo.ru",
                                          domain="",
                                          use_ntlm_v2=True)

connection.connect("192.168.213.238")
for path in connection.listPath("exchange", "/"):
            print(path.filename)



# Dir example
# with smbclient.open_file(r"\\192.168.213.238\exchange\temp", mode='br', buffering=0, file_type='dir',
#                          desired_access=DirectoryAccessMask.READ_CONTROL) as fd:
#     sd = get_sd(fd.fd, SecurityInfo.Owner | SecurityInfo.Dacl)
    #print(sd.set_owner())
    # print(str(sd.get_owner()))
    # print(sd.get_dacl().fields)
    # print(sd.get_dacl()["acl_revision"])
    # print(sd.get_dacl())

    # for element in sd.get_dacl():
    #     print(element)



