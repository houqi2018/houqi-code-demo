import React from 'react';
import { View, TouchableOpacity, Text, ScrollView, KeyboardAvoidingView, Alert, TextInput } from 'react-native';
import {styles} from './Style'

const Today = ({ navigation }) => {
  return (
    <View style={styles.container}>
      <KeyboardAvoidingView style={styles.container} behavior="padding">
        <Text style={styles.text}>Hi, {navigation.getParam('firstName')} {navigation.getParam('lastName')}</Text>
        <Text style={styles.text}>Activity(min): {navigation.getParam('realDailyActivity')} / {navigation.getParam('goalDailyActivity')}</Text>
        <Text style={styles.text}>Calories: {navigation.getParam('realDailyCalories')} / {navigation.getParam('goalDailyCalories')}</Text>
        <Text style={styles.text}>Carbohydrates: {navigation.getParam('realDailyCarbohydrates')} / {navigation.getParam('goalDailyCarbohydrates')}</Text>
        <Text style={styles.text}>Fat: {navigation.getParam('realDailyFat')} / {navigation.getParam('goalDailyFat')}</Text>
        <Text style={styles.text}>Protein: {navigation.getParam('realDailyProtein')} / {navigation.getParam('goalDailyProtein')}</Text>
        <TouchableOpacity style={styles.button} onPress={() => navigation.navigate('LoadingToday')}><Text style={styles.textWhite}>Refresh</Text></TouchableOpacity>
      </KeyboardAvoidingView>
    </View>
  )
};

export default Today;