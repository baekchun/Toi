import React, { Component } from "react";
import { View, Text, Image, TextInput, StyleSheet } from "react-native";

export default class IconTextInput extends Component {
  render() {
    const { icon, placeholder, onChangeText, value } = this.props;
    return (
      <View style={styles.container}>
        <Image style={styles.icon} source={icon} />
        <TextInput
          style={styles.textInput}
          value={value}
          onChangeText={onChangeText}
          placeholder={placeholder}
          placeholderTextColor={'#f7f7f7'}
        />
      </View>
    );
  }
}

const styles = StyleSheet.create({
  container: {
    flexDirection: "row",
    width: 200,
    height: 50,
    borderBottomWidth: 1,
    marginTop: 16, 
    // borderWidth: 1,
    borderColor: "white",
    alignItems: "flex-end",
    paddingBottom: 8
  },
  icon: {
    width: 24,
    height: 24
  },
  textInput: {
    flex: 1,
    color: "white",
    borderColor: "white",
    marginLeft: 8,

  }
});
