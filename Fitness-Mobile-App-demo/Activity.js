import React from 'react';
import { View, TouchableOpacity, Text, ScrollView, KeyboardAvoidingView, Alert, TextInput, FlatList } from 'react-native';
import {styles} from './Style'
import {Card} from 'react-native-elements'

function goToUpdateActivity(navigation, option, id, name, duration, date, calories) {
  // option: 'modify'/'delete'/'new'
  navigation.navigate('UpdateActivity', {option: option, id: id, name: name, duration: duration, date: date, calories: calories})
}

const Activity = ({ navigation }) => {
  return (
    <View style={styles.container}>
      <TouchableOpacity style={styles.buttonLargeMargin} onPress={() => goToUpdateActivity(navigation, 'new', '', '', '', '', '')}><Text style={styles.textWhite}>Add Activity</Text></TouchableOpacity>
      <FlatList keyExtractor={(item, index) => index.toString()} data={navigation.getParam('activities')} renderItem={({item}) => {
          return <>
            <Card title={item.name}>
            <Text style={styles.textSmallPadding}>Calories: {item.calories}</Text>
            <Text style={styles.textSmallPadding}>Duration(min): {item.duration}</Text>
            <Text style={styles.textSmallPadding}>Date: {item.date}</Text>
            <View style={styles.sameRowCenter}>
              <TouchableOpacity style={styles.buttonSmallDownPadding} onPress={() => goToUpdateActivity(navigation, 'modify', item.id, item.name, item.duration, item.date, item.calories)}><Text style={styles.textWhite}>Edit</Text></TouchableOpacity>
              <TouchableOpacity  style={styles.buttonSmallDownPadding} onPress={() => goToUpdateActivity(navigation, 'delete', item.id, item.name, item.duration, item.date, item.calories)}><Text style={styles.textWhite}>Delete</Text></TouchableOpacity>
            </View>
            </Card>
          </>
        }}
      />
    </View>
  )
};

export default Activity;