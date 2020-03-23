# -*- coding: utf-8 -*-
# * ********************************************************************* *
# *                                                                       *
# *   Tools to store and manage IDB bills                                 *
# *   This file is part of idbbilling. This project may be found at:      *
# *   https://github.com/IdentityBank/Python_idbbilling.                  *
# *                                                                       *
# *   Copyright (C) 2020 by Identity Bank. All Rights Reserved.           *
# *   https://www.identitybank.eu - You belong to you                     *
# *                                                                       *
# *   This program is free software: you can redistribute it and/or       *
# *   modify it under the terms of the GNU Affero General Public          *
# *   License as published by the Free Software Foundation, either        *
# *   version 3 of the License, or (at your option) any later version.    *
# *                                                                       *
# *   This program is distributed in the hope that it will be useful,     *
# *   but WITHOUT ANY WARRANTY; without even the implied warranty of      *
# *   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the        *
# *   GNU Affero General Public License for more details.                 *
# *                                                                       *
# *   You should have received a copy of the GNU Affero General Public    *
# *   License along with this program. If not, see                        *
# *   https://www.gnu.org/licenses/.                                      *
# *                                                                       *
# * ********************************************************************* *

################################################################################
# Import(s)                                                                    #
################################################################################

import logging

from .ProcessQuery import ProcessQuery
from secureclientserverservice import ScssServerInet, ScssSecurityHelper, ScssSecurityFirewall, ScssProtocol
from idbbilling import IdbConfig


################################################################################
# Module                                                                       #
################################################################################

class IdbServer(ScssServerInet):
    jscConfigFilePath = None
    connectionName = None

    def __init__(self, jscConfigFilePath: str, connectionName: str):
        self.jscConfigFilePath = jscConfigFilePath
        self.connectionName = connectionName
        configuration = IdbConfig.getConfig(jscConfigFilePath, connectionName)
        host = configuration["server"]["host"] if "server" in configuration and "host" in configuration["server"] else ""
        port = configuration["server"]["port"] if "server" in configuration and "port" in configuration["server"] else 87
        self.setConfiguration(configuration["server"])
        self.setConnectionFirewall(ScssSecurityFirewall.load(configuration))
        self.setConnectionSecurity(ScssSecurityHelper.load(configuration))
        super().__init__(host, port)

    def clientActionNone(self, connection, ip, port):
        try:
            idbBillCommand = ScssProtocol.receiveNoneData(connection, self.max_buffer_size)
            idbBillRespond = ProcessQuery.execute(self.jscConfigFilePath, self.connectionName, idbBillCommand)
            if not idbBillRespond:
                idbBillRespond = ''
            else:
                idbBillRespond = str(idbBillRespond)
            ScssProtocol.sendNoneData(connection, idbBillRespond)
        except:
            pass
        finally:
            connection.close()
            logging.info('Connection ' + ip + ':' + port + " ended")

    def clientActionToken(self, connection, ip, port):
        try:
            idbBillCommand = ScssProtocol.receiveTokenData(connection, self.connectionSecurity, self.max_buffer_size)
            idbBillRespond = ProcessQuery.execute(self.jscConfigFilePath, self.connectionName, idbBillCommand)
            if not idbBillRespond:
                idbBillRespond = ''
            else:
                idbBillRespond = str(idbBillRespond)
            ScssProtocol.sendTokenData(connection, self.connectionSecurity, idbBillRespond)
        except:
            pass
        finally:
            connection.close()
            logging.info('Connection ' + ip + ':' + port + " ended")

################################################################################
#                                End of file                                   #
################################################################################
