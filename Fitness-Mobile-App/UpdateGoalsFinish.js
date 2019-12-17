import React from 'react';
import { View, TouchableOpacity, Text, KeyboardAvoidingView, Alert, TextInput } from 'react-native';
import {styles} from './Style'

function updateNameAndGoals(navigation) {
  let username = navigation.dangerouslyGetParent().dangerouslyGetParent().getParam('username');
  let userToken = navigation.dangerouslyGetParent().dangerouslyGetParent().getParam('userToken');
  const url = 'https://mysqlcs639.cs.wisc.edu/users/' + username;
  let fetchData = {
    method: 'PUT',
    headers: {
      'Accept': 'application/json',
      'Content-Type': 'application/json',
      'x-access-token': userToken,
    },
    body: JSON.stringify({
      "admin": navigation.getParam('admin'),
      "firstName": navigation.getParam('firstName'),
      "goalDailyActivity": navigation.getParam('goalDailyActivity'),
      "goalDailyCalories": navigation.getParam('goalDailyCalories'),
      "goalDailyCarbohydrates": navigation.getParam('goalDailyCarbohydrates'),
      "goalDailyFat": navigation.getParam('goalDailyFat'),
      "goalDailyProtein": navigation.getParam('goalDailyProtein'),
      "lastName": navigation.getParam('lastName'),
      "username": navigation.getParam('username'),
    }),
    redirect: 'follow',
  };
  fetch(url, fetchData)
  .then(response => response.json())
  .then(result => {
    if ("message" in result && result.message === 'User has been updated!') {
      console.log("update goals finish.");
      navigation.navigate('Settings');
    }
    else {
      Alert.alert("User info not updated. Check your input.");
      navigation.navigate('UpdateGoals');
    }
  })
  .catch(error => Alert.alert("Error 2", error.message));
}

const UpdateGoalsFinish = ({ navigation }) => {
  updateNameAndGoals(navigation);
  return (
    <View style={styles.container}>
      <KeyboardAvoidingView style={styles.container} behavior="padding">
        <Text style={styles.textCenter}>Updating...</Text>
      </KeyboardAvoidingView>
    </View>
  )
};

export default UpdateGoalsFinish;