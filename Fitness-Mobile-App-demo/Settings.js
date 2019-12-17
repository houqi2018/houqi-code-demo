import React from 'react';
import { View, TouchableOpacity, Text, KeyboardAvoidingView, Alert, TextInput } from 'react-native';
import {styles} from './Style'

function logout(navigation) {
  navigation.navigate('Login');
}

function deleteAccount(navigation) {
  let username = navigation.dangerouslyGetParent().dangerouslyGetParent().getParam('username');
  let userToken = navigation.dangerouslyGetParent().dangerouslyGetParent().getParam('userToken');
  const url = 'https://mysqlcs639.cs.wisc.edu/users/' + username;
  let fetchData = { 
    method: 'DELETE',
    headers: {
      'x-access-token': userToken,
    },
    redirect: 'follow',
  };
  fetch(url, fetchData)
  .then(response => response.json())
  .then(result => {
    if ("message" in result && result.message === 'User has been deleted!') {
      navigation.navigate('Login');
    }
    else {
      Alert.alert("Account not deleted.");
    }
  })
  .catch(error => Alert.alert("Error 3", error.message));
}

const Settings = ({ navigation }) => {
  return (
    <View style={styles.container}>
      <KeyboardAvoidingView style={styles.container} behavior="padding">
        <TouchableOpacity style={styles.button} onPress={() => navigation.navigate('LoadingUpdateGoals')}><Text style={styles.textWhite}>Update Goals</Text></TouchableOpacity>
        <TouchableOpacity style={styles.button} onPress={() => logout(navigation)}><Text style={styles.textWhite}>Log Out</Text></TouchableOpacity>
        <TouchableOpacity style={styles.buttonDeleteAccount} onPress={() => deleteAccount(navigation)}><Text style={styles.textWhite}>Delete Account</Text></TouchableOpacity>
      </KeyboardAvoidingView>
    </View>
  )
};

export default Settings;