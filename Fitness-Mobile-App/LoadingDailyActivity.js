import React from 'react';
import { View, TouchableOpacity, Text, ScrollView, KeyboardAvoidingView, Alert, TextInput } from 'react-native';
import {styles} from './Style'

function RandomMeals(navigation) {
  navigation.setParams({
    realDailyCalories: Math.floor(Math.random() * Math.floor(10)),
    realDailyCarbohydrates: Math.floor(Math.random() * Math.floor(10)),
    realDailyFat: Math.floor(Math.random() * Math.floor(10)),
    realDailyProtein: Math.floor(Math.random() * Math.floor(10)),
  })
}

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
      // Filter data by current day
      let options = { year:'numeric', month:'2-digit', day:'numeric', hour:'numeric', minute:'numeric', second:'numeric'};
      let d = new Date().toLocaleDateString('en-US', options);
      let constructedDay = d.slice(6,10) + '-' + d.slice(0,2) + '-' + d.slice(3,5);
      data.filter(act => act.date.slice(0,10) == constructedDay);
      let realDailyActivity = data.map(item => item.duration).reduce((prev, next) => prev + next);

      // "Fetch" meals
      RandomMeals(navigation);

      // Combine data and send to Today
      let combinedData = {
        firstName: navigation.getParam('firstName'),
        lastName: navigation.getParam('lastName'),
        realDailyActivity: realDailyActivity,
        realDailyCalories: navigation.getParam('realDailyCalories'),
        realDailyCarbohydrates: navigation.getParam('realDailyCarbohydrates'),
        realDailyFat: navigation.getParam('realDailyFat'),
        realDailyProtein: navigation.getParam('realDailyProtein'),
        goalDailyActivity: navigation.getParam('goalDailyActivity'),
        goalDailyCalories: navigation.getParam('goalDailyCalories'),
        goalDailyCarbohydrates: navigation.getParam('goalDailyCarbohydrates'),
        goalDailyFat: navigation.getParam('goalDailyFat'),
        goalDailyProtein: navigation.getParam('goalDailyProtein'),
      };

      navigation.navigate('Today', combinedData);
      console.log("in LoadingDailyActivity: set params successfully");
    }
    else {
      console.log("Error in LoadingActivity: set params failure");
    }
  })
  .catch(error => Alert.alert("Error 1", error.message));
}

const LoadingDailyActivity = ({ navigation }) => {
  RunThisFirst(navigation);
  return (
    <View style={styles.container}>
      <KeyboardAvoidingView style={styles.container} behavior="padding">
        <Text style={styles.textCenter}>Loading...</Text>
      </KeyboardAvoidingView>
    </View>
  )
};

export default LoadingDailyActivity;