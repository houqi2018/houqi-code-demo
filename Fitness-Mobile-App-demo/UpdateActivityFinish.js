import React from 'react';
import { View, TouchableOpacity, Text, KeyboardAvoidingView, Alert, TextInput } from 'react-native';
import {styles} from './Style'

function deleteActivity(navigation) {
  let id = navigation.getParam('id');
  let userToken = navigation.dangerouslyGetParent().dangerouslyGetParent().getParam('userToken');
  const url = 'https://mysqlcs639.cs.wisc.edu/activities/' + id;
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
    if ("message" in result && result.message === 'Activity deleted!') {
      console.log('deleted')
      navigation.navigate('LoadingActivity');
    }
    else {
      Alert.alert("Activity not deleted.");
    }
  })
  .catch(error => Alert.alert("Error 5", error.message));
}

function modifyActivity(navigation) {
  let id = navigation.getParam('id');
  let userToken = navigation.dangerouslyGetParent().dangerouslyGetParent().getParam('userToken');
  const url = 'https://mysqlcs639.cs.wisc.edu/activities/' + id;
  let fetchData = {
    method: 'PUT',
    headers: {
      'Accept': 'application/json',
      'Content-Type': 'application/json',
      'x-access-token': userToken,
    },
    body: JSON.stringify({
      'id': navigation.getParam('id'),
      'name': navigation.getParam('name'),
      'duration': navigation.getParam('duration'),
      'date': navigation.getParam('date'),
      'calories': navigation.getParam('calories'),
    }),
    redirect: 'follow',
  };
  fetch(url, fetchData)
  .then(response => response.json())
  .then(result => {
    if ("message" in result && result.message === 'Activity updated!') {
      navigation.navigate('LoadingActivity');
    }
    else {
      Alert.alert("User info not updated. Check your input.");
    }
  })
  .catch(error => Alert.alert("Error 5", error.message));
}

function newActivity(navigation) {
  let userToken = navigation.dangerouslyGetParent().dangerouslyGetParent().getParam('userToken');
  const url = 'https://mysqlcs639.cs.wisc.edu/activities';
  let fetchData = { 
    method: 'POST',
    headers: {
      'Accept': 'application/json',
      'Content-Type': 'application/json',
      'x-access-token': userToken,
    },
    body: JSON.stringify({
        'id': navigation.getParam('id'),
        'name': navigation.getParam('name'),
        'duration': navigation.getParam('duration'),
        'date': navigation.getParam('date'),
        'calories': navigation.getParam('calories'),
    }),
    redirect: 'follow',
  };
  fetch(url, fetchData)
  .then(response => response.json())
  .then(result => {
    Alert.alert(result.message);
    // if ("message" in result && result.message == "Activity created!") {
      navigation.navigate('LoadingActivity');
    // }
  })
  .catch(error => Alert.alert("Error 6", error.message));
}

function updateActivity(navigation) {
  console.log(navigation.getParam('option'))
  // option: 'modify'/'delete'/'new'
  if (navigation.getParam('option') == 'delete') {
    deleteActivity(navigation);
  }
  else if(navigation.getParam('option') == 'modify') {
    modifyActivity(navigation);
  }
  else if(navigation.getParam('option') == 'new') {
    newActivity(navigation);
  }
}

const UpdateActivityFinish = ({ navigation }) => {
  updateActivity(navigation);
  return (
    <View style={styles.container}>
      <KeyboardAvoidingView style={styles.container} behavior="padding">
        <Text style={styles.textCenter}>Updating...</Text>
      </KeyboardAvoidingView>
    </View>
  )
};

export default UpdateActivityFinish;