package com.ahmrh.amryauth.data

import com.ahmrh.amryauth.data.local.database.Auth
import com.ahmrh.amryauth.data.local.database.AuthDao
import kotlinx.coroutines.flow.Flow


class Repository(
    private val authDao: AuthDao
){

    fun getAllAuths(): Flow<List<Auth>> = authDao.getAllAuths()

    suspend fun insertAuth(auth: Auth) = authDao.insert(auth)

    suspend fun deleteAuth(auth: Auth) = authDao.delete(auth)
}