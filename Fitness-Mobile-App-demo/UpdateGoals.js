import React from 'react';
import { View, TouchableOpacity, Text, ScrollView, KeyboardAvoidingView, Alert, TextInput } from 'react-native';
import {styles} from './Style'
import {Card} from 'react-native-elements'

function goToUpdateGoalsFinish(navigation) {
  let data = {
    admin: navigation.getParam('admin'),
    firstName: navigation.getParam('firstName'),
    lastName: navigation.getParam('lastName'),
    goalDailyActivity: navigation.getParam('goalDailyActivity'),
    goalDailyCalories: navigation.getParam('goalDailyCalories'),
    goalDailyCarbohydrates: navigation.getParam('goalDailyCarbohydrates'),
    goalDailyFat: navigation.getParam('goalDailyFat'),
    goalDailyProtein: navigation.getParam('goalDailyProtein'),
  };
  navigation.navigate('UpdateGoalsFinish', data);
}

const Today = ({ navigation }) => {
  return (
    <View style={styles.container}>
        <KeyboardAvoidingView style={styles.container} behavior="padding">
        <Card>
          <View style={styles.sameRow}>
            <Text style={styles.header3}>First Name</Text>
            <TextInput value={navigation.getParam('firstName')} onChangeText={(firstName) => navigation.setParams({firstName: firstName})} style={styles.input2}/>
          </View>
          <View style={styles.sameRow}>
            <Text style={styles.header3}>Last Name</Text>
            <TextInput value={navigation.getParam('lastName')} onChangeText={(lastName) => navigation.setParams({lastName: lastName})} style={styles.input2}/>
          </View>
          <View style={styles.sameRow}>
            <Text style={styles.header3}>Activity</Text>
            <TextInput value={navigation.getParam('goalDailyActivity')} onChangeText={(goalDailyActivity) => navigation.setParams({goalDailyActivity: goalDailyActivity})} style={styles.input2} keyboardType={'numeric'}/>
          </View>
          <View style={styles.sameRow}>
            <Text style={styles.header3}>Calories</Text>
            <TextInput value={navigation.getParam('goalDailyCalories')} onChangeText={(goalDailyCalories) => navigation.setParams({goalDailyCalories: goalDailyCalories})} style={styles.input2} keyboardType={'numeric'}/>
          </View>
          <View style={styles.sameRow}>
            <Text style={styles.header3}>Carbohydrates</Text>
            <TextInput value={navigation.getParam('goalDailyCarbohydrates')} onChangeText={(goalDailyCarbohydrates) => navigation.setParams({goalDailyCarbohydrates: goalDailyCarbohydrates})} style={styles.input2} keyboardType={'numeric'}/>
          </View>
          <View style={styles.sameRow}>
            <Text style={styles.header3}>Fat</Text>
            <TextInput value={navigation.getParam('goalDailyFat')} onChangeText={(goalDailyFat) => navigation.setParams({goalDailyFat: goalDailyFat})} style={styles.input2} keyboardType={'numeric'}/>
          </View>
          <View style={styles.sameRow}>
            <Text style={styles.header3}>Protein</Text>
            <TextInput value={navigation.getParam('goalDailyProtein')} onChangeText={(goalDailyProtein) => navigation.setParams({goalDailyProtein: goalDailyProtein})} style={styles.input2} keyboardType={'numeric'}/>
          </View>
          <TouchableOpacity style={styles.button} onPress={() => goToUpdateGoalsFinish(navigation)}><Text style={styles.textWhite}>Confirm Update</Text></TouchableOpacity>
          <TouchableOpacity style={styles.button} onPress={() => navigation.navigate('Settings')}><Text style={styles.textWhite}>Cancel</Text></TouchableOpacity>
          </Card>
        </KeyboardAvoidingView>
      </View>
  )
};

export default Today;