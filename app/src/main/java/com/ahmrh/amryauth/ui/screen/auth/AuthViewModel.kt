package com.ahmrh.amryauth.ui.screen.auth

import android.util.Log
import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.ahmrh.amryauth.common.UiState
import com.ahmrh.amryauth.data.Repository
import com.ahmrh.amryauth.data.local.database.Auth
import com.chaquo.python.Python
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.catch
import kotlinx.coroutines.launch
import javax.inject.Inject

@HiltViewModel
class AuthViewModel @Inject constructor(
    private val repository: Repository
) : ViewModel() {

    private var _authsUiState: MutableStateFlow<UiState<List<Auth>>> =
        MutableStateFlow(UiState.Idle)
    val authsUiState: StateFlow<UiState<List<Auth>>>
        get() = _authsUiState

    init {
        initUi()

    }

    private fun initUi(){

        viewModelScope.launch {
            val authsFlow = repository.getAllAuths()
            authsFlow
                .catch { e ->
                    _authsUiState.emit(UiState.Error(e.localizedMessage.toString()))
                }
                .collect { auths ->
                    _authsUiState.emit(UiState.Success())
                }
        }
    }

    private fun generateTOTP(key: String){
        val py = Python.getInstance()
        val module = py.getModule( "TOTP" )
        val TOTP = module["getTOTP"]


    }

    fun insertAuth(token: String) {
        viewModelScope.launch {
            repository.insertAuth(Auth(token = token))
            Log.d(TAG, authsUiState.value.toString())
        }
    }

    fun deleteAuth(auth: Auth){
        viewModelScope.launch{
            repository.deleteAuth(auth)
            Log.d(TAG, authsUiState.value.toString())

        }
    }

    companion object {
        private const val TAG = "AuthViewModel"
    }


}