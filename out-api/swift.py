# coding=utf-8
import swiftclient
import config.proxyinfo
from iobase import iobase

def makeConnection(needAuth=True, account=config.proxyinfo.swift_default_account, token=config.proxyinfo.swift_default_token, \
tenant=None, username=None, passwd=None):
    if needAuth==None:
        c_puburl=config.proxyinfo.swift_proxy_url+account
        c_token=token
        return swiftclient.client.Connection(preauthurl=c_puburl,preauthtoken=c_token)
    else:
        return swiftclient.client.Connection(authurl=config.proxyinfo.swift_auth_url, user=username, key=passwd, \
        auth_version=config.proxyinfo.auth_server_version, tenant_name=tenant)

class io_swift(iobase):
    # WARN: never forget to handle authentication error.
    metadata_prefix=u"X-Object-Meta-"

    def __init__(self,*args, **kw):
        self.swiftClient=makeConnection(*args, **kw)
        self.container=u"testcon"

    def put(self,filename,content,info={}):
        # WARN: add MD5 checksum in the future
        toput={}
        for key in info:
            toput[io_swift.metadata_prefix+key]=info[key]
        self.swiftClient.put_object(container=self.container,obj=filename,contents=content,headers=toput)

    def get(self,filename):
        '''if exist, return data buffer. Otherwise return None'''
        try:
            h,c=self.swiftClient.get_object(container=self.container,obj=filename)
        except swiftclient.exceptions.ClientException as e:
            if e.http_status==404:
                return None
            raise e
        nh={}
        for key in h:
            if key.startswith(io_swift.metadata_prefix):
                nh[key[len(io_swift.metadata_prefix):]]=h[key]
        return (nh,c)

    def putinfo(self,filename,info={}):
        toput={}
        for key in info:
            toput[io_swift.metadata_prefix+key]=info[key]
        self.swiftClient.post_object(container=self.container,obj=filename,headers=toput)

    def getinfo(self,filename):
        '''if exist, return data buffer. Otherwise return None'''
        try:
            h=self.swiftClient.head_object(container=self.container,obj=filename)
        except swiftclient.exceptions.ClientException as e:
            if e.http_status==404:
                return None
            raise e
        nh={}
        for key in h:
            if key.startswith(io_swift.metadata_prefix):
                nh[key[len(io_swift.metadata_prefix):]]=h[key]
        return nh
