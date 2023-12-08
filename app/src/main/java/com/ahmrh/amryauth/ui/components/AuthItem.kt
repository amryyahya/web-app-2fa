package com.ahmrh.amryauth.ui.components

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.material3.CircularProgressIndicator
import androidx.compose.material3.Divider
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.tooling.preview.Preview
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.ahmrh.amryauth.data.local.database.Auth
import com.ahmrh.amryauth.ui.theme.AmryAuthTheme

@Composable
fun AuthItem(
    modifier: Modifier = Modifier,
    auth: Auth? = null
){
    Column(
        modifier = modifier.fillMaxWidth()
    ){
        Text(auth?.token ?: "Identifier", fontSize = 24.sp)

        Row(
            modifier = Modifier.fillMaxWidth(),
            horizontalArrangement = Arrangement.SpaceBetween
        ){
            Text( auth?.token ?: "123 456", fontSize = 32.sp, color = MaterialTheme.colorScheme.primary)

            CircularProgressIndicator()

        }

        Spacer(modifier = Modifier.height(8.dp))
        Divider(color = MaterialTheme.colorScheme.outline, thickness = 1.dp)
    }
}

@Preview(showBackground = true)
@Composable
fun AuthItemPreview(){
    AmryAuthTheme {
        AuthItem()
    }
}