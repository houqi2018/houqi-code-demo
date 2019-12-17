import React from 'react';
import { View, TouchableOpacity, Text, KeyboardAvoidingView, Alert, TextInput } from 'react-native';
import {styles} from './Style'
import base64 from 'base-64';

function login(navigation) {
  const url = 'https://mysqlcs639.cs.wisc.edu/login';
  let username = navigation.getParam('username');
  let password = navigation.getParam('password');
  let fetchData = { 
    method: 'GET',
    headers: {
      'Authorization': 'Basic ' + base64.encode(username + ":" + password),
    },
    redirect: 'follow',
  };
  fetch(url, fetchData)
  .then(response => response.json())
  .then(result => {
    // Check validity of the token
    if (!("message" in result) && "token" in result) {
      console.log("debug login:", username, result.token);
      // navigation.push('Settings', {username: username, userToken: result.token});
      navigation.navigate('App', {username: username, userToken: result.token});
    }
    else {
      console.log("message in login:", result.message);
      Alert.alert(result.message);
    }
  })
  .catch(error => Alert.alert(error.message));
};

const Login = ({ navigation }) => {
  return (
    <View style={styles.container}>
      <KeyboardAvoidingView style={styles.container} behavior="padding">
      <TextInput value={navigation.getParam('username')} onChangeText={(username) => navigation.setParams({username: username})} placeholder={'Username'} style={styles.input}/>
      <TextInput value={navigation.getParam('password')} onChangeText={(password) => navigation.setParams({password: password})} placeholder={'Password'} style={styles.input} secureTextEntry={true}/>
      <TouchableOpacity style={styles.button} onPress={() => {login(navigation)}}><Text style={styles.textWhite}>Log In</Text></TouchableOpacity>
      <TouchableOpacity style={styles.signup} onPress={() => navigation.navigate('Signup')}><Text>New? Sign Up</Text></TouchableOpacity>
      </KeyboardAvoidingView>
    </View>
  );
};

export default Login;