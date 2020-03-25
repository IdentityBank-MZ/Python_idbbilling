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

from psycopg2 import sql

import idbank.idbankquery.IdbSqlQueryBuilder as IdbGenericSqlQueryBuilder


################################################################################
# Module                                                                       #
################################################################################

class IdbSqlQueryBuilder:

    @staticmethod
    def generateSqlGetPackages(queryData: dict) -> str:
        return IdbGenericSqlQueryBuilder.generateSqlGenericFindItems(queryData)

    @staticmethod
    def generateSqlCreatePackage(queryData: dict) -> str:
        return IdbGenericSqlQueryBuilder.generateSqlGenericPutItem(queryData)

    @staticmethod
    def generateSqlUpdateBusinessPackageItem(queryData: dict) -> str:
        return IdbGenericSqlQueryBuilder.generateSqlGenericUpdateItem(queryData)

    @staticmethod
    def generateSqlUpdatePackage(queryData: dict) -> str:
        if 'pid' in queryData and isinstance(queryData['pid'], int):
            queryData['dbTablePk'] = sql.SQL(str(queryData['pid']))
        return IdbGenericSqlQueryBuilder.generateSqlGenericUpdateItem(queryData)

    @staticmethod
    def generateSqlDeletePackage(queryData: dict) -> str:
        if 'pid' in queryData and isinstance(queryData['pid'], int):
            queryData['dbTablePk'] = sql.SQL(str(queryData['pid']))
        return IdbGenericSqlQueryBuilder.generateSqlGenericDeleteItem(queryData)

    @staticmethod
    def generateSqlCountTable(queryData: dict) -> str:
        queryData['businessDbId'] = queryData['account']
        queryData['dbTableName'] = queryData['dbTableName'].format(**queryData)
        queryData['dbTableNameIdentifier'] = sql.Identifier(queryData['dbTableName'])
        queryData = IdbGenericSqlQueryBuilder.generateSqlGenericTableCondition(queryData)
        return IdbGenericSqlQueryBuilder.generateSqlCountAllItems(queryData)

    @staticmethod
    def generateSqlFindTable(queryData: dict) -> str:
        return IdbGenericSqlQueryBuilder.generateSqlGenericFindItems(queryData)

    @staticmethod
    def generateSqlFindActionsCosts(queryData: dict) -> str:
        return IdbGenericSqlQueryBuilder.generateSqlGenericFindItems(queryData)

    @staticmethod
    def generateSqlAddActionCost(queryData: dict) -> str:
        return IdbGenericSqlQueryBuilder.generateSqlGenericPutItem(queryData)

    @staticmethod
    def generateSqlEditActionCost(queryData: dict) -> str:
        if 'id' in queryData and isinstance(queryData['id'], int):
            queryData['dbTablePk'] = sql.SQL(str(queryData['id']))
        return IdbGenericSqlQueryBuilder.generateSqlGenericUpdateItem(queryData)

    @staticmethod
    def generateSqlDeleteActionCost(queryData: dict) -> str:
        if 'id' in queryData and isinstance(queryData['id'], int):
            queryData['dbTablePk'] = sql.SQL(str(queryData['id']))
        return IdbGenericSqlQueryBuilder.generateSqlGenericDeleteItem(queryData)

    @staticmethod
    def generateSqlGetBusinessPackage(queryData: dict) -> str:
        if 'businessId' in queryData:
            queryData['dbTablePk'] = sql.Literal(queryData['businessId'])
        return IdbGenericSqlQueryBuilder.generateSqlGenericGetItem(queryData)

    @staticmethod
    def generateSqlAssignPackageToBusiness(queryData: dict) -> str:
        return IdbGenericSqlQueryBuilder.generateSqlGenericPutItem(queryData)

    @staticmethod
    def generateSqlFindBusinesses(queryData: dict) -> str:
        return IdbGenericSqlQueryBuilder.generateSqlGenericFindItems(queryData)

    @staticmethod
    def generateSqlFindInvoices(queryData: dict) -> str:
        return IdbGenericSqlQueryBuilder.generateSqlGenericFindItems(queryData)

    @staticmethod
    def generateSqlCreateInvoice(queryData: dict) -> str:
        return IdbGenericSqlQueryBuilder.generateSqlGenericPutItem(queryData)

    @staticmethod
    def generateSqlLogPayment(queryData: dict) -> str:
        return IdbGenericSqlQueryBuilder.generateSqlGenericPutItem(queryData)

    @staticmethod
    def generateSqlFindPayments(queryData: dict) -> str:
        return IdbGenericSqlQueryBuilder.generateSqlGenericFindItems(queryData)

    @staticmethod
    def generateSqlLogBillingAudit(queryData: dict) -> str:
        return IdbGenericSqlQueryBuilder.generateSqlGenericPutItem(queryData)

    @staticmethod
    def generateSqlAddBusiness(queryData: dict) -> str:
        return IdbGenericSqlQueryBuilder.generateSqlGenericPutItem(queryData)

################################################################################
#                                End of file                                   #
################################################################################
