import React, { Component } from "react";
import { View, Text, StyleSheet, TouchableOpacity } from "react-native";

export default class Button extends Component {
  render() {
    const { text, onPress, backgroundColor } = this.props;
    return (
      <TouchableOpacity
        onPress={onPress}
        style={[styles.container, { backgroundColor }]}
      >
        <Text style={styles.text}>{text}</Text>
      </TouchableOpacity>
    );
  }
}

const styles = StyleSheet.create({
  container: {
    paddingVertical: 16,
    paddingHorizontal: 32,
    justifyContent: "center",
    alignItems: "center",
    borderRadius: 100,
    backgroundColor: "transparent",
    margin: 16
  },
  text: {
    color: "white",
    fontWeight: "500",
    fontSize: 16
  }
});
