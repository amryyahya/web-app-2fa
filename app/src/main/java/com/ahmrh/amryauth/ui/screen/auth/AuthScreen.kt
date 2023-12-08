package com.ahmrh.amryauth.ui.screen.auth

import android.content.res.Configuration
import androidx.compose.animation.animateColorAsState
import androidx.compose.animation.core.animateFloatAsState
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Add
import androidx.compose.material.icons.outlined.Delete
import androidx.compose.material3.CircularProgressIndicator
import androidx.compose.material3.DismissDirection
import androidx.compose.material3.DismissValue
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.FloatingActionButton
import androidx.compose.material3.Icon
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Surface
import androidx.compose.material3.SwipeToDismiss
import androidx.compose.material3.Text
import androidx.compose.material3.TopAppBar
import androidx.compose.material3.TopAppBarDefaults.topAppBarColors
import androidx.compose.material3.rememberDismissState
import androidx.compose.runtime.Composable
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.scale
import androidx.compose.ui.tooling.preview.Preview
import androidx.compose.ui.unit.dp
import androidx.hilt.navigation.compose.hiltViewModel
import androidx.navigation.NavHostController
import com.ahmrh.amryauth.common.UiState
import com.ahmrh.amryauth.data.local.database.Auth
import com.ahmrh.amryauth.ui.components.AuthItem
import com.ahmrh.amryauth.ui.theme.AmryAuthTheme

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun AuthScreen(
    viewModel: AuthViewModel = hiltViewModel(),
    navHostController: NavHostController? = null,
    googleCodeScanner: () -> Unit,
) {



    Scaffold(
        topBar = {
            TopAppBar(
                title = {
                    Text("Photon Authenticator")
                },
                colors = topAppBarColors(
                    containerColor = MaterialTheme.colorScheme.primaryContainer,
                    titleContentColor = MaterialTheme.colorScheme.onPrimaryContainer
                )
            )
        },
        floatingActionButton = {
            FloatingActionButton(onClick = {
//                navHostController?.navigate(Screen.Scanner.route)

//                viewModel.insertAuth("some_random_token")
                googleCodeScanner()


            }) {
                Icon(Icons.Default.Add, contentDescription = "Add")
            }
        },
    ) { innerPadding ->

        Surface(
            modifier = Modifier.padding(innerPadding)
        ) {

            when (val uiState = viewModel.authsUiState.collectAsState().value) {
                is UiState.Idle -> {
                    AuthList(emptyList())
                }

                is UiState.Loading -> {
                    Loading()
                }

                is UiState.Success -> {
                    val auths = uiState.data
                    AuthList(auths, viewModel)
                }

                is UiState.Error -> {
                    Error(uiState.errorMessage)
                }
            }

        }


    }
}

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun AuthList(
    list: List<Auth>,
    viewModel: AuthViewModel? = null,
) {
    LazyColumn(
        modifier = Modifier.padding(horizontal = 16.dp, vertical = 8.dp),
        verticalArrangement = Arrangement.spacedBy(16.dp)
    ) {
        items(list) { auth ->

            val dismissState = rememberDismissState()

            if (dismissState.isDismissed(direction = DismissDirection.EndToStart)) {
                viewModel?.deleteAuth(auth)
            }
            SwipeToDismiss(
                state = dismissState,
                directions = setOf(
                    DismissDirection.EndToStart
                ),
                background = {
                    // this background is visible when we swipe.
                    // it contains the icon

                    // background color
                    val backgroundColor by animateColorAsState(
                        when (dismissState.targetValue) {
                            DismissValue.DismissedToStart -> MaterialTheme.colorScheme.error.copy(alpha = 0.8f)
                            else -> MaterialTheme.colorScheme.surface
                        }, label = "Background Color"
                    )

                    // icon size
                    val iconScale by animateFloatAsState(
                        targetValue = if (dismissState.targetValue == DismissValue.DismissedToStart) 1.3f else 0.5f,
                        label = "Icon Size"
                    )

                    Box(
                        Modifier
                            .fillMaxSize()
                            .background(color = backgroundColor)
                            .padding(end = 16.dp), // inner padding
                        contentAlignment = Alignment.CenterEnd // place the icon at the end (left)
                    ) {
                        Icon(
                            modifier = Modifier.scale(iconScale),
                            imageVector = Icons.Outlined.Delete,
                            contentDescription = "Delete",
                            tint =  MaterialTheme.colorScheme.surface
                        )
                    }
                },
                dismissContent = {

                    AuthItem(auth = auth)
                }
            )
        }

    }
}


@Composable
fun Loading() {
    CircularProgressIndicator()
}

@Composable
fun Error(errorMessage: String) {
    Text(errorMessage)
}

@Preview(showBackground = true, uiMode = Configuration.UI_MODE_NIGHT_YES)
@Composable
fun AuthScreenPreview() {
    AmryAuthTheme {
    }
}