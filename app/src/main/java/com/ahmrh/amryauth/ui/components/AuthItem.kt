package com.ahmrh.amryauth.ui.components

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.material3.Divider
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.tooling.preview.Preview
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.ahmrh.amryauth.ui.theme.AmryAuthTheme

@Composable
fun AuthItem(
    modifier: Modifier = Modifier,
    username: String? = null,
    token: String? = null,
    ticks: Int = 1,
    maxTick: Int = 30,
){
    Column(
        modifier = modifier
            .fillMaxWidth()
            .padding(horizontal = 16.dp,)
    ){
        Text(username ?: "Unidentified", fontSize = 24.sp)

        Row(
            modifier = Modifier.fillMaxWidth(),
            horizontalArrangement = Arrangement.SpaceBetween
        ){
            Text( token ?: "000 000", fontSize = 32.sp, color = MaterialTheme.colorScheme.primary)

            Indicator(sweepAngle = ticks / maxTick.toFloat() * 360)

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