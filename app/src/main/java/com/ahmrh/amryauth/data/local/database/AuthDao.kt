package com.ahmrh.amryauth.data.local.database

import androidx.room.Dao
import androidx.room.Delete
import androidx.room.Insert
import androidx.room.OnConflictStrategy
import androidx.room.Query
import kotlinx.coroutines.flow.Flow

@Dao
interface AuthDao {
    @Insert(onConflict = OnConflictStrategy.IGNORE)
    suspend fun insert(auth: Auth)

    @Delete
    suspend fun delete(auth: Auth)

    @Query("SELECT * FROM auth")
    fun getAllAuths(): Flow<List<Auth>>
}