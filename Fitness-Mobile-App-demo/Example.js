import React from 'react';
import { View, TouchableOpacity, Text, KeyboardAvoidingView, Alert, TextInput } from 'react-native';
import {styles} from './Style'

const Example = ({ navigation }) => {
  return (
    <View style={styles.container}>
      <KeyboardAvoidingView style={styles.container} behavior="padding">
      <TouchableOpacity style={styles.button} onPress={() => {console.log("example clicked")}}><Text style={styles.textWhite}>Example</Text></TouchableOpacity>
      </KeyboardAvoidingView>
    </View>
  );
};

export default Example;