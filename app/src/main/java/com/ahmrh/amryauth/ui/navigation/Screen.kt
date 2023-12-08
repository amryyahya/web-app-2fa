package com.ahmrh.amryauth.ui.navigation

import androidx.compose.runtime.Composable
import com.ahmrh.amryauth.ui.screen.auth.AuthScreen

sealed class Screen(val route: String){
    data object Auth: Screen(route = "auth")
    data object Scanner: Screen(route = "scanner")
}
