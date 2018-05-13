import React, { Component } from "react";
import { View, Text, StyleSheet, Image, TouchableOpacity } from "react-native";
import moment from "moment";

const POOPS = {
  1: require("../assets/poops/type1.png"),
  2: require("../assets/poops/type2.png"),
  3: require("../assets/poops/type3.png"),
  4: require("../assets/poops/type4.png"),
  5: require("../assets/poops/type5.png"),
  6: require("../assets/poops/type6.png"),
  7: require("../assets/poops/type7.png")
};

export default class PoopItem extends Component {
  constructor(props) {
    super(props);
    this.state = {
      data: props.data
    };
  }
  render() {
    const { data } = this.state;
    console.log(data);
    const { bristol_type, date } = data;
    const type = bristol_type;
    return (
      <TouchableOpacity
        onPress={() => this.props.onPress(data)}
        style={[styles.item, { flexDirection: "row", alignItems: "center" }]}
      >
        <Image style={{ width: 24, height: 24 }} source={POOPS[type]} />
        <View style={{ paddingLeft: 8 }}>
          <Text>Type {type}</Text>
          <Text style={{ fontSize: 12, color: "gray" }}>
            {moment(date).format("MMM Do YY h:mm:ss a")}
          </Text>
        </View>
      </TouchableOpacity>
    );
  }
}
const styles = StyleSheet.create({
  item: {
    backgroundColor: "white",
    flex: 1,
    borderRadius: 5,
    padding: 16,
    marginRight: 10,
    marginTop: 17
  }
});
