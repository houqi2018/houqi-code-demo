import React from 'react';
import { View, TouchableOpacity, Text, KeyboardAvoidingView, Alert, TextInput } from 'react-native';
import {styles} from './Style'

function RunThisFirst(navigation) {
  let username = navigation.dangerouslyGetParent().dangerouslyGetParent().getParam('username');
  let userToken = navigation.dangerouslyGetParent().dangerouslyGetParent().getParam('userToken');
  const url = 'https://mysqlcs639.cs.wisc.edu/users/' + username;
  let fetchData = { 
    method: 'GET',
    headers: {
      'x-access-token': userToken,
    },
    redirect: 'follow',
  };
  fetch(url, fetchData)
  .then(response => response.json())
  .then(result => {
    if ("message" in result) {
      Alert.alert("Error",result.message);
    }
    else {
      // Pass data to Today and Go to Today after fetching data
      let data = {
        admin: result.admin,
        firstName: result.firstName,
        lastName: result.lastName,
        goalDailyActivity: JSON.stringify(result.goalDailyActivity),
        goalDailyCalories: JSON.stringify(result.goalDailyCalories),
        goalDailyCarbohydrates: JSON.stringify(result.goalDailyCarbohydrates),
        goalDailyFat: JSON.stringify(result.goalDailyFat),
        goalDailyProtein: JSON.stringify(result.goalDailyProtein),
      };
      navigation.navigate('UpdateGoals', data);
      console.log("in LoadingUpdateGoals: set params successfully")
    }
  })
  .catch(error => Alert.alert("Error 4", error.message));
}

const LoadingUpdateGoals = ({ navigation }) => {
  RunThisFirst(navigation);
  return (
    <View style={styles.container}>
      <KeyboardAvoidingView style={styles.container} behavior="padding">
        <Text style={styles.textCenter}>Loading...</Text>
      </KeyboardAvoidingView>
    </View>
  )
};

export default LoadingUpdateGoals;