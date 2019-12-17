import React from 'react';
import { View, TouchableOpacity, Text, KeyboardAvoidingView, Alert, TextInput } from 'react-native';
import {styles} from './Style'

function signup(navigation) {
  const url = 'https://mysqlcs639.cs.wisc.edu/users';
  let username = navigation.getParam('username');
  let password = navigation.getParam('password');
  let fetchData = { 
    method: 'POST',
    headers: {
      'Accept': 'application/json',
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
        'username': username,
        'password': password,
    }),
    redirect: 'follow',
  };
  fetch(url, fetchData)
  .then(response => response.json())
  .then(result => {
    Alert.alert(result.message);
    // Go to log in page on successful signing up
    if ("message" in result && result.message == "User created!") {
      navigation.navigate('LogIn');
    }
  })
  .catch(error => Alert.alert(error.message));
};

const Signup = ({ navigation }) => {
  return (
    <View style={styles.container}>
      <KeyboardAvoidingView style={styles.container} behavior="padding">
      <TextInput value={navigation.getParam('username')} onChangeText={(username) => navigation.setParams({username: username})} placeholder={'Username'} style={styles.input}/>
      <TextInput value={navigation.getParam('password')} onChangeText={(password) => navigation.setParams({password: password})} placeholder={'Password'} style={styles.input} secureTextEntry={true}/>
      <TouchableOpacity style={styles.button} onPress={() => {signup(navigation)}}><Text style={styles.textWhite}>Sign Up</Text></TouchableOpacity>
      <TouchableOpacity style={styles.signup} onPress={() => navigation.navigate('Login')}><Text>Go back to Log In</Text></TouchableOpacity>
      </KeyboardAvoidingView>
    </View>
  );
};

export default Signup;