import React, { Component } from "react";
import { Text, Image, View, TouchableOpacity, StyleSheet } from "react-native";
import { Agenda } from "react-native-calendars";
import Colors from "../constants/Colors";
import { PoopItem } from "../components";

import firebase from "firebase";
import moment from "moment";

export default class HomeScreen extends Component {
  static navigationOptions = {
    header: null
  };

  constructor(props) {
    super(props);
    this.state = {
      items: {}
    };
  }

  renderHeader() {
    return (
      <View
        style={{
          flexDirection: "row",
          justifyContent: "space-between",
          alignItems: "center",
          paddingTop: 20,
          paddingHorizontal: 12,
          height: 64,
          backgroundColor: "white",
          borderBottomColor: "#7d7d7d",
          borderBottomWidth: StyleSheet.hairlineWidth
        }}
      >
        <View style={{ flex: 1 }}>
          <TouchableOpacity
            onPress={() => this.props.navigation.navigate("DrawerToggle")}
          >
            <Image
              style={{ width: 24, height: 24 }}
              source={require("../assets/icons/icons8-menu.png")}
            />
          </TouchableOpacity>
        </View>
        <View style={{ flex: 1, alignItems: "center" }}>
          <Text>Calendar</Text>
        </View>
        <View style={{ flex: 1 }} />
      </View>
    );
  }

  render() {
    return (
      <View style={{ flex: 1 }}>
        {this.renderHeader()}
        <Agenda
          items={this.state.items}
          loadItemsForMonth={this.loadItems.bind(this)}
          selected={moment().format("YYYY-MM-DD")}
          renderItem={this.renderItem.bind(this)}
          renderEmptyDate={this.renderEmptyDate.bind(this)}
          rowHasChanged={this.rowHasChanged.bind(this)}
          theme={{
            dotColor: Colors.main,
            selectedDotColor: "#ffffff",
            selectedDayBackgroundColor: Colors.main,
            agendaTodayColor: Colors.main,
            todayTextColor: Colors.main
          }}
        />
      </View>
    );
  }

  loadItems(day) {
    console.log("loading data");
    // this.randomGeneration(day);
    firebase
      .database()
      .ref("stools")
      .on("value", snapshot => {
        const data = snapshot.val();
        console.log("data came in");
        console.log(data);

        this.state.items = {};
        Object.keys(data).map(d => {
          console.log(data[d]);
          const strTime = this.timeToString(data[d].date);
          if (!this.state.items[strTime]) {
            this.state.items[strTime] = [];
          }
          this.state.items[strTime].push(data[d]);
        });

        const newItems = {};
        Object.keys(this.state.items).forEach(key => {
          newItems[key] = this.state.items[key];
        });
        this.setState({
          items: newItems
        });

        if (data == null) {
          console.log("no data");
          this.setState({ items: { 1: "hello" } });
          // this.randomGeneration(day);
        }
      });

    // setTimeout(() => {
    //   for (let i = -15; i < 85; i++) {
    //     const time = day.timestamp + i * 24 * 60 * 60 * 1000;
    //     const strTime = this.timeToString(time);
    //     if (!this.state.items[strTime]) {
    //       this.state.items[strTime] = [];
    //       const numItems = Math.floor(Math.random() * 5);
    //       for (let j = 0; j < numItems; j++) {
    //         this.state.items[strTime].push({
    //           name: "Item for " + strTime
    //         });
    //       }
    //     }
    //   }
    //   //console.log(this.state.items);
    //   const newItems = {};
    //   Object.keys(this.state.items).forEach(key => {
    //     newItems[key] = this.state.items[key];
    //   });
    //   this.setState({
    //     items: newItems
    //   });
    // }, 1000);
  }

  randomGeneration(day) {
    for (let i = -15; i < 85; i++) {
      const time = day.timestamp + i * 24 * 60 * 60 * 1000;
      const strTime = this.timeToString(time);
      if (!this.state.items[strTime]) {
        this.state.items[strTime] = [];
        const numItems = Math.floor(Math.random() * 5);
        for (let j = 0; j < numItems; j++) {
          this.state.items[strTime].push({
            name: "Item for " + strTime
          });
        }
      }
    }
    //console.log(this.state.items);
    const newItems = {};
    Object.keys(this.state.items).forEach(key => {
      newItems[key] = this.state.items[key];
    });
    this.setState({
      items: newItems
    });
  }

  renderItem(item) {
    return (
      <View style={[styles.item]}>
        <PoopItem
          data={item}
          onPress={data => this.props.navigation.navigate("Poop", { data })}
        />
      </View>
    );
  }

  renderEmptyDate() {
    return (
      <View style={styles.emptyDate}>
        <Text style={{ color: "#7d7d7d" }}>No data to display</Text>
      </View>
    );
  }

  rowHasChanged(r1, r2) {
    return r1.name !== r2.name;
  }

  timeToString(time) {
    const date = new Date(time);
    return date.toISOString().split("T")[0];
  }
}

const styles = StyleSheet.create({
  emptyDate: {
    height: 15,
    flex: 1,
    paddingTop: 44
  }
});
