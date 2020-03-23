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

import json
import logging
from psycopg2 import sql

from .IdbQueryError import IdbQueryError
from .IdbQuerySql import IdbQuerySql
from .IdbQueryResponse import IdbQueryResponse
from .IdbSqlQueryBuilder import IdbSqlQueryBuilder


################################################################################
# Module                                                                       #
################################################################################

class IdbQueryBilling:

    @staticmethod
    def executeQuery(configuration: dict,
                     queryData: dict) -> str:

        returnValue = IdbQueryError.requestError()

        try:
            if isinstance(queryData, dict) and 'query' in queryData and configuration['connectionBilling']:

                queryData['dbTableSchema'] = 'p57b_billing'
                queryData['dbTableSchemaIdentifier'] = sql.Identifier(queryData['dbTableSchema'])
                queryData['dbTableName'] = "{businessDbId}"
                if 'dbHost' in configuration['connectionBilling'] and \
                        'dbPort' in configuration['connectionBilling'] and \
                        'dbName' in configuration['connectionBilling'] and \
                        'dbUser' in configuration['connectionBilling'] and \
                        'dbPassword' in configuration['connectionBilling']:
                    dbConnection = {
                        "host": configuration['connectionBilling']['dbHost'],
                        "port": configuration['connectionBilling']['dbPort'],
                        "database": configuration['connectionBilling']['dbName'],
                        "user": configuration['connectionBilling']['dbUser'],
                        "password": configuration['connectionBilling']['dbPassword'],
                    }
                    if logging.getLevelName(logging.getLogger().getEffectiveLevel()) == 'DEBUG':
                        dbConnectionPrint = dbConnection.copy()
                        dbConnectionPrint.pop("password")
                        logging.debug(json.dumps(dbConnectionPrint))

                if queryData['query'] == 'getPackages':
                    queryData['account'] = "package"
                    if 'dbTableLimit' not in queryData:
                        queryData['dbTableLimit'] = 0
                    queryData['dbTableOrder'] = sql.SQL(', ').join([sql.Identifier('order'), sql.Identifier('id')])
                    returnValue = IdbQuerySql.fetchSqlQuery(dbConnection,
                                                            IdbSqlQueryBuilder.generateSqlGetPackages(
                                                                queryData))
                elif queryData['query'] == 'createPackage':
                    queryData['account'] = "package"
                    returnValue = IdbQuerySql.fetchSqlQuery(dbConnection,
                                                            IdbSqlQueryBuilder.generateSqlCreatePackage(
                                                                queryData), True)
                elif queryData['query'] == 'editPackage':
                    queryData['account'] = "package"
                    returnValue = IdbQuerySql.executeSqlQuery(dbConnection,
                                                              IdbSqlQueryBuilder.generateSqlUpdatePackage(
                                                                  queryData))
                elif queryData['query'] == 'deletePackage':
                    queryData['account'] = "package"
                    returnValue = IdbQuerySql.executeSqlQuery(dbConnection,
                                                              IdbSqlQueryBuilder.generateSqlDeletePackage(
                                                                  queryData))
                elif queryData['query'] == 'getCountAllPackages':
                    queryData['account'] = "package"
                    returnValue = IdbQueryBilling.__findCountAllTable(queryData, dbConnection)
                elif queryData['query'] == 'findActionsCosts':
                    queryData['account'] = "action_cost"
                    if 'dbTableLimit' not in queryData:
                        queryData['dbTableLimit'] = 0
                    returnValue = IdbQuerySql.fetchSqlQuery(dbConnection,
                                                            IdbSqlQueryBuilder.generateSqlFindActionsCosts(
                                                                queryData))
                elif queryData['query'] == 'findCountAllActionsCosts':
                    queryData['account'] = "action_cost"
                    returnValue = IdbQueryBilling.__findCountAllTable(queryData, dbConnection)
                elif queryData['query'] == 'addActionCost':
                    queryData['account'] = "action_cost"
                    returnValue = IdbQuerySql.fetchSqlQuery(dbConnection,
                                                            IdbSqlQueryBuilder.generateSqlAddActionCost(
                                                                queryData), True)
                elif queryData['query'] == 'editActionCost':
                    queryData['account'] = "action_cost"
                    returnValue = IdbQuerySql.executeSqlQuery(dbConnection,
                                                              IdbSqlQueryBuilder.generateSqlEditActionCost(
                                                                  queryData))
                elif queryData['query'] == 'deleteActionCost':
                    queryData['account'] = "action_cost"
                    returnValue = IdbQuerySql.executeSqlQuery(dbConnection,
                                                              IdbSqlQueryBuilder.generateSqlDeleteActionCost(
                                                                  queryData))
                elif queryData['query'] == 'getBusinessPackage':
                    queryData['account'] = "business_package"
                    queryData['dbTableColumnPk'] = "business_id"
                    returnValue = IdbQuerySql.fetchSqlQuery(dbConnection,
                                                            IdbSqlQueryBuilder.generateSqlGetBusinessPackage(
                                                                queryData))
                elif queryData['query'] == 'updateBusinessPackage':
                    queryData['account'] = "business_package"
                    queryData['idbId'] = queryData['id']
                    returnValue = IdbQuerySql.executeSqlQuery(dbConnection,
                                                              IdbSqlQueryBuilder.generateSqlUpdateBusinessPackageItem(
                                                                  queryData))
                elif queryData['query'] == 'assignPackageToBusiness':
                    queryData['account'] = "business_package"
                    returnValue = IdbQuerySql.fetchSqlQuery(dbConnection,
                                                            IdbSqlQueryBuilder.generateSqlAssignPackageToBusiness(
                                                                queryData), True)
                elif queryData['query'] == 'findCountAllBusinessPackage':
                    queryData['account'] = "business_package"
                    returnValue = IdbQueryBilling.__findCountAllTable(queryData, dbConnection)
                elif queryData['query'] == 'addBusiness':
                    queryData['account'] = "business"
                    returnValue = IdbQuerySql.fetchSqlQuery(dbConnection,
                                                            IdbSqlQueryBuilder.generateSqlAddBusiness(
                                                                queryData), True)
                elif queryData['query'] == 'findBusinesses':
                    queryData['account'] = "business"
                    returnValue = IdbQuerySql.fetchSqlQuery(dbConnection,
                                                            IdbSqlQueryBuilder.generateSqlFindBusinesses(
                                                                queryData))
                elif queryData['query'] == 'findCountAllBusinesses':
                    queryData['account'] = "business"
                    returnValue = IdbQueryBilling.__findCountAllTable(queryData, dbConnection)
                elif queryData['query'] == 'findInvoices':
                    queryData['account'] = "invoices"
                    returnValue = IdbQuerySql.fetchSqlQuery(dbConnection,
                                                            IdbSqlQueryBuilder.generateSqlFindInvoices(
                                                                queryData))
                elif queryData['query'] == 'findCountAllInvoices':
                    queryData['account'] = "invoices"
                    returnValue = IdbQueryBilling.__findCountAllTable(queryData, dbConnection)
                elif queryData['query'] == 'getInvoiceForPayment':
                    queryData['account'] = "invoices"
                    if 'paymentId' in queryData:
                        queryData['FilterExpression'] = {
                            "o": "=",
                            "l": "#paymentId",
                            "r": ":paymentId"
                        }
                        queryData['ExpressionAttributeNames'] = {
                            "#paymentId": "payment_id"
                        }
                        queryData['ExpressionAttributeValues'] = {
                            ":paymentId": queryData['paymentId']
                        }
                    returnValue = IdbQueryBilling.__findCountAllTable(queryData, dbConnection)
                elif queryData['query'] == 'getLastInvoiceNumber':
                    queryData['account'] = "invoices"
                    queryData['dbTableLimit'] = 1
                    queryData['DataTypes'] = {"database": ['invoice_number']}
                    queryData['OrderByDataTypes'] = {"timestamp": "DESC"}
                    returnValue = IdbQuerySql.fetchSqlQuery(dbConnection,
                                                            IdbSqlQueryBuilder.generateSqlFindInvoices(
                                                                queryData), True)
                elif queryData['query'] == 'createInvoice':
                    queryData['account'] = "invoices"
                    returnValue = IdbQuerySql.fetchSqlQuery(dbConnection,
                                                            IdbSqlQueryBuilder.generateSqlCreateInvoice(
                                                                queryData), True)
                elif queryData['query'] == 'logPayment':
                    queryData['account'] = "payments"
                    returnValue = IdbQuerySql.fetchSqlQuery(dbConnection,
                                                            IdbSqlQueryBuilder.generateSqlLogPayment(
                                                                queryData), True)
                elif queryData['query'] == 'findPayments':
                    queryData['account'] = "payments"
                    returnValue = IdbQuerySql.fetchSqlQuery(dbConnection,
                                                            IdbSqlQueryBuilder.generateSqlFindPayments(
                                                                queryData))
                elif queryData['query'] == 'findCountAllPayments':
                    queryData['account'] = "payments"
                    returnValue = IdbQueryBilling.__findCountAllTable(queryData, dbConnection)
                elif queryData['query'] == 'getPaymentsForOrganization':
                    queryData['account'] = "payments"
                    if 'oid' in queryData:
                        queryData['FilterExpression'] = {
                            "o": "=",
                            "l": "#oid",
                            "r": ":oid"
                        }
                        queryData['ExpressionAttributeNames'] = {
                            "#oid": "oid"
                        }
                        queryData['ExpressionAttributeValues'] = {
                            ":oid": queryData['oid']
                        }
                    returnValue = IdbQueryBilling.__findCountAllTable(queryData, dbConnection)
                elif queryData['query'] == 'addBillingAuditLog':
                    queryData['dbTableSchema'] = 'p57b_log'
                    queryData['dbTableSchemaIdentifier'] = sql.Identifier(queryData['dbTableSchema'])
                    queryData['account'] = "idb_credits_log"
                    returnValue = IdbQuerySql.fetchSqlQuery(dbConnection,
                                                            IdbSqlQueryBuilder.generateSqlLogBillingAudit(
                                                                queryData), True)
                elif queryData['query'] == 'getCountAllBillingAuditLogsForBusiness':
                    queryData['dbTableSchema'] = 'p57b_log'
                    queryData['dbTableSchemaIdentifier'] = sql.Identifier(queryData['dbTableSchema'])
                    queryData['account'] = "idb_credits_log"
                    if 'oid' in queryData:
                        queryData['FilterExpression'] = {
                            "o": "=",
                            "l": "#column",
                            "r": ":column"
                        }
                        queryData['ExpressionAttributeNames'] = {
                            "#column": "oid"
                        }
                        queryData['ExpressionAttributeValues'] = {
                            ":column": queryData['oid']
                        }
                        returnValue = IdbQueryBilling.__findCountAllTable(queryData, dbConnection)
                    else:
                        returnValue = IdbQueryError.requestError()

                else:
                    returnValue = IdbQueryError.requestNotImplemented()

        except Exception as e:
            returnValue = IdbQueryError.requestUnsupportedService(str(e))
            logging.error('Query error')
            logging.error(str(e))

        return returnValue

    @staticmethod
    def __findCountAllTable(queryData, dbConnection) -> str:
        if 'dbTableLimit' not in queryData:
            queryData['dbTableLimit'] = 0
        returnValue = IdbQuerySql.fetchSqlQuery(dbConnection,
                                                IdbSqlQueryBuilder.generateSqlCountTable(
                                                    dict(queryData)), False, True)
        if returnValue \
                and isinstance(returnValue, dict) \
                and 'Query' in returnValue \
                and returnValue['Query'] == 1 \
                and 'QueryData' in returnValue:
            countAll = returnValue['QueryData']
            if 'dbTableLimit' not in queryData:
                queryData['dbTableLimit'] = 0
            returnValue = IdbQuerySql.fetchSqlQuery(dbConnection,
                                                    IdbSqlQueryBuilder.generateSqlFindTable(
                                                        queryData), False, True)
            if returnValue \
                    and isinstance(returnValue, dict) \
                    and 'Query' in returnValue \
                    and 'QueryData' in returnValue:
                returnValue['CountAll'] = countAll
                returnValue = IdbQueryResponse.responseOkDict(returnValue)
            else:
                returnValue = IdbQueryError.requestQueryError()
        else:
            returnValue = IdbQueryError.requestQueryError()
        return returnValue

################################################################################
#                                End of file                                   #
################################################################################
