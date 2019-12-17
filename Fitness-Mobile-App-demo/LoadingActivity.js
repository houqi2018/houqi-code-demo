import React from 'react';
import { View, TouchableOpacity, Text, ScrollView, KeyboardAvoidingView, Alert, TextInput } from 'react-native';
import {styles} from './Style'

function RunThisFirst(navigation) {
  let userToken = navigation.dangerouslyGetParent().dangerouslyGetParent().getParam('userToken');
  const url = 'https://mysqlcs639.cs.wisc.edu/activities/';
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
      Alert.alert("Error 0", result.message);
    }
    else if ("activities" in result) {
      // Pass data to Activity and Go to Activity after fetching data
      let data = [];
      Object.values(result.activities).forEach((act) => {
        data.push({
            id: act.id,
            name: act.name, 
            duration: act.duration,
            date: act.date.slice(0,10) + ' ' + act.date.slice(11,19),
            calories: act.calories,
        });
      })
      navigation.navigate('Activity', {activities: data});
      console.log("in LoadingActivity: set params successfully");
    }
    else {
      console.log("Error in LoadingActivity: set params failure");
    }
  })
  .catch(error => Alert.alert("Error 1", error.message));
}

const LoadingActivity = ({ navigation }) => {
  RunThisFirst(navigation);
  return (
    <View style={styles.container}>
      <KeyboardAvoidingView style={styles.container} behavior="padding">
        <Text style={styles.textCenter}>Loading...</Text>
      </KeyboardAvoidingView>
    </View>
  )
};

export default LoadingActivity;