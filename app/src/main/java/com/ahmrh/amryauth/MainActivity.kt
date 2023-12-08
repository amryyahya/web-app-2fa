package com.ahmrh.amryauth

import android.os.Bundle
import android.widget.Toast
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.hilt.navigation.compose.hiltViewModel
import androidx.navigation.compose.NavHost
import androidx.navigation.compose.composable
import androidx.navigation.compose.rememberNavController
import com.ahmrh.amryauth.ui.navigation.Screen
import com.ahmrh.amryauth.ui.screen.auth.AuthScreen
import com.ahmrh.amryauth.ui.screen.auth.AuthViewModel
import com.ahmrh.amryauth.ui.screen.scanner.ScannerScreen
import com.ahmrh.amryauth.ui.theme.AmryAuthTheme
import com.chaquo.python.Python
import com.chaquo.python.android.AndroidPlatform
import com.google.mlkit.vision.barcode.common.Barcode
import com.google.mlkit.vision.codescanner.GmsBarcodeScannerOptions
import com.google.mlkit.vision.codescanner.GmsBarcodeScanning
import dagger.hilt.android.AndroidEntryPoint

@AndroidEntryPoint
class MainActivity : ComponentActivity() {

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        if( !Python.isStarted()) {
            Python.start(AndroidPlatform(this))
        }

        setContent {
            AmryAuthTheme {
                val navController = rememberNavController()
                NavHost(
                    navController = navController,
                    startDestination = Screen.Auth.route
                ) {
                    composable(route = Screen.Auth.route) {
                        val authViewModel: AuthViewModel = hiltViewModel()
                        AuthScreen(
                            navHostController = navController,
                            googleCodeScanner = {
                                googleCodeScanner(authViewModel::insertAuth)
                            },
                            viewModel = authViewModel,
                        )
                    }
                    composable(route = Screen.Scanner.route) {

                        ScannerScreen(navHostController = navController)
                    }
                }
            }
        }

    }


    private fun googleCodeScanner(insertAuth: (String) -> Unit) {
        val options = GmsBarcodeScannerOptions.Builder()
            .setBarcodeFormats(
                Barcode.FORMAT_QR_CODE,
                Barcode.FORMAT_AZTEC
            )
            .enableAutoZoom() // available on 16.1.0 and higher
            .build()

        val scanner = GmsBarcodeScanning.getClient(this, options)
        scanner.startScan()
            .addOnSuccessListener { barcode ->
                Toast.makeText(this, "Barcode found", Toast.LENGTH_LONG).show()

                val url = barcode.url!!.url
                insertAuth(url ?: "Unidentified Url")
            }
            .addOnCanceledListener {
                // Task canceled
                Toast.makeText(this, "Canceled", Toast.LENGTH_LONG).show()
            }
            .addOnFailureListener { e ->
                // Task failed with an exception
                Toast.makeText(this, "Failure", Toast.LENGTH_LONG).show()
            }
    }

}
