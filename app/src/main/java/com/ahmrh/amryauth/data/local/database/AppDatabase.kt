package com.ahmrh.amryauth.data.local.database

import android.content.Context
import androidx.room.Database
import androidx.room.Room
import androidx.room.RoomDatabase

@Database(
    entities = [Auth::class], version = 1, exportSchema = false,

)
abstract class AppDatabase : RoomDatabase() {
    abstract fun authDao(): AuthDao

    companion object {
        @Volatile
        private var Instance: AppDatabase? = null

        fun getDatabase(context: Context): AppDatabase {
            return Instance ?: synchronized(this) {
                Room.databaseBuilder(context, AppDatabase::class.java, "auth_database")
                    .build()
                    .also { Instance = it }
            }
        }

    }

}