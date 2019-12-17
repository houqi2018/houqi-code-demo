import React from 'react';
import { View, TouchableOpacity, Text, ScrollView, KeyboardAvoidingView, Alert, TextInput } from 'react-native';
import {styles} from './Style'
import DatePicker from 'react-native-datepicker'
import {Card} from 'react-native-elements'

function goToUpdateActivityFinish(navigation, option) {
  // option: 'modify'/'delete'/'new'
  let data = {
    option: option,
    id: navigation.getParam('id'),
    name: navigation.getParam('name'),
    duration: navigation.getParam('duration'),
    date: navigation.getParam('date'),
    calories: navigation.getParam('calories'),
  };
  console.log("date", navigation.getParam('date'))
  navigation.navigate('UpdateActivityFinish', data);
}

const UpdateActivity = ({ navigation }) => {
  let confirmBtn = <TouchableOpacity style={styles.button} onPress={() => goToUpdateActivityFinish(navigation, 'modify')}><Text style={styles.textWhite}>Confirm Update</Text></TouchableOpacity>;
  let newBtn = <TouchableOpacity style={styles.button} onPress={() => goToUpdateActivityFinish(navigation, 'new')}><Text style={styles.textWhite}>Confirm Create</Text></TouchableOpacity>;

  if (navigation.getParam('option') == 'delete') {
    goToUpdateActivityFinish(navigation, 'delete');
    return (
      <View style={styles.container}>
        <KeyboardAvoidingView style={styles.container} behavior="padding">
          <Text style={styles.textCenter}>Deleting...</Text>
        </KeyboardAvoidingView>
      </View>
    )
  }
  else {
    return (
        <View style={styles.container}>
          <KeyboardAvoidingView style={styles.container} behavior="padding">
          <Card>
            <View style={styles.sameRow}>
              <Text style={styles.header3}>Name</Text>
              <TextInput value={navigation.getParam('name')} onChangeText={(name) => navigation.setParams({ name: name })} style={styles.input2}/>
            </View>
            <View style={styles.sameRow}>
              <Text style={styles.header3}>Duration(min)</Text>
              <TextInput value={navigation.getParam('duration')} onChangeText={(duration) => navigation.setParams({ duration: duration })} style={styles.input2} keyboardType={'numeric'}/>
            </View>
            <View style={styles.sameRow}>
              <Text style={styles.header3}>Calories</Text>
              <TextInput value={navigation.getParam('calories')} onChangeText={(calories) => navigation.setParams({ calories: calories })} style={styles.input2} keyboardType={'numeric'}/>
            </View>
            <View style={styles.sameRow}>
              <Text style={styles.header3}>Date and Time</Text>
              <DatePicker customStyles={{dateIcon:{width:0,height:0}, dateInput:{width:100,height:30,borderColor:'black',borderWidth:1,marginBottom:5}}} date={navigation.state.time} mode="datetime" onDateChange={(date) => navigation.setParams({ date: date })}/>
            </View>
            {navigation.getParam('option') == 'new'? newBtn : confirmBtn}
            <TouchableOpacity style={styles.button} onPress={() => navigation.navigate('LoadingActivity')}><Text style={styles.textWhite}>Cancel</Text></TouchableOpacity>
            </Card>
          </KeyboardAvoidingView>
        </View>
      )
  }
};

export default UpdateActivity;