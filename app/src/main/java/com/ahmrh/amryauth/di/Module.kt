package com.ahmrh.amryauth.di

import android.content.Context
import com.ahmrh.amryauth.data.Repository
import com.ahmrh.amryauth.data.local.database.AppDatabase
import dagger.Module
import dagger.Provides
import dagger.hilt.InstallIn
import dagger.hilt.android.qualifiers.ApplicationContext
import dagger.hilt.components.SingletonComponent
import javax.inject.Singleton

@Module
@InstallIn(SingletonComponent::class)
object Module {

    @Provides
    @Singleton
    fun providesRepository(@ApplicationContext context: Context): Repository{
        return Repository(AppDatabase.getDatabase(context).authDao())
    }




}