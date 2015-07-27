# coding=utf-8
import swiftclient
import config.proxyinfo

def makeConnection(needAuth=True, account=config.proxyinfo.swift_default_account, token=config.proxyinfo.swift_default_token, \
tenant=None, username=None, passwd=None):
    if needAuth==None:
        c_puburl=config.proxyinfo.swift_proxy_url+account
        c_token=token
        return swiftclient.client.Connection(preauthurl=c_puburl,preauthtoken=c_token)
    else:
        return swiftclient.client.Connection(authurl=config.proxyinfo.swift_auth_url, user=username, key=passwd, \
        auth_version=config.proxyinfo.auth_server_version, tenant_name=tenant)
